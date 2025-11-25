# Configuración global para automatización de landing page

# URL principal
BASE_URL = "https://www.xtrim.com.ec/"

# Tiempos de espera (en milisegundos para Playwright)
WAIT_TIME_SHORT = 2000
WAIT_TIME_MEDIUM = 5000
WAIT_TIME_LONG = 10000

# Datos del formulario "Te llamamos"
FORM_DATA = {
    "nombres": "Juan Pérez",
    "cedula": "1234567890",
    "celular": "0987654321",
    "correo": "test@example.com"
}

# Configuración de capturas
SCREENSHOTS_FOLDER = "screenshots"
SCREENSHOT_PAGAR_SERVICIOS = "pagar_servicios_success.png"
SCREENSHOT_TE_LLAMAMOS = "te_llamamos_success.png"

# Selectores para Playwright
SELECTORS = {
    "banner_close": "button.close, .close, [aria-label='close'], [aria-label='cerrar']",
    "pagar_servicio": "#menu-main-menu a[title='Pagar Servicio']",
    "te_llamamos": "#menu-main-menu a[title='Te llamamos']",
    "form_nombres": "input[name='name'], input[placeholder*='nombre'], input[placeholder*='Nombre']",
    "form_cedula": "input[name='cedula'], input[placeholder*='cedula'], input[placeholder*='Cédula']",
    "form_celular": "input[name='phone'], input[placeholder*='celular'], input[placeholder*='teléfono']",
    "form_correo": "input[name='email'], input[type='email'], input[placeholder*='correo']",
    "checkbox_politica": "input[type='checkbox']",
    "btn_enviar": "button[type='submit'], input[type='submit'], text=enviar",
    "mensaje_gracias": "text=Gracias por contactarnos",
    "btn_regresar": "text=Regresar a inicio"
}