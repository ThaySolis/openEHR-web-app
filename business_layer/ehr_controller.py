import dateutil.parser

from data_layer import openehr_api, ids, rm_utils

def ehr_list():
    ehr_ids = openehr_api.get_all_ehr_ids()

    return {
        "ehr_ids": ehr_ids
    }

def ehr_data(ehr_id):
    ehr_metadata = openehr_api.get_ehr_metadata(ehr_id)

    time_created = dateutil.parser.isoparse(ehr_metadata[0]).strftime("%d/%m/%Y - %H:%M:%S %Z")

    uid = ehr_metadata[1]
    if ehr_metadata[2]==True:
        is_queryable ="Sim"
    else:
        is_queryable ="Não"
    if ehr_metadata[3]==True:
        is_modifiable ="Sim"
    else:
        is_modifiable="Não"
    archetype_node_id = ehr_metadata[4]

    return {
        "time_created": str(time_created),
        "uid": str(uid),
        "is_queryable": str(is_queryable),
        "is_modifiable": str(is_modifiable),
        "archetype_node_id": str(archetype_node_id),
        "ehr_id": ehr_id
    }

def ehr_versions(ehr_id):
    ehr_status_version_ids = openehr_api.get_version_ids_of_ehr_status(ehr_id)

    ehr_status_history = []
    for version_id in ehr_status_version_ids:
        version = openehr_api.get_versioned_ehr_status_version_by_id(ehr_id, version_id)
        contribution_id = rm_utils.extract_contribution_id_from_version(version)
        ehr_status_history.append({
            "version_id": version_id,
            "contribution_id": contribution_id
        })

    return {
        "ehr_id": ehr_id, 
        "ehr_status_history": ehr_status_history
    }

def compositions_by_ehr(ehr_id):
    composition_ids_and_names = openehr_api.get_all_composition_ids_and_names_of_ehr(ehr_id)
    
    compositions = []
    for composition_id_and_name in composition_ids_and_names:
        version_id = composition_id_and_name[0]
        composition_id = ids.extract_versioned_object_id_from_version_id(version_id)
        name = composition_id_and_name[1]
        compositions.append({
            "version_id": version_id,
            "composition_id": composition_id,
            "name": name
        })

    return {
        "ehr_id": ehr_id,
        "compositions": compositions
    }

def composition_versions(ehr_id, composition_id):
    composition_version_ids = openehr_api.get_version_ids_of_composition(ehr_id, composition_id)

    composition_history = []
    for version_id in composition_version_ids:
        version = openehr_api.get_versioned_composition_version_by_id(ehr_id, composition_id, version_id)
        contribution_id = rm_utils.extract_contribution_id_from_version(version)
        composition_history.append({
            "version_id": version_id,
            "contribution_id": contribution_id
        })

    return {
        "ehr_id": ehr_id,
        "composition_id": composition_id,
        "composition_history": composition_history
    }

def template_list():
    templates = openehr_api.get_templates_ids_and_names()

    return {
        "templates": templates
    }
