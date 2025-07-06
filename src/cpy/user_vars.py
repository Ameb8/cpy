import dbm
from pathlib import Path

DB_PATH = str(Path.home() / ".user_vars.db")

def save_kv(key, value):
    with dbm.open(DB_PATH, 'c') as db: # Save KV pair
        db[key.encode()] = value.encode()
        return True


def load_value(key):
    with dbm.open(DB_PATH, 'c') as db: # Load Value
        value = db.get(key.encode())
        return value.decode() if value else None


def list_kvs():
    with dbm.open(DB_PATH, 'c') as db: # Get dict of KV pairs
        return {k.decode(): v.decode() for k, v in db.items()}


def delete_kv(key):
    with dbm.open(DB_PATH, 'w') as db:
        key_bytes = key.encode() # Get encoded key

        if key_bytes in db: # Delete KV pair
            del db[key_bytes]
            return True
        
        return False # Key not found

