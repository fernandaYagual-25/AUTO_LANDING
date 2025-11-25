import os
import requests

token = os.getenv("QASE_TOKEN")

BASE_URL = "https://api.qase.io/v1"
PROJECT_CODE = "AL"

headers = {
    "Content-Type": "application/json",
    "Token": token
}

payload = {
    "title": "Prueba mínima API REST",
    "description": "Esto debe crear un Run desde GitHub"
}

res = requests.post(
    f"{BASE_URL}/run/{PROJECT_CODE}",
    json=payload,
    headers=headers
)

print("STATUS:", res.status_code)
print("BODY:", res.text)
