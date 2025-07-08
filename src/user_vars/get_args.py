import re

def extract_and_split(s):
    # Find arguments
    match = re.search(r'\(([^()]*)\)$', s)

    if not match: # No args passed
        return None 
    
    # Extract args
    inside = match.group(1)
    parts = [part.strip() for part in inside.split(',')]

    return parts