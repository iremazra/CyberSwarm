# app/auth/routes.py
from datetime import datetime
from app.auth.utils import token_Required
from flask import Blueprint,request, jsonify
from marshmallow import ValidationError
from . import auth_bp
from .models import Organization,User, Admin
from .service import delete_organization_by_Id, register_user, login_user, create_organization, update_user, register_admin, get_all_organizations,delete_user
from .schemas import RegisterSchema, LoginSchema, UpdateProfileSchema, AdminRegisterSchema
from .utils import role_required, token_Required

@auth_bp.route('/login', methods=['POST'])
def login():
    #Authentication and return JWT

    try:
        raw_data=request.get_json()
        validated_data=LoginSchema().load(raw_data)
    
        result,status_code=login_user(validated_data)
        return jsonify(result), status_code
    except ValidationError as ve:
        return jsonify({"error": ve.messages}), 400 

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        raw_data=request.get_json()
        validated_data=RegisterSchema().load(raw_data)

        #Doğrulanmış veriri iş mantığına (Service) gönderir.
        #Not: Kayıt sırasında "organization_name" da gönderilmeli
        result,status_code=register_user(validated_data)
        return jsonify(result), status_code
    except ValidationError as ve: #Şema doğrulama hatası
        return jsonify({"error": ve.messages}), 400
    

@auth_bp.route('/create_admin', methods=['POST']) #Admin sadece development aşamasında oluşturuluyor.
def create_admin():
    try:
        raw_data=request.get_json()
        validated_data=AdminRegisterSchema().load(raw_data)
        #Doğrulama basit olduğu için şema kullanılmadı
        result,status_code=register_admin(validated_data)
        return jsonify(result), status_code
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 401


@auth_bp.route('/organization', methods=['POST'])
@token_Required
def organization():
    try:
        raw_data=request.get_json()
        #Doğrulama basit olduğu için şema kullanılmadı
        result,status_code=create_organization(raw_data)
        return jsonify(result), status_code
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 401

@auth_bp.route('/get_all_organizations', methods=['GET'])
@token_Required
@role_required('admin')
def get_organizations():
    result,status_code=get_all_organizations()
    return jsonify(result), status_code

@auth_bp.route('/profile', methods=['GET'])
@token_Required
def get_profile():
    from .models import User, Admin  # Model isimlerine göre düzenle
    
    user_id = request.user.get('sub')
    user_role = request.user.get('role')

    # Veritabanından taze veriyi çekiyoruz
    if user_role == 'admin':
        user_obj = Admin.query.get(user_id)
    else:
        user_obj = User.query.get(user_id)

    if not user_obj:
        return jsonify({"error": "User not found"}), 404

    # Estetik ve detaylı bir response yapısı
    return jsonify({
        "status": "success",
        "timestamp": datetime.utcnow().isoformat(),
        "user_info": {
            "id": str(user_obj.id),
            "full_name": user_obj.name,
            "email": user_obj.email,
            "role": user_obj.role.upper(),
            "account_status": "ACTIVE",
            "member_since": user_obj.created_at.strftime("%d %B %Y"),
            "security": {
                "password_type": "BCRYPT_HASHED", # Şifre yerine güvenlik tipini belirtmek daha profesyoneldir
                "last_login_token_exp": datetime.fromtimestamp(request.user.get('exp')).isoformat()
            }
        },
        "organization": {
            "id": str(user_obj.organization_id) if hasattr(user_obj, 'organization_id') else None,
            "name": user_obj.organization.name if hasattr(user_obj, 'organization') and user_obj.organization else "System Administrator"
        }
    }), 200


@auth_bp.route('/update_profile', methods=['PUT'])
@token_Required
def update():
    try:
        raw_data=request.get_json()
        validated_data=UpdateProfileSchema().load(raw_data)

        result,status_code=update_user(request.user['sub'], validated_data)
        return jsonify(result), status_code
    except ValidationError as ve:
        return jsonify({"Validation Error": ve.messages}), 400
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 401
    


@auth_bp.route('/delete_user/<user_id>', methods=['DELETE'])
@token_Required
@role_required('admin')
def delete(user_id):
    try:
        if str(user_id) == str(request.user['sub']):
            return jsonify({"error": "Admin users cannot delete themselves."}), 400
        result,status_code=delete_user(user_id)
        return jsonify(result), status_code
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 401

@auth_bp.route('/delete_organization/<org_id>', methods=['DELETE'])
@token_Required
@role_required('admin')
def delete_organization(org_id):
    try:
        result,status_code=delete_organization_by_Id(org_id)
        return jsonify(result), status_code
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 401