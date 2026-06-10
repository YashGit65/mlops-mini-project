import requests

r = requests.get("https://dagshub.com")
print(r.status_code)