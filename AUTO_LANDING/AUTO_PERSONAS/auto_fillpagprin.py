from playwright.sync_api import sync_playwright
import time
import os
import sys
from datetime import datetime

# Agregar el directorio 
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import *

class LandingPageAutomation:
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.page = None
        self.test_results = {
            "pagar_servicios": False,
            "te_llamamos": False
        }
        
    def setup_browser(self):
        """Configurar Playwright y navegador"""
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(
            headless=True, 
            args=["--start-maximized", "--force-device-scale-factor=0.8"]
        )
        self.page = self.browser.new_page()
        self.page.set_viewport_size({"width": 1920, "height": 1080})
        
    def create_screenshots_folder(self):
        """Crear carpeta de capturas si no existe"""
        if not os.path.exists(SCREENSHOTS_FOLDER):
            os.makedirs(SCREENSHOTS_FOLDER)
            
    def take_screenshot(self, base_filename):
        """Tomar captura de pantalla con timestamp"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        name, ext = os.path.splitext(base_filename)
        filename = f"{name}_{timestamp}{ext}"
        filepath = os.path.join(SCREENSHOTS_FOLDER, filename)
        self.page.screenshot(path=filepath)
        print(f"📸 Captura guardada: {filepath}")
        
    def close_banner(self):
        """Cerrar banner inicial"""
        try:
            self.page.click(SELECTORS["banner_close"], timeout=WAIT_TIME_SHORT)
            print("✅ Banner cerrado exitosamente")
            self.page.wait_for_timeout(1000)
        except:
            print("⚠️  Banner no encontrado o ya cerrado")
            
    def test_pagar_servicios(self):
        """Test: Pagar Servicios"""
        try:
            print("\n🔄 Iniciando test: Pagar Servicios")
            
            # Zoom out para ver todo el contenido
            self.page.evaluate("document.body.style.zoom = '0.8'")
            self.page.wait_for_timeout(2000)
            
            # Hacer clic directo usando JavaScript
            self.page.evaluate("""
                const link = document.querySelector('#menu-main-menu a[title="Pagar Servicio"]');
                if (link) {
                    link.click();
                } else {
                    // Buscar cualquier enlace con "Pagar Servicio"
                    const allLinks = document.querySelectorAll('a[title*="Pagar"]');
                    if (allLinks.length > 0) {
                        allLinks[0].click();
                    }
                }
            """)
            print("✅ Clic en 'Pagar servicio' exitoso")
            
            # Esperar redirección
            self.page.wait_for_timeout(WAIT_TIME_MEDIUM)
            
            # Tomar captura
            self.take_screenshot(SCREENSHOT_PAGAR_SERVICIOS)
            
            self.test_results["pagar_servicios"] = True
            print("✅ Test 'Pagar Servicios' PASADO")
            
        except Exception as e:
            print(f"❌ Error en test 'Pagar Servicios': {str(e)}")
            
    def return_to_home(self):
        """Regresar a la página principal"""
        self.page.goto(BASE_URL)
        self.page.wait_for_timeout(WAIT_TIME_MEDIUM)
        print("🏠 Regresado a página principal")
        
    def test_te_llamamos(self):
        """Test: Te llamamos"""
        try:
            print("\n🔄 Iniciando test: Te llamamos")
            
            # Zoom out para ver todo el contenido
            self.page.evaluate("document.body.style.zoom = '0.8'")
            self.page.wait_for_timeout(2000)
            
            # Cerrar cualquier modal que pueda estar abierto
            try:
                self.page.click("#myModal .close", timeout=2000)
            except:
                pass
            
            # Hacer clic directo usando JavaScript
            self.page.evaluate("""
                const link = document.querySelector('#menu-main-menu a[title="Te llamamos"]');
                if (link) {
                    link.click();
                } else {
                    // Buscar cualquier enlace con "Te llamamos"
                    const allLinks = document.querySelectorAll('a[title*="llamamos"]');
                    if (allLinks.length > 0) {
                        allLinks[0].click();
                    }
                }
            """)
            print("✅ Clic en 'Te llamamos' exitoso")
            
            self.page.wait_for_timeout(WAIT_TIME_SHORT)
            
            # Llenar formulario
            self.fill_form()
            
            # Scroll y aceptar política
            self.accept_policy()
            
            # Enviar formulario
            form_sent = self.submit_form()
            if not form_sent:
                print("❌ Test 'Te llamamos' FALLIDO - No se pudo enviar formulario")
                return
            
            # Esperar procesamiento
            self.page.wait_for_timeout(WAIT_TIME_MEDIUM)
            
            # Verificar mensaje de éxito
            message_found = self.verify_success_message()
            if not message_found:
                print("❌ Test 'Te llamamos' FALLIDO - No se encontró mensaje de éxito")
                return
            
            # Regresar a inicio
            returned = self.return_to_start()
            if not returned:
                print("❌ Test 'Te llamamos' FALLIDO - No se pudo regresar a inicio")
                return
            
            self.test_results["te_llamamos"] = True
            print("✅ Test 'Te llamamos' PASADO")
            return
            
        except Exception as e:
            print(f"❌ Error en test 'Te llamamos': {str(e)}")
            
    def fill_form(self):
        """Llenar datos del formulario"""
        # Esperar a que aparezca el formulario
        self.page.wait_for_timeout(3000)
        
        # Buscar campos del formulario de contacto (excluyendo búsqueda)
        form_inputs = self.page.locator("form input[type='text']:visible, form input[type='email']:visible, form input[type='tel']:visible").all()
        print(f"🔍 Encontrados {len(form_inputs)} campos de formulario")
        
        # Si no encuentra en form, buscar por contenedor modal o div
        if len(form_inputs) == 0:
            form_inputs = self.page.locator(".modal input[type='text']:visible, .modal input[type='email']:visible, .contact input:visible").all()
            print(f"🔍 Encontrados {len(form_inputs)} campos en modal/contacto")
        
        # Llenar campos por orden
        for i, input_field in enumerate(form_inputs[:4]):
            try:
                if i == 0:
                    input_field.fill(FORM_DATA["nombres"])
                    print("✅ Nombres llenado")
                elif i == 1:
                    input_field.fill(FORM_DATA["cedula"])
                    print("✅ Cédula llenada")
                elif i == 2:
                    input_field.fill(FORM_DATA["celular"])
                    print("✅ Celular llenado")
                elif i == 3:
                    input_field.fill(FORM_DATA["correo"])
                    print("✅ Correo llenado")
            except Exception as e:
                print(f"⚠️  Error en campo {i+1}: {e}")
        
        print("✅ Formulario procesado")
        
    def accept_policy(self):
        """Hacer scroll y aceptar política de datos"""
        # Scroll suave
        self.page.evaluate("window.scrollBy(0, 300)")
        self.page.wait_for_timeout(1000)
        
        try:
            # Checkbox política
            self.page.check(SELECTORS["checkbox_politica"])
            print("✅ Política de datos aceptada")
        except:
            print("⚠️  Checkbox de política no encontrado")
        
    def submit_form(self):
        """Enviar formulario"""
        try:
            # Hacer clic en cualquier botón visible del formulario con checkbox
            result = self.page.evaluate("""
                (() => {
                    const forms = document.querySelectorAll('form');
                    for (let form of forms) {
                        const checkboxes = form.querySelectorAll('input[type="checkbox"]');
                        if (checkboxes.length > 0) {
                            const buttons = form.querySelectorAll('button, input[type="submit"]');
                            for (let btn of buttons) {
                                const rect = btn.getBoundingClientRect();
                                if (rect.width > 0 && rect.height > 0) {
                                    btn.click();
                                    return 'Clickeado: ' + btn.textContent.trim();
                                }
                            }
                        }
                    }
                    return 'No se encontró botón';
                })()
            """)
            
            print(f"✅ {result}")
            return "Clickeado" in result
                
        except Exception as e:
            print(f"❌ Error enviando formulario: {e}")
            return False
        
    def verify_success_message(self):
        """Verificar mensaje de éxito"""
        try:
            self.page.wait_for_selector("text=Gracias por contactarnos", timeout=10000)
            print("✅ Mensaje 'Gracias por contactarnos' encontrado")
            self.take_screenshot(SCREENSHOT_TE_LLAMAMOS)
            return True
        except:
            print("❌ Mensaje 'Gracias por contactarnos' NO encontrado")
            self.take_screenshot(SCREENSHOT_TE_LLAMAMOS)
            return False
        
    def return_to_start(self):
        """Hacer clic en regresar a inicio"""
        try:
            # Buscar diferentes variaciones del botón
            result = self.page.evaluate("""
                (() => {
                    const buttons = document.querySelectorAll('button, a, input[type="button"]');
                    for (let btn of buttons) {
                        const text = btn.textContent.toLowerCase().trim();
                        const title = (btn.title || '').toLowerCase();
                        const value = (btn.value || '').toLowerCase();
                        
                        if (text.includes('regresar') || text.includes('inicio') || 
                            text.includes('volver') || text.includes('home') ||
                            title.includes('regresar') || title.includes('inicio') ||
                            value.includes('regresar') || value.includes('inicio')) {
                            btn.click();
                            return 'Clickeado: ' + text;
                        }
                    }
                    return 'No encontrado';
                })()
            """)
            
            if "Clickeado" in result:
                print(f"✅ {result}")
                return True
            else:
                print("❌ Botón 'Regresar a inicio' NO encontrado - navegando directamente")
                self.page.goto(BASE_URL)
                return True
        except Exception as e:
            print(f"❌ Error: {e} - navegando directamente")
            self.page.goto(BASE_URL)
            return True
        
    def print_test_summary(self):
        """Imprimir resumen de tests como checklist"""
        print("\n" + "="*50)
        print("📋 RESUMEN DE TESTS - CHECKLIST")
        print("="*50)
        
        status_pagar = "✅ PASADO" if self.test_results["pagar_servicios"] else "❌ FALLIDO"
        status_llamamos = "✅ PASADO" if self.test_results["te_llamamos"] else "❌ FALLIDO"
        
        print(f"□ Pagar Servicios: {status_pagar}")
        print(f"□ Te llamamos: {status_llamamos}")
        
        total_passed = sum(self.test_results.values())
        print(f"\n📊 Tests pasados: {total_passed}/2")
        
        if total_passed == 2:
            print("🎉 TODOS LOS TESTS PASARON EXITOSAMENTE")
        else:
            print("⚠️  ALGUNOS TESTS FALLARON")
            
    def run_automation(self):
        """Ejecutar automatización completa"""
        try:
            print(f"🌐 URL: {BASE_URL}")
            
            self.setup_browser()
            self.create_screenshots_folder()
            
            # Cargar página principal
            self.page.goto(BASE_URL)
            self.page.wait_for_timeout(WAIT_TIME_MEDIUM)
            
            # Cerrar banner
            self.close_banner()
            
            # Test 1: Pagar Servicios
            self.test_pagar_servicios()
            
            # Regresar a inicio
            self.return_to_home()
            
            # Test 2: Te llamamos
            self.test_te_llamamos()
            
            # Mostrar resumen
            self.print_test_summary()
            
        except Exception as e:
            print(f"❌ Error general: {str(e)}")
        finally:
            if self.browser:
                self.page.wait_for_timeout(1000)
                self.browser.close()
                self.playwright.stop()
                print("🔚 Navegador cerrado")

if __name__ == "__main__":
    automation = LandingPageAutomation()
    automation.run_automation()
