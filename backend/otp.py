import smtplib
import random
from email.message import EmailMessage

# Gmail credentials
SMTP_EMAIL = "supersuperheros2@gmail.com"
SMTP_PASSWORD = "tfeaakkghafgxvtc"  # App Password without spaces

def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp_email(receiver_email, otp):
    msg = EmailMessage()
    msg.set_content(f"Your OTP is: {otp}")
    msg['Subject'] = "Your Signup OTP"
    msg['From'] = SMTP_EMAIL
    msg['To'] = receiver_email

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SMTP_EMAIL, SMTP_PASSWORD)
        server.send_message(msg)
        server.quit()
        print(f"✅ OTP '{otp}' sent successfully to {receiver_email}")
    except Exception as e:
        print("❌ Failed to send email:", str(e))

if __name__ == "__main__":
    otp = generate_otp()
    send_otp_email("er.anurag029@gmail.com", otp)
import smtplib
import random
from email.message import EmailMessage

# Gmail credentials
SMTP_EMAIL = "supersuperheros2@gmail.com"
SMTP_PASSWORD = "tfeaakkghafgxvtc"  # App Password without spaces

def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp_email(receiver_email, otp):
    msg = EmailMessage()
    msg.set_content(f"Your OTP is: {otp}")
    msg['Subject'] = "Your Signup OTP"
    msg['From'] = SMTP_EMAIL
    msg['To'] = receiver_email

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SMTP_EMAIL, SMTP_PASSWORD)
        server.send_message(msg)
        server.quit()
        print(f"✅ OTP '{otp}' sent successfully to {receiver_email}")
    except Exception as e:
        print("❌ Failed to send email:", str(e))

if __name__ == "__main__":
    otp = generate_otp()
    send_otp_email("er.anurag029@gmail.com", otp)
