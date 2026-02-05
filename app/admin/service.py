from .models import WhitelistIP, AuditLog
from app.extensions import db
from app.threats.models import ThreatLog
from sqlalchemy import func

def add_to_whitelist(ip, reason, admin_id):
    #16. madde: IP'yi beyaz listeye ekler ve loglar
    is_ip_present=WhitelistIP.query.filter_by(ip_address=ip).first()

    if is_ip_present:
        raise ValueError(f"IP {ip} is already whitelisted.")
    
    new_ip=WhitelistIP(ip_address=ip,reason=reason)
    db.session.add(new_ip)

    #Audit log kaydı
    log=AuditLog(admin_id=admin_id, action="ADD_WHITELIST", target=ip)
    
    try:
        db.session.add(log)
        db.session.commit()
        return new_ip
    except Exception as err:
        db.session.rollback()
        raise ValueError("Error creating log: " + str(err))
    
def remove_from_whitelist(ip,admin_id):
    #Whitelist'ten ıp siler ve bunu audit log'a kaydeder.

    #1. ip sistemde var mı kontrol et
    is_ip_present=WhitelistIP.query.filter_by(ip_address=ip).first()

    if not is_ip_present:
        raise ValueError(f"IP {ip} is not in the whitelist.")
    
    #2. audit log kaydı oluşturulacak
    log=AuditLog(
        admin_id=admin_id,
        action="REMOVE_WHITELIST",
        target=ip

        )
    
    try:
        db.session.delete(is_ip_present)
        db.session.add(log)
        db.session.commit()
        return True
    except Exception as err:
        db.session.rollback()
        raise ValueError(f"Delete operation failed: {str(err)}")

def get_admin_global_stats():
    #17.madde: Tüm  sistemin özetini çıkarır
    total_log=ThreatLog.query.count()
    whitelisted_count=WhitelistIP.query.count()

    vector_dist=db.session.query(
        ThreatLog.attack_vector, func.count(ThreatLog.id)
    ).group_by(ThreatLog.attack_vector).all()

    return{
        "total_threat_logs":total_log,
        "total_whitelisted_ips":whitelisted_count,
        "vectors": {v:c for v,c in vector_dist}
    }


    