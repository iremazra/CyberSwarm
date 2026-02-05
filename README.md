# CyberSwarm: Distributed Threat Intelligence System

**CyberSwarm**, dağıtık sistemlerden gelen siber tehdit verilerini (potansiyel saldırgan IP adresleri) merkezi bir yapıda toplamak, işlemek ve analiz etmek amacıyla geliştirilmiş bir **Distributed Threat Intelligence (Tehdit İstihbaratı)** sistemidir.

## Projenin Amacı
Sistem, farklı uç noktalardan (nodes) gelen şüpheli ağ aktivitelerini ve IP adreslerini gerçek zamanlı olarak toplar. Bu veriler, ağ güvenliğini artırmak ve proaktif savunma mekanizmaları (Moving Target Defense gibi) için girdi sağlamak amacıyla kullanılır.

## Sistem Mimarisi
Proje, mikroservis yaklaşımıyla tasarlanmış dağıtık bir yapıya sahiptir:
* **Nodes:** Dağıtık ağ noktalarında veri toplama işini üstlenir.
* **Central API:** Flask tabanlı merkezi sunucu, gelen verileri doğrular ve işler.
* **Database Katmanı:** Toplanan istihbarat verileri ilişkisel bir yapıda saklanır.

## Kullanılan Teknolojiler
* **Backend:** Python & Flask Framework.
* **Veritabanı:** PostgreSQL (Yüksek ölçeklenebilirlik ve veri bütünlüğü için).
* **Infrastructure:** Docker & Docker Compose (Konteynerleştirme ve izole çalışma ortamı).
  
## Hızlı Başlangıç (Docker ile)
Sistemi yerel ortamınızda ayağa kaldırmak için:

1. Depoyu klonlayın:
   ```bash
   git clone [https://github.com/kullaniciadi/CyberSwarm.git](https://github.com/kullaniciadi/CyberSwarm.git)
   cd CyberSwarm
