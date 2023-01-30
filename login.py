import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import os

class Login:
    def __init__(self, user, pswd) -> None:
        self.user = user
        self.pswd = pswd

        # Setup chrome options
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--start-maximized")

        # Set path to chromedriver as per your configuration
        homedir = os.path.expanduser("~")
        webdriver_service = Service(
            f"{homedir}/chromedriver/stable/chromedriver")

        self.browser = webdriver.Chrome(
            service=webdriver_service,
            options=chrome_options
        )

    def getAuth(self):
        self.browser.get("https://www.investidor.b3.com.br/")

        wait = WebDriverWait(self.browser, 10)
        wait.until(EC.visibility_of_element_located((By.ID, 'DOC_INPUT')))
        element = self.browser.find_element(By.ID, "DOC_INPUT")
        element.send_keys(self.user)
        element = self.browser.find_element(By.ID, "Btn_CONTINUE")
        element.click()
        wait.until(EC.visibility_of_element_located((By.ID, 'PASS_INPUT')))
        element = self.browser.find_element(By.ID, "PASS_INPUT")
        element.send_keys(self.pswd)

        element = self.browser.find_element(By.ID, "Btn_CONTINUE")
        WebDriverWait(self.browser, timeout=1000, poll_frequency=1).until(
            EC.staleness_of(element))

        wait.until(EC.title_is("Área logada | B3"))
        self.cacheGuid = self.browser.execute_script(
            "return sessionStorage.getItem('cache-guid');")
        self.token = 'Bearer ' + \
            str(self.browser.execute_script(
                "return sessionStorage.getItem('token');"))
