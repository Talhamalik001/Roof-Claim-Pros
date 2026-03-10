import random
from email.message import EmailMessage
from aiosmtplib import SMTP
from config.settings import SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD

otp_store = {}

async def send_email_otp(email, otp):
    message = EmailMessage()
    message["From"] = SMTP_USER
    message["To"] = email
    message["Subject"] = "Your OTP Code"
    message.set_content(f"Hello!\n\nYour OTP code is: {otp}\n\nUse this to verify your account.\n\nThanks!")

    smtp = SMTP(hostname=SMTP_HOST, port=SMTP_PORT, start_tls=True)
    await smtp.connect()
    await smtp.login(SMTP_USER, SMTP_PASSWORD)  # App Password here
    await smtp.send_message(message)
    await smtp.quit()

async def generate_otp(email):
    otp = str(random.randint(100000, 999999))
    otp_store[email] = otp
    print(f"[DEBUG] OTP for {email}: {otp}")  # Optional console debug
    await send_email_otp(email, otp)
    return otp

def verify_otp(email, otp):
    saved_otp = otp_store.get(email)
    return saved_otp == otp