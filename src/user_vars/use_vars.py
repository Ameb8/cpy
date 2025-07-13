import re
from .repository import load_value
from .manage_vars import (
    set_var,
    get_var,
    delete_var,
    list_vars,
    get_args
)

def handle_var_args(cl_args):
    if cl_args.delete:
        delete_var(cl_args.delete[0])

    if cl_args.set:
        set_var(cl_args.set[0], cl_args.set[1])

    if cl_args.get:
        get_var(cl_args.get[0])

    if cl_args.list:
        list_vars()


def use_var(var_cmd):
    key, args = get_args(var_cmd) # Extract variable name and args

    if not key: # Invalid name/arg format
        return None, f"Error: '{var_cmd}' is not valid variable name"

    val, params = load_value(key) # Retrieve value and params

    if not val: # Variable not found
        return None, f"Error: variable with name '{key}' not found"

    if args and params and len(params) != len(args): # Incorrect number of args
        return None, f"Error: incorrect number of arguments. Required arguments: {', '.join(params)}"

    if bool(args) != bool(params) and bool(args): # Args passed that var doesnt use
        return None, f"Error: variable '{key}' does not take any arguments"

    if bool(args) != bool(params) and bool(params): # Args passed that var doesnt use
        return None, f"Error: variable '{key}' requires the following arguments: {', '.join('\'' + param + '\''  for param in params)}"

    # Replace params with arguments
    if params and args:
        for param, arg in zip(params, args):
            val = val.replace(f"<<{param}>>", arg)

    return val, None



