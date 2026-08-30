import os
import requests
from flask import current_app
from dotenv import load_dotenv

def safe_int(val, default=0):
    try:
        return int(float(val))
    except (ValueError, TypeError):
        return default

def safe_float(val, default=0.0):
    try:
        return float(val)
    except (ValueError, TypeError):
        return default

def fetch_device_data(auth_token=None, server_url=None):
    load_dotenv()  # Load environment variables from .env file
    token = auth_token or os.getenv('BLYNK_AUTH_TOKEN')
    base_url = (server_url or os.getenv('BLYNK_SERVER', 'https://blynk.cloud')).rstrip('/')

    if not token:
        print("Missing BLYNK_AUTH_TOKEN parameter.")
        return {}

    pin_url = f"{base_url}/external/api/get?token={token}&v1&v2&v3&v4"
    name_url = f"{base_url}/external/api/device/meta?token={token}&metaFieldId=1"
    owner_url = f"{base_url}/external/api/device/meta?token={token}&metaFieldId=2"
    status_url = f"{base_url}/external/api/isHardwareConnected?token={token}"

    session = requests.Session()

    try:
        pins_res = session.get(pin_url, timeout=5)
        pins_data = pins_res.json() if pins_res.status_code == 200 else {}
    except Exception as e:
        print(f"Error fetching virtual pins: {e}")
        pins_data = {}

    try:
        name_res = session.get(name_url, timeout=5)
        name_data = name_res.json() if name_res.status_code == 200 else {}
    except Exception as e:
        print(f"Error fetching device name: {e}")
        name_data = {}

    try:
        owner_res = session.get(owner_url, timeout=5)
        owner_data = owner_res.json() if owner_res.status_code == 200 else {}
    except Exception as e:
        print(f"Error fetching device owner: {e}")
        owner_data = {}

    try:
        status_res = session.get(status_url, timeout=5)
        status_text = status_res.text if status_res.status_code == 200 else "false"
    except Exception as e:
        print(f"Error fetching hardware status: {e}")
        status_text = "false"

    device_owner = owner_data.get('value')
    user_id = str(owner_data.get('userId')) if owner_data.get('userId') is not None else None
    is_online = status_text.strip().lower() == 'true'

    return {
        'device_id': token[:10],
        'user_id': user_id,
        'device_name': name_data.get('value'),
        'device_owner': device_owner,
        'device_email': device_owner,
        'device_status': 'online' if is_online else 'offline',
        'minutes_focused': safe_int(pins_data.get('v1')),
        'average_per_session': safe_float(pins_data.get('v2')),
        'successful_sessions': safe_int(pins_data.get('v3')),
        'aborted_sessions': safe_int(pins_data.get('v4'))
    }

print(fetch_device_data())