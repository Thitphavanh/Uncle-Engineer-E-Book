# Uncle E-Book - Deployment Guide (DigitalOcean + Docker)

คู่มือการ Deploy โปรเจค Uncle E-Book บน DigitalOcean ด้วย Docker และ Docker Compose

## สารบัญ

1. [ภาพรวม](#ภาพรวม)
2. [Prerequisites](#prerequisites)
3. [การเตรียม DigitalOcean Droplet](#การเตรียม-digitalocean-droplet)
4. [การตั้งค่า Domain และ DNS](#การตั้งค่า-domain-และ-dns)
5. [การติดตั้ง Docker และ Docker Compose](#การติดตั้ง-docker-และ-docker-compose)
6. [การ Deploy โปรเจค](#การ-deploy-โปรเจค)
7. [การตั้งค่า SSL/HTTPS](#การตั้งค่า-sslhttps)
8. [การจัดการและ Maintenance](#การจัดการและ-maintenance)
9. [Troubleshooting](#troubleshooting)

---

## ภาพรวม

โปรเจคนี้ใช้:
- **Django 5.2.8** - Python Web Framework
- **PostgreSQL 15** - Database
- **Nginx** - Web Server & Reverse Proxy
- **Gunicorn** - WSGI HTTP Server
- **Docker & Docker Compose** - Containerization
- **Let's Encrypt** - SSL Certificate (ฟรี)
- **DigitalOcean** - Cloud Hosting

### Architecture

```
Internet
    ↓
Nginx (Port 80/443) → SSL/HTTPS
    ↓
Gunicorn (Port 8000) → Django Application
    ↓
PostgreSQL (Port 5432) → Database
```

---

## Prerequisites

### 1. บน Local Machine
- [ ] Git
- [ ] SSH Key สำหรับเข้า Server
- [ ] Domain Name (เช่น uncle-ebook.com)

### 2. บน DigitalOcean
- [ ] บัญชี DigitalOcean
- [ ] Droplet (แนะนำ: 2GB RAM ขึ้นไป)

### 3. ความรู้พื้นฐาน
- [ ] Linux Command Line
- [ ] Docker & Docker Compose
- [ ] Git

---

## การเตรียม DigitalOcean Droplet

### ขั้นตอนที่ 1: สร้าง Droplet

1. **เข้า DigitalOcean Dashboard**
   - ไปที่ https://cloud.digitalocean.com

2. **Create → Droplets**

3. **เลือก Configuration:**
   - **Image:** Ubuntu 22.04 LTS (แนะนำ)
   - **Plan:**
     - Basic
     - Regular (2 GB RAM / 1 vCPU) - $12/month (แนะนำสำหรับเริ่มต้น)
     - หรือ 4 GB RAM / 2 vCPU - $18/month (สำหรับ traffic ปานกลาง)
   - **Datacenter Region:** Singapore (เร็วสำหรับประเทศไทย)
   - **Authentication:** SSH keys (แนะนำ) หรือ Password
   - **Hostname:** uncle-ebook-prod

4. **Create Droplet** และรอ 1-2 นาที

5. **บันทึก IP Address** ของ Droplet (เช่น 143.198.123.456)

### ขั้นตอนที่ 2: เชื่อมต่อ SSH

```bash
# เชื่อมต่อด้วย SSH Key
ssh root@YOUR_DROPLET_IP

# หรือ เชื่อมต่อด้วย Password
ssh root@YOUR_DROPLET_IP
# (ใส่ password ที่ได้รับทาง email)
```

### ขั้นตอนที่ 3: Update System

```bash
# Update package list
sudo apt update

# Upgrade packages
sudo apt upgrade -y

# Install essential tools
sudo apt install -y curl git vim htop
```

### ขั้นตอนที่ 4: สร้าง User (แนะนำ - ไม่ควรใช้ root)

```bash
# สร้าง user ใหม่
adduser deploy

# เพิ่ม sudo privileges
usermod -aG sudo deploy

# สลับเป็น user deploy
su - deploy
```

---

## การตั้งค่า Domain และ DNS

### ขั้นตอนที่ 1: ตั้งค่า DNS Records

1. เข้า DNS Provider ของคุณ (Namecheap, Cloudflare, GoDaddy, etc.)

2. **เพิ่ม A Records:**

   | Type | Name | Value (IP Address) | TTL |
   |------|------|-------------------|-----|
   | A    | @    | YOUR_DROPLET_IP   | 3600 |
   | A    | www  | YOUR_DROPLET_IP   | 3600 |

3. **รอ DNS Propagation** (5-30 นาที)

### ขั้นตอนที่ 2: ตรวจสอบ DNS

```bash
# ตรวจสอบว่า domain ชี้ไปที่ IP ที่ถูกต้อง
dig uncle-ebook.com
dig www.uncle-ebook.com

# หรือใช้ nslookup
nslookup uncle-ebook.com
```

---

## การติดตั้ง Docker และ Docker Compose

### วิธีที่ 1: ติดตั้งด้วย Official Script (แนะนำ)

```bash
# Download และติดตั้ง Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# เพิ่ม user ปัจจุบันเข้า docker group
sudo usermod -aG docker $USER

# Logout และ Login ใหม่เพื่อให้ changes มีผล
exit
# (SSH เข้ามาใหม่)
```

### วิธีที่ 2: ติดตั้งแบบ Manual

```bash
# Update apt และติดตั้ง dependencies
sudo apt update
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common

# เพิ่ม Docker GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# เพิ่ม Docker repository
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# ติดตั้ง Docker
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# ตรวจสอบ version
docker --version
docker compose version
```

### ตรวจสอบการติดตั้ง

```bash
# ทดสอบ Docker
docker run hello-world

# ตรวจสอบ Docker Compose
docker compose version
# Output: Docker Compose version v2.xx.x
```

---

## การ Deploy โปรเจค

### ขั้นตอนที่ 1: Clone Repository

```bash
# สร้าง directory สำหรับเก็บโปรเจค
mkdir -p ~/apps
cd ~/apps

# Clone repository (เปลี่ยน URL เป็นของคุณ)
git clone https://github.com/YOUR_USERNAME/Uncle-Engineer-E-Book.git
cd Uncle-Engineer-E-Book

# หรือ ถ้าใช้ SSH
git clone git@github.com:YOUR_USERNAME/Uncle-Engineer-E-Book.git
cd Uncle-Engineer-E-Book
```

### ขั้นตอนที่ 2: ตั้งค่า Environment Variables

```bash
# คัดลอก .env.example เป็น .env.prod
cp .env.example .env.prod

# แก้ไข .env.prod
nano .env.prod
# หรือ
vim .env.prod
```

**แก้ไขค่าต่อไปนี้ใน .env.prod:**

```bash
# Django Settings
DJANGO_SETTINGS_MODULE=config.settings.prod
DJANGO_SECRET_KEY=YOUR_GENERATED_SECRET_KEY_HERE  # ⚠️ สร้างใหม่ (ดูด้านล่าง)
DJANGO_ALLOWED_HOSTS=uncle-ebook.com,www.uncle-ebook.com,YOUR_DROPLET_IP
DJANGO_SECURE_SSL_REDIRECT=True

# Database Settings
POSTGRES_DB=uncleebook_prod
POSTGRES_USER=uncleebook
POSTGRES_PASSWORD=YOUR_STRONG_DB_PASSWORD_HERE  # ⚠️ เปลี่ยนเป็นรหัสผ่านที่แข็งแกร่ง
POSTGRES_HOST=db-prod
POSTGRES_PORT=5432

# Internationalization
LANGUAGE_CODE=th
TIME_ZONE=Asia/Bangkok

# Email Settings (ถ้าต้องการส่ง email)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password  # ⚠️ ใช้ App Password ไม่ใช่รหัสผ่านจริง
DEFAULT_FROM_EMAIL=noreply@uncle-ebook.com
```

### ขั้นตอนที่ 3: สร้าง Django Secret Key

```bash
# วิธีที่ 1: ใช้ Docker (ถ้าติดตั้ง Docker แล้ว)
docker run --rm python:3.11-slim python -c "from secrets import token_urlsafe; print(token_urlsafe(50))"

# วิธีที่ 2: ใช้ Python บน local machine
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# วิธีที่ 3: ใช้ OpenSSL
openssl rand -base64 50
```

คัดลอก output และใส่ใน `DJANGO_SECRET_KEY` ใน `.env.prod`

### ขั้นตอนที่ 4: แก้ไข Nginx Configuration

```bash
# แก้ไข nginx config ให้ตรงกับ domain ของคุณ
nano nginx/conf.d/uncleebook.conf
```

เปลี่ยน `uncle-ebook.com` เป็น domain ของคุณ:

```nginx
server_name your-domain.com www.your-domain.com;
```

### ขั้นตอนที่ 5: แก้ไข SSL Setup Script

```bash
# แก้ไข init-letsencrypt.sh
nano init-letsencrypt.sh
```

เปลี่ยนค่าต่อไปนี้:

```bash
domains=(your-domain.com www.your-domain.com)  # เปลี่ยน domain
email="your-email@example.com"  # เปลี่ยนเป็น email ของคุณ
staging=0  # 0 = production, 1 = testing
```

```bash
# ทำให้ script execute ได้
chmod +x init-letsencrypt.sh
```

### ขั้นตอนที่ 6: Build และ Deploy (ครั้งแรก - ใช้ HTTP ก่อน)

เนื่องจาก SSL ยังไม่ได้ตั้ง ให้ทดสอบด้วย HTTP ก่อน:

```bash
# สร้าง HTTP-only nginx config ชั่วคราว
cat > nginx/conf.d/uncleebook-http.conf << 'EOF'
upstream django {
    server web-prod:8000;
}

server {
    listen 80;
    server_name uncle-ebook.com www.uncle-ebook.com;  # เปลี่ยนเป็น domain ของคุณ
    charset utf-8;

    client_max_body_size 20M;

    location /media/ {
        alias /app/media/;
    }

    location /static/ {
        alias /app/staticfiles/;
    }

    location / {
        proxy_pass http://django;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /health/ {
        access_log off;
        return 200 "healthy\n";
        add_header Content-Type text/plain;
    }
}
EOF

# Backup SSL config และใช้ HTTP config
cd nginx/conf.d
mv uncleebook.conf uncleebook-ssl.conf.backup
mv uncleebook-http.conf uncleebook.conf
cd ~/apps/Uncle-Engineer-E-Book

# Build Docker images
docker compose --profile prod build

# Start services (web, database, nginx)
docker compose --profile prod up -d

# ตรวจสอบว่า services กำลังรันอยู่
docker compose --profile prod ps

# ดู logs
docker compose --profile prod logs -f
```

### ขั้นตอนที่ 7: Run Database Migrations

```bash
# รัน migrations
docker compose --profile prod exec web-prod python manage.py migrate

# สร้าง superuser
docker compose --profile prod exec web-prod python manage.py createsuperuser

# Collect static files
docker compose --profile prod exec web-prod python manage.py collectstatic --noinput
```

### ขั้นตอนที่ 8: ทดสอบการทำงาน

เปิด browser ไปที่:
- http://your-domain.com
- http://YOUR_DROPLET_IP

ถ้าทำงานปกติ ไปขั้นตอนต่อไปเพื่อตั้งค่า SSL

---

## การตั้งค่า SSL/HTTPS

### ขั้นตอนที่ 1: Restore SSL Config

```bash
cd ~/apps/Uncle-Engineer-E-Book/nginx/conf.d

# นำ SSL config กลับมาใช้
mv uncleebook.conf uncleebook-http.conf.backup
mv uncleebook-ssl.conf.backup uncleebook.conf

cd ~/apps/Uncle-Engineer-E-Book
```

### ขั้นตอนที่ 2: เปิด Firewall Ports (ถ้ามี UFW)

```bash
# ตรวจสอบ firewall status
sudo ufw status

# ถ้ายังไม่เปิด ให้เปิด ports
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw enable
```

### ขั้นตอนที่ 3: รัน SSL Setup Script

```bash
# รัน init-letsencrypt.sh
./init-letsencrypt.sh
```

Script จะทำการ:
1. สร้าง dummy certificates
2. Start nginx
3. ขอ certificates จริงจาก Let's Encrypt
4. Reload nginx

### ขั้นตอนที่ 4: ตรวจสอบ HTTPS

เปิด browser ไปที่:
- https://your-domain.com
- https://www.your-domain.com

HTTP จะ redirect ไป HTTPS อัตโนมัติ

### ขั้นตอนที่ 5: ตรวจสอบ Certificate

```bash
# ตรวจสอบ certificate expiration
docker compose --profile prod exec certbot certbot certificates

# Test certificate renewal
docker compose --profile prod run --rm certbot renew --dry-run
```

### การ Renew Certificate อัตโนมัติ

Certbot container จะตรวจสอบและ renew certificates อัตโนมัติทุก 12 ชั่วโมง

ถ้าต้องการ renew manually:

```bash
docker compose --profile prod run --rm certbot renew
docker compose --profile prod exec nginx nginx -s reload
```

---

## การจัดการและ Maintenance

### ดูสถานะ Containers

```bash
# ดู running containers
docker compose --profile prod ps

# ดู logs ทั้งหมด
docker compose --profile prod logs -f

# ดู logs เฉพาะ service
docker compose --profile prod logs -f web-prod
docker compose --profile prod logs -f nginx
docker compose --profile prod logs -f db-prod
```

### Restart Services

```bash
# Restart ทุก services
docker compose --profile prod restart

# Restart เฉพาะ service
docker compose --profile prod restart web-prod
docker compose --profile prod restart nginx
```

### Stop/Start Services

```bash
# Stop ทุก services
docker compose --profile prod down

# Start ทุก services
docker compose --profile prod up -d
```

### Update Code จาก Git

```bash
cd ~/apps/Uncle-Engineer-E-Book

# Pull latest code
git pull origin main

# Rebuild และ restart
docker compose --profile prod build web-prod
docker compose --profile prod up -d web-prod

# Run migrations (ถ้ามี)
docker compose --profile prod exec web-prod python manage.py migrate

# Collect static files
docker compose --profile prod exec web-prod python manage.py collectstatic --noinput
```

### Database Backup

```bash
# สร้าง backup directory
mkdir -p ~/backups

# Backup database
docker compose --profile prod exec db-prod pg_dump -U uncleebook uncleebook_prod > ~/backups/db_backup_$(date +%Y%m%d_%H%M%S).sql

# ตรวจสอบ backup
ls -lh ~/backups/
```

### Database Restore

```bash
# Restore จาก backup file
cat ~/backups/db_backup_20240101_120000.sql | docker compose --profile prod exec -T db-prod psql -U uncleebook uncleebook_prod
```

### ตั้งค่า Auto Backup (Cron)

```bash
# สร้าง backup script
cat > ~/backup-db.sh << 'EOF'
#!/bin/bash
cd ~/apps/Uncle-Engineer-E-Book
docker compose --profile prod exec -T db-prod pg_dump -U uncleebook uncleebook_prod > ~/backups/db_backup_$(date +\%Y\%m\%d_\%H\%M\%S).sql

# ลบ backup ที่เก่ากว่า 7 วัน
find ~/backups/ -name "db_backup_*.sql" -mtime +7 -delete
EOF

# ทำให้ execute ได้
chmod +x ~/backup-db.sh

# เพิ่มใน crontab (backup ทุกวันเวลา 02:00)
crontab -e
```

เพิ่มบรรทัดนี้:
```
0 2 * * * /home/deploy/backup-db.sh >> /home/deploy/backup.log 2>&1
```

### Monitor Resources

```bash
# ดู resource usage
docker stats

# ดู disk space
df -h

# ดู memory usage
free -h

# ดู running processes
htop
```

### Clean Up Docker

```bash
# ลบ unused images
docker image prune -a

# ลบ unused volumes
docker volume prune

# ลบ unused containers
docker container prune

# ลบทุกอย่างที่ไม่ได้ใช้
docker system prune -a --volumes
```

---

## Troubleshooting

### 1. Site ไม่สามารถเข้าถึงได้

**ตรวจสอบ:**

```bash
# 1. ตรวจสอบว่า containers กำลังรันอยู่
docker compose --profile prod ps

# 2. ตรวจสอบ nginx logs
docker compose --profile prod logs nginx

# 3. ตรวจสอบ web-prod logs
docker compose --profile prod logs web-prod

# 4. ตรวจสอบว่า ports เปิดอยู่
sudo netstat -tlnp | grep -E ':(80|443|8000)'

# 5. ตรวจสอบ firewall
sudo ufw status

# 6. Test จาก server
curl http://localhost
curl http://localhost:8000
```

### 2. Database Connection Error

```bash
# ตรวจสอบว่า database container กำลังรันอยู่
docker compose --profile prod ps db-prod

# ตรวจสอบ database logs
docker compose --profile prod logs db-prod

# Test database connection
docker compose --profile prod exec db-prod psql -U uncleebook -d uncleebook_prod -c "SELECT 1;"

# ตรวจสอบ environment variables
docker compose --profile prod exec web-prod env | grep POSTGRES
```

### 3. Static Files ไม่แสดง

```bash
# Collect static files ใหม่
docker compose --profile prod exec web-prod python manage.py collectstatic --noinput

# ตรวจสอบ permissions
docker compose --profile prod exec web-prod ls -la /app/staticfiles/

# ตรวจสอบ nginx config
docker compose --profile prod exec nginx cat /etc/nginx/conf.d/uncleebook.conf

# Test nginx configuration
docker compose --profile prod exec nginx nginx -t

# Reload nginx
docker compose --profile prod exec nginx nginx -s reload
```

### 4. SSL Certificate Errors

```bash
# ตรวจสอบ certbot logs
docker compose --profile prod logs certbot

# ตรวจสอบ certificates
docker compose --profile prod exec certbot certbot certificates

# ลองขอ certificate ใหม่ (ใช้ staging mode)
# แก้ไข init-letsencrypt.sh: staging=1
./init-letsencrypt.sh

# ตรวจสอบว่า domain ชี้ไปที่ IP ที่ถูกต้อง
dig your-domain.com
```

### 5. "502 Bad Gateway" Error

```bash
# ตรวจสอบว่า web-prod container กำลังรันอยู่
docker compose --profile prod ps web-prod

# ตรวจสอบ logs
docker compose --profile prod logs web-prod

# Restart web-prod
docker compose --profile prod restart web-prod

# ตรวจสอบว่า gunicorn กำลังรันอยู่
docker compose --profile prod exec web-prod ps aux | grep gunicorn
```

### 6. Out of Memory

```bash
# ตรวจสอบ memory usage
free -h
docker stats

# ถ้า RAM ไม่พอ ให้เพิ่ม swap
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

# ทำให้ swap ถาวร
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

### 7. Port Already in Use

```bash
# ตรวจสอบว่า process ไหนใช้ port 80/443
sudo lsof -i :80
sudo lsof -i :443

# Kill process (ถ้าจำเป็น)
sudo kill -9 PID

# หรือ stop apache/nginx ที่อาจรันอยู่
sudo systemctl stop apache2
sudo systemctl stop nginx
```

### 8. Permission Denied Errors

```bash
# ตรวจสอบ ownership
ls -la ~/apps/Uncle-Engineer-E-Book/

# แก้ไข permissions ถ้าจำเป็น
sudo chown -R $USER:$USER ~/apps/Uncle-Engineer-E-Book/

# ตรวจสอบ Docker permissions
docker ps
# ถ้า permission denied, เพิ่ม user เข้า docker group
sudo usermod -aG docker $USER
# Logout และ login ใหม่
```

### 9. DNS Not Propagating

```bash
# ตรวจสอบ DNS
dig your-domain.com
nslookup your-domain.com

# ใช้ Google DNS เพื่อตรวจสอบ
dig @8.8.8.8 your-domain.com

# Test กับ IP โดยตรงก่อน
curl http://YOUR_DROPLET_IP
```

### 10. Can't Create Superuser

```bash
# ตรวจสอบว่า database พร้อมหรือยัง
docker compose --profile prod exec db-prod pg_isready

# รัน migrations
docker compose --profile prod exec web-prod python manage.py migrate

# ลองสร้าง superuser อีกครั้ง
docker compose --profile prod exec web-prod python manage.py createsuperuser

# หรือสร้างผ่าน shell
docker compose --profile prod exec web-prod python manage.py shell
# แล้วรันใน shell:
# from django.contrib.auth import get_user_model
# User = get_user_model()
# User.objects.create_superuser('admin', 'admin@example.com', 'password')
```

---

## Best Practices

### Security

1. **ใช้ Strong Passwords**
   - Database password
   - Django secret key
   - Superuser password

2. **อัพเดท Firewall Rules**
   ```bash
   sudo ufw default deny incoming
   sudo ufw default allow outgoing
   sudo ufw allow 22/tcp
   sudo ufw allow 80/tcp
   sudo ufw allow 443/tcp
   sudo ufw enable
   ```

3. **ปิด Debug Mode ใน Production**
   - ตรวจสอบว่า `DEBUG=False` ใน settings

4. **ใช้ Environment Variables**
   - อย่า commit `.env.prod` เข้า git
   - ใช้ `.env.example` แทน

5. **Regular Security Updates**
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

### Performance

1. **Enable Nginx Caching** (ถ้าจำเป็น)
2. **Use CDN** สำหรับ static files
3. **Monitor Resources** อย่างสม่ำเสมอ
4. **Scale Up/Out** เมื่อ traffic เพิ่มขึ้น

### Backup

1. **Automatic Database Backups** (ทุกวัน)
2. **Store Backups Off-site** (S3, Dropbox, etc.)
3. **Test Restore Procedure** เป็นประจำ
4. **Backup Media Files** ด้วย

### Monitoring

1. **Setup Logging**
   ```bash
   # ดู logs
   tail -f ~/apps/Uncle-Engineer-E-Book/logs/*.log
   ```

2. **Monitor Disk Space**
   ```bash
   df -h
   ```

3. **Monitor SSL Expiration**
   ```bash
   docker compose --profile prod exec certbot certbot certificates
   ```

4. **Use Monitoring Tools** (Optional)
   - Uptime Robot (ฟรี)
   - Sentry (error tracking)
   - New Relic
   - Datadog

---

## Useful Commands Reference

### Docker Compose

```bash
# Production commands
docker compose --profile prod up -d              # Start services
docker compose --profile prod down               # Stop services
docker compose --profile prod ps                 # List services
docker compose --profile prod logs -f            # View logs
docker compose --profile prod build              # Build images
docker compose --profile prod restart            # Restart services
docker compose --profile prod exec SERVICE CMD   # Run command in service

# Specific services
docker compose --profile prod restart web-prod
docker compose --profile prod logs -f nginx
docker compose --profile prod exec web-prod bash
```

### Django Management

```bash
# Run Django commands
docker compose --profile prod exec web-prod python manage.py COMMAND

# Common commands
docker compose --profile prod exec web-prod python manage.py migrate
docker compose --profile prod exec web-prod python manage.py createsuperuser
docker compose --profile prod exec web-prod python manage.py collectstatic --noinput
docker compose --profile prod exec web-prod python manage.py shell
docker compose --profile prod exec web-prod python manage.py dbshell
```

### Database

```bash
# Access PostgreSQL
docker compose --profile prod exec db-prod psql -U uncleebook uncleebook_prod

# Backup
docker compose --profile prod exec db-prod pg_dump -U uncleebook uncleebook_prod > backup.sql

# Restore
cat backup.sql | docker compose --profile prod exec -T db-prod psql -U uncleebook uncleebook_prod

# Check connection
docker compose --profile prod exec db-prod pg_isready
```

### Nginx

```bash
# Test configuration
docker compose --profile prod exec nginx nginx -t

# Reload
docker compose --profile prod exec nginx nginx -s reload

# View config
docker compose --profile prod exec nginx cat /etc/nginx/conf.d/uncleebook.conf
```

### SSL/Certbot

```bash
# List certificates
docker compose --profile prod exec certbot certbot certificates

# Renew certificates
docker compose --profile prod run --rm certbot renew

# Test renewal
docker compose --profile prod run --rm certbot renew --dry-run
```

---

## ติดต่อและ Support

หากมีปัญหาหรือคำถาม:

1. ตรวจสอบ [Troubleshooting](#troubleshooting) section
2. ดู logs: `docker compose --profile prod logs -f`
3. ติดต่อทีมพัฒนา

---

## License

Copyright © 2024 Uncle Engineer E-Book Project


เจอแล้วครับ! มีไฟล์ nginx config 2 ไฟล์ที่ประกาศ upstream django ซ้ำกัน:
  - uncleebook-http.conf
  - uncleebook.conf

  ให้ตรวจสอบว่าไฟล์ไหนใช้งาน:

  บน server:

  # ดูเนื้อหา uncleebook-http.conf
  cat ~/uncleebook/Uncle-Engineer-E-Book/nginx/conf.d/uncleebook-http.conf

  วิธีแก้: ลบไฟล์ uncleebook-http.conf ออก (เพราะเราใช้ uncleebook.conf ที่มีทั้ง HTTP
  และ HTTPS แล้ว):

  # ลบไฟล์ที่ไม่ใช้
  rm ~/uncleebook/Uncle-Engineer-E-Book/nginx/conf.d/uncleebook-http.conf

  # ตรวจสอบว่าเหลือแค่ไฟล์เดียว
  ls ~/uncleebook/Uncle-Engineer-E-Book/nginx/conf.d/

  # Restart nginx
  docker compose restart nginx

  # ดู logs
  docker compose logs nginx --tail=20

  # ทดสอบ
  curl -I https://uncle-ebook.com

  ลองรันตามลำดับแล้วบอกผลครับ