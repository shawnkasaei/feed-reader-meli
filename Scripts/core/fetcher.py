import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

class Fetcher:

    def __init__(self, timeout: int = 15):
       
        self.headers = {
            "User-Agent": "Mozilla/5.0"
        }
        self.timeout = timeout

    def get_text_by_selenium(self, url: str, css_selector_visibility_element:str="body") -> str:
        
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install())
        )

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