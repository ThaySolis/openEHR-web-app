from data_layer import openehr_api, prov_api, prov_utils

def ehr_status_prov(ehr_id):
    return {
        "ehr_id": ehr_id
    }

def plot_prov_document_of_ehr_status(ehr_id, format):
    prov_document = prov_api.create_prov_document_of_ehr_status(ehr_id)
    prov_diagram = prov_utils.plot_prov_document(prov_document, format)
    return prov_diagram

def composition_prov(ehr_id, composition_id):
    return {
        "ehr_id": ehr_id,
        "composition_id": composition_id
    }

def plot_prov_document_of_composition(ehr_id, composition_id, format):
    prov_document = prov_api.create_prov_document_of_composition(ehr_id, composition_id)
    prov_diagram = prov_utils.plot_prov_document(prov_document, format)
    return prov_diagram

def patient_prov(patient_id):
    return {
        "patient_id": patient_id
    }

def plot_prov_document_of_patient(patient_id, format):
    prov_document = prov_api.create_prov_document_of_patient(patient_id)
    prov_diagram = prov_utils.plot_prov_document(prov_document, format)
    return prov_diagram
