import io
from requests import Session
from requests.auth import HTTPBasicAuth
from prov.model import ProvDocument

from app_settings import PROV_API_BASE_URI, PROV_API_AUTH_USERNAME, PROV_API_AUTH_PASSWORD, VALIDATE_PROV_API_CERTIFICATE, USE_CUSTOM_PROV_API_CA_CERTIFICATE, OPENEHR_API_BASE_URI, DEMOGRAPHIC_API_BASE_URI
from data_layer import path_utils, api_exceptions
from data_layer.ssl_extension import HostNameIgnoringAdapter

base_uri = PROV_API_BASE_URI
validate_certificate = VALIDATE_PROV_API_CERTIFICATE
use_custom_certificate = USE_CUSTOM_PROV_API_CA_CERTIFICATE
api_auth = HTTPBasicAuth(username=PROV_API_AUTH_USERNAME, password=PROV_API_AUTH_PASSWORD)

session = Session()

extra_params = {}
if base_uri.startswith("https"):
    if validate_certificate:
        if use_custom_certificate:
            session.mount("https://", HostNameIgnoringAdapter())
            certificate_path = path_utils.relative_path("other_certificates", "prov_api_ca_certificate.pem")
            extra_params["verify"] = certificate_path
    else:
        extra_params["verify"] = False

def create_prov_document_of_resource(url : str) -> ProvDocument:
    try:
        response = session.get(
            url = f"{base_uri}/provenance/service",
            auth = api_auth,
            params = {
                "target": url
            },
            headers = {
                "Accept": "application/xml"
            },
            **extra_params
        )
    except ConnectionError as e:
        raise e

    if response.status_code == 200:
        document = ProvDocument.deserialize(io.BytesIO(response.content), format="xml")
        return document
    else:
        raise api_exceptions.UnknownException(f"An unknown error has occured. The status code is {response.status_code}")

def create_prov_document_of_ehr_status(ehr_id : str) -> ProvDocument:
    return create_prov_document_of_resource(f"{OPENEHR_API_BASE_URI}/v1/ehr/{ehr_id}/ehr_status")

def create_prov_document_of_composition(ehr_id, composition_id):
    return create_prov_document_of_resource(f"{OPENEHR_API_BASE_URI}/v1/ehr/{ehr_id}/composition/{composition_id}")

def create_prov_document_of_patient(patient_id):
    return create_prov_document_of_resource(f"{DEMOGRAPHIC_API_BASE_URI}/v1/patient/{patient_id}")
