import requests

uri = "http://bad.example.com/"

r = requests.get("http://www.google.com")

print(r.status_code)