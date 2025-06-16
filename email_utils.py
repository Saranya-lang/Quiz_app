import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import os

load_dotenv()

EMAIL = os.getenv("SENDER_EMAIL")
APP_PASSWORD = os.getenv("APP_PASSWORD")

def send_result(email, name, score, total):
    msg = EmailMessage()
    msg['Subject'] = 'Your Quiz Results'
    msg['From'] = 'saranyatest84@gmail.com'
    msg['To'] = email
    msg.set_content(f'Hi {name},\n\nYou scored {score}/{total}.\n\nThanks!')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL, APP_PASSWORD)
        smtp.send_message(msg)
    if __name__ == "__main__":
        print("send_result:", send_result)

if __name__ == "__main__":
    send_result("test@example.com", "Test User", 18, 20)