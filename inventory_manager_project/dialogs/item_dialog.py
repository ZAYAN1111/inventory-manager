import os
import shutil
from pathlib import Path
from PySide6.QtWidgets import (
    QDialog, QFormLayout, QLineEdit, QSpinBox, QDialogButtonBox, QMessageBox,
    QHBoxLayout, QPushButton, QLabel,
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt


PHOTOS_DIR = Path("photos")
PHOTOS_DIR.mkdir(exist_ok=True)


class ItemDialog(QDialog):
    """Add or edit a single inventory item, with optional photo."""

    def __init__(self, parent=None, item=None):
        super().__init__(parent)
        self.setWindowTitle("✏️ Edit Item" if item else "➕ Add Item")
        self.resize(420, 380)
        self.photo_path = None

        layout = QFormLayout(self)
        self.name = QLineEdit()
        self.brand = QLineEdit()
        self.model = QLineEdit()
        self.origin = QLineEdit()
        self.amount = QSpinBox()
        self.amount.setMaximum(999999)
        self.minimum = QSpinBox()
        self.minimum.setMaximum(999999)

        if item:
            _, name, brand, model, origin, amount, minimum, photo_path = item
            self.name.setText(name)
            self.brand.setText(brand or "")
            self.model.setText(model or "")
            self.origin.setText(origin or "")
            self.amount.setValue(amount)
            self.minimum.setValue(minimum)
            self.photo_path = photo_path

        for label, widget in [
            ("Name", self.name), ("Brand", self.brand), ("Model", self.model),
            ("Origin", self.origin), ("Stock", self.amount), ("Minimum", self.minimum),
        ]:
            layout.addRow(label, widget)

        # Photo section
        photo_row = QHBoxLayout()
        self.photo_label = QLabel("No photo" if not self.photo_path else "Photo selected")
        self.photo_label.setObjectName("EmptyState")
        photo_row.addWidget(self.photo_label)
        
        pick_btn = QPushButton("🖼️ Pick Photo")
        pick_btn.setToolTip("Upload a photo for this item")
        pick_btn.clicked.connect(self._pick_photo)
        photo_row.addWidget(pick_btn)
        
        if self.photo_path and os.path.exists(self.photo_path):
            remove_btn = QPushButton("🗑️ Remove Photo")
            remove_btn.setObjectName("DeleteBtn")
            remove_btn.clicked.connect(self._remove_photo)
            photo_row.addWidget(remove_btn)

        layout.addRow("Photo", photo_row)

        box = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        box.accepted.connect(self._on_save)
        box.rejected.connect(self.reject)
        layout.addWidget(box)

    def _pick_photo(self):
        from PySide6.QtWidgets import QFileDialog
        path, _ = QFileDialog.getOpenFileName(
            self, "Pick Item Photo", "", "Images (*.png *.jpg *.jpeg *.bmp *.gif)"
        )
        if path:
            # Copy to photos folder
            filename = f"item_{id(self)}_{Path(path).name}"
            dest = PHOTOS_DIR / filename
            shutil.copy(path, dest)
            self.photo_path = str(dest)
            self.photo_label.setText(f"✓ {Path(path).name}")

    def _remove_photo(self):
        if self.photo_path and os.path.exists(self.photo_path):
            try:
                os.remove(self.photo_path)
            except Exception:
                pass
        self.photo_path = None
        self.photo_label.setText("No photo")

    def _on_save(self):
        if not self.name.text().strip():
            QMessageBox.warning(self, "Missing Name", "Please enter an item name.")
            return
        self.accept()

    def values(self):
        return (
            self.name.text().strip(), self.brand.text().strip(),
            self.model.text().strip(), self.origin.text().strip(),
            self.amount.value(), self.minimum.value(),
            self.photo_path,
        )
