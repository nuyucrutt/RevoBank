from flask import request, jsonify, current_app
from functools import wraps
import jwt
from datetime import datetime, timedelta
from src.models import Pengguna

def authenticate_user():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return None
    
    token = auth_header.split(' ')[1]
    try:
        payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        return Pengguna.query.get(payload['pengguna_id'])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def jwt_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        user = authenticate_user()
        if not user:
            return jsonify({"message": "Autentikasi diperlukan"}), 401
        return f(*args, **kwargs)
    return decorated

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not authenticate_user():
            return jsonify({"message": "Autentikasi diperlukan"}), 401
        return f(*args, **kwargs)
    return decorated
