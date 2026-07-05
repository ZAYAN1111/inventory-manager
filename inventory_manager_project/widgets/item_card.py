import os
from PySide6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QProgressBar, QDialog
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt


class PhotoViewerDialog(QDialog):
    """Fullscreen photo viewer for an item."""
    
    def __init__(self, photo_path, item_name, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Photo: {item_name}")
        self.resize(700, 800)
        
        layout = QVBoxLayout(self)
        
        if os.path.exists(photo_path):
            photo_label = QLabel()
            pixmap = QPixmap(photo_path)
            # Scale to fit within 650x720 (leaving room for close button)
            # while maintaining aspect ratio and never exceeding bounds
            from PySide6.QtCore import QSize
            max_size = QSize(650, 720)
            scaled = pixmap.scaledToWidth(650, Qt.SmoothTransformation)
            # If height exceeds max, scale by height instead
            if scaled.height() > 720:
                scaled = pixmap.scaledToHeight(720, Qt.SmoothTransformation)
            photo_label.setPixmap(scaled)
            photo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(photo_label)
        else:
            layout.addWidget(QLabel("Photo not found"))
        
        close_btn = QPushButton("✖ Close")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)


class ItemCard(QFrame):
    """Card showing a single inventory item with edit/sell/delete actions.

    `controller` is the MainWindow -- it's not a Qt parent, just whatever
    object exposes edit_item/sell_item/delete_item.
    """

    def __init__(self, item, controller):
        super().__init__()
        self.setObjectName("Card")
        item_id, name, brand, model, origin, amount, minimum, photo_path = item

        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(6)
        layout.addWidget(QLabel(f"<h2>{name}</h2>"))
        layout.addWidget(QLabel(f"Brand: {brand}"))
        layout.addWidget(QLabel(f"Model: {model}"))
        layout.addWidget(QLabel(f"Origin: {origin}"))
        layout.addWidget(QLabel(f"Stock: {amount} | Min: {minimum}"))

        safe_min = max(minimum, 1)
        if amount == 0:
            color, status = "#e74c3c", "⛔ Out of Stock"
        elif amount < safe_min:
            color, status = "#f39c12", "⚠️ Low Stock"
        else:  # amount >= safe_min
            color, status = "#27ae60", "✅ In Stock"

        bar = QProgressBar()
        pct = min(int((amount / safe_min) * 100), 100)
        bar.setValue(pct)
        bar.setFormat(f"{pct}%")
        bar.setStyleSheet(f"QProgressBar::chunk{{background:{color};border-radius:8px;}}")
        bar.setToolTip(f"{amount} in stock (minimum: {minimum})")
        layout.addWidget(bar)

        badge = QLabel(status)
        badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        badge.setStyleSheet(f"background:{color};color:white;padding:6px;border-radius:8px;font-weight:600;")
        layout.addWidget(badge)

        row = QHBoxLayout()
        row.setSpacing(6)
        for text, tooltip, handler in [
            ("✏️ Edit", "Edit this item's details", lambda: controller.edit_item(item)),
            ("💰 Sell", "Record a sale for this item", lambda: controller.sell_item(item)),
        ]:
            btn = QPushButton(text)
            btn.setToolTip(tooltip)
            btn.clicked.connect(handler)
            row.addWidget(btn)

        # View Image button (only if photo exists)
        if photo_path and os.path.exists(photo_path):
            view_btn = QPushButton("🖼️ View")
            view_btn.setToolTip("View the full-size photo")
            view_btn.clicked.connect(lambda: PhotoViewerDialog(photo_path, name, self).exec())
            row.addWidget(view_btn)

        delete_btn = QPushButton("🗑️")
        delete_btn.setObjectName("DeleteBtn")
        delete_btn.setToolTip(f"Delete {name}")
        delete_btn.clicked.connect(lambda: controller.delete_item(item_id, name))
        row.addWidget(delete_btn)

        layout.addLayout(row)
