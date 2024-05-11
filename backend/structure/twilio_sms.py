from django.conf import settings
from twilio.rest import Client


def send_sms_notification():
    # Your Twilio Account SID and Auth Token
    account_sid = 'AC62f3fc0a0f13c513fc645e7b3437a1a7'
    auth_token = '0d39ff76293a8ee76e301c7f2d765f66'

    # Initialize Twilio client
    client = Client(account_sid, auth_token)

    # Twilio phone number
    from_number = '+12677192864'

    # User's phone number
    to_number = '+380968492092'

    # Compose the message
    message = "Hello Andrii"

    try:
        # Send SMS
        client.messages.create(
            body=message,
            from_=from_number,
            to=to_number
        )
        print("SMS notification sent successfully")
    except Exception as e:
        print(f"Failed to send SMS notification: {e}")

send_sms_notification()