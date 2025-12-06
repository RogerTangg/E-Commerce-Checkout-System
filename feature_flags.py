import json
import os
from functools import wraps
from flask import abort

# Load toggles from the configuration file defined by PM
def load_toggles():
    config_path = os.path.join(os.path.dirname(__file__), 'config', 'toggles.json')
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def is_toggle_enabled(feature_name):
    toggles = load_toggles()
    # Default to False if feature is missing for safety (Secure by Default)
    return toggles.get(feature_name, False)

# Decorator to protect routes based on feature flags
def feature_required(feature_name):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not is_toggle_enabled(feature_name):
                # Return 404 Not Found to hide the feature completely
                abort(404)
            return f(*args, **kwargs)
        return decorated_function
    return decorator