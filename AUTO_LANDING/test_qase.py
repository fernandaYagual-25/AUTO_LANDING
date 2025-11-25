import os
from qaseio.client import QaseApi
from qaseio.models import TestRunCreate

token = os.getenv("QASE_TOKEN")
print("TOKEN OK:", "Sí" if token else "No")

client = QaseApi(api_token=token)

print("🔍 Probando creación de run...")

run = client.test_runs.create(
    project_code="AL",
    test_run=TestRunCreate(
        title="Test conexión desde GitHub",
        description="Prueba directa con API oficial"
    )
)

print("✔ Run creado con ID:", run.result.id)
