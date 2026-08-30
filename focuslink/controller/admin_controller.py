"""Admin controller managing authentication, cookie clearing, and route protection."""

import hashlib
import os
import secrets
from functools import wraps
from flask import (
    request, redirect, url_for, render_template, current_app, make_response
)
from controller.api_engine import fetch_device_data
from controller.focuslink_data_controller import FocusLinkController
from controller.host_registry_controller import HostRegistryController

AUTH_COOKIE = 'FocusLink_Auth'
CLIENT_COOKIE = 'FocusLink_Client'


class AdminController:
    """Handles admin login processing, security verification, and decorators."""

    @staticmethod
    def _verify_credentials(username: str, password: str) -> tuple:
        """Verifies admin credentials using SHA-512 and configured salt."""
        expected_username = os.getenv('ADMIN_USERNAME', 'admin')
        salt = os.getenv('ADMIN_SALT', 'FocusLink')
        expected_hash = os.getenv('ADMIN_PASSWORD_HASH', '')

        if username != expected_username:
            return False, None

        salted_password = f"{salt}{password}".encode('utf-8')
        computed_hash = hashlib.sha512(salted_password).hexdigest()

        if computed_hash.lower() == expected_hash.lower():
            return True, computed_hash

        return False, None

    @staticmethod
    def require_admin_cookie(f):
        """Decorator validating incoming cookies against the known_hosts CSV registry."""
        @wraps(f)
        def decorated_function(*args, **kwargs):
            client_alias = request.cookies.get(CLIENT_COOKIE)
            raw_token = request.cookies.get(AUTH_COOKIE)

            is_verified = HostRegistryController.verify_client(client_alias, raw_token)

            if not is_verified:
                current_app.logger.warning(
                    f"Unauthorized access attempt for client alias: {client_alias}"
                )
                response = make_response(redirect(url_for('focuslink.login_view')))
                response.delete_cookie(AUTH_COOKIE)
                response.delete_cookie(CLIENT_COOKIE)
                return response

            return f(*args, **kwargs)
        return decorated_function

    @staticmethod
    def render_login():
        """Renders the login template."""
        return render_template('login.html')

    @staticmethod
    def authenticate_admin():
        """Authenticates user credentials, writes a DB snapshot, and registers host.

        Wipes pre-existing cookies prior to validation to prevent stale session 403 errors.
        """
        username = request.form.get('username', '')
        password = request.form.get('password', '')

        is_valid, _ = AdminController._verify_credentials(username, password)

        if is_valid:
            current_app.logger.info(f"Successful authentication for admin: {username}")

            device_data = fetch_device_data()
            user_email = device_data.get('device_email') or 'admin@focuslink.local'

            try:
                FocusLinkController.save_device_snapshot(
                    email=user_email,
                    username=username,
                    device_payload=device_data
                )
            except Exception as e:
                current_app.logger.error(f"Snapshot creation failed during login: {str(e)}")

            # 1. Generate encrypted SHA-512 client alias for cookie & registry
            client_alias = HostRegistryController.generate_client_alias(user_email)

            # 2. Generate random session token
            raw_token = secrets.token_urlsafe(32)

            # 3. Save alias and token_hash in data/known_hosts.csv
            HostRegistryController.register_client(
                client_alias=client_alias,
                raw_token=raw_token
            )

            response = make_response(redirect(url_for('focuslink.index')))

            # Flush any stale pre-login cookies
            response.delete_cookie(AUTH_COOKIE)
            response.delete_cookie(CLIENT_COOKIE)

            # Set fresh security cookies containing ONLY SHA-512 hashes/tokens
            response.set_cookie(
                AUTH_COOKIE, raw_token, httponly=True, samesite='Lax', max_age=86400
            )
            response.set_cookie(
                CLIENT_COOKIE, client_alias, httponly=True, samesite='Lax', max_age=86400
            )

            return response

        current_app.logger.warning(f"Failed authentication attempt for user: {username}")
        response = make_response(
            render_template('login.html', error="Invalid username or password"), 401
        )
        response.delete_cookie(AUTH_COOKIE)
        response.delete_cookie(CLIENT_COOKIE)
        return response

    @staticmethod
    def logout_admin():
        """Flushes session cookies and redirects to login view."""
        response = make_response(redirect(url_for('focuslink.login_view')))
        response.delete_cookie(AUTH_COOKIE)
        response.delete_cookie(CLIENT_COOKIE)
        current_app.logger.info("Admin user logged out and host cookies purged.")
        return response