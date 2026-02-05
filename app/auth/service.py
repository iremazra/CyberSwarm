# app/auth/service.py
from .utils import generate_jwt, hash_password, verify_password
import uuid
from .models import User,Organization, Admin
from app.extensions import db

def register_admin(data):
    email=data.get('email')
    password=data.get('password')
    name=data.get('name')
    if not email or not password:
        raise ValueError("Email and password are required")
    
    existing_admin=Admin.query.filter_by(email=email).first()
    if existing_admin:
        raise ValueError("Admin with this email already exists")

    new_admin=Admin(
        name='admin',
        email=email,
        password_hash=hash_password(password),
        role='admin'
        
    )
    
    try:
        db.session.add(new_admin)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise ValueError("Error creating admin: " + str(e))

    return {
        "message": "Admin registered successfully",
        "admin_id":str(new_admin.id)
    }, 201

def register_user(data):
    email=data.get('email')
    password=data.get('password')
    name=data.get('name')
    organization_name=data.get('organization_name') #Kullanıcı isim göndersin
    

    if not email or not password:
        raise ValueError("Email, password and organization name are required")
    
    
    org= Organization.query.filter_by(name=organization_name).first()
    if not org:
       raise ValueError("Organization does not exist")
       

   
    existing_user=User.query.filter_by(email=email).first()
    if existing_user:
        raise ValueError("User with this email already exists")

   
    new_user=User(
        name=name,
        email=email,
        password_hash=hash_password(password),
        organization_id=org.id,
        role='user'
        
    )
    
    try:
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise ValueError("Error creating user: " + str(e))

    return {
        "message": "User registered successfully",
        "user_id":str(new_user.id),
        "organization":org.name
    }, 201

def create_organization(data):
    name=data.get('name')
    if not name:
        raise ValueError("Organization name is required")
    
    existing_org=Organization.query.filter_by(name=name).first()
    if existing_org:
        raise ValueError("Organization with this name already exists")
    
    secure_key= f"cs_{uuid.uuid4().hex}"

    new_org=Organization(
        name=name,
        api_key=secure_key
    )

    try:
        db.session.add(new_org)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise ValueError("Error creating organization: " + str(e))

    return {
        "message": "Organization created successfully",
        "organization_id": str(new_org.id),
        "api_key": secure_key #kullanıcıya bu api key'i bir kez gösteririz.
    }, 201


def login_user(data):
    email=data.get('email')
    password=data.get('password')
    

    if not email or not password:
        raise ValueError("Email and password are required")

    user =Admin.query.filter_by(email=email).first()

    if not user:
        user=User.query.filter_by(email=email).first()
    
    if not user or not verify_password(password,user.password_hash):
        raise ValueError("Invalid email or password")

    token=generate_jwt({ "id":user.id, "email": email, "role": user.role, "organization_id": str(getattr(user, 'organization_id', None)) }) #Adminde organization_id olmayabilir.
    return {"token": token, "role":user.role},200

def update_user(user_id,validated_data):

    user=Admin.query.get(user_id)
    if not user:
        user=User.query.get(user_id)
    
    if not user:
        raise ValueError("User not found")
    
    #sadece gelen verileri güncelleyeceğiz
    for key, value in validated_data.items():
        if key=="email": #email değiştiği için benzersizlik kontrolü yapacağız.
            existing_user=User.query.filter_by(email=value).first()
            existing_admin=Admin.query.filter_by(email=value).first()
            target=existing_admin or existing_user
            if target and str(target.id) != str(user.id):
                raise ValueError("Email already in use by another user")

        if key=="password" and value:
            user.password_hash=hash_password(value)
        else:
            setattr(user, key, value)

    try:
        db.session.commit()
        return{ "message": "User updated successfully"}, 200
    except Exception as e:
        db.session.rollback()
        raise ValueError("Error updating user: " + str(e))


def get_all_organizations(): #Just admin can access this
    orgs=Organization.query.all()
    org_list=[{
        "id": str(org.id), 
        "name": org.name, 
        "api_key": org.api_key,
        "created_at": org.created_at.isoformat()
        } for org in orgs],200
    return org_list

def delete_user(user_id):
    user=User.query.get(user_id)
    if not user:
        raise ValueError("User not found")
    
    try:
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted successfully"}, 200
    except Exception as e:
        db.session.rollback()
        raise ValueError("Error deleting user: " + str(e))

def delete_organization_by_Id(org_id):
       
    org = Organization.query.get(org_id)
    
    if not org:
        raise ValueError("Organizasyon bulunamadı.")
    
    try:
        db.session.delete(org)
        db.session.commit()
        return {"message": f"'{org.name}'The organization and all associated users have been successfully deleted.."}, 200
    except Exception as e:
        db.session.rollback()
        raise ValueError(f"An error occurred during the deletion process.: {str(e)}")
