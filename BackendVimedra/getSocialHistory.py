import requests
import json
from requestToken import fetch_access_token  # Import the function to fetch the access token
from createJWT import JWTGenerator  # Import the class to generate JWT

# Configuration
token_endpoint = "https://fhir.epic.com/interconnect-fhir-oauth/oauth2/token"
base_url = "https://fhir.epic.com/interconnect-fhir-oauth/api/FHIR/R4/"
resource = "Patient"
resource2= "Observation"
patient_id = "eq081-VQEgP8drUUqCWzHfw3"  # Replace with the actual patient ID
patient_id2 ="erXuFYUfucBZaryVksYEcMg3"

# Client ID
client_id = "82148705-681d-4cc2-8c28-b6215b22991d"

# Generate JWT
jwt_generator = JWTGenerator(client_id)  # Assuming the JWTGenerator class is implemented in createJWT.py
jwt_token = jwt_generator.generate_jwt()  # This method should return the JWT

# Fetch Access Token
access_token = fetch_access_token(token_endpoint, jwt_token)  # Fetch the OAuth2 token using the generated JWT
if not isinstance(access_token, str):
    print("Error fetching access token:", access_token)
    exit()

loincs = "http%3A%2F%2Floinc.org%7C4548-4"  # A1c code
# Construct the URL to get social history data
urlSocialHistory = f"{base_url}{resource2}/{patient_id}"
urlVitalsHistory = f"{base_url}{resource2}?category=vital-signs&patient={patient_id}"
urlA1cHistory = f"{base_url}{resource2}?patient={patient_id2}&limit=50&code={loincs}"

# Set up the headers including the authorization token

headers = {
    "Authorization": f"Bearer {access_token}",
    "Accept": "application/fhir+json"
}

# Send the GET request
response = requests.get(urlA1cHistory, headers=headers)

# Check if the response is successful
if response.status_code == 200:
    try:
        data = response.json()  # Attempt to parse JSON
        file_path = "social_history_data3.json"
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)
        print("Social History Data:", data)
        print(f"Data has been saved to {file_path}")
    except ValueError:
        print("Response is not in JSON format:", response.text)
else:
    print(f"Failed to retrieve data. Status Code: {response.status_code}")
    print("Response Content:", response.text)
    try:
        # Print out the detailed error message from the response, if available
        error_data = response.json()  # Attempt to parse the error message in JSON format
        print("Error Details:", error_data)
    except ValueError:
        # If the response body is not in JSON format, print the raw response text
        print("Error Message:", response.text)