import os
import dbm
import json
from pathlib import Path


DEFAULT_DB_PATH = str(Path.home() / ".user_vars.db")

def get_db_path():
    return os.getenv("CPY_DP_PATH", DEFAULT_DB_PATH)

def _encode_key(key):
    return key.encode()

def _encode_value(value, lst=None):
    return json.dumps({
        "value": value,
        "list": lst or []
    }).encode()

def _decode_value(raw_bytes):
    try:
        obj = json.loads(raw_bytes.decode())
        return obj["value"], obj.get("list", [])
    except Exception:
        return None, []

def save_kv(key: str, value: str, items: list[str] = None):
    """
    Save or update a key with a string value and optional list of strings.
    Overwrites any previous list if items is None or not provided.
    """
    with dbm.open(DB_PATH, 'c') as db:
        db[_encode_key(key)] = _encode_value(value, items)

def load_value(key: str):
    """
    Load the value and associated list for a key.
    Returns (value: str, list: list[str]) or None if not found.
    """
    with dbm.open(DB_PATH, 'c') as db:
        raw = db.get(_encode_key(key))
        if raw:
            return _decode_value(raw)
        return None

def delete_kv(key: str):
    """
    Delete the key and any associated list.
    """
    with dbm.open(DB_PATH, 'w') as db:
        k = _encode_key(key)
        if k in db:
            del db[k]
            return True
        return False

def list_kvs():
    """
    List all key-value pairs and their associated lists.
    Returns a dict[str, tuple[str, list[str]]]
    """
    with dbm.open(DB_PATH, 'c') as db:
        return {
            k.decode(): _decode_value(v)
            for k, v in db.items()
        }
