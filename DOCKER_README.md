# Uncle E-Book - Docker Configuration Guide

## โครงสร้างโปรเจกต์

```
uncleebook/
├── uncleebook/
│   └── settings/
│       ├── __init__.py
│       ├── base.py      # การตั้งค่าพื้นฐานที่ใช้ร่วมกัน
│       ├── dev.py       # การตั้งค่าสำหรับ Development
│       └── prod.py      # การตั้งค่าสำหรับ Production
├── nginx/
│   ├── nginx.conf       # Nginx main configuration
│   └── conf.d/
│       └── uncleebook.conf  # Django app configuration
├── Dockerfile           # Production Dockerfile
├── Dockerfile.dev       # Development Dockerfile
├── docker-compose.yml   # Docker Compose configuration
├── .env.dev            # Development environment variables
├── .env.prod           # Production environment variables
├── .env.example        # Example environment variables
└── Makefile            # Commands shortcuts
```

## การเริ่มต้นใช้งาน

### 1. Development Environment

#### วิธีที่ 1: ใช้ Docker Compose โดยตรง

```bash
# สร้าง Docker images
docker compose --profile dev build

# รัน Development environment
docker compose --profile dev up -d

# ดู logs
docker compose --profile dev logs -f web-dev

# หยุดการทำงาน
docker compose --profile dev down
```

#### วิธีที่ 2: ใช้ Makefile (แนะนำ)

```bash
# สร้าง Docker images
make build-dev

# รัน Development environment
make up-dev

# ดู logs
make logs-dev

# หยุดการทำงาน
make down-dev
```

Development server จะรันที่: http://localhost:8000

### 2. Production Environment

#### วิธีที่ 1: ใช้ Docker Compose โดยตรง

```bash
# แก้ไข .env.prod ให้เหมาะสม
# สร้าง Docker images
docker compose --profile prod build

# รัน Production environment
docker compose --profile prod up -d

# ดู logs
docker compose --profile prod logs -f

# หยุดการทำงาน
docker compose --profile prod down
```

#### วิธีที่ 2: ใช้ Makefile (แนะนำ)

```bash
# แก้ไข .env.prod ให้เหมาะสม
# สร้าง Docker images
make build-prod

# รัน Production environment
make up-prod

# ดู logs
make logs-prod

# หยุดการทำงาน
make down-prod
```

Production server จะรันที่: http://localhost (ผ่าน Nginx)

## คำสั่งที่มีประโยชน์

### Development

```bash
# เข้า Django shell
make shell-dev
# หรือ
docker compose --profile dev exec web-dev python manage.py shell

# เข้า Bash shell
make bash-dev

# รัน migrations
make migrate-dev

# สร้าง superuser
make createsuperuser-dev

# รัน tests
make test

# Restart service
make restart-dev
```

### Production

```bash
# เข้า Django shell
make shell-prod

# เข้า Bash shell
make bash-prod

# รัน migrations
make migrate-prod

# สร้าง superuser
make createsuperuser-prod

# Restart service
make restart-prod
```

### ทั่วไป

```bash
# ดูคำสั่งทั้งหมด
make help

# ลบ Docker resources ทั้งหมด
make clean
```

## Environment Variables

### Development (.env.dev)

```bash
DJANGO_SETTINGS_MODULE=uncleebook.settings.dev
DJANGO_SECRET_KEY=django-insecure-dev-key-only-for-development
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

POSTGRES_DB=uncleebook_dev
POSTGRES_USER=uncleebook
POSTGRES_PASSWORD=uncleebook123
POSTGRES_HOST=db-dev
POSTGRES_PORT=5432
```

### Production (.env.prod)

```bash
DJANGO_SETTINGS_MODULE=uncleebook.settings.prod
DJANGO_SECRET_KEY=change-this-to-a-secure-random-secret-key
DJANGO_ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DJANGO_SECURE_SSL_REDIRECT=True

POSTGRES_DB=uncleebook_prod
POSTGRES_USER=uncleebook
POSTGRES_PASSWORD=strong-password-here
POSTGRES_HOST=db-prod
POSTGRES_PORT=5432

# Email settings
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@yourdomain.com
```

## ความแตกต่างระหว่าง Dev และ Prod

### Development
- ใช้ `runserver` สำหรับ hot-reload
- DEBUG=True
- SQLite หรือ PostgreSQL
- ALLOWED_HOSTS=['*']
- Console email backend
- No SSL/HTTPS enforced

### Production
- ใช้ Gunicorn + Nginx
- DEBUG=False
- PostgreSQL only
- ALLOWED_HOSTS ต้องระบุชัดเจน
- SMTP email backend
- SSL/HTTPS enforced
- WhiteNoise for static files
- Enhanced security settings

## การ Deploy Production

### 1. เตรียม Environment Variables

```bash
# คัดลอกและแก้ไข .env.prod
cp .env.example .env.prod
# แก้ไขค่าต่างๆ ใน .env.prod
```

### 2. สร้าง Secret Key

```python
# ใช้ Python เพื่อสร้าง Secret Key
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 3. Build และ Run

```bash
# Build images
make build-prod

# Start services
make up-prod

# Run migrations
make migrate-prod

# Create superuser
make createsuperuser-prod
```

### 4. ตรวจสอบ

```bash
# ดู logs
make logs-prod

# ตรวจสอบ health check
curl http://localhost/health/
```

## Troubleshooting

### ปัญหา: Database connection failed

```bash
# ตรวจสอบว่า database service กำลังรันอยู่
docker-compose --profile dev ps
# หรือ
docker-compose --profile prod ps

# ตรวจสอบ logs ของ database
docker-compose --profile dev logs db-dev
```

### ปัญหา: Static files ไม่แสดง

```bash
# Development
docker-compose --profile dev exec web-dev python manage.py collectstatic --noinput

# Production
docker-compose --profile prod exec web-prod python manage.py collectstatic --noinput
```

### ปัญหา: Port already in use

```bash
# ตรวจสอบว่า port 8000 หรือ 80 ถูกใช้งานอยู่
lsof -i :8000
lsof -i :80

# หยุด services ที่ใช้ port นั้นหรือเปลี่ยน port ใน docker-compose.yml
```

## Best Practices

1. **Never commit `.env` files** - ใช้ `.env.example` แทน
2. **Use strong passwords** สำหรับ production
3. **Regular backups** ของ database
4. **Monitor logs** อย่างสม่ำเสมอ
5. **Update dependencies** ให้เป็นปัจจุบัน
6. **Test in dev** ก่อน deploy ไป production

## Docker Commands Reference

```bash
# ดู running containers
docker ps

# ดู all containers
docker ps -a

# ดู logs ของ container
docker logs <container_name>

# เข้า container
docker exec -it <container_name> bash

# ลบ unused images
docker image prune

# ลบ unused volumes
docker volume prune

# ลบทุกอย่างที่ไม่ได้ใช้
docker system prune -a
```

## Support

หากมีปัญหาหรือคำถาม กรุณาติดต่อทีมพัฒนา
