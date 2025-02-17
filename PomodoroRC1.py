import time
import threading
import sys
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QIcon
from plyer import notification  # ✅ Notificaciones sin errores en Windows

# Duraciones de los temporizadores
COLOR_TO_SECONDS = {
    "30s": 30,
    "1m": 60,
    "2m": 120,
    "3m": 180,
    "5m": 300,
    "10m": 600
}

def show_notification(title, msg, duration=5):
    """Muestra una notificación en Windows usando plyer."""
    notification.notify(
        title=title,
        message=msg,
        timeout=duration
    )

def start_timer(label):
    """Inicia un temporizador en un hilo aparte y notifica al finalizar."""
    seconds = COLOR_TO_SECONDS.get(label, 0)
    if seconds == 0:
        print(f"❌ Error: Tiempo no encontrado para {label}")
        return 0  # Evita errores

    print(f"✅ Temporizador seleccionado: {label} ({seconds} segundos)")
    show_notification("⏳ Temporizador iniciado", f"Has seleccionado {label}.")

    def countdown():
        time.sleep(seconds)
        print(f"✅ Temporizador finalizado: {label}")
        show_notification("⏳ Temporizador finalizado", f"El temporizador de {label} ha terminado.")

    threading.Thread(target=countdown, daemon=True).start()
    
    return 0  # 🔹 Importante: Evita errores en Windows

def main():
    app = QApplication(sys.argv)

    # Crea el icono principal de la bandeja
    tray_icon = QSystemTrayIcon(QIcon("pomodoro.ico"), app)
    
    # Crea el menú
    menu = QMenu()

    # Lista de temporizadores con su respectivo icono
    timers = [
        ("30s", "celeste.png"),   # Celeste
        ("1m", "azul.png"),       # Azul
        ("2m", "amarillo.png"),   # Amarillo
        ("3m", "verde.png"),      # Verde
        ("5m", "naranja.png"),    # Naranja
        ("10m", "rojo.png")       # Rojo
    ]
    
    for label, icon_file in timers:
        action = QAction(QIcon(icon_file), label, menu)
        
        # 🔹 Definir callback para cada botón
        def timer_callback(checked=False, l=label):
            start_timer(l)
            return 0  # Evita el error en Windows

        action.triggered.connect(timer_callback)
        menu.addAction(action)
    
    # Agregar opción para salir
    exit_action = QAction("Salir", menu)
    exit_action.triggered.connect(app.quit)
    menu.addAction(exit_action)
    
    tray_icon.setContextMenu(menu)
    tray_icon.show()
    
    print("✅ Aplicación iniciada correctamente. Icono en la bandeja del sistema.")
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
