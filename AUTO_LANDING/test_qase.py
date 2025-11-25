import os
from qaseio.client import QaseClient
from qaseio.models import TestRunCreate

token = os.getenv("QASE_TOKEN")
print("TOKEN CARGADO:", "Sí" if token else "No")

client = QaseClient(api_token=token)

print("🔍 Probando creación de Run...")

run = client.test_runs.create(
    project_code="AL",
    test_run=TestRunCreate(
        title="Test conexión desde GitHub Actions",
        description="Prueba directa API moderna",
    )
)

print("✔ Run creado con ID:", run.result.id)
