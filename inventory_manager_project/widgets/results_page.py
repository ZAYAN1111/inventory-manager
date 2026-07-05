from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QScrollArea,
    QGridLayout, QLabel, QMessageBox,
)
from PySide6.QtCore import Qt
from audio_player import AudioPlayer
from dialogs.item_dialog import ItemDialog
from dialogs.sell_dialog import SellDialog
from dialogs.sales_log import SalesLog
from dialogs.stock_log import StockLog
from dialogs.summary_dialog import SummaryDialog
from widgets.item_card import ItemCard
from widgets.stat_card import StatCard

DEFAULT_FILTERS = {"search": "", "origin": "All Origins", "brand": "All Brands", "stock_status": None}


class ResultsPage(QWidget):
    """The 'boxes' view -- stat tiles + filtered item grid, reached after Search.

    `controller` is the MainWindow: used to get back to the search screen and
    to keep its Origin/Brand dropdowns in sync when items are added/edited/deleted.
    """

    def __init__(self, db, controller):
        super().__init__()
        self.db = db
        self.controller = controller
        self.filters = dict(DEFAULT_FILTERS)
        self.last_problem_count = 0  # Track if we already played audio for these results

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(12)

        top_bar = QHBoxLayout()
        back_btn = QPushButton("← New Search")
        back_btn.setToolTip("Return to the search screen and change filters")
        back_btn.clicked.connect(self.controller.show_search)
        top_bar.addWidget(back_btn)

        self.filter_summary = QLabel()
        top_bar.addWidget(self.filter_summary)
        top_bar.addStretch(1)

        reset_btn = QPushButton("♻️ Reset Filters")
        reset_btn.setToolTip("Clear all filters and show every item")
        reset_btn.clicked.connect(self.reset_filters)
        top_bar.addWidget(reset_btn)
        main_layout.addLayout(top_bar)

        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(12)
        self.total_stat = StatCard("📦", 0, "Total Items")
        self.low_stat = StatCard("⚠️", 0, "Low Stock")
        self.out_stat = StatCard("⛔", 0, "Out of Stock")
        self.in_stat = StatCard("✅", 0, "In Stock")
        for stat in (self.total_stat, self.low_stat, self.out_stat, self.in_stat):
            stats_layout.addWidget(stat)
        main_layout.addLayout(stats_layout)

        action_row = QHBoxLayout()
        action_row.setSpacing(8)
        self.refine = QLineEdit()
        self.refine.setPlaceholderText("🔍 Refine within these results…")
        self.refine.textChanged.connect(self._refine_changed)
        action_row.addWidget(self.refine)

        add_btn = QPushButton("➕ Add")
        add_btn.setToolTip("Add a new item to inventory")
        add_btn.clicked.connect(self.add_item)
        action_row.addWidget(add_btn)

        summary_btn = QPushButton("📋 Quick Summary")
        summary_btn.setToolTip("See a compact list of what's currently shown")
        summary_btn.clicked.connect(self.show_summary)
        action_row.addWidget(summary_btn)

        log_btn = QPushButton("🧾 Sales Log")
        log_btn.setToolTip("View, filter, and export sales history")
        log_btn.clicked.connect(lambda: SalesLog(self.db, self).exec())
        action_row.addWidget(log_btn)
        
        stock_btn = QPushButton("📊 Stock Log")
        stock_btn.setToolTip("View and export stock levels for the items shown")
        stock_btn.clicked.connect(lambda: StockLog(self.current_items(), self).exec())
        action_row.addWidget(stock_btn)
        main_layout.addLayout(action_row)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.cards_container = QWidget()
        self.grid = QGridLayout(self.cards_container)
        self.scroll.setWidget(self.cards_container)
        main_layout.addWidget(self.scroll)

    # --- entering / leaving this page -------------------------------------

    def load(self, filters):
        """Called by MainWindow right after the user hits Search."""
        self.filters = dict(filters)
        self.refine.blockSignals(True)
        self.refine.setText(self.filters.get("search", ""))
        self.refine.blockSignals(False)
        self._update_filter_summary()
        self.refresh()

    def reset_filters(self):
        self.filters = dict(DEFAULT_FILTERS)
        self.refine.blockSignals(True)
        self.refine.setText("")
        self.refine.blockSignals(False)
        self._update_filter_summary()
        self.refresh()

    def _refine_changed(self, text):
        self.filters["search"] = text
        self.refresh()

    def _update_filter_summary(self):
        parts = []
        if self.filters.get("origin") and self.filters["origin"] != "All Origins":
            parts.append(f"Origin: {self.filters['origin']}")
        if self.filters.get("brand") and self.filters["brand"] != "All Brands":
            parts.append(f"Brand: {self.filters['brand']}")
        if self.filters.get("stock_status"):
            parts.append(f"Status: {self.filters['stock_status']} Stock")
        self.filter_summary.setText(" · ".join(parts) if parts else "Showing all items")

    # --- data + grid --------------------------------------------------------

    def current_items(self):
        return self.db.items(
            search=self.filters.get("search", ""),
            origin=self.filters.get("origin"),
            brand=self.filters.get("brand"),
            stock_status=self.filters.get("stock_status"),
        )

    def refresh(self):
        while self.grid.count():
            widget = self.grid.takeAt(0).widget()
            if widget:
                widget.deleteLater()

        items = self.current_items()

        total = len(items)
        low = out = in_stock = 0
        for item in items:
            stock, minimum = item[5], max(item[6], 1)
            if stock == 0:
                out += 1
            elif stock < minimum:
                low += 1
            else:  # stock >= minimum
                in_stock += 1

        self.total_stat.set_value(total)
        self.low_stat.set_value(low)
        self.out_stat.set_value(out)
        self.in_stat.set_value(in_stock)

        for i, item in enumerate(items):
            self.grid.addWidget(ItemCard(item, self), i // 4, i % 4)

        if total == 0:
            empty_label = QLabel("🔍  No items match your search.\nTry adjusting or resetting your filters.")
            empty_label.setObjectName("EmptyState")
            empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.grid.addWidget(empty_label, 0, 0, 1, 4)
        
        # Play alert only if the number of problematic items changed
        # (not on every keystroke, only when results actually differ)
        problem_count = low + out
        if problem_count > 0 and problem_count != self.last_problem_count:
            print(f"[Results] Found {problem_count} problematic items, triggering audio alert")
            audio = AudioPlayer()
            audio.play_low_stock_alert()
        self.last_problem_count = problem_count

    def show_summary(self):
        SummaryDialog(self.current_items(), self).exec()

    # --- item actions (ItemCard calls these via `controller`) --------------

    def add_item(self):
        dialog = ItemDialog(self)
        if dialog.exec():
            self.db.add(*dialog.values())
            self.controller.search_page.refresh_filter_options()
            self.refresh()

    def edit_item(self, item):
        dialog = ItemDialog(self, item)
        if dialog.exec():
            self.db.update(item[0], *dialog.values())
            self.controller.search_page.refresh_filter_options()
            self.refresh()

    def sell_item(self, item):
        dialog = SellDialog(self, max_qty=item[5])
        if dialog.exec():
            ok, msg = self.db.sell(item[0], dialog.customer.text(), dialog.qty.value())
            if ok:
                QMessageBox.information(self, "Sale", msg)
            else:
                QMessageBox.warning(self, "Error", msg)
            self.refresh()

    def delete_item(self, item_id, item_name=""):
        reply = QMessageBox.question(
            self, "Delete Item",
            f"Delete '{item_name}'? This cannot be undone." if item_name else "Delete this item?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            self.db.delete(item_id)
            self.controller.search_page.refresh_filter_options()
            self.refresh()
