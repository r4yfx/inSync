import requests
import time
import traceback

# Import Libs required for Bearer Token OAuth2.0
from oauthlib.oauth2 import BackendApplicationClient
from requests.auth import HTTPBasicAuth
from requests_oauthlib import OAuth2Session

# Client credentials
client_id = '<client-id>'
secret_key = '<secret-key>'

# API base URL
api_url = "https://apis.druva.com/"

# Function to get the OAuth2.0 token
def get_token(client_id, secret_key):
    global auth_token, expires_at
    auth = HTTPBasicAuth(client_id, secret_key)
    client = BackendApplicationClient(client_id=client_id)
    oauth = OAuth2Session(client=client)
    response = oauth.fetch_token(token_url='https://apis.druva.com/token', auth=auth)
    auth_token = response['access_token']
    expires_at = response['expires_at']

# Function to make paginated API calls
def get_api_call(auth_token, api_url, api_path):
    nextpage = None
    while True:
        nextpage = _get_api_call(auth_token, api_url, api_path, nextpage)
        if not nextpage:
            break

# Helper function to make a single API call
def _get_api_call(auth_token, api_url, api_path, nextpage):
    headers = {'accept': 'application/json', 'Authorization': f'Bearer {auth_token}'}
    params = {'pageToken': nextpage} if nextpage else {}
    response = requests.get(api_url + api_path, headers=headers, params=params)

    try:
        print('Invoking API call')
        if response.status_code == 200:
            data = response.json()
            print(data)
            return data.get('nextPageToken')
        elif response.status_code == 429:
            print('Rate limit exceeded. Sleeping for 60 seconds...')
            time.sleep(60)
            return _get_api_call(auth_token, api_url, api_path, nextpage)
        else:
            print(f'Error occurred during API call. Status Code: {response.status_code}')
            print(response.text)
    except Exception as e:
        print('Exception occurred during API call:')
        print(traceback.format_exc())
        return None

# Main execution
if __name__ == "__main__":
    get_token(client_id, secret_key)
    print('Auth_token:', auth_token)

    # List all Users
    print('List all Users.')
    api_path = "insync/usermanagement/v1/users"
    get_api_call(auth_token, api_url, api_path)

    # List all Profiles
    print('List all Profiles.')
    api_path = "insync/profilemanagement/v1/profiles"
    get_api_call(auth_token, api_url, api_path)

    # List all Devices
    print('List all Devices.')
    api_path = "insync/endpoints/v1/devices"
    get_api_call(auth_token, api_url, api_path)

    # List all Devices Backups (Last Successful Backups)
    print('List all Devices Backups.')
    api_path = "insync/endpoints/v1/backups"
    get_api_call(auth_token, api_url, api_path)

    # List all Devices Restore activities
    print('List all Devices Restore activities.')
    api_path = "insync/endpoints/v1/restores"
    get_api_call(auth_token, api_url, api_path)

    # List all Storages
    print('List all Storages.')
    api_path = "insync/storagemanagement/v1/storages"
    get_api_call(auth_token, api_url, api_path)

