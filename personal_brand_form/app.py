import json
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
    200 once SES accepts the email, 400 on missing fields, 500 when the email fails
    (the forms then show the fallback that asks the visitor to email us).
    """
    try:
        raw = event.get("body") or "{}"
        body = json.loads(raw) if isinstance(raw, str) else raw
        if not isinstance(body, dict):
            body = {}
    except ValueError:
        return respond(400, {"error": "Body must be JSON."})

    name = str(body.get("name", "")).strip()
    email = str(body.get("email", "")).strip()
    company = str(body.get("company", "")).strip()
    question = str(body.get("question", "")).strip()
    message = str(body.get("message", "")).strip()

    if not all([name, email]):
        return respond(400, {"error": "Name and email are required fields."})

    site = site_of(event)
    received_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    # Logged before sending, so a failed email still leaves the lead in CloudWatch.
    print(json.dumps({"lead": {"site": site, "name": name, "email": email, "company": company,
                               "question": question, "message": message, "at": received_at}}))

    subject, text = build_email(name, email, company, question, message, site, received_at)
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
