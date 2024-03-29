from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import os
import requests

class Login:
    def __init__(self, auth) -> None:
        self.user = auth['user']
        self.pswd = auth['password']
        self.token = auth['token']
        self.cacheGuid = auth['cacheGuid']

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

    def validate(self):
        headers = {
            'Authorization': self.token,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        }

        params = {
            'cache-guid': self.cacheGuid,
        }

        response = requests.get(
            'https://investidor.b3.com.br/api/investidor/v1.1/cadastro',
            verify=False,
            params=params,
            headers=headers
        )
        if response.status_code == 200:
            self.browser.quit()
            return True
        else:
            return False

    def getAuth(self):
        if not self.validate():
            self.browser.get("https://www.investidor.b3.com.br/")

            wait = WebDriverWait(self.browser, 10)
            # wait.until(EC.visibility_of_element_located((By.ID, 'DOC_INPUT')))
            # element = self.browser.find_element(By.ID, "DOC_INPUT")
            wait.until(EC.visibility_of_element_located((By.ID, 'cpf_mask')))
            element = self.browser.find_element(By.ID, "cpf_mask")
            element.send_keys(self.user)
            # element = self.browser.find_element(By.ID, "Btn_CONTINUE")
            element = self.browser.find_element(By.XPATH, "/html/body/app-root/app-landing-page/div/div[2]/aside/div[1]/button")
            element.click()
            wait.until(EC.visibility_of_element_located((By.ID, 'PASS_INPUT')))
            element = self.browser.find_element(By.ID, "PASS_INPUT")
            element.send_keys(self.pswd)

            element = self.browser.find_element(By.ID, "Btn_CONTINUE")
            WebDriverWait(self.browser, timeout=1000, poll_frequency=1).until(
                EC.staleness_of(element))

            wait.until(EC.title_is("Área do Investidor | B3"))
            self.cacheGuid = self.browser.execute_script(
                "return sessionStorage.getItem('cache-guid');")
            self.token = 'Bearer ' + \
                str(self.browser.execute_script(
                    "return sessionStorage.getItem('token');"))
            self.browser.quit()