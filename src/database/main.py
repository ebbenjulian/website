import mariadb
from dotenv import dotenv_values

def get_connection():
    """Maak verbinding met de database."""
    config = dotenv_values(".env")
    try:
        connectie = mariadb.connect(
            host=config["DB_HOST"],
            port=int(config["DB_PORT"]),
            user=config["DB_USER"],
            password=config["DB_PASSWORD"],
            database=config["DB_DATABASE_NAME"],
            autocommit=True,
            ssl_verify_cert=True
        )
        db = connectie.cursor(dictionary=True)
        return db
    except mariadb.Error as e:
        print(f"Fout bij het maken van de databaseverbinding: {e}")
        return None


def _close(db):
    """Sluit cursor en verbinding netjes."""
    try:
        if db:
            conn = db.connection
            db.close()
            conn.close()
    except Exception as e:
        print(f"Fout bij sluiten van verbinding: {e}")


def fetch_one(query, params=None):
    """
    Voer query uit en geef een tuple terug:
    (success, data_or_none, error_message_or_none)
    """
    db = get_connection()
    if not db:
        return False, None, "Could not create database connection"

    try:
        db.execute(query, params or ())
        result = db.fetchone()
        return True, result, None
    except mariadb.Error as e:
        print(f"Query error in fetch_one: {e}")
        print(f"Query: {query}")
        print(f"Params: {params}")
        return False, None, str(e)
    finally:
        _close(db)

def fetch_all(query, params=None):
    """
    Voer query uit en geef een tuple terug:
    (success, data_or_none, error_message_or_none)
    """
    db = get_connection()
    if not db:
        return False, None, "Could not create database connection"

    try:
        db.execute(query, params or ())
        result = db.fetchall()
        return True, result, None
    except mariadb.Error as e:
        print(f"Query error in fetch_one: {e}")
        print(f"Query: {query}")
        print(f"Params: {params}")
        return False, None, str(e)
    finally:
        _close(db)

def execute(query, params=None):
    """
    Voer query uit en geef terug:
    (success, error_message_or_none)
    """
    db = get_connection()
    if not db:
        return False, "Could not create database connection"

    try:
        db.execute(query, params or ())
        return True, None
    except mariadb.Error as e:
        print(f"Query error in execute: {e}")
        print(f"Query: {query}")
        print(f"Params: {params}")
        return False, str(e)
    finally:
        _close(db)
