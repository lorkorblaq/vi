import req as req



# import os
# import base64

# # Generate a random 32-byte state value
# state_value = base64.urlsafe_b64encode(os.urandom(32)).decode('utf-8')

#vimedra non-prod client id
client_id = "f0cc4bee-fa06-49bc-943f-7ad3ad89ebe5"

# demo patient ID
patient_id = "f0cc4bee-fa06-49bc-943f-7ad3ad89ebe5"
# url = f"https://vimedra.replit.app/api/FHIR/R4/Patient/{patient_id}"

# base URL for the Epic FHIR API
base_url_api = "https://fhir.epic.com/interconnect-fhir-oauth/api/FHIR/R4"

# token endpoint
token_url = 'https://fhir.epic.com/interconnect-fhir-oauth/oauth2/token'


# Authorization Endpoint
auth_url = "https://fhir.epic.com/interconnect-fhir-oauth/oauth2/authorize"

url = (
    "https://fhir.epic.com/interconnect-fhir-oauth/oauth2/authorize?"
    "client_id=e3073934-68c1-4ca7-9b59-3d8b934187f1&"
    "scope=openid%20fhirUser&"
    "response_type=code&"
    "redirect_uri=http%3A%2F%2Fvimedra.replit.app%2Fapp.html&"
    "state=example-state-value-should-fail&"
    "code_challenge_method=S256&"
    "code_challenge=PHHQCoInTVWPbe78fWbQSftF5f6nn7hgskfLfEm4L6s&"
    "aud=https%3A%2F%2Ffhir.epic.com%2Finterconnect-fhir-oauth%2Fapi%2FFHIR%2FR4"
)



response = req.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    patient_data = response.json()
    print(patient_data)
else:
    print(f"Failed to retrieve patient data: {response.status_code}")
