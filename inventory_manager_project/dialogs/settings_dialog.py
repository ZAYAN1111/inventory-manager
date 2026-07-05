from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QSlider, QPushButton, QCheckBox,
)
from PySide6.QtCore import Qt
from audio_player import AudioPlayer
from app_settings import load_settings, save_settings


class SettingsDialog(QDialog):
    """Settings popup for audio volume, dark mode, and other preferences.

    `controller` is the MainWindow -- used to apply the theme live so the
    person sees the change immediately instead of needing a restart.
    """

    def __init__(self, controller=None, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.settings = load_settings()
        self.setWindowTitle("⚙️ Settings")
        self.resize(420, 240)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)
        layout.addWidget(QLabel("<b>🔊 Audio Alert Settings</b>"))

        # Volume control
        volume_row = QHBoxLayout()
        volume_row.addWidget(QLabel("Alert Volume:"))

        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setMinimum(0)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setValue(self.settings.get("volume", 80))
        self.volume_slider.sliderMoved.connect(self._update_volume_label)
        volume_row.addWidget(self.volume_slider)

        self.volume_label = QLabel(f"{self.settings.get('volume', 80)}%")
        self.volume_label.setMinimumWidth(40)
        volume_row.addWidget(self.volume_label)

        layout.addLayout(volume_row)

        layout.addWidget(QLabel("<b>🎨 Appearance</b>"))

        self.dark_mode_checkbox = QCheckBox("Dark Mode")
        self.dark_mode_checkbox.setToolTip("Switch between light and dark theme")
        self.dark_mode_checkbox.setChecked(self.settings.get("dark_mode", False))
        self.dark_mode_checkbox.toggled.connect(self._toggle_dark_mode)
        layout.addWidget(self.dark_mode_checkbox)

        layout.addStretch()

        # Close button
        close_btn = QPushButton("✖ Close")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)

    def _update_volume_label(self, value):
        self.volume_label.setText(f"{value}%")
        AudioPlayer().set_volume(value)
        self.settings["volume"] = value
        save_settings(self.settings)

    def _toggle_dark_mode(self, checked):
        self.settings["dark_mode"] = checked
        save_settings(self.settings)
        if self.controller is not None:
            self.controller.apply_theme(checked)

    def get_volume(self):
        return self.volume_slider.value()
