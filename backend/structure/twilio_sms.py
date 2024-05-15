from django.conf import settings
from twilio.rest import Client


def send_sms_notification(phone, text):
    account_sid = settings.account_sid
    auth_token = settings.auth_token

    # Initialize Twilio client
    client = Client(account_sid, auth_token)

    # Twilio phone number
    from_number = '+12677192864'

    # User's phone number
    to_number = phone

    # Compose the message
    message = text

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


send_sms_notification('+1234567890', 'Alert message from the server')

{
    "_id": ObjectId("60d5d52713e4c80e1cd5cf47"),
    "monitoring_object": ObjectId("60d5d52713e4c80e1cd5cf48"),
    "sensor_type": ObjectId("60d5d52713e4c80e1cd5cf49"),
    "is_active": true,
    "normal_min": 15,
    "normal_max": 35,
    "max_per_day": 10
}