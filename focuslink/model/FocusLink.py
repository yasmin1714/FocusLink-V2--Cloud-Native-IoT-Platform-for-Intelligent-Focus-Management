"""Database model representing FocusLink snapshot records."""

from datetime import datetime, timezone
from model import db


class FocusLink(db.Model):
    """SQLAlchemy model for storing time-series IoT device snapshots.

    Only the primary key `id` carries a UNIQUE constraint. Attributes such
    as `username` and `email` explicitly permit non-unique duplicate rows,
    enabling continuous time-series append logging on every login event.

    Attributes:
        id (int): Primary key unique identifier.
        username (str): System username associated with the snapshot.
        email (str): User email address.
        user_id (str): Unique hardware/platform user ID string.
        device_id (str): Hardware device ID string.
        device_name (str): Readable name of the connected IoT hardware.
        device_owner (str): Owner identifier returned from telemetry API.
        device_email (str): Telemetry account email address.
        device_status (str): Hardware status string (e.g., 'online', 'offline').
        minutes_focused (int): Cumulative focused minutes recorded.
        average_per_session (float): Computed average focus session length.
        successful_sessions (int): Count of completed focus sessions.
        aborted_sessions (int): Count of interrupted focus sessions.
        created_at (datetime): UTC timestamp when the record was inserted.
        updated_at (datetime): UTC timestamp when the record was updated.
    """

    __tablename__ = 'focus_link'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), nullable=False, unique=False)
    email = db.Column(db.String(120), nullable=False, unique=False)
    user_id = db.Column(db.String(100), nullable=True)
    device_id = db.Column(db.String(100), nullable=True)
    device_name = db.Column(db.String(100), nullable=True)
    device_owner = db.Column(db.String(100), nullable=True)
    device_email = db.Column(db.String(120), nullable=True)
    device_status = db.Column(db.String(50), nullable=True, default='offline')
    minutes_focused = db.Column(db.Integer, nullable=True, default=0)
    average_per_session = db.Column(db.Float, nullable=True, default=0.0)
    successful_sessions = db.Column(db.Integer, nullable=True, default=0)
    aborted_sessions = db.Column(db.Integer, nullable=True, default=0)
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

    def to_dict(self) -> dict:
        """Serializes the FocusLink instance into a Python dictionary.

        Returns:
            dict: Key-value representations of model attributes.
        """
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'user_id': self.user_id,
            'device_id': self.device_id,
            'device_name': self.device_name,
            'device_owner': self.device_owner,
            'device_email': self.device_email,
            'device_status': self.device_status,
            'minutes_focused': self.minutes_focused or 0,
            'average_per_session': float(self.average_per_session or 0.0),
            'successful_sessions': self.successful_sessions or 0,
            'aborted_sessions': self.aborted_sessions or 0,
            'created_at': (
                self.created_at.isoformat() if self.created_at else None
            ),
            'updated_at': (
                self.updated_at.isoformat() if self.updated_at else None
            )
        }