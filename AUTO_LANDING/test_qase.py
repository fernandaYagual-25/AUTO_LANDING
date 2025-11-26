import os
import requests

QASE_TOKEN = os.getenv("QASE_TOKEN")
PROJECT_CODE = "AL"   # 👈 tu código real del proyecto

API_URL = f"https://api.qase.io/v1/run/{PROJECT_CODE}"

headers = {
    "Content-Type": "application/json",
    "Token": QASE_TOKEN
}

body = {
    "title": "Test de conexión desde GitHub Actions"
}

print("🔄 Probando conexión con Qase...")

response = requests.post(API_URL, json=body, headers=headers)

print("📤 Código HTTP:", response.status_code)
print("📥 Respuesta:")
print(response.text)

if response.status_code == 200 and '"status":true' in response.text:
    print("✅ Conexión exitosa con Qase")
else:
    print("❌ Conexión fallida con Qase")
    exit(1)
