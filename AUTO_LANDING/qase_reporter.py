import os
import requests

QASE_TOKEN = os.getenv("QASE_TOKEN")
PROJECT_CODE = "AL"

BASE_URL = "https://api.qase.io/v1"

HEADERS = {
    "Content-Type": "application/json",
    "Token": QASE_TOKEN
}

def report_to_qase(case_id: int, status: bool, comment=""):
    """Crea un run + envía el resultado usando la API real"""

    # 1️⃣ crear un RUN
    run_payload = {
        "title": "GitHub Actions Run",
        "description": "Run generado automáticamente desde CI",
        "cases": [case_id]
    }

    run_res = requests.post(
        f"{BASE_URL}/run/{PROJECT_CODE}",
        json=run_payload,
        headers=HEADERS
    )

    if run_res.status_code != 200:
        print("❌ Error creando RUN:", run_res.text)
        return

    run_id = run_res.json()["result"]["id"]
    print("✔ Run creado:", run_id)

    # 2️⃣ enviar RESULTADO
    result_payload = {
        "status": "passed" if status else "failed",
        "comment": comment
    }

    result_res = requests.post(
        f"{BASE_URL}/result/{PROJECT_CODE}/{run_id}/{case_id}",
        json=result_payload,
        headers=HEADERS
    )

    if result_res.status_code != 200:
        print("❌ Error enviando resultado:", result_res.text)
    else:
        print("✔ Resultado enviado correctamente")
