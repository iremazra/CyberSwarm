#app/nodes/models.py
import uuid
from datetime import datetime
from app.extensions import db

class Node(db.Model):
    __tablename__ = 'nodes'

    id=db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name=db.Column(db.String(100), nullable=False)
    node_type=db.Column(db.String(50), nullable=False, default='sensor')  # Örneğin: sensor, actuator, gateway
    status=db.Column(db.String(50), nullable=False, default='active')  # Örneğin: active, inactive, maintenance

    #Güvenlik: Sensörlerin merkeze veri atarken kullanacağı özel anahtar
    api_key=db.Column(db.String(255), unique=True, nullable=False, default=lambda: f"node_{uuid.uuid4().hex}")

    #TrustRank algoritması temeli : başlangıç güven skoru
    reputation_score=db.Column(db.Float, nullable=False, default=10.0)

    last_seen=db.Column(db.DateTime, default=datetime.utcnow)
    created_at=db.Column(db.DateTime, default=datetime.utcnow)

    #Foreign key: Auth modülündeki organizasyon tablosuna bağlıyoruz
    organization_id=db.Column(db.UUID(as_uuid=True), db.ForeignKey('organizations.id'), nullable=True)  

    organization_obj = db.relationship('Organization', back_populates='nodes')