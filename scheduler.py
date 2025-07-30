from apscheduler.schedulers.background import BackgroundScheduler
from scraper import scrape_businesses_without_websites
from mailer import send_daily_email
from models import Client, db
from datetime import datetime, timedelta

def collect_and_save():
    results = scrape_businesses_without_websites()
    for r in results:
        exists = Client.query.filter_by(business_name=r["business_name"], location=r["location"]).first()
        if not exists:
            client = Client(**r)
            db.session.add(client)
    db.session.commit()

def send_daily_summary():
    cutoff = datetime.utcnow() - timedelta(days=1)
    new_clients = Client.query.filter(Client.found_at >= cutoff).all()
    send_daily_email(new_clients)

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(collect_and_save, 'interval', hours=6)  # Scrape every 6 hrs
    scheduler.add_job(send_daily_summary, 'cron', hour=6, minute=30)  # Email at 6:30 AM
    scheduler.start()
