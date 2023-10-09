import logging 
import time 
from src.init import BaseDriver
from scheme.scheme import SITE_SCHEME
from selenium.common.exceptions import NoSuchElementException

class Inicial_Protocol():
    @BaseDriver.screen_decorator("Protocol")
    def navigate_to_protocol_screen(self):
        if self.outputProcess != '':
            return True
        self.find_locator("screenProtocol").click()
        self.click_btn_signer()
        logging.info(f"ID={self.ID}, protocol is confirmd")

    def click_btn_signer(self):
        time.sleep(2)
        for i in range(2):
            try:
                self.find_locator("btnSigner").click()
                return self.check_is_protocol()
            except:
                continue
        raise ValueError("Failed to click in button protocol")



    def check_is_protocol(self):
        self.outputProcess = str()
        try:
            link = self.find_locator("btncomprovante", retry_count=20).get_attribute("onclick")
            link = link.split("'")[3]
            if "reportPDF" in link:
                self.outputProcess  = link
            return self.outputProcess 
        except:
            raise ValueError("Failed to confirm protocol")


    @BaseDriver.screen_decorator("SignDocs")
    def navigate_to_docs_screen(self):
        self.find_locator("screenDocs").click()
        self.check_if_was_registered()
        if self.outputProcess != "":
            return self.switch_to_screen("Protocol")

        self.check_if_docs_is_signed()
        return self.switch_to_screen("Protocol")


    def check_if_was_registered(self):
        self.outputProcess = str()
        try:
            self.find_locator("btncomprovante", retry_count=2)
            self.outputProcess = "This process has already been signed"
            logging.warning(f'ID={self.ID}, {self.outputProcess}')
            return True
        except:
            return False
        
    def check_if_docs_is_signed(self):
        try:
            self.find_locator("btnSigner", retry_count=5).click()
            self.wait_signer("mpProgressoContainer")
            self.check_docs_signed()
        except NoSuchElementException:
            logging.info(f"ID={self.ID}, button docs not found")


    def check_docs_signed(self):
        page = self.DRIVER.page_source
        if "Documento(s) assinado(s) com sucesso." in page:
            logging.info(f"ID={self.ID}, docs have been signed")
            return self.switch_to_screen("Protocol")
        raise ValueError("Docs were not signed")
