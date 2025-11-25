from qaseio import QaseApi, models
import os

QASE_TOKEN = os.getenv("QASE_TOKEN")
PROJECT_CODE = "AL"

api = QaseApi(token=QASE_TOKEN)

def report_to_qase(case_id: int, status: bool, comment=""):
    """Crea un run y envía el resultado dentro de ese run"""

    # 1️⃣ Crear un Run nuevo
    run = api.runs.create(
        code=PROJECT_CODE,
        data=models.RunCreate(
            title="Run automático GitHub Actions",
            description="Ejecución CI desde GitHub",
            cases=[case_id]
        )
    )

    run_id = run.result.id   # Extraer el id del run creado

    # 2️⃣ Enviar el resultado dentro del run
    api.results.create(
        code=PROJECT_CODE,
        run_id=run_id,
        data=models.TestResultCreate(
            case_id=case_id,
            status="passed" if status else "failed",
            comment=comment
        )
    )
