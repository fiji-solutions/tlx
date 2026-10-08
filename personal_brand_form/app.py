import json
import math
import os
import re
from datetime import datetime, timezone

import boto3

# Every contact form on fijisolutions.net and peakcodeconsulting.ch posts here.
# A submission is emailed to LEAD_TO through Amazon SES, with Reply-To set to the lead.
# Discord and Salesforce were dropped on 2026-10-08: the deployed copy had an empty
# Discord channel and token (never committed, so every pipeline deploy blanked them) and
# every submission returned 500.
LEAD_TO = os.environ.get("LEAD_TO", "")
LEAD_FROM = os.environ.get("LEAD_FROM", "")

CORS_HEADERS = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Headers": "*",
    "Access-Control-Allow-Methods": "*",
    "Access-Control-Allow-Origin": "*",
}

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

# Spam screening, added 2026-10-08 after bot submissions with random strings in every field
# ("hJAJvTXFbfVWByJZwvd", "dCYilTntLxKKtvDSEwniRgn").
#
# Dropped: the visitor gets the same 200 a real lead gets, so a bot learns nothing, no email is
# sent, and the submission is logged in full under "spam" so a false positive can be recovered.
# 1. Honeypot: the forms send "website", the value of an input people never see. Text in it is
#    a bot filling every input it finds.
# 2. Speed: the forms send "elapsed_ms", the time between the form appearing and the submit.
#    Under MIN_ELAPSED_MS is not a person typing. A missing value is let through, so a page
#    cached from before this change still works.
#
# Flagged, not dropped: the email is sent with "[Likely spam]" in the subject, because this check
# can be wrong about a real person and a dropped lead is never seen again.
# 3. Gibberish: a word of 8+ letters that switches from lower to upper case 3+ times inside
#    itself. Real names and company names top out at one or two (LinkedIn, McDonald, ThyssenKrupp);
#    all-caps words, Greek or Latin, switch zero times. Code identifiers (camundaProcessEngine)
#    can reach three, which is why a hit in one free-text field alone is not enough.
MIN_ELAPSED_MS = int(os.environ.get("MIN_ELAPSED_MS", "3000"))
MAX_FIELD_CHARS = 5000
WORD_RE = re.compile(r"[^\W\d_]{8,}")


def is_gibberish_word(word):
    return sum(1 for a, b in zip(word, word[1:]) if a.islower() and b.isupper()) >= 3


def has_gibberish(value):
    return any(is_gibberish_word(w) for w in WORD_RE.findall(value))


def drop_reason(body):
    honeypot = body.get("website")
    if isinstance(honeypot, str) and honeypot.strip():
        return "honeypot"
    elapsed = body.get("elapsed_ms")
    if (isinstance(elapsed, (int, float)) and not isinstance(elapsed, bool)
            and math.isfinite(elapsed) and 0 <= elapsed < MIN_ELAPSED_MS):
        return f"too fast ({int(elapsed)} ms)"
    return None


def looks_like_spam(name, company, question, message):
    if has_gibberish(name):
        return True
    # Some forms copy the question or the company into the message, so one word typed once
    # would count twice. Each distinct value the visitor typed counts once.
    for copied in (question, company):
        if copied:
            message = message.replace(copied, "")
    return sum(1 for v in (company, question, message) if has_gibberish(v)) >= 2

_ses_client = None


def ses():
    global _ses_client
    if _ses_client is None:
        _ses_client = boto3.client("ses")
    return _ses_client


def respond(status, payload):
    return {"statusCode": status, "headers": CORS_HEADERS, "body": json.dumps(payload)}


def one_line(value, limit=200):
    """Collapse a value to one line, so it is safe in an email header."""
    return " ".join(str(value).split())[:limit]


def site_of(event):
    headers = {k.lower(): v for k, v in (event.get("headers") or {}).items()}
    origin = headers.get("origin") or headers.get("referer") or ""
    if "peakcodeconsulting" in origin:
        return "Peak Code"
    if "fijisolutions" in origin:
        return "Fiji"
    return one_line(origin, 80) or "unknown site"


def build_email(name, email, company, question, message, site, received_at):
    subject = one_line(f"New lead ({site}): {name}" + (f", {company}" if company else ""))
    body = (
        f"New form submission from {site}, {received_at}\n\n"
        f"Name: {name}\n"
        f"Email: {email}\n"
        f"Company: {company}\n"
        f"Question: {question}\n\n"
        f"Message:\n{message}\n\n"
        "Reply to this email to answer the lead directly.\n"
    )
    return subject, body


def lambda_handler(event, context):
    """
    Expected body: {"name", "email", "company", "question", "message"}; name and email required.
    Optional: "website" (the honeypot, empty for a person) and "elapsed_ms" (see drop_reason).
    200 once SES accepts the email, 200 with no email for dropped spam, 400 on missing fields,
    500 when the email fails (the forms then show the fallback that asks the visitor to email us).
    """
    try:
        raw = event.get("body") or "{}"
        body = json.loads(raw) if isinstance(raw, str) else raw
        if not isinstance(body, dict):
            body = {}
    except ValueError:
        return respond(400, {"error": "Body must be JSON."})

    name = str(body.get("name", "")).strip()[:MAX_FIELD_CHARS]
    email = str(body.get("email", "")).strip()[:MAX_FIELD_CHARS]
    company = str(body.get("company", "")).strip()[:MAX_FIELD_CHARS]
    question = str(body.get("question", "")).strip()[:MAX_FIELD_CHARS]
    message = str(body.get("message", "")).strip()[:MAX_FIELD_CHARS]

    if not all([name, email]):
        return respond(400, {"error": "Name and email are required fields."})

    site = site_of(event)
    received_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    headers = {k.lower(): v for k, v in (event.get("headers") or {}).items()}
    seen = {"ip": ((event.get("requestContext") or {}).get("identity") or {}).get("sourceIp"),
            "ua": one_line(headers.get("user-agent", ""), 200),
            "elapsed_ms": body.get("elapsed_ms"),
            "website": one_line(body.get("website", ""), 100)}

    reason = drop_reason(body)
    if reason:
        print(json.dumps({"spam": {"reason": reason, "site": site, "name": name, "email": email,
                                   "company": company, "question": question, "message": message,
                                   "at": received_at, **seen}}, ensure_ascii=False, default=str))
        return respond(200, {"message": "Form submission processed successfully"})
    likely_spam = looks_like_spam(name, company, question, message)

    # Logged before sending, so a failed email still leaves the lead in CloudWatch.
    print(json.dumps({"lead": {"site": site, "name": name, "email": email, "company": company,
                               "question": question, "message": message, "at": received_at,
                               "likely_spam": likely_spam, **seen}}, ensure_ascii=False, default=str))

    subject, text = build_email(name, email, company, question, message, site, received_at)
    if likely_spam:
        subject = "[Likely spam] " + subject
    send_args = {
        "Source": f"Website forms <{LEAD_FROM}>",
        "Destination": {"ToAddresses": [LEAD_TO]},
        "Message": {
            "Subject": {"Data": subject, "Charset": "UTF-8"},
            "Body": {"Text": {"Data": text, "Charset": "UTF-8"}},
        },
    }
    if EMAIL_RE.match(email):
        send_args["ReplyToAddresses"] = [email]

    try:
        ses().send_email(**send_args)
    except Exception as e:
        print(f"Error sending lead email: {e}")
        return respond(500, {"error": "Could not process the submission."})

    return respond(200, {"message": "Form submission processed successfully"})
