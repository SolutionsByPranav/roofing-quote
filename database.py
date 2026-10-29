import sqlite3

DB_PATH = "roofing.db"

SHINGLE_PRICES = [
    ("IKO Dynasty", "shingle", "bundle", 4599),
    ("IKO Cambridge", "shingle", "bundle", 3999),
    ("Hip and Ridge", "capping", "bundle", 6999),
    ("Leading Edge", "starter", "bundle", 6999),
]

SHINGLE_COLORS = [
    ("IKO Dynasty", "Granite Black"),
    ("IKO Dynasty", "Shadow Brown"),
    ("IKO Dynasty", "Frostone Grey"),
    ("IKO Dynasty", "Summit Grey"),
    ("IKO Dynasty", "Driftshake"),
    ("IKO Dynasty", "Brownstone"),
    ("IKO Dynasty", "Emerald Green"),
    ("IKO Dynasty", "Monaco Red"),
    ("IKO Dynasty", "Cornerstone"),
    ("IKO Cambridge", "Dual Black"),
    ("IKO Cambridge", "Dual Brown"),
    ("IKO Cambridge", "Dual Grey"),
    ("IKO Cambridge", "Charcoal Grey"),
    ("IKO Cambridge", "Harvard Slate"),
    ("IKO Cambridge", "WeatherWood"),
    ("IKO Cambridge", "Driftwood"),
    ("IKO Cambridge", "Earthstone Cedar"),
]

ACCESSORY_PRICES = [
    ("Synthetic Underlayment", "accessory", "roll", 12999),
    ("Ice & Water Shield", "accessory", "roll", 9499),
    ("Drip Edge", "accessory", "piece", 1299),
    ("Coil Roofing Nails 1-1/4in", "accessory", "box", 5499),
    ("Roofvent", "accessory", "piece", 399)
]

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")  
    return conn

def create_tables(conn):
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS shingles (
            id          INTEGER PRIMARY KEY,
            name        TEXT    NOT NULL UNIQUE,
            category    TEXT    NOT NULL,
            unit        TEXT    NOT NULL,
            price_cents INTEGER NOT NULL
        );

        CREATE TABLE IF NOT EXISTS colors (
            id          INTEGER PRIMARY KEY,
            shingle_id INTEGER NOT NULL,
            color       TEXT    NOT NULL,
            FOREIGN KEY (shingle_id) REFERENCES shingles(id)
        );

        CREATE TABLE IF NOT EXISTS accessories (
            id          INTEGER PRIMARY KEY,
            name        TEXT    NOT NULL,
            category    TEXT    NOT NULL,
            unit        TEXT    NOT NULL,
            price_cents INTEGER NOT NULL
        );
    """)
    conn.commit()

def seed_products(conn):
    """Insert the sample products, but only if the table is empty."""

    #Insert shinlge prices
    if conn.execute("SELECT COUNT(*) FROM shingles").fetchone()[0] == 0:
        conn.executemany("INSERT INTO shingles (name, category, unit, price_cents) VALUES (?, ?, ?, ?)", SHINGLE_PRICES)

    #insert colors of shingles
    if conn.execute("SELECT COUNT(*) FROM colors").fetchone()[0] == 0:
        conn.executemany("INSERT INTO colors (shingle_id, color) SELECT id, ? FROM shingles WHERE name = ?", [(color, name) for name, color in SHINGLE_COLORS])

    #insert accessory prices
    if conn.execute("SELECT COUNT(*) FROM accessories").fetchone()[0] == 0:
        conn.executemany("INSERT INTO accessories (name, category, unit, price_cents) VALUES (?, ?, ?, ?)", ACCESSORY_PRICES)

    conn.commit()

def get_shingles(conn, category=None):
    """Return all shingles, or only those of a specific category if given."""
    if category:
        return conn.execute("SELECT * FROM shingles WHERE category = ?", (category,)).fetchall()
    else:
        return conn.execute("SELECT * FROM shingles").fetchall()

def get_accessories(conn, category=None):
    """Return all accessories, or only those of a specific category if given."""
    if category:
        return conn.execute("SELECT * FROM accessories WHERE category = ?", (category,)).fetchall()
    else:
        return conn.execute("SELECT * FROM accessories").fetchall()

def get_colors(conn, shingle_name=None):
    """Return all colors, or only those for a specific shingle if given."""
    if shingle_name:
        return conn.execute("""SELECT colors.color 
                               FROM colors JOIN shingles 
                               ON colors.shingle_id = shingles.id WHERE shingles.name = ?""", (shingle_name,)).fetchall()
    else:
        return conn.execute("""SELECT colors.id, colors.color, shingles.name AS shingle_name 
                               FROM colors JOIN shingles 
                               ON colors.shingle_id = shingles.id""").fetchall()

if __name__ == "__main__":
    conn = get_connection()
    create_tables(conn)
    seed_products(conn)
    seed_products(conn)   

    assert len(get_shingles(conn)) == 4
    assert len(get_colors(conn)) == 17
    assert len(get_colors(conn, "IKO Dynasty")) == 9
    assert len(get_accessories(conn)) == 5
    print("All tests passed")

    for color in get_colors(conn, "IKO Cambridge"):
        print(color["color"])
    conn.close()