#---------IMPORTS--------------------------------------------
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
import selenium.common.exceptions
import os
import warnings
#---------IMPORTS--------------------------------------------


class IgEnvironment:

    def __init__(self,driver_path):

        self.driver_path = driver_path

        
        self.username = "dcr.z0"
        self.password = "Lolj123jdq"
        # self.username = str(input("Username: "))
        # self.password = str(input("Password: "))

        self.final_search_field = ""

        self.initEnvironment()

    def initEnvironment(self):

        os.environ['PATH'] += self.driver_path

        chrome_options = Options()

        # chrome_options.add_argument('headless')
        chrome_options.add_argument('window-size=0x0')
        chrome_options.add_argument("disable-gpu")

        chrome_options.add_experimental_option("detach", True)

        self.driver = webdriver.Chrome(options=chrome_options)

        self.driver.get("https://www.instagram.com/")

        username = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"input[name='username']")))
        password = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"input[name='password']")))

        username.send_keys(self.username)
        password.send_keys(self.password)

        submit_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"button[type='submit']"))).click()

        not_now = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH,"//button[contains(text(), 'Ahora no')]"))).click()
        not_now = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH,"//button[contains(text(), 'Ahora no')]"))).click()

        search_field = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"svg[aria-label='Buscar']"))).click()

        self.final_search_field = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"input[placeholder='Buscar']")))


    def scrape_by_search_query(self,query = str,tags = ["img"],extract_img_url = True,mult_number_of_imgs = 1):

        self.final_search_field.send_keys(query)
        self.final_search_field.send_keys(Keys.ENTER)

        self.final_search_field = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,f"a[href='/explore/tags/{query}/'"))).click()
        raw = []
        time.sleep(10)
        self.driver.execute_script(f"window.scrollTo(0,{4000*mult_number_of_imgs});")
        for tag in tags:
            temp = self.driver.find_elements(By.TAG_NAME,tag)
            if extract_img_url:
                temp = [t.get_attribute("src") for t in temp]

            raw.extend(temp)
        return raw

    def scrape_by_profile_query(self,query = str,mult_number_of_imgs = 1):
        try:
            self.final_search_field.send_keys(query)
            self.final_search_field.send_keys(Keys.ENTER)

            self.final_search_field = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,f"a[href='/{query}/'"))).click()

            time.sleep(10)
            self.driver.execute_script(f"window.scrollTo(0,{4000*mult_number_of_imgs});")
            
            imgs = self.driver.find_elements(By.TAG_NAME,"img")
            imgs = [t.get_attribute("src") for t in imgs]

            return imgs
        except selenium.common.exceptions.TimeoutException:

            print("The search query could not be found")

if __name__ == "__main__":
    app = IgEnvironment(input("Enter the chromedriver path: "))
    
    while True:
        warnings.filterwarnings("ignore")
        choice = input("Select 'Q' for search by query or 'P' for search by profile or 'x' to abort[Q/P/x]: ")
        if choice == "Q":
            print(app.scrape_by_search_query(input("type in the search query: ")))
            continue
        elif choice == "P":
            print(app.scrape_by_profile_query(input("type in the profile you want to scrape: ")))
            continue
        elif choice == "x":
            break
        else:
            continue








