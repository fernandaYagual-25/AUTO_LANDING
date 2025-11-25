import os
from qaseio.client import QaseClient
from qaseio.models import TestRunCreate, TestResultCreate, ResultStatus

QASE_TOKEN = os.getenv("QASE_TOKEN")
PROJECT_CODE = "AL"

client = QaseClient(api_token=QASE_TOKEN)

def report_to_qase(case_id: int, status: bool, comment=""):
    """Crea un run y envía resultado a Qase (API moderna)"""

    # 1. Crear un Run
    run = client.test_runs.create(
        project_code=PROJECT_CODE,
        test_run=TestRunCreate(
            title="GitHub Actions Run",
            description="Ejecución automática CI",
        )
    )

    run_id = run.result.id

    # 2. Enviar resultado
    client.test_results.create(
        project_code=PROJECT_CODE,
        run_id=run_id,
        test_result=TestResultCreate(
            case_id=case_id,
            status=ResultStatus.PASSED if status else ResultStatus.FAILED,
            comment=comment
        )
    )
