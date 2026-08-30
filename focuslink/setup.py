#!/usr/bin/env python3
"""Project bootstrap script for FocusLink IoT Application.

Initializes directory structure, runtime environment configuration (.env),
host registry files, and database schema prior to running app.py.
"""

import hashlib
import os
import secrets
import subprocess
import sys

# Core directory layout definition
REQUIRED_DIRECTORIES = [
    "controller",
    "data",
    "docs",
    "logs",
    "model",
    "routes",
    "templates",
]

DEFAULT_ENV_CONTENT = """# FocusLink Environment Configuration

# Flask Application Settings
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY={secret_key}

# Security & Authentication Settings
ADMIN_USERNAME=admin
ADMIN_PASSWORD_HASH={admin_password_hash}
ADMIN_SALT={admin_salt}

# Database Configuration
DATABASE_URL=sqlite:///data/focuslink.db
"""


def log_status(message: str, symbol: str = "[*]") -> None:
    """Helper to log clean console status output."""
    print(f"{symbol} {message}")


def create_directories() -> None:
    """Creates required project directories if they do not exist."""
    log_status("Checking and creating directory structure...")
    for folder in REQUIRED_DIRECTORIES:
        os.makedirs(folder, exist_ok=True)
    log_status("Directories verified.", symbol="[✔]")


def generate_default_env() -> None:
    """Generates a populated .env file with default salted admin credentials if missing."""
    env_path = ".env"
    if os.path.exists(env_path):
        log_status(".env file already exists. Skipping creation.", symbol="[!] ")
        return

    log_status("Generating default .env configuration file...")

    # Default bootstrap credentials: username='admin', password='adminpassword'
    admin_salt = secrets.token_hex(16)
    default_password = "Admin#123"
    salted_pwd = f"{admin_salt}{default_password}".encode("utf-8")
    admin_password_hash = hashlib.sha512(salted_pwd).hexdigest()
    secret_key = secrets.token_hex(32)

    env_content = DEFAULT_ENV_CONTENT.format(
        secret_key=secret_key,
        admin_password_hash=admin_password_hash,
        admin_salt=admin_salt,
    )

    with open(env_path, "w", encoding="utf-8") as f:
        f.write(env_content)

    log_status(
        "Generated .env with default credentials (admin / adminpassword)",
        symbol="[✔]",
    )


def initialize_known_hosts() -> None:
    """Ensures data/known_hosts.csv exists with proper column headers."""
    csv_path = os.path.join("data", "known_hosts.csv")
    if not os.path.exists(csv_path):
        log_status("Initializing data/known_hosts.csv registry...")
        with open(csv_path, "w", encoding="utf-8") as f:
            f.write("client_alias,token_hash,updated_at\n")
        log_status("Created known_hosts.csv.", symbol="[✔]")


def run_database_init() -> None:
    """Executes db_init.py to create SQLite tables."""
    db_init_script = "db_init.py"
    if not os.path.exists(db_init_script):
        log_status(
            f"Warning: {db_init_script} not found in root directory.",
            symbol="[!]",
        )
        return

    log_status("Initializing database tables via db_init.py...")
    try:
        result = subprocess.run(
            [sys.executable, db_init_script],
            check=True,
            capture_output=True,
            text=True,
        )
        if result.stdout:
            print(result.stdout.strip())
        log_status("Database initialization complete.", symbol="[✔]")
    except subprocess.CalledProcessError as err:
        log_status(f"Error running db_init.py:\n{err.stderr}", symbol="[✘]")
        sys.exit(1)


def main() -> None:
    """Runs setup tasks sequentially."""
    print("=" * 55)
    print("       FocusLink IoT App Bootstrap Setup       ")
    print("=" * 55)

    create_directories()
    generate_default_env()
    initialize_known_hosts()
    run_database_init()

    print("=" * 55)
    log_status("Setup complete! You can now launch the application:", symbol="🚀")
    print("      python app.py")
    print("=" * 55)


if __name__ == "__main__":
    main()