# token_request.py
import requests

def fetch_access_token(token_endpoint, jwt_token):
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "client_credentials",
        "client_assertion_type": "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
        "client_assertion": jwt_token
    }

    response = requests.post(token_endpoint, headers=headers, data=data)

    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        return {"error": response.json()}
