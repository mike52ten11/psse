import traceback

def error_handler(func):
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return {"success": True, "data": result, "error": None}
        except Exception as e:
            traceback_str = traceback.format_exc()
            
            return {
                "success": False,
                "data": None,
                "error": {
                    "function": func.__name__,
                    "message": str(e),
                    "type": type(e).__name__,
                    "traceback": traceback_str
                }
            }
    return wrapper