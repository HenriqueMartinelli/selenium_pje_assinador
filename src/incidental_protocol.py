import logging
from src.init import BaseDriver
from selenium.common.exceptions import NoSuchElementException

class Incidental_Protocol():
    @BaseDriver.screen_decorator("IncidentalProtocol")
    def navigate_to_incidental_page(self):
        self.find_locator("confirmPage", retry_count=10)
        self.outputProcess = str()
        self.submit_checkbox()
        self._check_if_docs_is_signed()


    def _check_if_docs_is_signed(self):
        try:
            self.find_locator("btnSigner", retry_count=1).click()
            self.wait_signer("mpProgressoContainer")
            self._check_docs_signed()
        except NoSuchElementException:
            logging.info(f"ID={self.ID}, button docs not found")
            raise ValueError("button docs not found or this process have been signed")

    def _check_docs_signed(self):
        try:
            msg = self.find_locator("confirmSigner", retry_count=5).text
            if "Documento(s) assinado(s) com sucesso." in msg:
                self.outputProcess = "docs have been signed"
                logging.info(f"ID={self.ID}, docs have been signed")
                return self.outputProcess
            raise ValueError("Docs were not signed")
        except:
            raise ValueError("Docs were not signed")

    def submit_checkbox(self):
        try:
            element = 'document.querySelectorAll("#expTb > tbody > tr > td > input")'
            check_boxs = self.DRIVER.execute_script(f'return {element}')

            for i in range(len(check_boxs)):
                self.DRIVER.execute_script(f'{element}[{i}].click()')
        except NoSuchElementException:
            raise ValueError("failed to mark checkboxs")
