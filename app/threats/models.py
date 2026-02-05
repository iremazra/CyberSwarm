import uuid
from datetime import datetime
from app.extensions import db

class ThreatLog(db.Model):
    __tablename__ = 'threat_logs'

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    attacker_ip = db.Column(db.String(45), nullable=False, index=True) #saldırgan IP adresi
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False) #saldırı zamanı
    attack_vector = db.Column(db.String(255), nullable=False) #saldırı tipi
    node_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('nodes.id'), nullable=False) #hangi sensör saldırıyı tespit etti. Trustrank hesaplaması için önemli
    reporter_node=db.Relationship('Node', backref='reported_threats', lazy=True)

    node = db.relationship('Node', backref=db.backref('threat_logs', lazy=True))

    def __repr__(self):
        return f"<ThreatLog {self.attacker_ip} via {self.attack_vector}>"