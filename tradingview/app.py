import json
import requests
import base64

DISCORD_BOT_TOKEN = ""
CHANNEL_ID = ""

USER_TAGS = "<@217278463889899522> <@363658083211149313>"


def send_discord_message(channel_id, message, token):
    url = f"https://discord.com/api/v10/channels/{channel_id}/messages"
    headers = {
        "Authorization": f"Bot {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "content": message
    }
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()


def lambda_handler(event, context):
    try:
        headers = {k.lower(): v for k, v in (event.get("headers") or {}).items()}
        content_type = headers.get("content-type", "")

        # Event body may be base64 encoded depending on API Gateway configuration
        body = event["body"]
        if event.get("isBase64Encoded"):
            body = base64.b64decode(body).decode("utf-8")

        if "application/json" in content_type:
            data = json.loads(body)
            message = data.get("text", "")
        else:
            message = body

        if not message:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Message is empty."})
            }

        full_message = f"{message}\n\n{USER_TAGS}"

        send_discord_message(CHANNEL_ID, full_message, DISCORD_BOT_TOKEN)
        return {
            "statusCode": 200,
            "body": json.dumps({"message": message})
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
