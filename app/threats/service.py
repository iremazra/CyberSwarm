from datetime import datetime
from app.extensions import db
from .models import ThreatLog
from app.nodes.models import Node
from app.admin.models import WhitelistIP

def create_threat_report(node_id, data):
    #11. madde: saldırı raporunu veri tabanına kaydeder.
   
    new_report=ThreatLog(
        attacker_ip=data['attacker_ip'],
        attack_vector=data['attack_vector'],
        timestamp=data.get('timestamp',datetime.utcnow()),
        node_id=node_id

    )

    try:
        db.session.add(new_report)
        db.session.commit()
        return new_report
    except Exception as e:
        db.session.rollback()
        raise ValueError("Error creating report: " + str(e))


def calculate_ip_reputation(ip_address):
    #12. madde: IP skorunu rapor sayısına ve sensör güvrninr göre hesaplar
    is_whitelisted=WhitelistIP.query.filter_by(ip_address=ip_address).first()
    if is_whitelisted:
        return {
            "attacker_ip":ip_address,
            "reputation_score":10.0,
            "total_reports":0,
            "is_whitelisted":True
            }
        
    reports=ThreatLog.query.filter_by(attacker_ip=ip_address).all()

    if not reports:
        return {"attacker_ip":ip_address, "reputation_score":10.0, "total_reports:":0}
    
    #Her rapor skoru 0.5 düşürür. Minimum (0.0)

    base_score=10.0
    penalty=len(reports)*0.5
    final_score=max(0.0,base_score-penalty)

    return {
        "attacker_ip":ip_address,
        "reputation_score":round(final_score,2),
        "total_reports":len(reports),
        "last_attack_at":reports[-1].timestamp
    }

def get_high_risk_blocklist(threshold=8.0):
    #Belirlenen eşik değerinin altındaki, yüksek riskli ıp'leri dönecek

    all_ips=db.session.query(ThreatLog.attacker_ip).distinct().all()

    blocklist=[]
    for(ip,) in all_ips:
        reputation=calculate_ip_reputation(ip) #Her ip için skor hesaplanıyot

        if reputation['reputation_score']<=threshold:
            blocklist.append(ip)
        
    return blocklist
    
