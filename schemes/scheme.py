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
    "Parts": {
        "elements": {
            "screenPart": "//*[@id=\"tabPartes_lbl\"]",
            "addPartA": "//*[@id=\"addParteA\"]",
            "addPartP": "//*[@id=\"addParteP\"]",
            "categorySelect": "//*[@id=\"divTipoPartePolo\"]/div[1]/div[2]/form/select",
            "typeCnpj": "//*[@id=\"preCadastroPessoaFisicaForm:tipoPessoaDecoration:tipoPessoa:1\"]",
            "inputDocument": "input[id*=\"preCadastroPessoaFisicaForm:preCadastroPessoaFisica_nr\"]",
            "searchButton": "//*[@id=\"preCadastroPessoaFisicaForm:pesquisarDocumentoPrincipal\"]",
            "confirmButton": "//*[@id=\"preCadastroPessoaFisicaForm:btnConfirmarCadastro\"]",
            "activeTable": "#gridPartesPoloAtivoList\\:tb > tr",
            "passiveTable": "#gridPartesPoloPassivoList\\:tb > tr",
            "waitWindowClose": "//div[@id='mpAssociarParteProcessoContainer' and contains(@style, 'none')]"
        }
    },
    
    "AddAddress": {
        "actions": ["get_pratical_exam_categories", "set_pratical_exam_category", "solve_captcha"],
        "elements": {
            "screenAddress": "//*[@id=\"formInserirParteProcesso:enderecoUsuario_lbl\"]",
            "inputCep": "input[id*=\"EnderecoCEP\"]",
            "searchResult": "setInterval(()=>document.querySelector(\"tr.rich-sb-int.richfaces_suggestionEntry.rich-sb-int-sel\").dispatchEvent(new Event(\"click\")), 1000)",
            "districtInsert": "input[id*=\"EndereconomeBairro\"]",
            "streetInsert": "input[id*=\"EndereconomeLogradouro\"]",
            "complementInsert": "input[id*=\"Enderecocomplemento\"]",
            "numberInsert": "input[id*=\"Endereconumero\"]",
            "saveButton": "input[id*=\"GravarEndereco\"]",
            "addPartButton": "input[id*=\"btnInserirParteProcesso\"]",
        }
    },

    "Protocol": {
        "actions": ["get_pratical_exam_categories", "set_pratical_exam_category", "solve_captcha"],
        "elements": {
            "screenProtocol": "//*[@id=\"informativo_lbl\"]",
            "btnSigner": "//*[@id=\"formBotoesAcao:btnProtocolar\"]"

        }
    },

    "SignDocs": {
        "actions": ["get_pratical_exam_categories", "set_pratical_exam_category", "solve_captcha"],
        "elements": {
            "screenDocs": "//*[@id=\"novoAnexo_lbl\"]",
            "btnSigner": "//*[@id=\"btn-assinador\"]"
        }
    },

}
