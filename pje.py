import logging

from src.init import BaseDriver
from src.login import Login
from src.inicial_protocol import Inicial_Protocol
from src.incidental_protocol import Incidental_Protocol

class Pje_Selenium(BaseDriver, Login, Inicial_Protocol, Incidental_Protocol):
    def __exit__(self, type, value, traceback):
        if self.DRIVER:
            self.DRIVER.quit()
        
    def __enter__(self): 
        self.setDriver(self.driver_path, self.chrome_options)
        return self


    def start(self, contents):
        self.login(contents)
        for content in contents['lote']:
            try:
                if contents['tipo'] == 0:
                    self.inicial_protocol(content)
                elif contents['tipo'] == 1:
                    self.incidental_protocol(content)
                else: raise ValueError(f"tipo: {contents['tipo']} - invalid method")
            except Exception as e:
                self.returnMsg(inputs=content, error=True, msg=e.args[0])
                logging.warning(f'ID={self.ID}, ERRO EM 1 PROCESSO - ' + str(e.args[0]))


    def inicial_protocol(self, content):
        self.global_variables(content)
        self.switch_to_screen("SignDocs")
        self.navigate_to_docs_screen()
        self.navigate_to_protocol_screen()
        self.returnMsg(inputs=content)
    
    def incidental_protocol(self, content):
        self.global_variables(content)
        self.switch_to_screen("IncidentalProtocol")
        self.navigate_to_incidental_page()
        self.returnMsg(inputs=content)



