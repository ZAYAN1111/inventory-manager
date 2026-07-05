from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel
from PySide6.QtCore import Qt


class StatCard(QFrame):
    """Small dashboard tile showing one inventory statistic (e.g. Low Stock count).

    Reuses the QFrame#Card styling from styles.py so it matches the item cards.
    Call set_value() to update the number after a refresh.
    """

    def __init__(self, icon, value, caption):
        super().__init__()
        self.setObjectName("Card")
        self.icon = icon

        layout = QVBoxLayout(self)
        self.value_lbl = QLabel()
        self.value_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.value_lbl.setStyleSheet("font-size:28px;font-weight:bold;")

        caption_lbl = QLabel(caption)
        caption_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(self.value_lbl)
        layout.addWidget(caption_lbl)

        self.set_value(value)

    def set_value(self, value):
        self.value_lbl.setText(f"{self.icon} {value}")
