from flask import Blueprint, make_response, render_template

from business_layer import prov_controller

blueprint = Blueprint("PROV Routes", __name__)

@blueprint.route("/ehrs/<ehr_id>/ehr_status/prov", methods=['GET'])
def ehr_prov(ehr_id):
    """
    Exibe uma página com o diagrama de proveniência de um EHR_STATUS.
    """

    # gera os parâmetros para enviar ao template.
    template_parameters = prov_controller.ehr_status_prov(ehr_id)

    # gera a resposta HTTP baseada no template.
    return render_template('ehr_status_prov.html', **template_parameters)

@blueprint.route("/ehrs/<ehr_id>/ehr_status/prov_diagram.png", methods=['GET'])
def show_ehr_prov(ehr_id):
    """
    Exibe uma imagem gerada a partir do documento PROV de um EHR.
    """

    # gera o diagrama PROV em formato PNG.
    prov_diagram_png = prov_controller.plot_prov_document_of_ehr_status(ehr_id, "png")

    # gera a resposta HTTP com a imagem PNG.
    response = make_response(prov_diagram_png)
    response.headers.set('Content-Type', 'image/png')
    return response

@blueprint.route("/ehrs/<ehr_id>/compositions/<composition_id>/prov", methods=['GET'])
def composition_prov(ehr_id, composition_id):
    """
    Exibe uma página com o diagrama de proveniência de um COMPOSITIN.
    """

    # gera os parâmetros para enviar ao template.
    template_parameters = prov_controller.composition_prov(ehr_id, composition_id)

    # gera a resposta HTTP baseada no template.
    return render_template('composition_prov.html', **template_parameters)

@blueprint.route("/ehrs/<ehr_id>/compositions/<composition_id>/prov_diagram.png", methods=['GET'])
def show_ehr_composition_prov(ehr_id, composition_id):
    """
    Exibe uma imagem gerada a partir do documento PROV de uma COMPOSITION de um EHR.
    """

    # gera o diagrama PROV em formato PNG.
    prov_diagram_png = prov_controller.plot_prov_document_of_composition(ehr_id, composition_id, "png")

    # gera a resposta HTTP com a imagem PNG.
    response = make_response(prov_diagram_png)
    response.headers.set('Content-Type', 'image/png')
    return response

@blueprint.route("/patients/<patient_id>/prov", methods=['GET'])
def patient_prov(patient_id):
    """
    Exibe uma página com o diagrama de proveniência de um paciente.
    """

    # gera os parâmetros para enviar ao template.
    template_parameters = prov_controller.patient_prov(patient_id)

    # gera a resposta HTTP baseada no template.
    return render_template('patient_prov.html', **template_parameters)

@blueprint.route("/patients/<patient_id>/prov_diagram.png", methods=['GET'])
def show_ehr_patient_prov(patient_id):
    """
    Exibe uma imagem gerada a partir do documento PROV de um paciente.
    """

    # gera o diagrama PROV em formato PNG.
    prov_diagram_png = prov_controller.plot_prov_document_of_patient(patient_id, "png")

    # gera a resposta HTTP com a imagem PNG.
    response = make_response(prov_diagram_png)
    response.headers.set('Content-Type', 'image/png')
    return response
