from app.threats.service import calculate_ip_reputation

def perform_bulk_analysis(ip_list):
    results=[]
    for ip in ip_list:
        data=calculate_ip_reputation(ip)
        results.append(data)
    return results