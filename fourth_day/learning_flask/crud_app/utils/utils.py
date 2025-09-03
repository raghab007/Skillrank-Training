from pymongo import MongoClient
from urllib.parse import quote_plus
from selenium import webdriver
import os
import time
from selenium.webdriver.common.by import By
import os
from bs4 import BeautifulSoup
import pandas as pd
from openai import AzureOpenAI
import json


#  configuring open ai model
client = AzureOpenAI(
    api_version="2024-12-01-preview",
    azure_endpoint=os.getenv("AZURE_ENDPOINT"),
    api_key=os.getenv("API_KEY")
)
password = quote_plus("Praghab@123##")
username = "pokhrelraghab60"

mongo_client = MongoClient(f'mongodb+srv://{username}:{password}@cluster0.q4dyd0y.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0');
db = mongo_client['mydb']
def skip_limit(page_size, page_num):
    # Calculate number of documents to skip
    print(type(page_size), page_num)
    skips = page_size * (page_num - 1)
  # Skip and liit
    cursor = db['users'].find().skip(skips).limit(page_size)
    print(cursor)
       
    return [x for x in cursor]


def scrape(search):
    os.makedirs("data", exist_ok=True)  # creates 'data' if it doesn't exist
    os.environ["PATH"] += os.pathsep + "/Users/raghabpokhrel/Downloads/chromedriver-mac-arm64"
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

def collect(files):
    collection  =[]
    for file in files:
        try:
            with open("data/"+file) as f:
                html_doc = f.read()
            soup = BeautifulSoup(html_doc,'html.parser')
            t = soup.find("h2")
            title = t.get_text()
            l= t.parent
            link = l['href']
            p =soup.find("span",attrs={"class":"a-price"})
            price = (p.find("span").get_text())
            collection.append({"title":title, "link":link,"price":price})
        except Exception as e:
            print(e)
    return collection

# df  = pd.DataFrame(data=collection)
# df.to_csv("data.csv")

def ai_response(content):
    system_prompt = """
    You are a JSON API generator. 
    Convert user requests into CRUD operations for MongoDB.
    Response format ONLY:
    {
      "operation": "create|read|update|delete",
      "collection": "users",
      "filter": {...},     # for read, update, delete
      "data": {...}        # for create, update
    }
    """
    try:
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": content,
                }
            ],
            max_completion_tokens=16384,
            model="gpt-5-mini"
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        print(f"Error in AI response: {e}")
        return {"response": "Sorry, I encountered an error processing your request. Please try again."}
    


def serialize_user(user_doc):
    if not user_doc:
        return None
    user_doc["_id"] = str(user_doc["_id"])
    return user_doc














