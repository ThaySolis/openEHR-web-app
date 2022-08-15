from flask import Blueprint, render_template

from business_layer import ehr_controller

blueprint = Blueprint("EHR Routes", __name__)

@blueprint.route("/ehrs", methods=['GET'])
def ehr_list():
    """
    Exibe uma página com a lista de EHRs do sistema.
    """

    # gera os parâmetros para enviar ao template.
    template_parameters = ehr_controller.ehr_list()

    # gera a resposta HTTP baseada no template.
    return render_template('ehr_list.html', **template_parameters)

@blueprint.route("/ehrs/<ehr_id>", methods=['GET'])
def ehr_data(ehr_id):
    """
    Exibe uma página com os dados de um EHR específico.
    """

    # gera os parâmetros para enviar ao template.
    template_parameters = ehr_controller.ehr_data(ehr_id)

    # gera a resposta HTTP baseada no template.
    return render_template('ehr_data.html', **template_parameters)

@blueprint.route("/ehrs/<ehr_id>/ehr_status/history", methods=['GET'])
def ehr_versions(ehr_id):
    """
    Exibe uma página com a listagem de versões do EHR_STATUS de um EHR
    """

    # gera os parâmetros para enviar ao template.
    template_parameters = ehr_controller.ehr_versions(ehr_id)

    # gera a resposta HTTP baseada no template.
    return render_template("ehr_status_versions.html", **template_parameters)

@blueprint.route("/ehrs/<ehr_id>/compositions", methods=['GET'])
def compositions_by_ehr(ehr_id):
    """
    Exibe uma página com as compositions de um EHR específico.
    """
 
    # gera os parâmetros para enviar ao template.
    template_parameters = ehr_controller.compositions_by_ehr(ehr_id)

    # gera a resposta HTTP baseada no template.
    return render_template('composition_list.html', **template_parameters)

@blueprint.route("/ehrs/<ehr_id>/compositions/<composition_id>/history", methods=['GET'])
def composition_versions(ehr_id, composition_id):
    """
    Exibe uma página com a listagem de versões de uma COMPOSITION específica de um EHR
    """

    # gera os parâmetros para enviar ao template.
    template_parameters = ehr_controller.composition_versions(ehr_id, composition_id)

    # gera a resposta HTTP baseada no template.
    return render_template('composition_versions.html', **template_parameters)

@blueprint.route("/templates", methods=['GET'])
def template_list():
    """
    Exibe uma página com a lista de templates do sistema.
    """
 
    # gera os parâmetros para enviar ao template.
    template_parameters = ehr_controller.template_list()

    # gera a resposta HTTP baseada no template.
    return render_template('template_list.html', **template_parameters)
