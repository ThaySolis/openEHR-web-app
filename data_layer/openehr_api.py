from requests import Session
from requests.auth import HTTPBasicAuth

from app_settings import OPENEHR_API_BASE_URI, OPENEHR_API_AUTH_USERNAME, OPENEHR_API_AUTH_PASSWORD, VALIDATE_OPENEHR_API_CERTIFICATE, USE_CUSTOM_OPENEHR_API_CA_CERTIFICATE
from data_layer import path_utils, api_exceptions
from data_layer.ssl_extension import HostNameIgnoringAdapter

base_uri = OPENEHR_API_BASE_URI
validate_certificate = VALIDATE_OPENEHR_API_CERTIFICATE
use_custom_certificate = USE_CUSTOM_OPENEHR_API_CA_CERTIFICATE
api_auth = HTTPBasicAuth(username=OPENEHR_API_AUTH_USERNAME, password=OPENEHR_API_AUTH_PASSWORD)

session = Session()

extra_params = {}
if base_uri.startswith("https"):
    if validate_certificate:
        if use_custom_certificate:
            session.mount("https://", HostNameIgnoringAdapter())
            certificate_path = path_utils.relative_path("other_certificates", "openehr_api_ca_certificate.pem")
            extra_params["verify"] = certificate_path
    else:
        extra_params["verify"] = False

def get_all_ehr_ids():
    """
    Get the IDs of all EHRs.

    Returns:
        An array where each element is the ID of an EHR.
    """

    # source: https://specifications.openehr.org/releases/ITS-REST/latest/query.html#query-execute-query-get

    # creates an AQL query to retrieve the IDs of the EHRs.
    aql_query = "SELECT e/ehr_id/value AS ehr_id FROM EHR e"

    # sends the request to the openEHR API server.
    # operation name: "Execute ad-hoc (non-stored) AQL query".
    # documentation: https://specifications.openehr.org/releases/ITS-REST/latest/query.html#query-execute-query-get
    try:
        response = session.get(
            url = f"{base_uri}/v1/query/aql",
            auth = api_auth,
            params = {
                "q": aql_query
            },
            headers = {
                "Accept": "application/json"
            },
            **extra_params
        )
    except ConnectionError as e:
        raise e

    if response.status_code == 200:
        aql_query_response = response.json()
        # the response is a RESULT_SET and has the following format:
        # {
        #   "rows": [
        #     [ <ehr_id #1> ],
        #     [ <ehr_id #2> ],
        #     [ <ehr_id #3> ],
        #     ...
        #   ]
        # }
        # documentation: https://specifications.openehr.org/releases/SM/latest/openehr_platform.html#_result_set_class

        # the next code converts it to the following format:
        # [
        #   <ehr_id #1>,
        #   <ehr_id #2>,
        #   <ehr_id #3>,
        #   ...
        # ]
        ehr_ids = []
        for row in aql_query_response["rows"]:
            ehr_id = row[0]
            ehr_ids.append(ehr_id)

        return ehr_ids
    elif response.status_code == 204:
        return []
    elif response.status_code == 400:
        raise api_exceptions.BadRequestException("The server was unable to execute the query due to invalid input.")
    elif response.status_code == 408:
        raise api_exceptions.RequestTimeoutException("Maximum query execution time reached, therefore the server aborted the execution of the query.")
    else:
        raise api_exceptions.UnknownException(f"An unknown error has occured. The status code is {response.status_code}")

def get_all_composition_ids_and_names_of_ehr(ehr_id):
    """
    Gets IDs and names of all COMPOSITIONs of a given EHR.

    Parameters:
    ehr_id - the ID of the EHR.

    Returns:
        An array where each element is a pair of ID and name of the COMPOSITION.
    """

    # source: https://specifications.openehr.org/releases/ITS-REST/latest/query.html#query-execute-query-get

    # creates an AQL query to retrieve the IDs and names of the compositions.
    aql_query = f"SELECT c/uid/value AS version_id, c/name/value AS name FROM EHR e CONTAINS COMPOSITION c WHERE e/ehr_id/value = '{ehr_id}'"

    # sends the request to the openEHR API server.
    # operation name: "Execute ad-hoc (non-stored) AQL query".
    # documentation: https://specifications.openehr.org/releases/ITS-REST/latest/query.html#query-execute-query-get
    try:
        response = session.get(
            url = f"{base_uri}/v1/query/aql",
            auth = api_auth,
            params = {
                "q": aql_query
            },
            headers = {
                "Accept": "application/json"
            },
            **extra_params
        )
    except ConnectionError as e:
        raise e

    if response.status_code == 200:
        aql_query_response = response.json()
        # the response is a RESULT_SET and has the following format:
        # {
        #   "rows": [
        #     [ <composition_version_id #1>, <composition_name #1> ],
        #     [ <composition_version_id #2>, <composition_name #2> ],
        #     [ <composition_version_id #3>, <composition_name #3> ],
        #     ...
        #   ]
        # }
        # documentation: https://specifications.openehr.org/releases/SM/latest/openehr_platform.html#_result_set_class

        # the next code converts it to the following format:
        # [
        #   [ <composition_version_id #1>, <composition_name #1> ],
        #   [ <composition_version_id #2>, <composition_name #2> ],
        #   [ <composition_version_id #3>, <composition_name #3> ],
        #   ...
        # ]
        composition_ids_and_names = []
        for row in aql_query_response["rows"]:
            composition_version_id = row[0]
            composition_name = row[1]
            composition_ids_and_names.append([composition_version_id, composition_name])
        return composition_ids_and_names
    elif response.status_code == 204:
        return []
    elif response.status_code == 400:
        raise api_exceptions.BadRequestException("The server was unable to execute the query due to invalid input.")
    elif response.status_code == 408:
        raise api_exceptions.RequestTimeoutException("Maximum query execution time reached, therefore the server aborted the execution of the query.")
    else:
        raise api_exceptions.UnknownException(f"An unknown error has occured. The status code is {response.status_code}")

def get_ehr_metadata(ehr_id):
    """
    Gets the creation date and time of an EHR, the ID of its most recent version and the parameters "is queryable", "is modifiable" and "archetype_node_id".

    Parameters:
        ehr_id - the ID of the EHR.

    Returns:
        An array with the following elements:
        - date/time of creation
        - ID of the most recent version of the EHR_STATUS
        - is queryable
        - is modifiable
        - archetype_node_id
    """

    # sends the request to the openEHR API server.
    # operation name: "Get EHR summary by id".
    # documentation: https://specifications.openehr.org/releases/ITS-REST/latest/ehr.html#ehr-ehr-get
    try:
        response = session.get(
            url = f"{base_uri}/v1/ehr/{ehr_id}",
            auth = api_auth,
            headers = {
                "Accept": "application/json"
            },
            **extra_params
        )
    except ConnectionError as e:
        raise e

    if response.status_code == 200:
        ehr_summary = response.json()
        # the response is an EHR and has the following format:
        # {
        #   "time_created": {
        #     "value": <date/time of creation>
        #   },
        #   "ehr_status": {
        #     "uid": {
        #       "value": <ID of the latest version of the EHR_STATUS>
        #     },
        #     "is_modifiable": <is the EHR modifiable?>,
        #     "is_queriable": <is the EHR queriable?>,
        #     "archetype_node_id": <name of the EHR_STATUS archetype>,
        #     ...
        #   },
        #   ...
        # }
        # documentation: https://specifications.openehr.org/releases/RM/latest/ehr.html#_ehr_class

        # the next code converts it to the following format:
        # [
        #   <date/time of creation>,
        #   <ID of the latest version of the EHR_STATUS>,
        #   <is the EHR modifiable?>,
        #   <is the EHR queriable?>,
        #   <name of the EHR_STATUS archetype>
        # ]
        time_created = ehr_summary["time_created"]["value"]
        ehr_status_version_id = ehr_summary["ehr_status"]["uid"]["value"]
        is_ehr_status_modifiable = ehr_summary["ehr_status"]["is_modifiable"]
        is_ehr_status_queryable = ehr_summary["ehr_status"]["is_queryable"]
        ehr_status_archetype_node_id = ehr_summary["ehr_status"]["archetype_node_id"]

        ehr_metadata = []
        ehr_metadata.append(time_created)
        ehr_metadata.append(ehr_status_version_id)
        ehr_metadata.append(is_ehr_status_modifiable)
        ehr_metadata.append(is_ehr_status_queryable)
        ehr_metadata.append(ehr_status_archetype_node_id)

        return ehr_metadata
    elif response.status_code == 404:
        raise api_exceptions.NotFoundException(f"An EHR with {ehr_id} does not exist.")
    else:
        raise api_exceptions.UnknownException(f"An unknown error has occured. The status code is {response.status_code}")

def get_version_ids_of_ehr_status(ehr_id):
    """
    Lists the version IDS of the EHR_STATUS of a given EHR.

    Parameters:
        ehr_id - the ID of the EHR.

    Returns:
        An array where each element is a version ID.
    """

    # sends the request to the openEHR API server.
    # operation name: "Get versioned EHR_STATUS revision history".
    # documentation: https://specifications.openehr.org/releases/ITS-REST/latest/ehr.html#ehr_status-versioned_ehr_status-get-1
    try:
        response = session.get(
            url = f"{base_uri}/v1/ehr/{ehr_id}/versioned_ehr_status/revision_history",
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

        # fallback for REVISION_HISTORY which is a plain list.
        if isinstance(revision_history, list):
            revision_history = { "items": revision_history }

        # the next code converts it to the following format:
        # [
        #   <ID of version #1>,
        #   <ID of version #2>,
        #   <ID of version #3>,
        #   ...
        # ]
        ehr_status_versions = []
        for revision_history_item in revision_history["items"]:
            ehr_status_versions.append(revision_history_item["version_id"]["value"])

        return ehr_status_versions
    elif response.status_code == 404:
        raise api_exceptions.NotFoundException(f"An EHR with {ehr_id} does not exist.")
    else:
        raise api_exceptions.UnknownException(f"An unknown error has occured. The status code is {response.status_code}")

def get_version_ids_of_composition(ehr_id, composition_id):
    """
    Lists the version IDS of a given COMPOSITION of a given EHR.

    Parameters:
        ehr_id - the ID of the EHR which owns the COMPOSITION.
        composition_id - the ID of the composition.

    Returns:
        An array where each element is a version ID.
    """

    # sends the request to the openEHR API server.
    # operation name: "Get versioned composition revision history".
    # documentation: https://specifications.openehr.org/releases/ITS-REST/latest/ehr.html#composition-versioned_composition-get-1
    try:
        response = session.get(
            url = f"{base_uri}/v1/ehr/{ehr_id}/versioned_composition/{composition_id}/revision_history",
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

        # fallback for REVISION_HISTORY which is a plain list.
        if isinstance(revision_history, list):
            revision_history = { "items": revision_history }

        # the next code converts it to the following format:
        # [
        #   <ID of version #1>,
        #   <ID of version #2>,
        #   <ID of version #3>,
        #   ...
        # ]
        composition_versions = []
        for revision_history_item in revision_history["items"]:
            composition_versions.append(revision_history_item["version_id"]["value"])

        return composition_versions
    elif response.status_code == 404:
        raise api_exceptions.NotFoundException(f"An EHR with {ehr_id} does not exist or a VERSIONED_COMPOSITION with {composition_id} does not exist.")
    else:
        raise api_exceptions.UnknownException(f"An unknown error has occured. The status code is {response.status_code}")

def get_versioned_ehr_status_version_by_id(ehr_id, version_id):
    """
    Retrieves a `VERSION` identified by `version_id` of a `VERSIONED_EHR_STATUS` of the `EHR` identified by `ehr_id`.

    Parameters:
        ehr_id - the ID of the EHR.
        version_id - the ID of the VERSIONED_EHR_STATUS version.

    Returns:
        The `VERSION<EHR_STATUS>`.
    """

    # sends the request to the openEHR API server.
    # operation name: "Get versioned EHR_STATUS version by id".
    # documentation: https://specifications.openehr.org/releases/ITS-REST/latest/ehr.html#ehr_status-versioned_ehr_status-get-3
    try:
        response = session.get(
            url = f"{base_uri}/v1/ehr/{ehr_id}/versioned_ehr_status/version/{version_id}",
            auth = api_auth,
            headers = {
                "Accept": "application/json"
            },
            **extra_params
        )
    except ConnectionError as e:
        raise e

    if response.status_code == 200:
        version_of_ehr_status = response.json()
        return version_of_ehr_status
    elif response.status_code == 404:
        raise api_exceptions.NotFoundException(f"An EHR with {ehr_id} does not exist or a VERSION with {version_id} does not exist.")
    else:
        raise api_exceptions.UnknownException(f"An unknown error has occured. The status code is {response.status_code}")

def get_versioned_composition_version_by_id(ehr_id, composition_id, version_id):
    """
    Retrieves a `VERSION` identified by `version_id` of a `VERSIONED_COMPOSITION` identifier by `composition_id` or the `EHR` identified by `ehr_id`.

    Parameters:
        ehr_id - the ID of the EHR which owns the COMPOSITION.
        composition_id - the ID of the composition.
        version_id - the ID of the VERSIONED_COMPOSITION version.

    Returns:
        The `VERSION<COMPOSITION>`.
    """

    # sends the request to the openEHR API server.
    # operation name: "Get versioned composition version by id".
    # documentation: https://specifications.openehr.org/releases/ITS-REST/latest/ehr.html#composition-versioned_composition-get-2
    try:
        response = session.get(
            url = f"{base_uri}/v1/ehr/{ehr_id}/versioned_composition/{composition_id}/version/{version_id}",
            auth = api_auth,
            headers = {
                "Accept": "application/json"
            },
            **extra_params
        )
    except ConnectionError as e:
        raise e

    if response.status_code == 200:
        version_of_composition = response.json()
        return version_of_composition
    elif response.status_code == 404:
        raise api_exceptions.NotFoundException(f"An EHR with {ehr_id} does not exist or a VERSIONED_COMPOSITION with {composition_id} does not exist or a VERSION with {version_id} does not exist.")
    else:
        raise api_exceptions.UnknownException(f"An unknown error has occured. The status code is {response.status_code}")

def get_templates_ids_and_names():
    """
    Lists the IDs and names of all available templates.

    Returns:
        An array where each element is a pair of ID and name (concept) of the template.
    """

    # sends the request to the openEHR API server.
    # operation name: "List ADL 1.4 templates".
    # documentation: https://specifications.openehr.org/releases/ITS-REST/latest/definitions.html#definitions-adl-1.4-template-get
    try:
        response = session.get(
            url = f"{base_uri}/v1/definition/template/adl1.4",
            auth = api_auth,
            headers = {
                "Accept": "application/json"
            },
            **extra_params
        )
    except ConnectionError as e:
        raise e

    if response.status_code == 200:
        templates_adl14 = response.json()
        # the response has the following format:
        # [
        #   {
        #     "template_id": <template ID>,
        #     "concept": <template name (concept)>,
        #     "archetype_id": <archetype ID>,
        #     "created_timestamp": <date/time of creation>
        #   },
        #   ...
        # ]

        # the next code converts it to the following format:
        # [
        #   [ <template name (concept)>, <template ID>, <archetype ID> ],
        #   ...
        # ]
        templates = []
        for template_data in templates_adl14:
            concept = template_data["concept"]
            template_id = template_data["template_id"]
            archetype_id = template_data["archetype_id"]
            templates.append([concept, template_id, archetype_id])

        return templates
    else:
        raise api_exceptions.UnknownException(f"An unknown error has occured. The status code is {response.status_code}")
