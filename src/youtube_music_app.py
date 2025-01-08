import sys
import os
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QSystemTrayIcon, QMenu
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEngineProfile, QWebEnginePage
from PySide6.QtGui import QIcon, QWindow

class CustomWebEnginePage(QWebEnginePage):
    def __init__(self, profile, parent=None):
        super().__init__(profile, parent)

class YouTubeMusicApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_window()
        self.setup_browser()
        self.setup_tray()
        self.setup_taskbar_icon()

    def setup_window(self):
        """Configure la fenêtre principale"""
        self.setWindowTitle("YouTube Music")
        self.setGeometry(100, 100, 1024, 768)
        
        # Ajout du logo partout où c'est possible
        icon_path = self.get_icon_path()
        if os.path.exists(icon_path):
            self.app_icon = QIcon(icon_path)
            self.setWindowIcon(self.app_icon)
            QApplication.setWindowIcon(self.app_icon)  # Icône globale pour l'application

    def setup_taskbar_icon(self):
        """Assure que l'icône est visible dans la barre des tâches"""
        if hasattr(self, 'app_icon'):
            # Force l'icône dans la barre des tâches Windows
            if hasattr(self.windowHandle(), 'setIcon'):
                self.windowHandle().setIcon(self.app_icon)
            # Mettre à jour l'icône pour toutes les fenêtres
            for window in QApplication.allWindows():
                if isinstance(window, QWindow):
                    window.setIcon(self.app_icon)

    def get_icon_path(self):
        """Obtient le chemin de l'icône en fonction du contexte (développement ou production)"""
        if getattr(sys, 'frozen', False):
            # Si on est dans l'exe (PyInstaller)
            return os.path.join(sys._MEIPASS, 'assets', 'icon.ico')
        else:
            # Si on est en développement
            return os.path.join(os.path.dirname(__file__), '..', 'assets', 'icon.ico')

    def setup_browser(self):
        """Configure le navigateur et la gestion des cookies"""
        self.browser = QWebEngineView(self)
        
        # Configuration du profil persistant
        profile_path = os.path.join(os.path.expanduser('~'), '.youtube-music-app')
        self.profile = QWebEngineProfile('YouTube Music', self)
        self.profile.setPersistentStoragePath(profile_path)
        self.profile.setPersistentCookiesPolicy(QWebEngineProfile.ForcePersistentCookies)
        
        # Création d'une page personnalisée avec le profil
        custom_page = CustomWebEnginePage(self.profile, self.browser)
        self.browser.setPage(custom_page)
        
        # Configuration des callbacks
        custom_page.loadFinished.connect(self.on_load_finished)
        
        # Chargement de YouTube Music
        self.browser.setUrl("https://music.youtube.com")
        self.setCentralWidget(self.browser)

    def setup_tray(self):
        """Configure l'icône dans la barre des tâches"""
        self.tray_icon = QSystemTrayIcon(self)
        icon_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'icon.ico')
        if os.path.exists(icon_path):
            self.tray_icon.setIcon(QIcon(icon_path))
        
        # Menu contextuel
        tray_menu = QMenu()
        show_action = tray_menu.addAction("Afficher/Cacher")
        quit_action = tray_menu.addAction("Quitter")
        
        show_action.triggered.connect(self.toggle_window)
        quit_action.triggered.connect(self.quit_application)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

    def toggle_window(self):
        """Affiche ou cache la fenêtre principale"""
        if self.isVisible():
            self.hide()
        else:
            self.show()
            self.activateWindow()

    def closeEvent(self, event):
        """Gère la fermeture de la fenêtre"""
        event.ignore()
        self.hide()
        self.tray_icon.showMessage(
            "YouTube Music",
            "L'application continue de fonctionner en arrière-plan",
            QSystemTrayIcon.Information,
            2000
        )

    def quit_application(self):
        """Quitte complètement l'application"""
        QApplication.quit()

    def on_load_finished(self, success):
        """Callback appelé quand la page est chargée"""
        if success:
            print("YouTube Music chargé avec succès!")
        else:
            print("Erreur lors du chargement de YouTube Music")

def main():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)  # Empêche la fermeture lors de la minimisation
    window = YouTubeMusicApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
