# Dictionary with the description of the site screens,
# each screen has an indication of screen iframe, available actions and elements for interaction
SITE_SCHEME = {
    "Login": {
        "elements": {
            "usernameInput": "//input[@data-testtoolid='idusuario']",
            "passwordInput": "//input[@data-testtoolid='senha']",
            "enterButton": "//button[@data-testtoolid='onclickenviar']"
        }
    },

    "Protocol": {
        "actions": ["get_pratical_exam_categories", "set_pratical_exam_category", "solve_captcha"],
        "elements": {
            "screenProtocol": "//*[@id=\"informativo_lbl\"]",
            "btnSigner": "//*[@id=\"formBotoesAcao:btnProtocolar\"]",
            "btncomprovante": "//*[@id=\"formBotoesAcao:btnSalvarComprovante\"]"
        }
    },

    "SignDocs": {
        "actions": ["get_pratical_exam_categories", "set_pratical_exam_category", "solve_captcha"],
        "elements": {
            "btncomprovante": "//*[@id=\"formBotoesAcao:btnSalvarComprovante\"]",
            "screenDocs": "//*[@id=\"novoAnexo_lbl\"]",
            "btnSigner": "//*[@id=\"btn-assinador\"]"
        }
    },
    "IncidentalProtocol": {
        "actions": ["get_pratical_exam_categories", "set_pratical_exam_category", "solve_captcha"],
        "elements": {
            "confirmPage": "//*[@id=\"divDocumentoPrincipal\"]",
            "checkBoxs": "//*[@id=\"expTb:tb\"]",
            "btnSigner": "//*[@id=\"btn-assinador\"]",
            "confirmSigner": "//*[@id=\"dvMsg\"]/dl/dt[1]/span"
        }
    }
}
