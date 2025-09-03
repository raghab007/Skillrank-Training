import os
from bs4 import BeautifulSoup
files = os.listdir("data")
import pandas as pd

collection = {"title":[],"price":[],"link":[]}
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
        collection["link"].append(link)
        collection["price"].append(price)
        collection["title"].append(title)
    except Exception as e:
        print(e)

df  = pd.DataFrame(data=collection)
df.to_csv("data.csv")


