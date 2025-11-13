# 🚀 Uncle E-Book - Production Deployment Guide (DigitalOcean)

คู่มือการ Deploy โปรเจค Uncle E-Book ขึ้น Production Server บน DigitalOcean

## 📋 สารบัญ

1. [ข้อกำหนดเบื้องต้น](#ข้อกำหนดเบื้องต้น)
2. [สร้าง Droplet บน DigitalOcean](#สร้าง-droplet-บน-digitalocean)
3. [ตั้งค่า Server](#ตั้งค่า-server)
4. [ติดตั้ง Docker และ Docker Compose](#ติดตั้ง-docker-และ-docker-compose)
5. [Deploy Application](#deploy-application)
6. [ตั้งค่า Domain และ SSL](#ตั้งค่า-domain-และ-ssl)
7. [การจัดการและ Monitoring](#การจัดการและ-monitoring)
8. [Backup และ Restore](#backup-และ-restore)
9. [Troubleshooting](#troubleshooting)

---

## 🎯 ข้อกำหนดเบื้องต้น

### สิ่งที่ต้องมี:
- ✅ บัญชี DigitalOcean ([สมัครที่นี่](https://www.digitalocean.com/))
- ✅ Domain name (เช่น example.com)
- ✅ SSH Key สำหรับ authentication
- ✅ Git repository ของโปรเจค
- ✅ ความรู้พื้นฐานเรื่อง Linux, Docker, และ Django

### ค่าใช้จ่ายโดยประมาณ:
- Droplet Basic ($6-12/เดือน)
- Managed Database (Optional: $15+/เดือน)
- Domain name ($10-20/ปี)

---

## 🌊 สร้าง Droplet บน DigitalOcean

### 1. เข้าสู่ DigitalOcean Console
```
https://cloud.digitalocean.com/
```

### 2. สร้าง Droplet ใหม่

**คลิก** "Create" → "Droplets"

#### เลือก Configuration:

**Image:**
- Ubuntu 22.04 (LTS) x64

**Plan:**
- Basic Plan
- Regular CPU
- 1 GB RAM / 1 CPU ($6/month) - สำหรับทดสอบ
- 2 GB RAM / 1 CPU ($12/month) - แนะนำสำหรับ production

**Datacenter:**
- Singapore (SGP1) - เหมาะสำหรับประเทศไทย
- หรือ Bangkok (BLR1) - ถ้ามี

**Authentication:**
- เลือก "SSH keys" (แนะนำ)
- หรือ "Password" (ถ้าจำเป็น)

**Hostname:**
```
uncleebook-prod
```

### 3. สร้าง SSH Key (ถ้ายังไม่มี)

**บนเครื่อง Local:**
```bash
# สร้าง SSH key
ssh-keygen -t rsa -b 4096 -C "your-email@example.com"

# คัดลอก public key
cat ~/.ssh/id_rsa.pub
```

**เพิ่ม Public Key ใน DigitalOcean:**
1. คลิก "New SSH Key"
2. วาง public key ที่คัดลอกมา
3. ตั้งชื่อ: "my-laptop" หรือชื่อที่เหมาะสม

---

## ⚙️ ตั้งค่า Server

### 1. เชื่อมต่อไปยัง Server

```bash
# เชื่อมต่อผ่าน SSH (แทน YOUR_SERVER_IP ด้วย IP จริง)
ssh root@YOUR_SERVER_IP
```

### 2. Update และ Upgrade System

```bash
# Update package lists
apt update

# Upgrade installed packages
apt upgrade -y

# Install essential tools
apt install -y curl wget git vim htop unzip
```

### 3. สร้าง User ใหม่ (Security Best Practice)

```bash
# สร้าง user ใหม่
adduser deploy

# เพิ่ม sudo privileges
usermod -aG sudo deploy

# คัดลอก SSH keys
rsync --archive --chown=deploy:deploy ~/.ssh /home/deploy
```

### 4. ตั้งค่า Firewall (UFW)

```bash
# เปิดใช้งาน UFW
ufw allow OpenSSH
ufw allow 80/tcp
ufw allow 443/tcp
ufw enable

# ตรวจสอบสถานะ
ufw status
```

### 5. เข้าสู่ระบบด้วย User ใหม่

```bash
# ออกจาก root
exit

# เข้าใหม่ด้วย deploy user
ssh deploy@YOUR_SERVER_IP
```

---

## 🐳 ติดตั้ง Docker และ Docker Compose

### 1. ติดตั้ง Docker

```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# เพิ่ม user เข้า docker group
sudo usermod -aG docker $USER

# Apply group changes
newgrp docker

# ทดสอบ Docker
docker --version
docker run hello-world
```

### 2. ติดตั้ง Docker Compose

```bash
# ติดตั้ง Docker Compose
sudo apt install -y docker-compose-plugin

# ทดสอบ
docker compose version
```

---

## 📦 Deploy Application

### 1. Clone Repository

```bash
# สร้างโฟลเดอร์สำหรับโปรเจค
mkdir -p ~/apps
cd ~/apps

# Clone repository (แทน YOUR_REPO_URL ด้วย URL จริง)
git clone https://github.com/YOUR_USERNAME/uncleebook.git
cd uncleebook
```

### 2. สร้างไฟล์ Environment Variables

```bash
# สร้าง .env.prod
nano .env.prod
```

**เนื้อหาของ .env.prod:**
```env
# Django Settings
DJANGO_SETTINGS_MODULE=config.settings.prod
DJANGO_SECRET_KEY=your-very-secure-random-secret-key-here-change-this
DJANGO_ALLOWED_HOSTS=uncle-ebook.com,www.uncle-ebook.com,YOUR_SERVER_IP
DJANGO_SECURE_SSL_REDIRECT=True

# Database Settings
POSTGRES_DB=uncleebook_prod
POSTGRES_USER=uncleebook_user
POSTGRES_PASSWORD=your-very-secure-database-password-here
POSTGRES_HOST=db-prod
POSTGRES_PORT=5432

# Internationalization
LANGUAGE_CODE=th
TIME_ZONE=Asia/Bangkok

# Email Settings (ตัวอย่างใช้ Gmail)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-specific-password
DEFAULT_FROM_EMAIL=Uncle EBook <your-email@gmail.com>

# Security (Production)
DJANGO_DEBUG=False
DJANGO_CSRF_TRUSTED_ORIGINS=https://uncle-ebook.com,https://www.uncle-ebook.com
```

**บันทึกไฟล์:** `Ctrl + X` → `Y` → `Enter`

### 3. สร้าง Django Secret Key ใหม่

```bash
# วิธีที่ 1: ใช้ Python
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# วิธีที่ 2: ใช้ OpenSSL
openssl rand -base64 50
```

คัดลอกผลลัพธ์ไปใส่ใน `DJANGO_SECRET_KEY`

### 4. ตรวจสอบ Docker Compose Configuration

```bash
# ดู docker-compose.yml
cat docker-compose.yml
```

### 5. Build และรัน Production Containers

```bash
# Build images
docker compose --profile prod build

# Start services
docker compose --profile prod up -d

# ตรวจสอบสถานะ
docker compose --profile prod ps
```

### 6. รัน Database Migrations

```bash
# รัน migrations
docker compose --profile prod exec web-prod python manage.py migrate

# สร้าง superuser
docker compose --profile prod exec web-prod python manage.py createsuperuser

# Collect static files
docker compose --profile prod exec web-prod python manage.py collectstatic --noinput
```

### 7. ทดสอบการเข้าถึง

```bash
# เปิดเบราว์เซอร์ไปที่
http://YOUR_SERVER_IP
```

---

## 🌐 ตั้งค่า Domain และ SSL

### 1. ตั้งค่า DNS Records

ไปที่ผู้ให้บริการ Domain ของคุณและเพิ่ม DNS Records:

| Type | Name | Value | TTL |
|------|------|-------|-----|
| A | @ | YOUR_SERVER_IP | 3600 |
| A | www | YOUR_SERVER_IP | 3600 |

**รอ DNS Propagation:** ประมาณ 5-30 นาที

**ตรวจสอบ DNS:**
```bash
# บนเครื่อง local
nslookup uncle-ebook.com
dig uncle-ebook.com
```

### 2. ติดตั้ง Certbot สำหรับ SSL

```bash
# ติดตั้ง Certbot
sudo apt install -y certbot python3-certbot-nginx

# หยุด nginx container ชั่วคราว
docker compose --profile prod stop nginx
```

### 3. แก้ไข Nginx Configuration

```bash
# แก้ไขไฟล์ nginx config
nano nginx/conf.d/uncleebook.conf
```

**อัพเดท server_name:**
```nginx
upstream django {
    server web-prod:8000;
}

server {
    listen 80;
    server_name uncle-ebook.com www.uncle-ebook.com;
    charset utf-8;

    # Max upload size
    client_max_body_size 20M;

    # Django media files
    location /media/ {
        alias /app/media/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Django static files
    location /static/ {
        alias /app/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Django application
    location / {
        proxy_pass http://django;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;

        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # Health check endpoint
    location /health/ {
        access_log off;
        return 200 "healthy\n";
        add_header Content-Type text/plain;
    }
}
```

### 4. สร้าง SSL Certificate

```bash
# ขอ SSL certificate
sudo certbot certonly --standalone -d uncle-ebook.com -d www.uncle-ebook.com

# ป้อนอีเมลสำหรับ renewal notifications
# ตอบ Y เพื่อยอมรับ Terms of Service
```

### 5. อัพเดท Nginx สำหรับ SSL

**สร้างไฟล์ Nginx config ใหม่:**
```bash
nano nginx/conf.d/uncleebook-ssl.conf
```

**เนื้อหา:**
```nginx
upstream django {
    server web-prod:8000;
}

# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name uncle-ebook.com www.uncle-ebook.com;
    return 301 https://$server_name$request_uri;
}

# HTTPS Server
server {
    listen 443 ssl http2;
    server_name uncle-ebook.com www.uncle-ebook.com;
    charset utf-8;

    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/uncle-ebook.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/uncle-ebook.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    # Security Headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Max upload size
    client_max_body_size 20M;

    # Django media files
    location /media/ {
        alias /app/media/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Django static files
    location /static/ {
        alias /app/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Django application
    location / {
        proxy_pass http://django;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;

        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # Health check endpoint
    location /health/ {
        access_log off;
        return 200 "healthy\n";
        add_header Content-Type text/plain;
    }
}
```

### 6. อัพเดท Docker Compose สำหรับ SSL

```bash
# แก้ไข docker-compose.yml
nano docker-compose.yml
```

**อัพเดท nginx service:**
```yaml
  nginx:
    image: nginx:alpine
    container_name: uncleebook-nginx
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/conf.d:/etc/nginx/conf.d:ro
      - static_volume:/app/staticfiles:ro
      - media_volume:/app/media:ro
      - /etc/letsencrypt:/etc/letsencrypt:ro  # เพิ่มบรรทัดนี้
    ports:
      - "80:80"
      - "443:443"
    depends_on:
      - web-prod
    networks:
      - uncleebook-network
    profiles:
      - prod
```

### 7. ลบ config เก่าและรัน nginx ใหม่

```bash
# ลบ config เก่า
rm nginx/conf.d/uncleebook.conf

# Restart services
docker compose --profile prod down
docker compose --profile prod up -d

# ตรวจสอบ logs
docker compose --profile prod logs nginx
```

### 8. ตั้งค่า Auto-renewal สำหรับ SSL

```bash
# ทดสอบ renewal
sudo certbot renew --dry-run

# ตั้งค่า cron job สำหรับ auto-renewal
sudo crontab -e
```

**เพิ่มบรรทัดนี้:**
```cron
0 0 * * 0 certbot renew --quiet && docker compose --profile prod restart nginx
```

---

## 📊 การจัดการและ Monitoring

### คำสั่งพื้นฐานสำหรับการจัดการ

```bash
# ดูสถานะ containers
docker compose --profile prod ps

# ดู logs
docker compose --profile prod logs -f

# ดู logs เฉพาะ service
docker compose --profile prod logs -f web-prod
docker compose --profile prod logs -f nginx
docker compose --profile prod logs -f db-prod

# รัน Django commands
docker compose --profile prod exec web-prod python manage.py migrate
docker compose --profile prod exec web-prod python manage.py createsuperuser
docker compose --profile prod exec web-prod python manage.py collectstatic

# Restart services
docker compose --profile prod restart web-prod
docker compose --profile prod restart nginx

# Stop all services
docker compose --profile prod down

# Start all services
docker compose --profile prod up -d
```

### Monitoring System Resources

```bash
# ติดตั้ง monitoring tools
sudo apt install -y htop iotop nethogs

# ดู resource usage
htop                    # CPU, Memory, Process
docker stats            # Docker containers stats
df -h                   # Disk usage
free -h                 # Memory usage
```

### ตั้งค่า Log Rotation

```bash
# สร้างไฟล์ logrotate config
sudo nano /etc/logrotate.d/uncleebook
```

**เนื้อหา:**
```
/home/deploy/apps/uncleebook/logs/*.log {
    daily
    missingok
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 deploy deploy
    sharedscripts
}
```

---

## 💾 Backup และ Restore

### 1. Backup Database

```bash
# สร้างโฟลเดอร์สำหรับ backups
mkdir -p ~/backups

# Backup database
docker compose --profile prod exec db-prod pg_dump -U uncleebook_user uncleebook_prod > ~/backups/db-backup-$(date +%Y%m%d-%H%M%S).sql

# Backup ด้วย compression
docker compose --profile prod exec db-prod pg_dump -U uncleebook_user uncleebook_prod | gzip > ~/backups/db-backup-$(date +%Y%m%d-%H%M%S).sql.gz
```

### 2. Backup Media Files

```bash
# Backup media folder
tar -czf ~/backups/media-backup-$(date +%Y%m%d-%H%M%S).tar.gz ./media
```

### 3. สร้าง Backup Script อัตโนมัติ

```bash
# สร้าง backup script
nano ~/backup.sh
```

**เนื้อหา:**
```bash
#!/bin/bash

# Variables
BACKUP_DIR="/home/deploy/backups"
PROJECT_DIR="/home/deploy/apps/uncleebook"
DATE=$(date +%Y%m%d-%H%M%S)
DB_NAME="uncleebook_prod"
DB_USER="uncleebook_user"

# Create backup directory
mkdir -p $BACKUP_DIR

# Backup database
docker compose --profile prod exec -T db-prod pg_dump -U $DB_USER $DB_NAME | gzip > $BACKUP_DIR/db-$DATE.sql.gz

# Backup media files
tar -czf $BACKUP_DIR/media-$DATE.tar.gz -C $PROJECT_DIR media

# Keep only last 7 days backups
find $BACKUP_DIR -name "db-*.sql.gz" -mtime +7 -delete
find $BACKUP_DIR -name "media-*.tar.gz" -mtime +7 -delete

echo "Backup completed: $DATE"
```

**ทำให้ script executable:**
```bash
chmod +x ~/backup.sh
```

**ตั้งค่า cron job:**
```bash
crontab -e
```

**เพิ่มบรรทัดนี้ (backup ทุกวันเวลา 2:00 AM):**
```cron
0 2 * * * /home/deploy/backup.sh >> /home/deploy/backup.log 2>&1
```

### 4. Restore Database

```bash
# Restore จาก backup file
gunzip < ~/backups/db-backup-20250101-020000.sql.gz | docker compose --profile prod exec -T db-prod psql -U uncleebook_user -d uncleebook_prod

# หรือถ้าไม่มี compression
cat ~/backups/db-backup-20250101-020000.sql | docker compose --profile prod exec -T db-prod psql -U uncleebook_user -d uncleebook_prod
```

### 5. Restore Media Files

```bash
# Extract media backup
cd ~/apps/uncleebook
tar -xzf ~/backups/media-backup-20250101-020000.tar.gz
```

---

## 🔧 Troubleshooting

### 1. Container ไม่ start

```bash
# ดู logs
docker compose --profile prod logs web-prod

# ตรวจสอบ container status
docker compose --profile prod ps

# Rebuild และ restart
docker compose --profile prod down
docker compose --profile prod build --no-cache
docker compose --profile prod up -d
```

### 2. Database Connection Error

```bash
# ตรวจสอบว่า database container ทำงานไหม
docker compose --profile prod ps db-prod

# ตรวจสอบ database logs
docker compose --profile prod logs db-prod

# เข้าไปใน database container
docker compose --profile prod exec db-prod psql -U uncleebook_user -d uncleebook_prod

# ทดสอบ connection จาก web container
docker compose --profile prod exec web-prod python manage.py dbshell
```

### 3. Static/Media Files ไม่แสดง

```bash
# Collect static files ใหม่
docker compose --profile prod exec web-prod python manage.py collectstatic --clear --noinput

# ตรวจสอบ permissions
docker compose --profile prod exec web-prod ls -la /app/staticfiles
docker compose --profile prod exec web-prod ls -la /app/media

# Restart nginx
docker compose --profile prod restart nginx
```

### 4. SSL Certificate Issues

```bash
# ตรวจสอบ certificate
sudo certbot certificates

# Renew certificate manually
sudo certbot renew

# Restart nginx
docker compose --profile prod restart nginx
```

### 5. Memory Issues

```bash
# ดู memory usage
free -h
docker stats

# ลด workers ใน gunicorn (แก้ไข Dockerfile)
# เปลี่ยนจาก --workers 3 เป็น --workers 2

# Restart services
docker compose --profile prod restart web-prod
```

### 6. Disk Space Full

```bash
# ตรวจสอบ disk usage
df -h

# ลบ unused Docker resources
docker system prune -a --volumes

# ลบ old logs
sudo journalctl --vacuum-time=7d

# ลบ old backups
find ~/backups -mtime +30 -delete
```

---

### 7. CSRF Verification Error

```bash
# ถ้าเจอ error: "CSRF verification failed. Request aborted."
# แก้ไขโดยเพิ่มใน .env.prod:
DJANGO_CSRF_TRUSTED_ORIGINS=http://uncle-ebook.com,http://www.uncle-ebook.com,https://uncle-ebook.com,https://www.uncle-ebook.com

# Restart containers
docker compose --profile prod restart web-prod
```

### 8. Logging Handler Error

```bash
# ถ้าเจอ error: "ValueError: Unable to configure handler 'file'"
# สร้างโฟลเดอร์ logs
mkdir -p logs
chmod 755 logs

# Rebuild และ restart
docker compose --profile prod down
docker compose --profile prod build
docker compose --profile prod up -d
```

---

## 📝 Checklist ก่อน Deploy Production

- [ ] เปลี่ยน `DJANGO_SECRET_KEY` เป็นค่าใหม่ที่ปลอดภัย
- [ ] ตั้งค่า `DJANGO_DEBUG=False`
- [ ] เปลี่ยน `POSTGRES_PASSWORD` เป็นรหัสผ่านที่แข็งแรง
- [ ] ตั้งค่า `DJANGO_ALLOWED_HOSTS` ให้ถูกต้อง (รวม domain และ IP)
- [ ] ตั้งค่า `DJANGO_CSRF_TRUSTED_ORIGINS` สำหรับ domain
- [ ] ตั้งค่า Email settings สำหรับ production
- [ ] สร้างโฟลเดอร์ `logs` ให้พร้อม
- [ ] ตั้งค่า Firewall (UFW)
- [ ] ติดตั้ง SSL certificate
- [ ] ตั้งค่า auto-renewal สำหรับ SSL
- [ ] ตั้งค่า automated backups
- [ ] ทดสอบ backup และ restore
- [ ] ตั้งค่า log rotation
- [ ] ตรวจสอบ security headers
- [ ] เปิดใช้งาน HTTPS redirect
- [ ] ทดสอบการทำงานของเว็บไซต์
- [ ] ทดสอบ admin panel (/admin/)
- [ ] ตรวจสอบ static และ media files

---

## 🔐 Security Best Practices

1. **ไม่เปิดเผย Secret Keys** - เก็บไว้ใน `.env` file เท่านั้น
2. **ใช้ Strong Passwords** - สำหรับ database และ admin accounts
3. **Update Regularly** - อัพเดท packages และ dependencies เป็นประจำ
4. **Enable Firewall** - จำกัดการเข้าถึงเฉพาะ ports ที่จำเป็น
5. **Use SSL/TLS** - บังคับใช้ HTTPS เสมอ
6. **Regular Backups** - สำรองข้อมูลทุกวัน
7. **Monitor Logs** - ตรวจสอบ logs เป็นประจำ
8. **Disable Debug Mode** - ปิด DEBUG ใน production
9. **Use Strong SSH Keys** - ใช้ SSH keys แทน passwords
10. **Limit Database Access** - อนุญาตเฉพาะ containers ที่จำเป็น

---

## 📚 Resources

- [DigitalOcean Documentation](https://docs.digitalocean.com/)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)
- [Docker Documentation](https://docs.docker.com/)
- [Let's Encrypt Documentation](https://letsencrypt.org/docs/)
- [Nginx Documentation](https://nginx.org/en/docs/)

---

## 🆘 Support

หากพบปัญหาหรือมีคำถาม:
- เปิด Issue ใน GitHub repository
- ติดต่อทีม support
- ตรวจสอบ logs: `docker compose --profile prod logs -f`

---

## 🚀 Quick Start Guide

สำหรับผู้ที่ต้องการ deploy ด่วน:

```bash
# 1. Clone repository
git clone https://github.com/Thitphavanh/Uncle-Engineer-E-Book.git
cd Uncle-Engineer-E-Book

# 2. สร้าง .env.prod (แก้ไขค่าต่างๆ ให้ถูกต้อง)
nano .env.prod

# 3. สร้างโฟลเดอร์ logs
mkdir -p logs

# 4. Build และ Start containers
docker compose --profile prod build
docker compose --profile prod up -d

# 5. รัน migrations
docker compose --profile prod exec web-prod python manage.py migrate

# 6. สร้าง superuser
docker compose --profile prod exec web-prod python manage.py createsuperuser

# 7. Collect static files
docker compose --profile prod exec web-prod python manage.py collectstatic --noinput

# 8. ทดสอบ
curl http://YOUR_SERVER_IP
```

---

## 🔗 Links

- **GitHub Repository**: https://github.com/Thitphavanh/Uncle-Engineer-E-Book
- **Live Site**: https://uncle-ebook.com
- **Admin Panel**: https://uncle-ebook.com/admin

---

**Last Updated:** 2025-11-13
**Version:** 2.0.0
**Author:** Uncle Engineer Team
