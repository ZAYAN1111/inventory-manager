from PySide6.QtWidgets import QDialog, QFormLayout, QLineEdit, QSpinBox, QDialogButtonBox, QLabel


class SellDialog(QDialog):
    """Collect a customer name and quantity for a sale.

    max_qty, if given, caps the spinner at the item's current stock so the
    user can't even attempt to oversell -- previously this was only caught
    after hitting Save, via a popup error.
    """

    def __init__(self, parent=None, max_qty=None):
        super().__init__(parent)
        self.setWindowTitle("💰 Sell Item")

        layout = QFormLayout(self)
        self.customer = QLineEdit()
        self.customer.setPlaceholderText("Customer name")
        self.qty = QSpinBox()
        self.qty.setMinimum(1)
        self.qty.setMaximum(max_qty if max_qty else 999999)

        layout.addRow("Customer", self.customer)
        layout.addRow("Qty", self.qty)
        if max_qty is not None:
            stock_note = QLabel(f"📦 {max_qty} in stock")
            stock_note.setObjectName("EmptyState")
            layout.addRow(stock_note)

        box = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        box.accepted.connect(self.accept)
        box.rejected.connect(self.reject)
        layout.addWidget(box)
