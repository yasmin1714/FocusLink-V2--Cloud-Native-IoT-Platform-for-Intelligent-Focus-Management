"""Database initialization script for FocusLink.

Initializes the application context and ensures all model tables are created
in the target SQLite database prior to executing operational API syncs.
"""

import sys
from app import create_app
from model import db
from model.FocusLink import FocusLink


def init_database():
    """Initializes the database schema using the Flask application context."""
    app = create_app()

    with app.app_context():
        db_uri = app.config.get('SQLALCHEMY_DATABASE_URI')
        app.logger.info(f"Targeting Database URI: {db_uri}")

        try:
            db.create_all()
            app.logger.info("Database tables initialized successfully.")
            print("[SUCCESS] FocusLink database tables created/verified.")
        except Exception as e:
            app.logger.error(f"Failed to initialize database: {str(e)}")
            print(f"[ERROR] Database initialization failed: {str(e)}", file=sys.stderr)
            sys.exit(1)


if __name__ == '__main__':
    init_database()