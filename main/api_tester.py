# Проверяет апишку

import requests
from bs4 import BeautifulSoup as BS
import json
url = "https://digitalportfolio.pythonanywhere.com/api/token/"
data = {
    "username": "XcenaX",
    "password": "Dagad582#"
}
r = requests.post(url, data=data)
html = BS(r.content, "html.parser")
print(r.content)
token = (json.loads(r.content))["access"]

print(token)
url = "https://digitalportfolio.pythonanywhere.com/students/"
token_str = "Bearer "+token
headers = {
    "Authorization": token_str,
    "X-TokenAuth": token
}

'''
data = {
    "login": "vlad3454",
    "password": "123",
    "username": "XcenaX",
    "name": "Yo"
}
'''

r = requests.get(url, headers=headers)
html = BS(r.content, "html.parser")
print(r.content)