from selenium import webdriver
import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv

os.environ["PATH"] += os.pathsep + "/Users/raghabpokhrel/Downloads/chromedriver-mac-arm64"
driver =  webdriver.Chrome()

load_dotenv()
PHONE = os.getenv("PHONE")
PASSWORD = os.getenv("PASSWORD")

# driver.get(f"https://www.amazon.in/s?k={search}&page={page}&xpid=RbFd-a7yjl6Ny&crid=35FEBR8R2BS66&qid=1755844083&sprefix=lapt%2Caps%2C333&ref=sr_pg_2")
driver.get('https://www.amazon.in/')
driver.implicitly_wait(3)
element = driver.find_element(By.ID,"nav-link-accountList-nav-line-1")
element.click();
time.sleep(3)
login_el = driver.find_element(by=By.ID,value="ap_email_login")
login_el.send_keys(PHONE)

submit_el = driver.find_element(by=By.CLASS_NAME, value="a-button-input")
submit_el.click()

password_el = driver.find_element(by=By.ID,value="ap_password")
print(password_el)
driver.execute_script("arguments[0].value = arguments[1];", password_el, PASSWORD)


# element = WebDriverWait(driver, 10).until(
#     EC.text_to_be_present_in_element((By.ID, "ap_password"), "Raghab@123##")
# )

sign_in_el = driver.find_element(by=By.ID,value="signInSubmit")
print(sign_in_el)
sign_in_el.submit();

time.sleep(10);











    
