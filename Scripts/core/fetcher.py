import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Fetcher:

    def __init__(self, timeout: int = 15):
       
        self.headers = {
            "User-Agent": "Mozilla/5.0"
        }
        self.timeout = timeout

    def get_text_by_selenium(self, url: str, css_selector_visibility_element:str="body") -> str:
        
        options = Options()
        options.add_argument("--headless")

        driver = webdriver.Chrome(options=options)
        driver.set_page_load_timeout(self.timeout)
        driver.get(url)

        WebDriverWait(driver, self.timeout).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, css_selector_visibility_element))
        )

        html = driver.page_source
        driver.quit()
        
        return html

    def get_text_by_requests(self, url: str) -> str:
        
        r = requests.get(url, headers=self.headers, timeout=self.timeout)
        r.raise_for_status()
        return r.text
    
    def get_json_by_requests(self, url: str) -> dict:
       
        r = requests.get(url, headers=self.headers, timeout=self.timeout)
        r.raise_for_status()
        return r.json()