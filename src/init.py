import time
import logging
import ctypes
import ctypes.wintypes
import selenium

from datetime import datetime
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import TimeoutException, InvalidElementStateException, ElementClickInterceptedException
import traceback
from scheme.scheme import SITE_SCHEME

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class BaseDriver:
    def __init__(self,
                 chrome_options: webdriver.ChromeOptions = None):

        # self.chrome_options = Options()
        # self.chrome_options.add_argument('--headless')
        self.chrome_options = chrome_options
        # self.driver_path: str = ChromeDriverManager().install()
        self.driver_path = ""
        self.ID = "NOT DEFINED"
        self.outputEvent = list()


    def setDriver(self, executable_path, chrome_options):
        # self.DRIVER: webdriver = webdriver.Chrome(executable_path=executable_path, chrome_options=chrome_options)chrome_options.add_argument('--no-sandbox')
        self.DRIVER = selenium.webdriver.Chrome(options=chrome_options)
        return self.DRIVER
    
    def global_variables(self, content):
        self.ID = content['idTarefa']
        self.URL_PROCESS = content['url_processo']
        self.DRIVER.get(self.URL_PROCESS)


    def find_element(self, value, by=By.XPATH, retry_count=7, retry_sleep=1) -> WebElement:
        for attempt in range(retry_count):
            try:
                return self.DRIVER.find_element(by, value)
            except (NoSuchElementException, TimeoutException):
                logging.warning(f"ID={self.ID}, {by}={value}: Element not found {attempt + 1}/{retry_count}")
                time.sleep(retry_sleep)
        raise NoSuchElementException(f"ID={self.ID}, {by}={value}: Element not found") 
        

    def send_keys_if_visible(self, element, text, by=By.CSS_SELECTOR, retry_count=7, retry_sleep=1) -> WebElement:
        screen = self.current_screen
        value = SITE_SCHEME[screen]["elements"][element]
        for attempt in range(retry_count):
            try:
                input_element = self.DRIVER.find_element(by, value)
                input_element.clear()
                return input_element.send_keys(text)
            except (NoSuchElementException, InvalidElementStateException, StaleElementReferenceException):
                logging.warning(f"ID={self.ID}, {by}={value}: Element not found {attempt + 1}/{retry_count}")
                time.sleep(retry_sleep)
        raise InvalidElementStateException(f"ID={self.ID}, {by}={value}: Element not Interactable") 
    
    

    def find_locator(self, element: str, screen: str = None, retry_count=7, retry_sleep=1, method=None, by=By.XPATH):
        screen = screen or self.current_screen
        locator = SITE_SCHEME[screen]["elements"][element]
        return self.find_element(locator, by=by, retry_count=retry_count, retry_sleep=retry_sleep)
    
    def wait_signer(self, pathContainer):
        attempt = 200
        while attempt:
            try:
                time.sleep(1)
                ProgressPje = self.find_element(f"//*[@id='{pathContainer}']", by=By.XPATH, retry_count=3, retry_sleep=1)
                display = ProgressPje.get_attribute("style")
                if "display: none;" in display:
                    time.sleep(1)
                    return
                self.find_and_click_ok_button("Insira o Pin:")
                attempt -= 1
            except NoSuchElementException:
                return
        raise ValueError("Pje Office stopped responding or window pje not found")


    def find_and_click_ok_button(self, window_title):
        try:
            user32 = ctypes.windll.user32

            window_handle = user32.FindWindowW(None, window_title)
            if window_handle:
                user32.SetForegroundWindow(window_handle)
                time.sleep(0.5)  # Espera um pouco para garantir que a janela esteja em foco
                user32.keybd_event(0x0D, 0, 0, 0)  # Simula pressionamento de Enter
                user32.keybd_event(0x0D, 0, 2, 0)  # Simula liberação de Enter
        except Exception as error:
            logging.warning(f"ID={self.ID}, {error}")


    
    def switch_to_screen(self, screen: str):
        if screen in SITE_SCHEME:
            self.current_screen = screen
        else:
            raise Exception(f"Screen {screen} not found")
        

    def returnMsg(self, inputs=dict(), error=False, msg=None):
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

        if error:
            event = {
                "error": True,
                "msg": msg,
                "created_at": dt_string,
                "idTarefa": inputs.get("idTarefa"),
                "url": inputs.get('url_processo')
            }
        else:
            event = {
                "output": self.outputProcess,
                "error": False,
                "created_at": dt_string,
                "idTarefa": inputs.get("idTarefa"),
                "url": inputs.get('url_processo'),
            }
        self.outputEvent.append(event)
        return event
        # requests.request("POST", url=self.URL_WOOK, json=event, timeout=10)


    @staticmethod
    def screen_decorator(screen: str):
        def decorator(func):
            def wrapper(self, *args, **kwargs):
                if self.current_screen != screen:
                    raise Exception(f"Need to be on {screen} screen: {self.current_screen}")
                return func(self, *args, **kwargs)
            return wrapper
        return decorator
