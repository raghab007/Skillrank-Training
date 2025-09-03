from selenium import webdriver
import os
import time
from selenium.webdriver.common.by import By
os.makedirs("data", exist_ok=True)  # creates 'd' if it doesn't exist

os.environ["PATH"] += os.pathsep + "/Users/raghabpokhrel/Downloads/chromedriver-mac-arm64"
search = input("What do you want to search in amazon? ")
driver =  webdriver.Chrome()
unique_file = 0;
for page in range(1,6):
    driver.get(f"https://www.amazon.in/s?k={search}&page={page}&xpid=RbFd-a7yjl6Ny&crid=35FEBR8R2BS66&qid=1755844083&sprefix=lapt%2Caps%2C333&ref=sr_pg_2")
    # driver.get('https://www.amazon.in/')
    driver.implicitly_wait(3)
    elements = driver.find_elements(By.CLASS_NAME,"puis-card-container")
    print(f"Total items found in page {page} {len(elements)}")
    for element in elements:
        with open(f"data/{search}_{unique_file}.html",'w',encoding="utf-8") as newFile:
            newFile.write(element.get_attribute('outerHTML'))
        unique_file+=1






    
