from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton,
)
from PySide6.QtCore import Qt
from widgets.stat_card import StatCard


class SearchPage(QWidget):
    """Landing screen: a simple, browser-homepage-style search bar with filters.

    Clicking Search (or pressing Enter) calls on_search(filters) with whatever
    was picked, and the caller is responsible for switching to the results view.
    """

    STOCK_OPTIONS = {"All Stock Levels": None, "Low Stock": "Low", "Out of Stock": "Out", "In Stock": "In"}

    def __init__(self, db, on_search):
        super().__init__()
        self.db = db
        self.on_search = on_search

        outer = QVBoxLayout(self)
        outer.addStretch(1)

        title = QLabel("<h1>📦 Inventory Search</h1>")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        outer.addWidget(title)

        subtitle = QLabel("Search your stock by name, brand, model, or origin")
        subtitle.setObjectName("EmptyState")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        outer.addWidget(subtitle)

        outer.addSpacing(10)

        search_row = QHBoxLayout()
        search_row.addStretch(1)
        self.query = QLineEdit()
        self.query.setPlaceholderText("🔍 Search items…")
        self.query.setMinimumWidth(420)
        self.query.returnPressed.connect(self._search)
        search_row.addWidget(self.query)

        search_btn = QPushButton("Search")
        search_btn.setToolTip("Search (or just press Enter)")
        search_btn.clicked.connect(self._search)
        search_row.addWidget(search_btn)
        search_row.addStretch(1)
        outer.addLayout(search_row)

        outer.addSpacing(14)

        filter_row = QHBoxLayout()
        filter_row.addStretch(1)

        self.origin_combo = QComboBox()
        self.origin_combo.setToolTip("Filter by country of origin")
        self.brand_combo = QComboBox()
        self.brand_combo.setToolTip("Filter by brand")
        self.stock_combo = QComboBox()
        self.stock_combo.setToolTip("Filter by stock level")
        self.stock_combo.addItems(list(self.STOCK_OPTIONS.keys()))

        for combo in (self.origin_combo, self.brand_combo, self.stock_combo):
            combo.setMinimumWidth(160)
            filter_row.addWidget(combo)

        filter_row.addStretch(1)
        outer.addLayout(filter_row)

        outer.addSpacing(24)

        stats_row = QHBoxLayout()
        stats_row.addStretch(1)
        self.total_stat = StatCard("📦", 0, "Total Items")
        self.low_stat = StatCard("⚠️", 0, "Low Stock")
        self.out_stat = StatCard("⛔", 0, "Out of Stock")
        self.in_stat = StatCard("✅", 0, "In Stock")
        for stat in (self.total_stat, self.low_stat, self.out_stat, self.in_stat):
            stat.setMaximumWidth(220)
            stats_row.addWidget(stat)
        stats_row.addStretch(1)
        outer.addLayout(stats_row)

        outer.addStretch(2)

        self.refresh_filter_options()
        self.refresh_stats()

    def refresh_stats(self):
        """Re-pull overall stock counts across the whole inventory (no filters)."""
        items = self.db.items()

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

    def refresh_filter_options(self):
        """Re-pull Origin/Brand options from the DB. Call after items change."""
        prev_origin = self.origin_combo.currentText() if self.origin_combo.count() else "All Origins"
        prev_brand = self.brand_combo.currentText() if self.brand_combo.count() else "All Brands"

        self.origin_combo.clear()
        self.origin_combo.addItem("All Origins")
        self.origin_combo.addItems(self.db.origins())
        idx = self.origin_combo.findText(prev_origin)
        self.origin_combo.setCurrentIndex(idx if idx >= 0 else 0)

        self.brand_combo.clear()
        self.brand_combo.addItem("All Brands")
        self.brand_combo.addItems(self.db.brands())
        idx = self.brand_combo.findText(prev_brand)
        self.brand_combo.setCurrentIndex(idx if idx >= 0 else 0)

    def get_filters(self):
        return {
            "search": self.query.text(),
            "origin": self.origin_combo.currentText(),
            "brand": self.brand_combo.currentText(),
            "stock_status": self.STOCK_OPTIONS.get(self.stock_combo.currentText()),
        }

    def _search(self):
        self.on_search(self.get_filters())
