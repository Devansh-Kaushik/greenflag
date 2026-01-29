import os
import sys

# --- Configuration Constants ---

# Environment Checks
BASE_DOMAIN = os.getenv("BASE_DOMAIN", "si.mycro.cloud")

# Token Loading Logic
env_token = os.getenv("BEARER_TOKEN")
file_token = None

token_path = os.path.join(os.path.dirname(__file__), 'token.txt')
if os.path.exists(token_path):
    with open(token_path, 'r') as f:
        file_token = f.read().strip()

# Decision Logic (Prioritize File if Env is short/likely junk, or just log it)
if env_token and len(env_token) > 50:
    BEARER_TOKEN = env_token
    print(f"CONFIG: Using Bearer Token from ENVIRONMENT VARIABLE ({BEARER_TOKEN[:10]}...)")
elif file_token and len(file_token) > 50:
    BEARER_TOKEN = file_token
    print(f"CONFIG: Using Bearer Token from FILE 'token.txt' ({BEARER_TOKEN[:10]}...)")
else:
    # Fallback to whatever we have, or warn
    BEARER_TOKEN = env_token or file_token
    print(f"CONFIG: WARNING - Token seems missing or too short. Valid/File Token required.")

if not BEARER_TOKEN:
    print("ERROR: No BEARER_TOKEN found.")

# Constructed URL
BASE_URL = f"https://gfdtv-platform-api.{BASE_DOMAIN}"
ETA_ENDPOINT = "/gfdtv-platform-ms-eta-deflection-update/v1/rescue/eta"

# Performance Thresholds
RESPONSE_TIME_THRESHOLD_MS = int(os.getenv("RESPONSE_TIME_THRESHOLD_MS", "1500"))
REQUEST_TIMEOUT = float(os.getenv("REQUEST_TIMEOUT", "10.0"))

# Data
DATA_FILE_PATH = os.getenv("DATA_FILE_PATH", "phones.csv")

# Traffic Weights
WEIGHT_VALID = int(os.getenv("WEIGHT_VALID", "80"))
WEIGHT_INVALID = int(os.getenv("WEIGHT_INVALID", "10"))
WEIGHT_AUTH_FAIL = int(os.getenv("WEIGHT_AUTH_FAIL", "10"))

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
