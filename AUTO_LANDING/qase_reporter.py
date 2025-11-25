from qaseio import QaseApi, models
import os

QASE_TOKEN = os.getenv("QASE_TOKEN")
PROJECT_CODE = "AL"   # Código real del proyecto en Qase

api = QaseApi(token=QASE_TOKEN)

def report_to_qase(case_id: int, status: bool, comment=""):
    """Envía resultados a Qase"""
    status_text = "passed" if status else "failed"

    api.results.create(
        code=PROJECT_CODE,
        data=models.TestResultCreate(
            case_id=case_id,
            status=status_text,
            comment=comment
        )
    )
