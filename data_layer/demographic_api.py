from requests import Session
from requests.auth import HTTPBasicAuth

from app_settings import DEMOGRAPHIC_API_BASE_URI, DEMOGRAPHIC_API_AUTH_USERNAME, DEMOGRAPHIC_API_AUTH_PASSWORD, VALIDATE_DEMOGRAPHIC_API_CERTIFICATE, USE_CUSTOM_DEMOGRAPHIC_API_CA_CERTIFICATE
from data_layer import path_utils, api_exceptions
from data_layer.ssl_extension import HostNameIgnoringAdapter

base_uri = DEMOGRAPHIC_API_BASE_URI
validate_certificate = VALIDATE_DEMOGRAPHIC_API_CERTIFICATE
use_custom_certificate = USE_CUSTOM_DEMOGRAPHIC_API_CA_CERTIFICATE
api_auth = HTTPBasicAuth(username=DEMOGRAPHIC_API_AUTH_USERNAME, password=DEMOGRAPHIC_API_AUTH_PASSWORD)

session = Session()

extra_params = {}
if base_uri.startswith("https"):
    if validate_certificate:
        if use_custom_certificate:
            session.mount("https://", HostNameIgnoringAdapter())
            certificate_path = path_utils.relative_path("other_certificates", "demographic_api_ca_certificate.pem")
            extra_params["verify"] = certificate_path
    else:
        extra_params["verify"] = False

def get_patient_by_version_id(version_id):
    """
    Retrieves particular version of the patient identified by `version_id`

    Returns:
        The patient data
    """
    # Sends the request to the openEHR server
    try:
        response = session.get(
            url = f"{base_uri}/v1/patient/{version_id}",
            auth = api_auth,
            headers = {
                "Accept": "application/json"
            },
            **extra_params
        )
    except ConnectionError as e:
        raise e

    if response.status_code == 200:
        patient = response.json()
        return patient
    elif response.status_code == 204:
        raise api_exceptions.NoContentException(f"The patient is deleted (logically).")
    elif response.status_code == 404:
        raise api_exceptions.NotFoundException(f"A patient with {version_id} does not exist")
    else:
        raise api_exceptions.UnknownException(f"An unknown error has occured. The status code is {response.status_code}")

def get_patient_at_time(patient_id, version_at_time):
    """
    Retrieves a version of the patient identified by `patient_id`. If `version_at_time` is supplied,
    retrieves the version extant at specified time, otherwise retrieves the latest patient version.

    Returns:
        The patient data
    """
    # Sends the request to the openEHR server
    try:
        response = session.get(
            url = f"{base_uri}/v1/patient/{patient_id}",
            auth = api_auth,
            headers = {
                "Accept": "application/json"
            },
            params = {
                "version_at_time": version_at_time
            },
            **extra_params
        )
    except ConnectionError as e:
        raise e

    if response.status_code == 200:
        patient = response.json()
        return patient
    elif response.status_code == 204:
        raise api_exceptions.NoContentException(f"The patient {patient_id} is deleted (logically) at time {version_at_time}.")
    elif response.status_code == 404:
        raise api_exceptions.NotFoundException(f"A patient with {patient_id} does not exist or a patient does not exists at {version_at_time} time.")
    else:
        raise api_exceptions.UnknownException(f"An unknown error has occured. The status code is {response.status_code}")

def get_versioned_patient(patient_id):
    """
    Retrieves a `VERSIONED_PARTY` identified by `patient_id`

    Returns:
        The versioned patient metadata
    """
    # Sends the request to the openEHR server
    try:
        response = session.get(
            url = f"{base_uri}/v1/versioned_patient/{patient_id}",
            auth = api_auth,
            headers = {
                "Accept": "application/json"
            },
            **extra_params
        )
    except ConnectionError as e:
        raise e

    if response.status_code == 200:
        versioned_patient = response.json()
        return versioned_patient
    elif response.status_code == 404:
        raise api_exceptions.NotFoundException(f"A patient with {patient_id} does not exist.")
    else:
        raise api_exceptions.UnknownException(f"An unknown error has occured. The status code is {response.status_code}")

def get_versioned_patient_revision_history(patient_id):
    """
    Retrieves the revision history of the `VERSIONED_PARTY` identified by `patient_id`.

    Returns:
        The revision history
    """
    # Sends the request to the openEHR server
    try:
        response = session.get(
            url = f"{base_uri}/v1/versioned_patient/{patient_id}/revision_history",
            auth = api_auth,
            headers = {
                "Accept": "application/json"
            },
            **extra_params
        )
    except ConnectionError as e:
        raise e

    if response.status_code == 200:
        revision_history = response.json()

        # fallback for REVISION_HISTORY which is a plain list.
        if isinstance(revision_history, list):
            revision_history = { "items": revision_history }

        return revision_history
    elif response.status_code == 404:
        raise api_exceptions.NotFoundException(f"A patient with {patient_id} does not exist.")
    else:
        raise api_exceptions.UnknownException(f"An unknown error has occured. The status code is {response.status_code}")

def get_versioned_patient_version_by_id(patient_id, version_id):
    """
    Retrieves a `VERSION` identified by `version_id` of a `VERSIONED_PARTY` identified by `patient_id`.

    Returns:
        The patient version metadata
    """
    # Sends the request to the openEHR server
    try:
        response = session.get(
            url = f"{base_uri}/v1/versioned_patient/{patient_id}/version/{version_id}",
            auth = api_auth,
            headers = {
                "Accept": "application/json"
            },
            **extra_params
        )
    except ConnectionError as e:
        raise e

    if response.status_code == 200:
        version_of_patient = response.json()
        return version_of_patient
    elif response.status_code == 404:
        raise api_exceptions.NotFoundException(f"A patient with {patient_id} does not exist or a `VERSION` with {version_id} does not exist.")
    else:
        raise api_exceptions.UnknownException(f"An unknown error has occured. The status code is {response.status_code}")

def get_versioned_patient_version_at_time(patient_id, version_at_time):
    """
    Retrieves a `VERSION` from the `VERSIONED_PARTY` identified by `patient_id`.
    If `version_at_time` is supplied, retrieves the `VERSION` extant at specified time,
    otherwise retrieves the latest `VERSION`.

    Returns:
        The patient version metadata
    """
    # Sends the request to the openEHR server
    try:
        response = session.get(
            url = f"{base_uri}/v1/versioned_patient/{patient_id}/version",
            auth = api_auth,
            headers = {
                "Accept": "application/json"
            },
            params = {
                "version_at_time": version_at_time
            },
            **extra_params
        )
    except ConnectionError as e:
        raise e

    if response.status_code == 200:
        version_of_patient = response.json()
        return version_of_patient
    elif response.status_code == 404:
        raise api_exceptions.NotFoundException(f"A patient with {patient_id} does not exist or a patient does not exists at {version_at_time} time.")
    else:
        raise api_exceptions.UnknownException(f"An unknown error has occured. The status code is {response.status_code}")

def list_patients():
    """
    Lists the IDs of all the patients in the system.

    Returns:
        The patients' IDs
    """
    # Sends the request to the openEHR server
    try:
        response = session.get(
            url = f"{base_uri}/v1/patient",
            auth = api_auth,
            headers = {
                "Accept": "application/json"
            },
            **extra_params
        )
    except ConnectionError as e:
        raise e

    if response.status_code == 200:
        patient_object_ids = response.json()
        patient_ids = [ object_id["value"] for object_id in patient_object_ids["uids"] ]
        return patient_ids
    else:
        raise api_exceptions.UnknownException(f"An unknown error has occured. The status code is {response.status_code}")

def get_ehr_id_from_patient(patient_id):
    """
    Retrieves the EHR identifier associated with a given patient.

    Returns:
        The ID of the EHR.
    """
    # Sends the request to the openEHR server
    try:
        response = session.get(
            url = f"{base_uri}/v1/versioned_patient/{patient_id}/ehr",
            auth = api_auth,
            headers = {
                "Accept": "application/json"
            },
            **extra_params
        )
    except ConnectionError as e:
        raise e

    if response.status_code == 200:
        ehr_of_patient = response.json()
        # the response has the following format:
        # {
        #   "ehr_id": <EHR ID>
        # }

        return ehr_of_patient.get("ehr_id", None)
    elif response.status_code == 404:
        raise api_exceptions.NotFoundException(f"A patient with {patient_id} does not exist or was already deleted (logically).")
    else:
        raise api_exceptions.UnknownException(f"An unknown error has occured. The status code is {response.status_code}")

def get_contribution(patient_id, contribution_id):
    """
    Retrieves a contribution of a given patient

    Returns:
        The contribution
    """
    # Sends the request to the openEHR server
    try:
        response = session.get(
            url = f"{base_uri}/v1/versioned_patient/{patient_id}/contribution/{contribution_id}",
            auth = api_auth,
            headers = {
                "Accept": "application/json"
            },
            **extra_params
        )
    except ConnectionError as e:
        raise e

    if response.status_code == 200:
        contribution = response.json()
        return contribution
    elif response.status_code == 404:
        raise api_exceptions.NotFoundException(f"A patient with {patient_id} does not exist or the contribution {contribution_id} does not exist.")
    else:
        raise api_exceptions.UnknownException(f"An unknown error has occured. The status code is {response.status_code}")

def get_version_ids_of_patient(patient_id):
    """
    Lists the version IDS of a given patient.

    Parameters:
        patient_id - the ID of the patient.

    Returns:
        An array where each element is a version ID.
    """

    revision_history = get_versioned_patient_revision_history(patient_id)
    # the response is a REVISION_HISTORY and has the following format:
    # {
    #     "items": [
    #     {
    #       "version_id": {
    #         "value": <ID of version #1>
    #       },
    #       ...
    #     },
    #     {
    #       "version_id": {
    #         "value": <ID of version #2>
    #       },
    #       ...
    #     },
    #     {
    #       "version_id": {
    #         "value": <ID of version #3>
    #       },
    #       ...
    #     },
    #     ...
    #   ]
    # }
    # documentation: https://specifications.openehr.org/releases/RM/latest/common.html#_revision_history_class

    # the next code converts it to the following format:
    # [
    #   <ID of version #1>,
    #   <ID of version #2>,
    #   <ID of version #3>,
    #   ...
    # ]
    patient_versions = []
    for revision_history_item in revision_history["items"]:
        patient_versions.append(revision_history_item["version_id"]["value"])

    return patient_versions
