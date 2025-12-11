import sqlite3

DB_NAME = "cynophile.db"

def get_connection():
    """
    Ouvre une connexion vers la base SQLite.
    """
    conn = sqlite3.connect(DB_NAME)
    return conn

def init_db():
    """
    Crée les tables si elles n'existent pas encore.
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Table des entreprises cynophiles
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS entreprises (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT,
        adresse TEXT,
        departement TEXT,
        place_id TEXT UNIQUE
    )
    """)

    # Table des avis Google (on l'utilisera plus tard)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS avis (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        place_id TEXT,
        auteur TEXT,
        note INTEGER,
        texte TEXT,
        date TEXT
    )
    """)

    # Table des scores de risque par entreprise
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS risques (
        place_id TEXT,
        score INTEGER,
        niveau TEXT
    )
    """)

    conn.commit()
    conn.close()
