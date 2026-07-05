import sqlite3

DB_PATH = "inventory.db"


class DBM:
    """Lightweight wrapper around the SQLite inventory database."""

    def __init__(self, path=DB_PATH):
        self.conn = sqlite3.connect(path)
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS items(
                id INTEGER PRIMARY KEY,
                name TEXT,
                brand TEXT,
                model TEXT,
                origin TEXT,
                amount INTEGER,
                min_amount INTEGER,
                photo_path TEXT
            )
        """)
        # Migration: add photo_path column if it doesn't exist
        cursor = self.conn.execute("PRAGMA table_info(items)")
        columns = [row[1] for row in cursor]
        if "photo_path" not in columns:
            self.conn.execute("ALTER TABLE items ADD COLUMN photo_path TEXT")
        
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS sales(
                id INTEGER PRIMARY KEY,
                customer TEXT,
                item_name TEXT,
                brand TEXT,
                model TEXT,
                quantity INTEGER,
                sale_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.conn.commit()

    def items(self, search="", origin=None, brand=None, stock_status=None):
        """Fetch items, optionally filtered.

        stock_status: None/"All Stock Levels", "Low", "Out", or "In".
        Thresholds: Out = 0, Low = 0 < x < min, In = x >= min
        """
        clauses = ["(name LIKE ? OR brand LIKE ? OR model LIKE ? OR origin LIKE ?)"]
        q = f"%{search}%"
        params = [q, q, q, q]

        if origin and origin != "All Origins":
            clauses.append("origin = ?")
            params.append(origin)

        if brand and brand != "All Brands":
            clauses.append("brand = ?")
            params.append(brand)

        if stock_status == "Out":
            clauses.append("amount = 0")
        elif stock_status == "Low":
            clauses.append("amount > 0 AND amount < MAX(min_amount, 1)")
        elif stock_status == "In":
            clauses.append("amount >= MAX(min_amount, 1)")

        where = " AND ".join(clauses)
        return self.conn.execute(
            f"SELECT * FROM items WHERE {where} ORDER BY name", params
        ).fetchall()

    def origins(self):
        rows = self.conn.execute(
            "SELECT DISTINCT origin FROM items WHERE origin IS NOT NULL AND origin != '' ORDER BY origin"
        ).fetchall()
        return [r[0] for r in rows]

    def brands(self):
        rows = self.conn.execute(
            "SELECT DISTINCT brand FROM items WHERE brand IS NOT NULL AND brand != '' ORDER BY brand"
        ).fetchall()
        return [r[0] for r in rows]

    def add(self, *values):
        # values should be: name, brand, model, origin, amount, min_amount, [photo_path]
        if len(values) == 6:
            values = (*values, None)  # No photo
        self.conn.execute(
            "INSERT INTO items(name,brand,model,origin,amount,min_amount,photo_path) VALUES(?,?,?,?,?,?,?)",
            values,
        )
        self.conn.commit()

    def update(self, item_id, *values):
        # values should be: name, brand, model, origin, amount, min_amount, [photo_path]
        if len(values) == 6:
            values = (*values, None)  # No photo change
        self.conn.execute(
            "UPDATE items SET name=?,brand=?,model=?,origin=?,amount=?,min_amount=?,photo_path=? WHERE id=?",
            (*values, item_id),
        )
        self.conn.commit()

    def delete(self, item_id):
        self.conn.execute("DELETE FROM items WHERE id=?", (item_id,))
        self.conn.commit()

    def sell(self, item_id, customer, qty):
        if qty <= 0:
            return False, "Quantity must be at least 1"

        row = self.conn.execute(
            "SELECT name,brand,model,amount FROM items WHERE id=?", (item_id,)
        ).fetchone()
        if not row:
            return False, "Item not found"

        name, brand, model, stock = row
        if qty > stock:
            return False, f"Only {stock} in stock"

        self.conn.execute("UPDATE items SET amount=amount-? WHERE id=?", (qty, item_id))
        self.conn.execute(
            """INSERT INTO sales(customer,item_name,brand,model,quantity)
               VALUES(?,?,?,?,?)""",
            (customer, name, brand, model, qty),
        )
        self.conn.commit()
        return True, "Sale completed"

    def sales(self):
        return self.conn.execute(
            """SELECT item_name,brand,model,quantity,sale_time,customer
               FROM sales ORDER BY sale_time DESC"""
        ).fetchall()
