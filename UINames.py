import requests

r = requests.get("http://uinames.com/api/")

print(r.status_code)