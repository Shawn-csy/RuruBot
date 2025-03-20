import requests
import json
from bs4 import BeautifulSoup

url = "https://rinakawaei.blogspot.com"

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

jump_link = soup.select_one(".jump-link.flat-button a")
if jump_link:
    print("Jump Link:")
    print("URL:", jump_link["href"])
    print("Title:", jump_link.get("title", "No title"))

post_link = soup.select_one("h3.post-title.entry-title a")
if post_link:
    print("\nPost Link:")
    print("URL:", post_link["href"])
    print("Title:", post_link.text)


