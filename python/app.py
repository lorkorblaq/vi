import os
import base64
import requests
from flask import Flask, redirect, request, url_for
import urllib.parse 
from urllib.parse import urlencode
from fhirclient import client,server
from fhirclient.models.patient import Patient

app = Flask(__name__)

# settings = {
#     'app_id': 'd81ed990-b75a-4fb8-94b5-a9df0e809631',
#     'api_base': 'https://fhir.epic.com/interconnect-fhir-oauth/api/FHIR/R4'
# }

# smart = server.FHIRServer(None, 'https://r4.smarthealthit.org')
# patient = Patient.read('eq081-VQEgP8drUUqCWzHfw', smart)
# print(patient.name[0].given)

# smart = client.FHIRClient(settings=settings)
# patient = Patient.read('eq081-VQEgP8drUUqCWzHfw3', smart.server)
# print(patient.birthDate.isostring)




# FHIR API and OAuth details
client_id = "d81ed990-b75a-4fb8-94b5-a9df0e809631"  # Your Client ID
patient_id = "eq081-VQEgP8drUUqCWzHfw3"  # Your demo patient ID
# client_secret = "d91EymMbcRIF1BX0"  # Your Client Secret
redirect_uri = "http://127.0.0.1:5000/callback"  # Redirect URI for localhost
auth_url = "https://fhir.epic.com/interconnect-fhir-oauth/oauth2/authorize"
token_url = "https://fhir.epic.com/interconnect-fhir-oauth/oauth2/token"
base_url_api = "https://fhir.epic.com/interconnect-fhir-oauth/api/FHIR/R4"

# Generate a random state value for CSRF protection
state_value = base64.urlsafe_b64encode(os.urandom(32)).decode('utf-8')
print(f"Generated state value: {state_value}")


added_scope = (
    "patient/Binary.read patient/CarePlan.read patient/CareTeam.read "
    "patient/Communication.read patient/Condition.read patient/Condition.write "
    "patient/Coverage.read patient/Device.read patient/DeviceRequest.read "
    "patient/DeviceUseStatement.read patient/DiagnosticReport.read "
    "patient/DocumentReference.read patient/DocumentReference.write "
    "patient/Encounter.read patient/FamilyMemberHistory.read patient/Flag.read "
    "patient/Goal.read patient/Immunization.read patient/ImmunizationRecommendation.read "
    "patient/List.read patient/Location.read patient/Medication.read "
    "patient/MedicationDispense.read patient/MedicationRequest.read "
    "patient/Observation.read patient/Observation.write patient/Organization.read "
    "patient/Patient.read patient/Practitioner.read patient/PractitionerRole.read "
    "patient/Procedure.read patient/Provenance.read patient/Questionnaire.read "
    "patient/QuestionnaireResponse.Read patient/QuestionnaireResponse.read "
    "patient/RelatedPerson.read patient/ServiceRequest.read patient/Specimen.read "
    "patient/Substance.read launch/patient"
)

# Concatenate the openid and fhirUser scope with the additional permissions

scope = f"openid fhirUser {added_scope}"
encoded_scope = urllib.parse.quote(scope)



# Define the OAuth URL for Epic's authorization
def get_authorization_url():
    # Parameters to include in the authorization URL
    params = {
        'client_id': client_id,
        'scope': scope,
        'response_type': 'code',
        'redirect_uri': redirect_uri,
        'state': state_value,
        'code_challenge_method': 'S256',
        'code_challenge': 'PHHQCoInTVWPbe78fWbQSftF5f6nn7hgskfLfEm4L6s',
        'aud': base_url_api
    }
    # Encode the parameters using urlencode
    encoded_params = urlencode(params)
    
    # Concatenate base URL with encoded parameters
    url = f"{auth_url}?{encoded_params}"
    print(f"Authorization URL: {url}")  # Debug: print the generated URL
    
    return url

# Route to start the authorization process
@app.route('/')
def index():
    print("Redirecting to the authorization URL...")  # Debug: indicate redirection
    auth_url = get_authorization_url()
    
    return redirect(auth_url)

# Callback route to handle the redirect from Epic with authorization code
@app.route('/callback')
def callback():
    # Get the authorization code and state from the URL
    code = request.args.get('code')
    state = request.args.get('state')

    print(f"Received state: {state}")  # Debug: print the received state
    print(f"Received code: {code}")    # Debug: print the received authorization code

    # Verify the state (to protect against CSRF)
    if state != state_value:
        print("State value mismatch. Potential CSRF attack.")  # Debug: print mismatch message
        return "State value mismatch. Potential CSRF attack.", 400

    if not code:
        print("Error: No authorization code received.")  # Debug: print error message
        return "Error: No authorization code received.", 400

    # Exchange the authorization code for an access token
    token_data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': redirect_uri,
        'client_id': client_id,
        # 'client_secret': client_secret,
    }

    print(f"Token request data: {token_data}")  # Debug: print the token request data

    # Make the request to get the token
    response = requests.post(token_url, data=token_data)

    # Debug: print the response status code and text
    print(f"Response status code: {response.status_code}")
    print(f"Response text: {response.text}")

    if response.status_code == 200:
        # Successfully obtained access token
        token_response = response.json()
        access_token = token_response.get('access_token')
        print(f"Successfully obtained access token: {access_token}")  # Debug: print access token
        
        # Now, use the access token to make API calls to Epic FHIR API
        # Example: Retrieve Patient Information (GET request)

        get_patient_data(access_token)  # Call the function to retrieve patient data    

    else:
        print(f"Error: {response.status_code} - {response.text}")  # Debug: print error if token request fails
        return f"Error: {response.status_code} - {response.text}", 400


def get_patient_data(access_token):
    # Construct the FHIR endpoint URL (assuming you want to retrieve patient info)
    patient_url = f"{base_url_api}/Patient/{patient_id}"  # Replace with the appropriate endpoint

    # Authorization header using the access token
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Accept': 'application/fhir+json',
    }

    # Make a GET request to the Epic FHIR API
    response = requests.get(patient_url, headers=headers)

    if response.status_code == 200:
        patient_data = response.json()
        return patient_data
    else:
        return f"Error retrieving patient data: {response.status_code} - {response.text}"

if __name__ == '__main__':
    app.run(debug=True, port=5000)
