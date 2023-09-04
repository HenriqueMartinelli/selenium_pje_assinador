from fastapi import FastAPI, Request
from pje import Pje_Selenium

import logging
app = FastAPI()


@app.post("/assinador")
async def create_process(request: Request):
    try:
        content = await request.json()
        idTarefa =  content['idTarefa']

        with Pje_Selenium() as client:
            client.start(content)

        return client.outputEvent
    except Exception as e:
        logging.critical(f"idTarefa={idTarefa}: {e}", exc_info=True) 

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
