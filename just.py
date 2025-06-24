import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Linkedin:
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

        username_field = self.driver.find_element(By.ID, "username")
        password_field = self.driver.find_element(By.ID, "password")
        username_field.send_keys(f"{self.email}")
        password_field.send_keys(f"{self.password}")
        password_field.send_keys(Keys.RETURN)

    def searching(self):
        self.wait.until(EC.presence_of_element_located((By.ID, "global-nav-search")))
        self.driver.get("https://www.linkedin.com/jobs")
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input.jobs-search-box__text-input")))
        
        with open("user_input.txt", 'r') as f2:
            self.title = f2.readline().strip()
            self.location = f2.readline().strip()
            self.experience = f2.readline().strip()
            self.num = f2.readline().strip()

        
        
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[aria-label='City, state, or zip code']")))
        location_search = self.driver.find_element(By.CSS_SELECTOR, "input[aria-label='City, state, or zip code']")
        location_search.clear()
        location_search.send_keys(f"{self.location}")
        time.sleep(2)

        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[aria-label='Search by title, skill, or company']")))
        job_search = self.driver.find_element(By.CSS_SELECTOR, 'input[aria-label="Search by title, skill, or company"]')
        job_search.clear()
        job_search.send_keys(f"{self.title}")
        time.sleep(2)

        job_search.send_keys(Keys.RETURN)
        time.sleep(2)

        search_b = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[aria-label='Search by title, skill, or company']")))
        search_b.send_keys(Keys.RETURN)
        time.sleep(10)

    def scroller(self):
        start = time.time()
        initialScroll = 0
        finalScroll = 1000

        while True:
            self.driver.execute_script(f"window.scrollTo({initialScroll},{finalScroll})")
            initialScroll = finalScroll
            finalScroll += 1000

            time.sleep(5)

            end = time.time()

            if round(end - start) > 20:
                break

    def data_mining(self):
        job_titles = []
        company_names = []
        locations = []
        links = []
        
        result = self.driver.find_elements(By.CLASS_NAME, "jobs-search-results__list_item")

        for i in result:
            if len(job_titles) >= int(self.num):
                break
            
            title = i.find_element(By.CSS_SELECTOR, "a.job-card-list__title--link").get_attribute("aria-label")
            company = i.find_element(By.CSS_SELECTOR, "div.artdeco-entity-lockup__subtitle").text
            location = i.find_element(By.CSS_SELECTOR, "div.artdeco-entity-lockup__caption").text
            link = i.find_element(By.CSS_SELECTOR, "a.job-card-list__title--link").get_attribute("href")


            job_titles.append(title)
            company_names.append(company)
            locations.append(location)
            links.append(link)

        df = pd.DataFrame({
            'Title': job_titles,
            'Company': company_names,
            'Location': locations,
            'Link': links
        })

        df.to_csv('result.csv', index=False)

    def quit(self):
        self.driver.close()

    def run(self):
        self.open_site()
        self.login_in_site()
        self.searching()
        self.scroller()
        self.data_mining()
        self.quit()


if __name__ == "__main__" :
    data = Linkedin()
    data.run()


    