from app.extensions import db
from datetime import datetime
import uuid

class WhitelistIP(db.Model):
    #16. madde: Güvenilir IP'lerin tutulduğu tablo

    id=db.Column(db.UUID(as_uuid=True),primary_key=True,default=uuid.uuid4 )
    ip_address=db.Column(db.String(45),unique=True, nullable=False)
    reason=db.Column(db.String(255))
    added_at=db.Column(db.DateTime,default=datetime.utcnow)


class AuditLog(db.Model):
    #18. madde: Sistem denetim kayıtları

    id=db.Column(db.UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)  
    admin_id=db.Column(db.UUID(as_uuid=True), db.ForeignKey('admins.id'), nullable=False) #işlemi yapan admin
    action=db.Column(db.String(100),nullable=False)
    target=db.Column(db.String(255))  #işlem yapılan hedef (örn bir IP)
    timestamp=db.Column(db.DateTime, default=datetime.utcnow)
    ip_address=db.Column(db.String(45)) #işlemi yapan kişinin ip'si
    admin = db.relationship('Admin', back_populates='audit_logs')

