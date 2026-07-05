import sys

from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QMenuBar
from PySide6.QtCore import Qt

from database import DBM
from styles import get_style
from widgets.search_page import SearchPage
from widgets.results_page import ResultsPage
from dialogs.settings_dialog import SettingsDialog
from audio_player import AudioPlayer
from app_settings import load_settings


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = DBM()
        self.resize(1400, 800)
        self.setWindowTitle("📦 Inventory Manager")

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.search_page = SearchPage(self.db, on_search=self.show_results)
        self.results_page = ResultsPage(self.db, self)

        self.stack.addWidget(self.search_page)
        self.stack.addWidget(self.results_page)
        
        # Add menu bar with Settings
        self.create_menu_bar()

        self.show_search()
    
    def create_menu_bar(self):
        menubar = QMenuBar(self)
        self.setMenuBar(menubar)
        
        # Settings menu
        settings_action = menubar.addAction("⚙️ Settings")
        settings_action.triggered.connect(self.show_settings)
    
    def show_settings(self):
        dialog = SettingsDialog(controller=self, parent=self)
        dialog.exec()

    def apply_theme(self, dark_mode: bool):
        """Swap the global stylesheet immediately (no restart needed)."""
        app = QApplication.instance()
        if app is not None:
            app.setStyleSheet(get_style(dark_mode))

    def show_search(self):
        self.search_page.refresh_filter_options()
        self.search_page.refresh_stats()
        self.stack.setCurrentWidget(self.search_page)

    def show_results(self, filters):
        self.results_page.load(filters)
        self.stack.setCurrentWidget(self.results_page)


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    settings = load_settings()
    app.setStyleSheet(get_style(settings.get("dark_mode", False)))
    AudioPlayer().set_volume(settings.get("volume", 80))

    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
