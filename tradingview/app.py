import json
import requests
import base64

DISCORD_BOT_TOKEN = ""
CHANNEL_ID = ""

ALERT_USER_TAGS = {
    "1": "<@217278463889899522> <@363658083211149313>",
    "2": "<@217278463889899522> <@363658083211149313>",
    "3": "<@217278463889899522> <@363658083211149313>",
    "4": "<@217278463889899522> <@363658083211149313>",
    "5": "<@217278463889899522> <@363658083211149313>",
    "6": "<@217278463889899522> <@363658083211149313>",
}

ALERT_TITLES = {
    "1": "🚨 Bullrun Profit Maximizert (Default)",
    "2": "📈 Bullrun Profit Maximizert (BTC/ETH/SOL/SUI)",
    "3": "⚠️ AI x Meme Impulse Tracker",
    "4": "🪙 Trend Titan Neutronstar BTC",
    "5": "💠 Trend Titan Neutronstar ETH",
    "6": "🟣 Trend Titan Neutronstar SOL",
}


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
        alert_id = event["queryStringParameters"].get("alert")

        title = ALERT_TITLES.get(alert_id, "Generic Alert")
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

        user_tags = ALERT_USER_TAGS.get(alert_id, "")
        full_message = f"{title}\n\n{message}\n\n{user_tags}"

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
