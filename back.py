import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class DataMining:
    def __init__(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)

    def open_site(self):
        self.driver.get("https://linkedin.com/login")

    def login_in_site(self):
        self.wait.until(EC.presence_of_element_located((By.ID, "username")))
        with open("user_email.txt", 'r') as f1:
            self.email = f1.readline().strip()
            self.password = f1.readline().strip()

        self.username_field = self.driver.find_element(By.ID, "username")
        self.password_field = self.driver.find_element(By.ID, "password")
        self.username_field.send_keys(f"{self.email}")
        self.password_field.send_keys(f"{self.password}")
        self.password_field.send_keys(Keys.RETURN)

    def run():
        pass