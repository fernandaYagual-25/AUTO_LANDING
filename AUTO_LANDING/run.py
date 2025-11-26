#import os
#import sys

# Ruta donde está este archivo (AUTO_LANDING)
#BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Ruta del directorio AUTO_PERSONAS
#PERSONAS_DIR = os.path.join(BASE_DIR, "AUTO_PERSONAS")


#def run_automation():
   # """Ejecutar automatización de landing page"""
    #try:
     #   print("🚀 Iniciando automatización de landing page...")

        # Verificar que existe el directorio AUTO_PERSONAS
      #  if not os.path.exists(PERSONAS_DIR):
       #     print(f"❌ Error: Directorio AUTO_PERSONAS no encontrado en:\n{PERSONAS_DIR}")
        #    return

        # Verificar que existe el archivo auto_fillpagprin.py
       # script_path = os.path.join(PERSONAS_DIR, "auto_fillpagprin.py")
       # if not os.path.exists(script_path):
        #    print(f"❌ Error: Archivo auto_fillpagprin.py no encontrado en:\n{script_path}")
         #   return

        # Agregar el directorio AUTO_PERSONAS al path
        #sys.path.insert(0, PERSONAS_DIR)

        # Importar y ejecutar la automatización
        #from auto_fillpagprin import LandingPageAutomation  # type: ignore

        #automation = LandingPageAutomation()
        #automation.run_automation()

        #print("✔️ Automatización finalizada correctamente.")

    #except ImportError as e:
     #   print(f"❌ Error de importación: {e}")
      #  print("💡 Solución: ejecuta primero: python install.py")
    #except Exception as e:
     #   print(f"❌ Error ejecutando automatización: {e}")
      #  import traceback
       # traceback.print_exc()

#if __name__ == "__main__":
   # run_automation()

from playwright.sync_api import sync_playwright
import os
import sys
import time
from datetime import datetime
import requests

# 🔹 Config
QASE_TOKEN = os.getenv("QASE_TOKEN")
QASE_PROJECT = "AL"
BASE_URL = "https://www.xtrim.com.ec/"
SCREENSHOTS_FOLDER = "AUTO_LANDING/screenshots"
WAIT = 2000

# ======================================
#   FUNCIONES QASE (DENTRO DEL RUN.PY)
# ======================================

import requests

def create_qase_run():
    """Crear un Run en Qase (API v2) con debugging robusto"""
    if not QASE_TOKEN:
        raise Exception("QASE_TOKEN no está definido en el entorno")

    url = f"https://api.qase.io/v2/test-runs/{QASE_PROJECT}"
    payload = {
        "title": "Run automático GitHub Actions",
        "description": "Ejecución CI integrada con Playwright"
    }
    headers = {"Content-Type": "application/json", "Token": QASE_TOKEN}

    response = requests.post(url, json=payload, headers=headers)

    # DEBUG: mostrar estado y body para entender errores
    print("🔁 create_qase_run → status:", response.status_code)
    print("🔁 create_qase_run → body:", repr(response.text)[:2000])

    # Intentar parsear JSON solo si status OK
    if response.status_code in (200, 201):
        try:
            data = response.json()
        except Exception as e:
            raise Exception(f"Respuesta no JSON al crear run: {e}\nBody: {response.text}")
        run_id = data.get("result", {}).get("id")
        if not run_id:
            raise Exception(f"No se obtuvo run_id. Body: {data}")
        print(f"✔ RUN creado en Qase: {run_id}")
        return run_id

    # manejo de errores comunes
    if response.status_code == 401:
        raise Exception("401 Unauthorized — token inválido o sin permisos")
    if response.status_code == 404:
        raise Exception("404 Not Found — proyecto no existe o endpoint incorrecto")
    raise Exception(f"Error creando run ({response.status_code}): {response.text}")

def report_to_qase(run_id, case_id, status, comment=""):
    """Reportar resultado a Qase API v2 con debugging"""
    if not QASE_TOKEN:
        print("⚠ QASE_TOKEN no definido; omitiendo reporte")
        return

    url = f"https://api.qase.io/v2/test-runs/{run_id}/results"
    payload = {
        "case_id": case_id,
        "status": "passed" if status else "failed",
        "comment": comment
    }
    headers = {"Content-Type": "application/json", "Token": QASE_TOKEN}

    response = requests.post(url, json=payload, headers=headers)
    print(f"📤 report_to_qase → status: {response.status_code}")
    print("📤 report_to_qase → body:", repr(response.text)[:2000])

    if response.status_code not in (200, 201):
        # no romper el flujo, pero informar bien
        print(f"❌ Error enviando resultado: ({response.status_code}) {response.text}")

# ======================================
#     AUTOMATIZACIÓN PLAYWRIGHT
# ======================================

class LandingPageAutomation:

    def __init__(self, run_id):
        self.run_id = run_id
        self.playwright = None
        self.browser = None
        self.page = None

    def setup(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=True)
        self.page = self.browser.new_page()

    def screenshot(self, name):
        if not os.path.exists(SCREENSHOTS_FOLDER):
            os.makedirs(SCREENSHOTS_FOLDER)

        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        file = f"{SCREENSHOTS_FOLDER}/{name}_{ts}.png"
        self.page.screenshot(path=file)
        print(f"📸 Screenshot guardado: {file}")

    # ===============================
    #          TEST 1
    # ===============================

    def test_pagar_servicios(self):
        try:
            print("🔄 Test: Pagar Servicios")
            self.page.goto(BASE_URL)
            time.sleep(2)

            # Ejemplo
            self.page.click("text=Pagar Servicios")
            time.sleep(2)

            # Si pasa:
            report_to_qase(self.run_id, case_id=1, status=True, comment="Pagar servicios OK")
            print("✅ Test Pagar Servicios PASÓ")
            return True

        except Exception as e:
            self.screenshot("error_pagar_servicios")
            report_to_qase(self.run_id, case_id=1, status=False, comment=str(e))
            print("❌ Test Pagar Servicios FALLÓ")
            return False

    # ===============================
    #          TEST 2
    # ===============================

    def test_te_llamamos(self):
        try:
            print("🔄 Test: Te llamamos")

            self.page.goto(BASE_URL)
            time.sleep(2)

            # Ejemplo
            self.page.click("text=Te llamamos")
            time.sleep(2)

            # Si pasa:
            report_to_qase(self.run_id, case_id=2, status=True, comment="Te llamamos OK")
            print("✅ Test Te llamamos PASÓ")
            return True

        except Exception as e:
            self.screenshot("error_te_llamamos")
            report_to_qase(self.run_id, case_id=2, status=False, comment=str(e))
            print("❌ Test Te llamamos FALLÓ")
            return False

    # ===============================
    #        EJECUCIÓN TOTAL
    # ===============================

    def run(self):
        try:
            print("🚀 Iniciando ejecución")
            self.setup()

            self.test_pagar_servicios()
            self.test_te_llamamos()

        finally:
            if self.browser:
                self.browser.close()
                self.playwright.stop()
            print("🔚 Navegador cerrado")

#      MAIN

if __name__ == "__main__":
    run_id = create_qase_run()  # ✔ CREA EL RUN AQUÍ
    automation = LandingPageAutomation(run_id)
    automation.run()
