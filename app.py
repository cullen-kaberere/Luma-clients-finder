from flask import Flask
from config import Config
from models import db
from scheduler import start_scheduler

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

@app.route("/")
def home():
    return "Lead Gen Bot is running."

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    start_scheduler()
    app.run(debug=False)
