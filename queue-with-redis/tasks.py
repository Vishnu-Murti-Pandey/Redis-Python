import time

def send_email(
    to_email: str,
    subject: str,
    body: str
):
    print(f"Sending email to {to_email}")

    # Simulate email delay
    time.sleep(10)

    print(f"Email sent to {to_email}")

    return {
        "status": "success",
        "email": to_email
    }