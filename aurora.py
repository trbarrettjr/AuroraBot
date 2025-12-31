#!/usr/bin/python
import requests
import json
import robots
import os

DATA_URL = "https://services.swpc.noaa.gov/json/planetary_k_index_1m.json"
USER_AGENT = "AuroraBot/1.0 https://aurorabot.tmbarrett.com"
HEADER_DATA_ADD = [("User-Agent", USER_AGENT), ("Accept", "application/json")]

PO_USER_KEY = os.environ.get('PO_USER_KEY')
PO_APP_KEY = os.environ.get('PO_APP_KEY')
PO_API_END = "https://api.pushover.net/1/messages.json"
PO_HEADER = [("User-Agent", USER_AGENT), ("Content-Type", "application/json")]
PO_BODY = {
    "token": PO_APP_KEY,
    "user": PO_USER_KEY,
    "title": "AuroraBot Notification",
}

def start():
    allowed_robots = robots.check_robots_txt()
    if allowed_robots:
        kp_data = get_kp_data()
    else:
        print("Not Allowed by robots.txt; notification required")
        send_pushover(f"Not allowed by robots.txt, please research for more details.")
        exit(403)

    latest = kp_data[-1]
    kp = latest["kp_index"]
    timestamp = latest["time_tag"]

def send_pushover(msg):
    if not (PO_APP_KEY and PO_USER_KEY):
        return None
    
    key, value = ("message", msg)
    body = PO_BODY.copy()
    body[key] = value
    r = requests.post(PO_API_END, json=body, headers=dict(PO_HEADER))
    if r.status_code not in range(200, 300):
        print(f"Pushover error: {r.status_code} {r.text}")
    

def get_kp_data():
    try:
        req = requests.get(DATA_URL, headers=dict(USER_AGENT), timeout=5)
    except requests.RequestException as e:
        send_pushover(f"Error fetching K-index data: {e}")
        exit(502)

    if not (200 <= req.status_code < 300):
        send_pushover(f"NOAA returned {req.status_code}")
        exit(502)
    
    try:
        return req.json()
    except ValueError:
        send_pushover("NOAA returned invalid JSON")
        exit(502)

if __name__ == "__main__":
    start()