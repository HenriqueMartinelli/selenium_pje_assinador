import time
from selenium.webdriver.common.by import By

class Login():

    def login(self, content):
        instancia = content['instancia']
        URL_1 = 'https://pje.tjba.jus.br/pje'
        URL_2 = 'https://pje2g.tjba.jus.br/pje'
        self.URL_BASE = URL_1 if instancia in (1, '1') else URL_2
        self.URL_LOGIN = self.URL_BASE + "/login.seam"

        self.DRIVER.get(self.URL_LOGIN)
        self.find_element("//*[@id='loginAplicacaoButton']", by=By.XPATH, retry_count=3, retry_sleep=1).click()
        self.wait_signer("mp_formValidarContainer")
        return self
