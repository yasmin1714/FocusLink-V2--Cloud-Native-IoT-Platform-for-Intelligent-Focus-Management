"""Controller managing client hardware fingerprint verification via CSV registry."""

import csv
import hashlib
import os
from flask import current_app
from datetime import datetime, timezone

REGISTRY_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "data", "known_hosts.csv"
)


class HostRegistryController:
    """Manages reading and writing client fingerprint hashes in known_hosts.csv."""

    @staticmethod
    def generate_client_alias(user_email: str) -> str:
        """Generates a keyed SHA-512 fingerprint alias for a user email.

        Args:
            user_email (str): Plain-text email address.

        Returns:
            str: 64-character SHA-512 client alias hex string.
        """
        salt = os.getenv("ADMIN_SALT", "FocusLink")
        salted_email = f"FocusLink_Client:{salt}:{user_email}".encode("utf-8")
        return hashlib.sha512(salted_email).hexdigest()

    @staticmethod
    def _ensure_file_exists() -> None:
        """Ensures that data/known_hosts.csv exists with correct header rows."""
        os.makedirs(os.path.dirname(REGISTRY_PATH), exist_ok=True)
        if not os.path.exists(REGISTRY_PATH):
            with open(REGISTRY_PATH, mode="w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["client_alias", "token_hash", "updated_at"])


    @staticmethod
    def register_client(client_alias: str, raw_token: str) -> None:
        HostRegistryController._ensure_file_exists()

        salt = os.getenv("ADMIN_SALT", "FocusLink")
        token_hash = hashlib.sha512(
            f"FocusLink_Token:{salt}:{raw_token}".encode("utf-8")
        ).hexdigest()

        current_timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        rows = []
        updated = False

        if os.path.exists(REGISTRY_PATH):
            with open(REGISTRY_PATH, mode="r", newline="", encoding="utf-8") as f:
                reader = csv.reader(f)
                header = next(reader, None)
                for row in reader:
                    if row and row[0] == client_alias:
                        rows.append([client_alias, token_hash, current_timestamp])
                        updated = True
                    elif row:
                        rows.append(row)

        if not updated:
            rows.append([client_alias, token_hash, current_timestamp])

        with open(REGISTRY_PATH, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["client_alias", "token_hash", "updated_at"])
            writer.writerows(rows)

    @staticmethod
    def verify_client(client_alias: str, raw_token: str) -> bool:
        """Verifies if the client alias and raw token match the known_hosts registry.

        Args:
            client_alias (str): Encrypted client alias extracted from incoming cookie.
            raw_token (str): Raw auth token extracted from incoming cookie.

        Returns:
            bool: True if verification succeeds, False otherwise.
        """
        if not client_alias or not raw_token or not os.path.exists(REGISTRY_PATH):
            return False

        salt = os.getenv("ADMIN_SALT", "FocusLink")
        computed_token_hash = hashlib.sha512(
            f"FocusLink_Token:{salt}:{raw_token}".encode("utf-8")
        ).hexdigest()

        with open(REGISTRY_PATH, mode="r", newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                if row and len(row) >= 2:
                    if row[0] == client_alias and row[1] == computed_token_hash:
                        return True

        return False
