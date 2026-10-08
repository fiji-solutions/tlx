import json

import pytest

from personal_brand_form import app


class FakeSes:
    def __init__(self, fail=False):
        self.fail = fail
        self.sent = []

    def send_email(self, **kwargs):
        if self.fail:
            raise RuntimeError("SES rejected the message")
        self.sent.append(kwargs)
        return {"MessageId": "test"}


@pytest.fixture()
def fake_ses(monkeypatch):
    fake = FakeSes()
    monkeypatch.setattr(app, "ses", lambda: fake)
    monkeypatch.setattr(app, "LEAD_TO", "leads@example.com")
    monkeypatch.setattr(app, "LEAD_FROM", "leads@example.com")
    return fake


def event(body, origin="https://www.peakcodeconsulting.ch"):
    return {"body": json.dumps(body), "headers": {"origin": origin}}


FULL = {
    "name": "Test",
    "email": "test@example.com",
    "company": "Test AG",
    "question": "Business units / repositories on Camunda 7: 10",
    "message": "[PEAK CODE CONSULTING] Camunda 7 migration roadmap request\n\nHow did you hear about us: AI",
}


def test_full_submission_is_emailed(fake_ses):
    res = app.lambda_handler(event(FULL), None)
    assert res["statusCode"] == 200
    assert res["headers"]["Access-Control-Allow-Origin"] == "*"
    sent = fake_ses.sent[0]
    assert sent["Destination"]["ToAddresses"] == ["leads@example.com"]
    assert sent["ReplyToAddresses"] == ["test@example.com"]
    assert sent["Message"]["Subject"]["Data"] == "New lead (Peak Code): Test, Test AG"
    text = sent["Message"]["Body"]["Text"]["Data"]
    for value in FULL.values():
        assert value in text


def test_fiji_origin_is_named(fake_ses):
    app.lambda_handler(event(FULL, origin="https://www.fijisolutions.net"), None)
    assert fake_ses.sent[0]["Message"]["Subject"]["Data"].startswith("New lead (Fiji)")


def test_missing_email_is_400_and_sends_nothing(fake_ses):
    res = app.lambda_handler(event({"name": "Test", "email": ""}), None)
    assert res["statusCode"] == 400
    assert fake_ses.sent == []


def test_bad_json_is_400(fake_ses):
    res = app.lambda_handler({"body": "{not json"}, None)
    assert res["statusCode"] == 400


def test_newlines_never_reach_the_subject(fake_ses):
    app.lambda_handler(event(dict(FULL, name="Evil\r\nBcc: x@example.com")), None)
    assert "\n" not in fake_ses.sent[0]["Message"]["Subject"]["Data"]


def test_invalid_reply_address_is_left_out(fake_ses):
    res = app.lambda_handler(event(dict(FULL, email="not an email")), None)
    assert res["statusCode"] == 200
    assert "ReplyToAddresses" not in fake_ses.sent[0]


def test_ses_failure_is_500(monkeypatch):
    monkeypatch.setattr(app, "ses", lambda: FakeSes(fail=True))
    res = app.lambda_handler(event(FULL), None)
    assert res["statusCode"] == 500


def test_filled_honeypot_is_dropped_with_200(fake_ses):
    res = app.lambda_handler(event(dict(FULL, website="http://spam.example")), None)
    assert res["statusCode"] == 200
    assert fake_ses.sent == []


def test_too_fast_submit_is_dropped(fake_ses):
    res = app.lambda_handler(event(dict(FULL, elapsed_ms=900)), None)
    assert res["statusCode"] == 200
    assert fake_ses.sent == []


def test_normal_submit_with_new_fields_is_emailed(fake_ses):
    res = app.lambda_handler(event(dict(FULL, website="", elapsed_ms=45000)), None)
    assert res["statusCode"] == 200
    assert len(fake_ses.sent) == 1
    assert not fake_ses.sent[0]["Message"]["Subject"]["Data"].startswith("[Likely spam]")


def test_random_strings_are_flagged_but_still_emailed(fake_ses):
    junk = dict(FULL, name="hJAJvTXFbfVWByJZwvd", company="dCYilTntLxKKtvDSEwniRgn", message="qWeRtYuIoPaSdFgH")
    res = app.lambda_handler(event(junk), None)
    assert res["statusCode"] == 200
    assert fake_ses.sent[0]["Message"]["Subject"]["Data"].startswith("[Likely spam]")


def test_real_names_are_not_flagged(fake_ses):
    real = dict(FULL, name="Charalampos Moutafidis", company="ThyssenKrupp McDonald LinkedIn", message="We use camundaProcessEngine in production")
    app.lambda_handler(event(real), None)
    assert not fake_ses.sent[0]["Message"]["Subject"]["Data"].startswith("[Likely spam]")
