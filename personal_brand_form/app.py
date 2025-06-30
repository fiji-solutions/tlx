import json
import requests
import urllib.parse

# Constants
DISCORD_BOT_TOKEN = ""
CHANNEL_ID = ""
USER_TO_PING = "<@217278463889899522>"

SALESFORCE_CLIENT_ID = ""
SALESFORCE_CLIENT_SECRET = ""
SALESFORCE_INSTANCE = "https://cmoutafidis-test-dev-ed.my.salesforce.com"


def send_discord_message(channel_id, message, token):
    """Send a message to a Discord channel using the Discord API."""
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
    return response


def get_salesforce_token():
    """Get Salesforce access token using Client Credentials flow."""
    token_url = f"{SALESFORCE_INSTANCE}/services/oauth2/token"

    data = {
        "grant_type": "client_credentials",
        "client_id": SALESFORCE_CLIENT_ID,
        "client_secret": SALESFORCE_CLIENT_SECRET
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = requests.post(
        token_url,
        data=urllib.parse.urlencode(data),
        headers=headers
    )
    response.raise_for_status()
    return response.json()["access_token"]


def create_salesforce_lead(name, email, company, description):
    """Create a lead in Salesforce using the Salesforce API."""
    # Get access token
    access_token = get_salesforce_token()

    # API endpoint for creating a lead
    salesforce_url = f"{SALESFORCE_INSTANCE}/services/data/v64.0/sobjects/Lead"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "LastName": name,
        "Email": email,
        "Company": company,
        "Description": description
    }

    try:
        response = requests.post(salesforce_url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error creating Salesforce lead: {str(e)}")
        # Print more details for debugging
        if hasattr(e, 'response') and e.response:
            print(f"Response status: {e.response.status_code}")
            print(f"Response body: {e.response.text}")
        raise e


def lambda_handler(event, context):
    """
    Lambda handler for processing personal brand form submissions.

    Expected event body:
    {
        "name": "John Doe",
        "email": "johndoe@example.com",
        "company": "Example Inc",
        "question": "What services do you offer?",
        "message": "I'm interested in your consulting services."
    }
    """
    try:
        # Parse request body
        if isinstance(event.get('body'), str):
            body = json.loads(event.get('body', '{}'))
        else:
            body = event.get('body', {})

        # Extract form data
        name = body.get('name', '')
        email = body.get('email', '')
        company = body.get('company', '')
        question = body.get('question', '')
        message = body.get('message', '')

        # Validate required fields
        if not all([name, email]):
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Name and email are required fields."})
            }

        # Create Discord message
        discord_message = f"{USER_TO_PING} New Form Submission:\n\n" \
                          f"**Name:** {name}\n" \
                          f"**Email:** {email}\n" \
                          f"**Company:** {company}\n" \
                          f"**Question:** {question}\n" \
                          f"**Message:** {message}"

        # Send Discord notification
        send_discord_message(CHANNEL_ID, discord_message, DISCORD_BOT_TOKEN)

        # Create combined description for Salesforce
        salesforce_description = f"Question: {question}\n\nMessage: {message}"

        # Create Salesforce lead
        salesforce_response = create_salesforce_lead(name, email, company, salesforce_description)

        # Return success response
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "*",
                "Access-Control-Allow-Origin": "*",
            },
            "body": json.dumps({
                "message": "Form submission processed successfully"
            })
        }

    except Exception as e:
        error_message = str(e)
        print(f"Error processing form submission: {error_message}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": f"Error processing submission: {error_message}"})
        }