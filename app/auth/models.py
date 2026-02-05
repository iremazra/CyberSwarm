# app/auth/models.py
import uuid #rastgele ama çakışma ihtimali yok denecek kadar az ID üretir
from datetime import datetime 
from app.extensions import db


class Organization(db.Model):
    __tablename__ = 'organizations'
    
    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(100),  nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    api_key = db.Column(db.String(255), unique=True, nullable=False) #Her organizasyonun benzersiz bir API anahtarı olur    
    
    # Cascade ayarını buraya ekliyoruz:
    # cascade="all, delete-orphan" -> Organizasyon silinirse tüm üyeleri de siler.
    users = db.relationship('User', back_populates='organization_obj', cascade="all, delete-orphan", lazy=True)
    nodes = db.relationship('Node', back_populates='organization_obj', cascade="all, delete-orphan", lazy=True)
   # users = db.relationship('User', backref='organization', lazy=True)
 
class User(db.Model):
    __tablename__='users'

    id=db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name=db.Column(db.String(100), nullable=False)
    email=db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash=db.Column(db.String(255),nullable=False)
    role=db.Column(db.String(50), nullable=False, default='user')
    organization_id=db.Column(db.UUID(as_uuid=True), db.ForeignKey('organizations.id'), nullable=False)
    created_at=db.Column(db.DateTime, default=datetime.utcnow)
    # BU SATIRI EKLE:
    # Bu sayede user.organization diyerek Organizasyon nesnesine erişebilirsin.
    organization_obj = db.relationship('Organization', back_populates='users')


class Admin(db.Model):
    __tablename__='admins'

    id=db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email=db.Column(db.String(120), unique=True, nullable=False, index=True)
    name=db.Column(db.String(100), nullable=False)
    password_hash=db.Column(db.String(255),nullable=False)
    created_at=db.Column(db.DateTime, default=datetime.utcnow)
    role=db.Column(db.String(50), nullable=False, default='admin')
    audit_logs = db.relationship('AuditLog', back_populates='admin')