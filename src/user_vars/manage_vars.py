import re
from .repository import save_kv, load_value, list_kvs, delete_kv

def var_str(key, val, params=None):
    return f"{key}({", ".join(params)}):\t{val}"

def get_args(s):
    s = s.strip()

    # No arguments
    if '(' not in s and ')' not in s:
        if re.fullmatch(r'\w+', s):
            return s, None
        else:
            return None, None

    # Arguments passed
    match = re.fullmatch(r'(\w+)\s*\(([\w\s,]*)\)', s)
    if not match:
        return None, None

    name = match.group(1)
    param_str = match.group(2)

    # Split and validate each parameter
    params = [p.strip() for p in param_str.split(',') if p.strip()]

    if not params:
        return None, None

    return name, params

def parse_var_definition(key_str):
    key, params = get_args(key_str)

    # Validate each param (must be only alphanum or underscores)
    if not all(re.fullmatch(r'\w+', param) for param in params):
        return None, None

    return key, params

def set_var(key_str, val):
    key, params = parse_var_definition(key_str) # Parse arguments

    if not key: # Validate key syntax
        print(f"'{key_str}' is not a valid key. Keys must contain only letters, digits, and underscores")

    save_kv(key, val, params) # Save variable

def get_var(key):
    val, params = load_value(key)

    if not val:  # Key not found
        print(f"No variable defined for Key {key}")
    else:  # Display Key-Value pair
        print(var_str(key, val, params))

def list_vars():
    defined_vars = list_kvs() # Get variables

    for key, val in defined_vars.items(): # Print all variables
        print(var_str(key, val[0], val[1]))

def delete_var(key):
    if delete_kv(key):
        print(f"variable '{key}' successfully deleted")
    else:
        print(f"Could not delete variable '{key}' as it has not been defined")
