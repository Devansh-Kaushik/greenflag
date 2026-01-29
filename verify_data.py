import requests
import config
import data
import utils
import logging

# Setup basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("DataVerifier")

def verify_first_record():
    print("-" * 50)
    print("RUNNING DATA VERIFICATION")
    print("-" * 50)

    # 1. Load Data
    try:
        data.DataLoader.load_data()
        record = data.DataLoader.get_valid_record()
        print(f"Data Loaded. Testing with Record: {record}")
    except Exception as e:
        print(f"FAILED to load data: {e}")
        return

    # 2. Prepare Request
    phone = record['telephoneNumber']
    payload = {"telephoneNumber": phone}
    headers = utils.get_headers()
    url = config.BASE_URL + config.ETA_ENDPOINT

    print(f"Target URL: {url}")
    print(f"Payload: {payload}")
    print(f"Token (First 20 chars): {headers.get('Authorization', '')[:27]}...")

    # 3. Send Request
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        
        print("-" * 50)
        print(f"STATUS CODE: {response.status_code}")
        print(f"RESPONSE BODY: {response.text}")
        print("-" * 50)

        if response.status_code == 200:
            print("✅ SUCCESS! The data is valid and the API accepted it.")
            utils.validate_eta_logic(response, record['scenario'])
            print("✅ Business Logic Validation Passed.")
        elif response.status_code == 401:
            print("❌ AUTH FAILED. Your token is invalid or expired.")
        elif response.status_code == 400:
            print("❌ BAD REQUEST. The phone number was rejected by the backend.")
            print("👉 ACTION: Update phones.csv with a valid Green Flag rescue number.")
        else:
            print(f"❌ FAILED. Unexpected status code.")

    except Exception as e:
        print(f"❌ EXCEPTION during request: {e}")

if __name__ == "__main__":
    verify_first_record()
