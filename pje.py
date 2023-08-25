from selenium.webdriver.support.select import Select, By
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
from src.init import BaseDriver
from src.schemes.scheme import SITE_SCHEME
from src.login import Login

import logging

class Pje_Selenium(BaseDriver, Login):
    def __exit__(self, type, value, traceback):
        if self.DRIVER:
            self.DRIVER.quit()  
        
    def __enter__(self): 
        self.setDriver(self.driver_path, self.chrome_options)
        return self


    @BaseDriver.screen_decorator("Parts")
    def navigate_to_part_screen(self, content):
        self.find_locator("screenPart").click()
        self.add_all_parts(content)
        return self.switch_to_screen("Protocol")

    def add_all_parts(self, content):
        for cpf_ativo in content['polo_ativo']:
            self.find_locator("addPartA", method="click")
            self.set_options_part(cpf_ativo)
            result = self.verify_part_in_process(cpf_ativo, "activeTable")
            cpf_ativo.update(result)

        for cpf_passivo in content['polo_passivo']:
            self.find_locator("addPartP", method="click")
            self.set_options_part(cpf_passivo)
            result = self.verify_part_in_process(cpf_passivo, "passiveTable")
            cpf_passivo.update(result)


    def set_options_part(self, InfosPart):
            self.set_type_part(infosPart=InfosPart)
            self.add_part_category(category=InfosPart["tipo_parte"])
            self.add_document(InfosPart['cpf'])
            dict_address = self.add_address(InfosPart)
            self.find_locator("addPartButton", by=By.CSS_SELECTOR, method="click")
            return dict_address
    
    @BaseDriver.screen_decorator("Protocol")
    def navigate_to_protocol_screen(self):
        self.find_locator("screenProtocol").click()
        self.find_locator("btnSigner").click()
        self.wait_signer("mpProgressoContainer")


    @BaseDriver.screen_decorator("SignDocs")
    def navigate_to_docs_screen(self):
        self.find_locator("screenDocs").click()
        self.find_locator("btnSigner").click()
        self.wait_signer("mpProgressoContainer")
        self.check_docs_signed()
        return self.switch_to_screen("Protocol")

    def check_docs_signed(self):
        page = self.DRIVER.page_source
        if "Documento(s) assinado(s) com sucesso." in page:
            logging.info(f"ID={self.ID}, docs have been signed")
        raise ValueError("Docs were not signed")

    def set_type_part(self, infosPart):
        if infosPart.get("cnpj"):
            return self.find_locator("typeCnpj").click()


    def add_part_category(self, category: str):
        self.switch_to_screen("Parts")
        categories = self.get_part_categories()
        if category and category not in categories:
            raise ValueError(f"pole {category} not found")
        select_element = self.find_locator("categorySelect")    
        select_object = Select(select_element)
        select_object.select_by_visible_text(category)

    
    def get_part_categories(self):
        select_element = self.find_locator("categorySelect")
        select_object = Select(select_element)
        categories = [option.text.strip() for option in select_object.options]
        return categories
    

    def add_document(self, document):
        self.find_locator("inputDocument", by=By.CSS_SELECTOR).send_keys(document)    
        self.find_locator("searchButton").click()
        self.find_locator("confirmButton").click()
        return self.switch_to_screen("AddAddress")


    @BaseDriver.screen_decorator("AddAddress")
    def add_address(self, content):
        self.find_locator("screenAddress").click()
        self.find_locator("inputCep", by=By.CSS_SELECTOR).send_keys(content['cep'])
        self.find_locator("searchResult", method="script")
        return self.set_atributes_address(content=content)
        
    def set_atributes_address(self, content):
        self.send_inputs_address(district=content['bairro'], street=content['logradouro'],
                                          complement=content['endereco'], number=content['numeroEndereco'])
        return self.find_address(content['cep'])


    def find_address(self, cep):
        import time
        time.sleep(2)
        soup = BeautifulSoup(self.DRIVER.page_source)
        table_address= soup.select_one(
            'tbody[id*="cadastroPartePessoaEndereco"]')
        
        for tr in table_address.findAll('tr'):
            if cep == tr.findAll('td')[2].span.text:
                tds = tr.findAll('td')
                return {
                    "check_cep": True,
                    "cep": tds[2].text,
                    "Logradouro": tds[3].text,
                    "Número": tds[4].text,
                    "Complemento": tds[5].text
                }
        raise RuntimeError({"Error": "Cep not found in address list"})

    

    def send_inputs_address(self, district, street, complement, number) -> str:
        self.send_keys_if_visible("districtInsert", district, by=By.CSS_SELECTOR)
        self.send_keys_if_visible("streetInsert", street, by=By.CSS_SELECTOR)
        self.send_keys_if_visible("complementInsert", complement, by=By.CSS_SELECTOR)
        self.send_keys_if_visible("numberInsert", number, by=By.CSS_SELECTOR)
        return self.find_locator("saveButton", by=By.CSS_SELECTOR).click()


    def verify_part_in_process(self, infosPart, pole):
        self.switch_to_screen("Parts")
        self.find_locator("waitWindowClose")
        self.find_locator(pole, by=By.CSS_SELECTOR,)
        locator = SITE_SCHEME[self.current_screen]["elements"][pole]

        soup = BeautifulSoup(self.DRIVER.page_source, "html.parser")
        for tr in soup.select(locator):
            part = tr.select_one("td:nth-child(2) > span > div > span")
            if infosPart['cpf'] in part.text:
                    return self.appendPart(msg=f"Added part:{part.text}", screen="SetParts", error=False,
                                           contentAddress="Address")
        raise ValueError({"Error": f"part not found: {infosPart['cpf']}"})
    

    def appendPart(self, msg, error, screen, contentAddress, response=200):
        if not screen:
            screen = self.current_screen
        if msg:
            return {
                "screen": screen,
                "msg": msg,
                "error": error,
                "status_code": response,
                "address_registered": contentAddress}
    

    def start(self, contents):
        self.login()
        for content in contents:
            try:
                self.global_variables(content)
                self.switch_to_screen("Protocol")
                self.navigate_to_docs_screen()
                self.navigate_to_protocol_screen()
                self.returnMsg(inputs=content)
            except Exception as e:
                self.returnMsg(inputs=content, error=True, msg=e)
                logging.warning(f'ID={self.ID}, ERRO EM 1 PROCESSO - ' + str(e))
            






