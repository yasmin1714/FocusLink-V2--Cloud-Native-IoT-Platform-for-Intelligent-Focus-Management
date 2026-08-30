import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from model import db
from routes.Focuslink import focuslink_bp

BLYNK_AUTH_TOKEN = os.getenv("BLYNK_AUTH_TOKEN")


def create_app():
    app = Flask(__name__)

    base_dir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(base_dir, "data", "focuslink.db")
    log_dir = os.path.join(base_dir, "logs")
    log_file = os.path.join(log_dir, "focuslink.log")

    os.makedirs(log_dir, exist_ok=True)
    os.makedirs(os.path.join(base_dir, "data"), exist_ok=True)

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "default-dev-secret-key")
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    logger = logging.getLogger("focuslink")
    logger.setLevel(logging.INFO)

    file_handler = RotatingFileHandler(log_file, maxBytes=10485760, backupCount=5)
    file_handler.setFormatter(
        logging.Formatter("[%(asctime)s] %(levelname)s in %(module)s: %(message)s")
    )

    if not logger.handlers:
        logger.addHandler(file_handler)

    app.logger = logger

    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(focuslink_bp)

    return app


app = create_app()

if __name__ == "__main__":
    if not BLYNK_AUTH_TOKEN:
        app.logger.warning("BLYNK_AUTH_TOKEN environment variable is not set.")

    app.run(debug=True, port=5000)
