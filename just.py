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
        
        WebDriverWait(self.driver, 180).until(EC.presence_of_element_located((By.ID, "global-nav-search")))
        



    def searching(self):
        self.wait.until(EC.presence_of_element_located((By.ID, "global-nav-search")))
        self.driver.get("https://www.linkedin.com/jobs")
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input.jobs-search-box__text-input")))
        
        with open("user_input.txt", 'r') as f2:
            self.title = f2.readline().strip()
            self.location = f2.readline().strip()
            self.experience = f2.readline().strip()
            self.num = int(f2.readline().strip())
        

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

        WebDriverWait(self.driver, 100).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[aria-label='Search by title, skill, or company']")))
        search_b = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[aria-label='Search by title, skill, or company']")))
        search_b.send_keys(Keys.RETURN)
        time.sleep(10)
    
  

    def data_mining(self):
        jobs = self.wait.until(EC.presence_of_all_elements_located(
            (By.XPATH, "//li[contains(@class, 'occludable-update') and contains(@class, 'scaffold-layout__list-item')]")
        ))
        titles = []
        company_names = []
        locations = []
        types = []
        links= []
        existing_titles = set()
        index = 0
        
        time.sleep(5)
        number_job = 1
        while len(titles)< self.num:
            
            jobs = self.wait.until(EC.presence_of_all_elements_located(
            (By.XPATH, "//li[contains(@class, 'occludable-update') and contains(@class, 'scaffold-layout__list-item')]")
        ))
            try :
                job=jobs[index]
            except IndexError:
                print(f"errored jobs done or something happening")
                
                break


            try:
                self.driver.execute_script("arguments[0].scrollIntoView();", job)
                time.sleep(1)

                title = job.find_element(By.CSS_SELECTOR, "a.job-card-container__link").get_attribute("aria-label")
                if title in existing_titles:
                    index+=1
                    continue
                existing_titles.add(title)

                company = job.find_element(By.CSS_SELECTOR, "div.artdeco-entity-lockup__subtitle").text
                location = job.find_element(By.CSS_SELECTOR, "div.artdeco-entity-lockup__caption").text
                link = job.find_element(By.CSS_SELECTOR, "a.job-card-list__title--link").get_attribute("href")

                loc, type_ = location.split("(")
                type_ = type_[:-1]

                titles.append(title)
                company_names.append(company)
                locations.append(loc)
                types.append(type_)
                links.append(link)
                index += 1
                self.driver.execute_script("window.scrollBy(0, 150);")
                time.sleep(1)

                print("job",number_job,": success full")
                number_job += 1

            except Exception as e:
                print(e)
                continue

        df = pd.DataFrame({
            'Title': titles,
            'Company': company_names,
            'Location': locations,
            'Types': types,
            'Link': links
        })

        df.to_csv('result.csv', index=False, encoding='utf-8')

    def quit(self):
        self.driver.close()

    def run(self):
        self.open_site()
        self.login_in_site()
        self.searching()
        self.data_mining()
        self.quit()


if __name__ == "__main__" :
    data = Linkedin()
    data.run()


    