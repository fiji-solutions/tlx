import json
import requests

# Constants
DISCORD_BOT_TOKEN = ""
CHANNEL_ID = ""
SALESFORCE_TOKEN = ""
USER_TO_PING = "<@217278463889899522>"


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


def create_salesforce_lead(name, email, company, description):
    """Create a lead in Salesforce using the Salesforce API."""
    # This would typically connect to Salesforce REST API
    # For production, you would need to implement Salesforce OAuth and API calls
    # Example placeholder for now:

    salesforce_url = "https://cmoutafidis-test-dev-ed.my.salesforce.com/services/data/v57.0/sobjects/Lead"

    headers = {
        "Authorization": f"Bearer {SALESFORCE_TOKEN}",
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
        discord_message = f"{USER_TO_PING} New Personal Brand Form Submission:\n\n" \
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
        return {
            "statusCode": 500,
            "body": json.dumps({"error": f"Error processing submission: {str(e)}"})
        }