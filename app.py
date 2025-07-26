# app.py

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_apscheduler import APScheduler
from datetime import datetime
import os
import sendgrid
from sendgrid.helpers.mail import Mail
from models import db, Lead
import config

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_URI
db.init_app(app)

scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

# --------- Helper: Add Lead Safely ---------
def add_lead(business_name, location, email, website_url, website_status):
    exists = Lead.query.filter_by(business_name=business_name, location=location).first()
    if exists:
        print(f"[SKIP] {business_name} already exists.")
        return False
    lead = Lead(
        business_name=business_name,
        location=location,
        email=email,
        website_url=website_url,
        website_status=website_status,
        contacted=False
    )
    db.session.add(lead)
    db.session.commit()
    print(f"[ADDED] {business_name}")
    return True

# --------- Route: Add Lead via API (Example) ---------
@app.route('/add_test_lead')
def add_test_lead():
    add_lead("Sunlight Cafe", "Vancouver", "sunlight@biz.com", None, "Missing")
    return "Test lead added."

# --------- Daily Email Job ---------
@scheduler.task('cron', id='daily_email', hour=9)
def daily_email_job():
    with app.app_context():
        leads = Lead.query.filter_by(contacted=False).all()
        if not leads:
            print("[EMAIL] No new leads.")
            return

        html_content = render_template('email.html', leads=leads)
        send_email("🔥 Daily New Leads Report", html_content)

# --------- Email Sender ---------
def send_email(subject, html_content):
    sg = sendgrid.SendGridAPIClient(api_key=config.SENDGRID_API_KEY)
    message = Mail(
        from_email=config.EMAIL_SENDER,
        to_emails=config.EMAIL_RECEIVER,
        subject=subject,
        html_content=html_content
    )
    try:
        response = sg.send(message)
        print(f"[EMAIL SENT] Status Code: {response.status_code}")
    except Exception as e:
        print(f"[EMAIL ERROR] {e}")

# --------- Initialize DB (once) ---------
@app.before_first_request
def setup():
    db.create_all()

# --------- Main ---------
if __name__ == '__main__':
    app.run(debug=True)
