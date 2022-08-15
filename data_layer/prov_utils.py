import tempfile
import os

def plot_prov_document(doc, format):
    """
    Plota (gera uma imagem a partir de) um documento PROV.

    O parâmetro "format" é o formato da imagem. Os valores "svg" e "png" são suportados.
    """

    # cria um arquivo temporário.
    with tempfile.NamedTemporaryFile(suffix='.' + format) as temp:
        file_name = temp.name

    # plota a imagem no arquivo, lê o arquivo e apaga.
    try:
        doc.plot(filename=file_name)
        with open(file_name, mode="r+b") as opened_file:
            bytes = opened_file.read()
    finally:
        os.remove(file_name)
    
    # retorna os bytes com a imagem.
    return bytes
