# config.py

import os

# Replace with your real DB URI
DATABASE_URI = os.getenv("DATABASE_URI", "postgresql://postgres:password@localhost:5432/leads_db")
EMAIL_SENDER = os.getenv("EMAIL_SENDER", "youremail@example.com")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER", "yourinbox@example.com")
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY", "your_sendgrid_api_key")
