# SSL Certificate Setup for uncle-ebook.com

## Quick Start (HTTP Only - For Testing)

If you want to test the site first without HTTPS:

1. **Temporarily use HTTP-only config:**
   ```bash
   cd nginx/conf.d
   mv uncleebook.conf uncleebook-ssl.conf.backup
   mv uncleebook-http-only.conf.backup uncleebook.conf
   ```

2. **Start services:**
   ```bash
   docker compose --profile prod up -d
   ```

3. **Access via HTTP:**
   - http://uncle-ebook.com

## SSL Setup (HTTPS - Production)

### Prerequisites
- Domain must point to your server IP
- Ports 80 and 443 must be open
- Email address for Let's Encrypt notifications

### Step 1: Prepare Configuration

1. **Edit init-letsencrypt.sh** and change the email:
   ```bash
   nano init-letsencrypt.sh
   ```
   Update this line:
   ```bash
   email="your-email@example.com"  # Change to your actual email
   ```

2. **Make script executable:**
   ```bash
   chmod +x init-letsencrypt.sh
   ```

### Step 2: Restore SSL-enabled Nginx Config

Make sure you're using the SSL-enabled config:
```bash
cd nginx/conf.d
# If you switched to HTTP-only, restore SSL config:
mv uncleebook.conf uncleebook-http-only.conf.backup
mv uncleebook-ssl.conf.backup uncleebook.conf
```

### Step 3: Run SSL Certificate Setup

```bash
./init-letsencrypt.sh
```

This script will:
1. Create dummy certificates
2. Start nginx
3. Request real certificates from Let's Encrypt
4. Reload nginx with real certificates

### Step 4: Verify HTTPS

Your site should now be accessible via:
- https://uncle-ebook.com
- https://www.uncle-ebook.com

HTTP traffic will automatically redirect to HTTPS.

## Certificate Renewal

Certificates auto-renew via the certbot container (checks twice daily).

To manually renew:
```bash
docker compose --profile prod run --rm certbot renew
docker compose --profile prod exec nginx nginx -s reload
```

## Troubleshooting

### "Connection refused" error
1. Check containers are running:
   ```bash
   docker compose --profile prod ps
   ```

2. Check nginx logs:
   ```bash
   docker compose --profile prod logs nginx
   ```

3. Verify ports are accessible:
   ```bash
   sudo netstat -tlnp | grep -E ':(80|443)'
   ```

### SSL certificate errors
1. Check certbot logs:
   ```bash
   docker compose --profile prod logs certbot
   ```

2. Verify domain DNS:
   ```bash
   dig uncle-ebook.com
   ```

3. Test with staging first (edit init-letsencrypt.sh, set `staging=1`)
