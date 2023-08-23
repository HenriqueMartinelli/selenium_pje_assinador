import time
class Login():

    def login(self):
        script = '''requisicao = {"sessao" : document.cookie, "aplicacao": "PJe", "servidor" : WEB_ROOT, "codigoSeguranca": PJE_OFFICE_CODIGO_SEGURANCA, "tarefaId": "cnj.autenticador",      "tarefa": { "enviarPara": "/logarPJeOffice.seam?cid=" + CONVERSATION_ID, "mensagem": ASSINATURA_MENSAGEM } }; var t = requisicao.tarefa; requisicao.tarefa = PJeOffice.stringify(t); var r =    PJeOffice.stringify(requisicao); r = encodeURIComponent(r); link = "http://localhost:8800/pjeOffice/requisicao/?r=" + r + "&u=" + new Date().getTime(); return link;'''
        tentativas = 2
        login = False
        while tentativas:
            try:
                CONVERSATION_ID = self.DRIVER.execute_script('return CONVERSATION_ID;')
                remote_link = self.DRIVER.execute_script(script)
                login = True
                break
            except Exception as e:
                tentativas -= 1
                time.sleep(2)

            assert login, 'Falha no Login'

        self.DRIVER.get(remote_link)
        self.DRIVER.get(f'{self.URL_BASE}/homePJeOffice.seam?cid={CONVERSATION_ID}')
        return self
