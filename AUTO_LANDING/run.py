import os
import sys

def run_automation():
    """Ejecutar automatización de landing page"""
    try:
        print("🚀 Iniciando automatización de landing page...")
        
        # Verificar que existe el directorio AUTO_PERSONAS
        auto_personas_path = os.path.join(os.getcwd(), "AUTO_PERSONAS")
        if not os.path.exists(auto_personas_path):
            print("❌ Error: Directorio AUTO_PERSONAS no encontrado")
            return
        
        # Verificar que existe el archivo auto_fillpagprin.py
        script_path = os.path.join(auto_personas_path, "auto_fillpagprin.py")
        if not os.path.exists(script_path):
            print("❌ Error: Archivo auto_fillpagprin.py no encontrado")
            return
        
        # Agregar el directorio AUTO_PERSONAS al path
        sys.path.insert(0, auto_personas_path)
        
        # Importar y ejecutar la automatización
        from auto_fillpagprin import LandingPageAutomation  # type: ignore
        
        automation = LandingPageAutomation()
        automation.run_automation()
        
    except ImportError as e:
        print(f"❌ Error de importación: {e}")
        print("💡 Ejecuta primero: python install.py")
    except Exception as e:
        print(f"❌ Error ejecutando automatización: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_automation()
    input("\nPresiona Enter para salir...")