# utils.py
import json
def safe_str(obj):
    try:
        return json.dumps(obj, default=str)
    except Exception:
        return str(obj)
