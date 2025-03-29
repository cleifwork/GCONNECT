import os
import time
import json
import requests
import logging
from utils import FILE_PATHS

# Suppress logs from googleapiclient.discovery_cache
logging.getLogger("googleapiclient.discovery_cache").setLevel(logging.ERROR)

# Configure logging
class CustomStreamHandler(logging.StreamHandler):
    def emit(self, record):
        message = self.format(record)
        # Remove timestamp and log level from console output
        clean_message = message.split(" - ", 2)[-1]
        print(clean_message)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log", mode="a"),
        CustomStreamHandler()  # Use custom stream handler for console output
    ]
)

# File paths
TOKEN_FILE = FILE_PATHS["tokens"]
CREDS_FILE = FILE_PATHS["creds"]
CSV_FOLDER = FILE_PATHS["csv_folder"]
local_csv_path = os.path.join(CSV_FOLDER, 'VoucherList.csv')

# Freshness interval (24 hours)
FRESHNESS_INTERVAL = 24 * 60 * 60

# Ensure the raw_csv folder exists
os.makedirs(CSV_FOLDER, exist_ok=True)

# Token management functions
def load_credentials():
    try:
        with open(CREDS_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        logging.error("Credentials file not found!")
        return {}

def load_tokens():
    try:
        with open(TOKEN_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        logging.warning("Token file not found! Generating new tokens...")
        return {}

def save_tokens(access_token, refresh_token, expires_in):
    tokens = {
        "accessToken": access_token,
        "refreshToken": refresh_token,
        "expiresIn": time.time() + expires_in,
    }
    try:
        with open(TOKEN_FILE, "w") as file:
            json.dump(tokens, file)
        logging.info("Tokens saved successfully.")
    except Exception as e:
        logging.error(f"Failed to save tokens: {e}")



def generate_new_tokens():
    creds = load_credentials()
    url = "https://aps1-omada-northbound.tplinkcloud.com/openapi/authorize/token?grant_type=client_credentials"
    payload = {
        "omadacId": creds.get("omadac_id"),
        "client_id": creds.get("client_id"),
        "client_secret": creds.get("client_secret")
    }
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, json=payload, headers=headers, verify=False)
        if response.status_code == 200:
            response_json = response.json()
            if response_json.get("errorCode") == 0:
                result = response_json["result"]
                save_tokens(result["accessToken"], result["refreshToken"], result["expiresIn"])
                return result["accessToken"]
            else:
                logging.error(f"API Error: {response_json.get('msg')}")
        else:
            logging.error(f"HTTP Error {response.status_code}: {response.reason}")
    except requests.RequestException as e:
        logging.error(f"Failed to connect to API: {e}")
    return None


# Refresh the access token using the refresh token
def refresh_access_token():
    creds = load_credentials()
    tokens = load_tokens()
    refresh_token = tokens.get("refreshToken")
    
    if not refresh_token:
        logging.warning("No refresh token found! Re-authenticating...")
        return generate_new_tokens()

    url = "https://aps1-omada-northbound.tplinkcloud.com/openapi/authorize/token"

    # Request payload (mimicking cURL format)
    params = {
        "client_id": creds.get("client_id"),
        "client_secret": creds.get("client_secret"),
        "refresh_token": refresh_token,
        "grant_type": "refresh_token",
    }

    # headers = {"Content-Type": "application/json"}

    try:
        # Use `data=json.dumps(payload)` instead of `json=payload`
        # response = requests.post(url, data=json.dumps(payload), headers=headers, verify=False)
        response = requests.post(url, params=params, verify=False)
 
        if response.status_code == 200:
            response_json = response.json()
            
            if response_json.get("errorCode") == 0:
                result = response_json["result"]
                save_tokens(result["accessToken"], result["refreshToken"], result["expiresIn"])
                return result["accessToken"]
            else:
                logging.error(f"API Error: {response_json.get('msg')}")
        else:
            logging.error(f"HTTP Error {response.status_code}: {response.reason}")
    
    except requests.RequestException as e:
        logging.error(f"Failed to connect to API: {e}")

    # return None
        
    # If refresh fails, try full authentication again
    logging.warning("Refresh token failed, attempting full re-authentication...")
    return generate_new_tokens()


# Get a valid access token, refreshing or generating if necessary
def get_access_token():
    tokens = load_tokens()
    BUFFER_TIME = 10  # seconds

    if time.time() + BUFFER_TIME >= tokens.get("expiresIn", 0):
        logging.info("Access token expired or about to expire, refreshing...")
        return refresh_access_token()

    logging.info("Access token is valid, returning...")
    return tokens["accessToken"]

# Check file freshness
def is_file_fresh(file_path):
    if os.path.exists(file_path):
        last_modified = os.path.getmtime(file_path)
        return (time.time() - last_modified) < FRESHNESS_INTERVAL
    return False

# Fetch CSV data
def fetch_csv_from_api():
    omadac_id = "8663e0ef7add5a56bfc9dabe5adc9b14"
    site_id = "647eb8d0fb5fdb303898f445"
    api_url = f"https://aps1-omada-northbound.tplinkcloud.com/openapi/v1/{omadac_id}/files/hotspot/sites/{site_id}/vouchers/export"

    headers = {
        "Authorization": f"AccessToken={get_access_token()}",
        "Content-Type": "application/json"
    }
    payload = {
        "format": 0,
        "queryData": {
            "page": 1,
            "pageSize": 1000,
            "sorts": {},
            "searchKey": "",
            "filters": {},
            "searchField": ""
        },
        "type": 0,
        "groupIds": []
    }

    response = requests.post(api_url, headers=headers, json=payload)
    if response.status_code == 200:
        with open(local_csv_path, 'wb') as file:
            file.write(response.content)
        logging.info(f"CSV file saved to {local_csv_path}")
    else:
        logging.error(f"Failed to fetch CSV: {response.json()}")

# Main function
def main():
    if is_file_fresh(local_csv_path):
        logging.info(f"Using local CSV file: {local_csv_path}")
    else:
        logging.info("Fetching new VoucherList from your controller...")
        fetch_csv_from_api()

if __name__ == "__main__":
    main()
