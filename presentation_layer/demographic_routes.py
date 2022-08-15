from flask import Blueprint, make_response, render_template

from business_layer import demographic_controller

blueprint = Blueprint("Demographic Routes", __name__)

@blueprint.route("/patients", methods=['GET'])
def patient_list():
    """
    Exibe uma página com a lista de pacientes do sistema.
    """

    # gera os parâmetros para enviar ao template.
    template_parameters = demographic_controller.patient_list()

    # gera a resposta HTTP baseada no template.
    return render_template('patient_list.html', **template_parameters)

@blueprint.route("/patients/<patient_id>", methods=['GET'])
def patient_data(patient_id):
    """
    Exibe uma página com os dados de um paciente específico.
    """

    # gera os parâmetros para enviar ao template.
    template_parameters = demographic_controller.patient_data(patient_id)

    # gera a resposta HTTP baseada no template.
    return render_template('patient_data.html', **template_parameters)

@blueprint.route("/patients/<patient_id>/history", methods=['GET'])
def patient_versions(patient_id):
    """
    Exibe uma página com a listagem de versões de um paciente
    """

    # gera os parâmetros para enviar ao template.
    template_parameters = demographic_controller.patient_versions(patient_id)

    # gera a resposta HTTP baseada no template.
    return render_template("patient_versions.html", **template_parameters)
