import subprocess
import sys

def install_dependencies():
    """Actualizar pip, instalar Playwright y navegadores"""
    print("📦 Instalando dependencias...")
    
    try:
        print("\n⬆️  Actualizando pip...")
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], check=True)
        
        print("\n🔧 Instalando Playwright...")
        subprocess.run([sys.executable, "-m", "pip", "install", "playwright"], check=True)
        
        print("\n🌐 Instalando navegadores...")
        subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=True)
        
        print("\n✅ Instalación completada exitosamente")
        print("🚀 Ahora puedes ejecutar: python run.py")
        
    except subprocess.CalledProcessError:
        print("❌ Error: No se pudo instalar Playwright")
        print("💡 Solución: Instala Visual Studio Build Tools")
        print("   https://visualstudio.microsoft.com/visual-cpp-build-tools/")
        sys.exit(1)

if __name__ == "__main__":
    install_dependencies()
    input("\nPresiona Enter para salir...")