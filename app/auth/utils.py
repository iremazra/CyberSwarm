# app/auth/utils.py
from flask import request, jsonify # MUTLAKA BU OLMALI
import jwt
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash   
from .models import Admin, User


SECRET_KEY = 'your_secret_key'
ALGORITHM = 'HS256'

#Password hashing
def hash_password(password):
    return generate_password_hash(password)

def verify_password(password, hashed_password):
    return check_password_hash(hashed_password, password)


def generate_jwt(user_data):
    payload = {
        'sub':str(user_data['id']),
        'email': user_data['email'],
        'role': user_data['role'],
        'organization_id': str(user_data['organization_id']),
        'exp': datetime.utcnow() + timedelta(days=5) #Token 5 gün geçerli
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token



#RBAC(Role-Based Access Control) dekatörleri
from functools import wraps

def token_Required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            auth_header= request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return {'message': 'Token format is invalid!'}, 401
    
        if not token:
            return {'message': 'Token is missing!'}, 401
        
        try:
            #token'ı çözüp payload'ı alıcaz
            data=jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

            if data['role']=='admin':
                current_user=Admin.query.get(data['sub'])
            else:
                current_user=User.query.get(data['sub'])

            if not current_user:
                return {'message': 'User not found!'}, 401
            
            request.user=data #request objesine user bilgisini ekliyoruz
        
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except Exception:
            return {'message': 'Token is invalid!'}, 401
        return f(*args, **kwargs)
    return decorated

def role_required(roles): # Parametre ismini 'roles' yapalım ki karışıklık olmasın
    # Eğer tek bir rol dizgi (string) olarak geldiyse listeye çeviriyoruz
    if isinstance(roles, str):
        roles = [roles]

    def decorator(f):
        @wraps(f)
        @token_Required # Önce token kontrolü yapılacak
        def decorated(*args, **kwargs):
            # Token decode edildikten sonra request.user içine yerleşmişti
            user_role = request.user.get('role')
            
            # Kullanıcının rolü izin verilen listemizde var mı?
            if user_role not in roles:
                return jsonify({
                    "error": "Access denied",
                    "message": f"Required roles: {roles}. Your role: {user_role}"
                }), 403
                
            return f(*args, **kwargs)
        return decorated
    return decorator

def user_or_node_required(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        from app.nodes.models import Node
        api_key = request.headers.get('X-API-KEY')
        auth_header = request.headers.get('Authorization')

        
        # 1. Senaryo: SENSÖR DOĞRULAMA (API Key)
        if api_key:
            node = Node.query.filter_by(api_key=api_key).first()
            # Production farkı: Sadece anahtara değil, sensörün aktifliğine de bakıyoruz
            if node and node.status == 'active':
                request.node = node # Fonksiyon içinde node bilgilerini kullanabilmek için
                return f(*args, **kwargs)
            return jsonify({"error":"Invalid API key"})
               
        if auth_header:
            try:
                # 'Bearer <token>' formatından sadece token kısmını alıyoruz
                token = auth_header.split(" ")[1]
                # Token'ı gerçek anlamda doğruluyoruz (Production farkı budur!)
                user_data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) 
                if user_data:
                    request.user = user_data
                    return f(*args, **kwargs)
            except Exception:
                return jsonify({"error": "Invalid or expired token"}), 401
            
        return jsonify({"error": "Valid Token or API Key required"}), 401
    return decorated