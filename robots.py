#!/usr/bin/python3
import requests
import urllib.robotparser

ROBOTS_URL = "https://services.swpc.noaa.gov/robots.txt"
USER_AGENT = "AuroraBot/1.0 https://aurorabot.tmbarrett.com"

HEADER_ROBOTS_ADD = [("User-Agent", USER_AGENT)]

def check_robots_txt():
    #Check robots.txt with desginated UA
    try:
        resp = request.get(ROBOTS_URL, headers=HEADER_ROBOTS_ADD, timeout=5)
    except requests.RequestException as e:
        print(f"Error fetching robots.txt: {e}")
        return False
    
    if resp.status_code == 404:
        # No robots.txt means you're allowed by convention
        return True
    
    if not (200 <= resp.status_code < 300):
        print(f"Unexpected robots.txt status: {resp.status_code}")
        return False
    
    rp = urllib.robotparser.RobotFileParser()
    rp.parse(resp.text.splitlines())

    allowed = rp.can_fetch(USER_AGENT, "https://services.swpc.noaa.gov/json/planetary_k_index_1m.json")

    if not allowed:
        print("Robots.txt disallows AuroraBot from accessing the data endpoint.")
        return False
    
    return True