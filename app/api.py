from fastapi import FastAPI, Request
from pje import Pje_Selenium

import logging
app = FastAPI()


@app.post("/selenium")
async def create_process(request: Request):
    try:
        form = await request.json()
        content = get_content(content=form, required_fields=["cookies", "instancia","idTarefa", 
                                                             "polo_ativo", "polo_passivo",])
        idTarefa =  content['idTarefa']

        with Pje_Selenium() as client:
            client.switch_to_screen("Parts")
            client.navigate_to_part_screen(content=content)
            client.navigate_to_protocol_screen()

    except Exception as error:
        logging.critical(f"ID={idTarefa}: {error}", exc_info=True)

#   Utils
###################################################################


def get_content(content, required_fields):
    validate_content(content, required_fields)
    return content

def validate_content(content, required_fields):
    for field in required_fields:
        if field not in content:
            raise ValueError("Requisição inválida.")



def error(msg="Erro desconhecido ao processar requisição."):
    return {
        "sucesso": False,
        "msg": msg
    }


def invalid_request():
    return error(msg="Requisição inválida.")


def ok():
    return {
        "sucesso": True
    }
