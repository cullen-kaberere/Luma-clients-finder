import smtplib
from email.mime.text import MIMEText
from config import Config

def send_daily_email(clients):
    if not clients:
        return

    body = "\n\n".join(
        f"{c.business_name} | {c.location} | {c.email} | {c.source_url}"
        for c in clients
    )
    msg = MIMEText(body)
    msg["Subject"] = "New Web Design Leads (Last 24 Hours)"
    msg["From"] = Config.EMAIL_USER
    msg["To"] = Config.EMAIL_TO

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(Config.EMAIL_USER, Config.EMAIL_PASS)
        server.sendmail(Config.EMAIL_USER, Config.EMAIL_TO, msg.as_string())
