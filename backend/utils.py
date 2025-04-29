import smtplib
import random
import os
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

SMTP_EMAIL = os.getenv("SMTP_EMAIL")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

# Store OTPs for verification (simple dict for demo; use cache/db in production)
otp_store = {}

def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp(receiver_email):
    otp = generate_otp()
    otp_store[receiver_email] = otp  # Save OTP for that email
    msg = EmailMessage()
    msg.set_content(f"Your OTP is: {otp}")
    msg['Subject'] = "Your Signup OTP"
    msg['From'] = SMTP_EMAIL
    msg['To'] = receiver_email

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(SMTP_EMAIL, SMTP_PASSWORD)
            server.send_message(msg)
            print(f"✅ OTP sent to {receiver_email}")
        return True
    except Exception as e:
        print("❌ Failed to send email:", e)
        return False

def verify_otp(receiver_email, entered_otp):
    correct_otp = otp_store.get(receiver_email)
    return entered_otp == correct_otp
