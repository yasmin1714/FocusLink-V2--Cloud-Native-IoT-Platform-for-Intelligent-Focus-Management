"""Dashboard controller rendering dedicated templates for application tabs."""

from flask import render_template
from controller.api_engine import fetch_device_data
from controller.focuslink_data_controller import FocusLinkController


class DashboardController:
    """Provides read-only template rendering for metrics, device status, and timeline."""

    @staticmethod
    def render_dashboard():
        """Renders Tab 1: Focus Metrics Dashboard.

        Retrieves the latest snapshot record from SQLite without writing new data.

        Returns:
            Response: Rendered dashboard.html page template.
        """
        latest_record = FocusLinkController.get_latest_record()

        metrics = {
            'minutes_focused': latest_record.minutes_focused if latest_record else 0,
            'average_per_session': latest_record.average_per_session if latest_record else 0.0,
            'successful_sessions': latest_record.successful_sessions if latest_record else 0,
            'aborted_sessions': latest_record.aborted_sessions if latest_record else 0
        }

        return render_template('dashboard.html', active_tab='metrics', metrics=metrics)

    @staticmethod
    def render_device_details():
        """Renders Tab 2: Hardware Device Details.

        Executes a real-time live telemetry check via the external API engine.

        Returns:
            Response: Rendered device.html page template.
        """
        live_device_data = fetch_device_data()
        return render_template('device.html', device=live_device_data)

    @staticmethod
    def render_timeline():
        """Renders Tab 3: Historical Snapshot Archive.

        Queries all existing database snapshots in descending creation order.

        Returns:
            Response: Rendered timeline.html page template.
        """
        records = FocusLinkController.get_all_records()
        return render_template('timeline.html', records=records)

    @staticmethod
    def render_about():
        """Renders Tab 4: About FocusLink.

        Displays information about the application and its features.

        Returns:
            Response: Rendered about.html page template.
        """
        return render_template('about.html')