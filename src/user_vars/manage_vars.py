import re

def parse_var_definition(s):
    s = s.strip()

    # Case: No parentheses
    if '(' not in s and ')' not in s:
        if re.fullmatch(r'\w+', s):
            return s, None
        else:
            return None

    # Case: One valid set of parentheses at the end
    match = re.fullmatch(r'(\w+)\s*\(([\w\s,]*)\)', s)
    if not match:
        return None

    name = match.group(1)
    param_str = match.group(2)

    # Split and validate each parameter
    params = [p.strip() for p in param_str.split(',') if p.strip()]
    if not params:
        return None

    # Validate each param (must be only alphanum or underscores)
    if not all(re.fullmatch(r'\w+', param) for param in params):
        return None

    return name, params

