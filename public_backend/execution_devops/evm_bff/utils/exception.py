from functools import wraps
import traceback
from rest_framework.response import Response

resp_headers = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type"
}

# Decorator to catch unexpected exception of view
def exception_catcher(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:   
            traceback.print_exc() 
            return Response(status=500, data={'code': 100,'errmsg': str(e)}, headers=resp_headers)
    return wrapper
