from qaseio import QaseApi, models
import os

print("🔍 Probando conexión con Qase...")

token = os.getenv("QASE_TOKEN")
print("TOKEN CARGADO:", "Sí" if token else "No")

try:
    api = QaseApi(token=token)

    # 1) Crear un Run vacío
    run = api.runs.create(
        code="AL",
        data=models.RunCreate(
            title="Test conexión desde GitHub",
            description="Esto debería crear un Run en Qase",
            cases=[]
        )
    )

    print("✔ Run creado:", run.result.id)

except Exception as e:
    print("❌ ERROR:", e)
