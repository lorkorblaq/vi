from fhirclient import client,server
from fhirclient.models.patient import Patient




# app = Flask(__name__)

settings = {
    'app_id': 'd81ed990-b75a-4fb8-94b5-a9df0e809631',
    'api_base': 'https://fhir.epic.com/interconnect-fhir-oauth/api/FHIR/R4'
}

smart = server.FHIRServer(None, 'https://fhir.epic.com/interconnect-fhir-oauth/api/FHIR/R4')
patient = Patient.read('eq081-VQEgP8drUUqCWzHfw', smart)
print(patient.name[0].given)