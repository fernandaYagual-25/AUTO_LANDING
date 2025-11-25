import os
import sys

# Ruta donde está este archivo (AUTO_LANDING)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Ruta del directorio AUTO_PERSONAS
PERSONAS_DIR = os.path.join(BASE_DIR, "AUTO_PERSONAS")


def run_automation():
    """Ejecutar automatización de landing page"""
    try:
        print("🚀 Iniciando automatización de landing page...")

        # Verificar que existe el directorio AUTO_PERSONAS
        if not os.path.exists(PERSONAS_DIR):
            print(f"❌ Error: Directorio AUTO_PERSONAS no encontrado en:\n{PERSONAS_DIR}")
            return

        # Verificar que existe el archivo auto_fillpagprin.py
        script_path = os.path.join(PERSONAS_DIR, "auto_fillpagprin.py")
        if not os.path.exists(script_path):
            print(f"❌ Error: Archivo auto_fillpagprin.py no encontrado en:\n{script_path}")
            return

        # Agregar el directorio AUTO_PERSONAS al path
        sys.path.insert(0, PERSONAS_DIR)

        # Importar y ejecutar la automatización
        from auto_fillpagprin import LandingPageAutomation  # type: ignore

        automation = LandingPageAutomation()
        automation.run_automation()

        print("✔️ Automatización finalizada correctamente.")

    except ImportError as e:
        print(f"❌ Error de importación: {e}")
        print("💡 Solución: ejecuta primero: python install.py")
    except Exception as e:
        print(f"❌ Error ejecutando automatización: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    run_automation()
