import base64
import json
import time
from functools import wraps
import traceback
from rest_framework.response import Response

resp_headers = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type"
}

# Generate token
def jwt_encode_token(user_name, time_out=24 * 60 * 60):
    payload = {
        'user_name': user_name,
        'iat': time.time(),
        'exp': time.time() + time_out
    }
    token = base64.b64encode(json.dumps(payload).encode())
    return token

# Parse tokens
def jwt_decode_token(token):
    payload = json.loads(base64.b64decode(token).decode())
    return payload

# Decorator to verify token required in http header
def token_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            # check token
            request = args[1]
            token = request.headers.get('Authentication', None)
            print(token)
            payload = jwt_decode_token(token)
        except Exception:   
            traceback.print_exc() 
            return Response(status=403, data={'code': 100,'errmsg':'token invalid !',}, headers=resp_headers)
        user_name = payload.get('user_name')
        exp = payload.get('exp')
        now = time.time()
        # token expire or not
        if exp < now:
            return Response(status=403, data={'code':100,'errmsg':'token expired !',}, headers=resp_headers)
        return func(*args, **kwargs)
    return wrapper