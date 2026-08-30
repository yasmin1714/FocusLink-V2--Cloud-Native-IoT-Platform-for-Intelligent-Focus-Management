"""Data controller handling SQLAlchemy database interaction for FocusLink."""

from flask import current_app
from model import db
from model.FocusLink import FocusLink


class FocusLinkController:
    """Provides isolated transaction methods and read views for snapshot metrics."""

    @staticmethod
    def save_device_snapshot(email: str, username: str, device_payload: dict) -> FocusLink:
        """Saves a fresh telemetry API snapshot record into the database.

        Opens an explicit database transaction and commits the new snapshot record.

        Args:
            email (str): Target account email address.
            username (str): System username.
            device_payload (dict): Structured metric dictionary from external API.

        Returns:
            FocusLink: Persisted database model instance.

        Raises:
            Exception: Re-raises database exceptions after performing transaction rollback.
        """
        record = FocusLink(
            username=username or 'admin',
            email=email or 'admin@focuslink.local',
            user_id=str(device_payload.get('user_id', '')),
            device_id=str(device_payload.get('device_id', '')),
            device_name=device_payload.get('device_name', 'FocusLink IoT Node'),
            device_owner=device_payload.get('device_owner', 'Admin'),
            device_email=device_payload.get('device_email', email),
            device_status=device_payload.get('device_status', 'offline'),
            minutes_focused=device_payload.get('minutes_focused', 0),
            average_per_session=device_payload.get('average_per_session', 0.0),
            successful_sessions=device_payload.get('successful_sessions', 0),
            aborted_sessions=device_payload.get('aborted_sessions', 0)
        )

        try:
            db.session.add(record)
            db.session.commit()
            current_app.logger.info(f"DB Snapshot #{record.id} written for {email}")
            return record
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Failed writing database snapshot: {str(e)}")
            raise e

    @staticmethod
    def get_latest_record() -> FocusLink:
        """Retrieves the most recent record snapshot across all records.

        Returns:
            FocusLink: Most recent FocusLink database instance, or None.
        """
        return FocusLink.query.order_by(FocusLink.id.desc()).first()

    @staticmethod
    def get_all_records() -> list:
        """Retrieves all historical record snapshots.

        Returns:
            list: Collection of all FocusLink instances ordered newest first.
        """
        return FocusLink.query.order_by(FocusLink.created_at.desc()).all()