from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QListWidget, QListWidgetItem


class SummaryDialog(QDialog):
    """Compact 'shopping list' style popup, e.g.:
        3x Bus AC
        4x Compressor
    Shows whatever items are currently visible on the results page
    (i.e. respects the active search/filter).
    """

    def __init__(self, items, parent=None):
        super().__init__(parent)
        self.setWindowTitle("📋 Quick Summary")
        self.resize(380, 440)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.addWidget(QLabel(f"<b>📦 {len(items)} item(s) in current view</b>"))

        if not items:
            empty = QLabel("No items to summarize.\nTry adjusting your filters.")
            empty.setObjectName("EmptyState")
            layout.addWidget(empty)
            return

        listw = QListWidget()
        listw.setAlternatingRowColors(True)
        for item in items:
            item_id, name, brand, model, origin, amount, minimum, photo_path = item
            # Format: "3x Bus AC (Denso BA-1, Japan)"
            details = f"{amount}x {name}"
            if brand or model or origin:
                parts = []
                if brand:
                    parts.append(brand)
                if model:
                    parts.append(model)
                if origin:
                    parts.append(origin)
                details += f" ({', '.join(parts)})"
            listw.addItem(QListWidgetItem(details))
        layout.addWidget(listw)
