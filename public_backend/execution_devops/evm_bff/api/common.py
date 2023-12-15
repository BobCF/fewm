import requests
from urllib3.util.retry import Retry
from urllib.parse import urlencode
from urllib.parse import urljoin,quote
from requests.adapters import HTTPAdapter
from requests.auth import HTTPBasicAuth

## Common RestAPI
def generate_url(base_url, params):
    query_string = urlencode(params)
    complete_url = f"{base_url}?{query_string}"
    return complete_url

def call_api(url, username, password, method="GET", data=None):
    # Configure retry settings
    retry_strategy = Retry(
        total=3,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "OPTIONS", "POST", "PUT", "DELETE"],
        backoff_factor=1,
    )

    headers = {
        "Content-Type": "application/json",
        "Accept": "*/*",
        "Connection":"keep-alive"
    }

    # Create an HTTPAdapter with the retry strategy
    adapter = HTTPAdapter(max_retries=retry_strategy)

    # Create a requests.Session object to add retry and authentication
    session = requests.Session()
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    session.auth = HTTPBasicAuth(username, password)

    # Make the API request in a try-catch block
    try:
        if method == "GET":
            response = session.get(url, verify=False, headers = headers,proxies= {'http':'',"https":''})
        elif method == "POST":
            response = session.post(url, verify=False, json=data, headers = headers,proxies= {'http':'',"https":''})
        elif method == "PUT":
            response = session.put(url, verify=False, json=data, headers = headers,proxies= {'http':'',"https":''})
        else:
            raise ValueError("Invalid method. Only 'GET' and 'POST' are supported.")

        if response.status_code == 200:
            return response.status_code, response.json()
        else:
            print(response.text)
            return response.status_code, None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while making the API request: {e}")
        return None, None
