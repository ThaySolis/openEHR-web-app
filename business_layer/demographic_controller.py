from data_layer import demographic_api, rm_utils

def patient_list():
    patient_ids = demographic_api.list_patients()

    return {
        "patient_ids": patient_ids
    }

def patient_data(patient_id):
    versioned_patient = demographic_api.get_versioned_patient(patient_id)

    time_created = rm_utils.extract_time_created_from_versioned_object(versioned_patient)

    return {
        "patient_id": patient_id,
        "time_created": time_created.strftime("%d/%m/%Y - %H:%M:%S %Z"),
    }

def patient_versions(patient_id):
    version_ids = demographic_api.get_version_ids_of_patient(patient_id)

    patient_history = []
    for version_id in version_ids:
        version = demographic_api.get_versioned_patient_version_by_id(patient_id, version_id)
        contribution_id = rm_utils.extract_contribution_id_from_version(version)
        patient_history.append({
            "version_id": version_id,
            "contribution_id": contribution_id
        })

    return {
        "patient_id": patient_id, 
        "patient_history": patient_history
    }
