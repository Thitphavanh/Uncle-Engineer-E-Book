#!/bin/bash

# Initialize Let's Encrypt SSL certificates for uncle-ebook.com

set -e

domains=(uncle-ebook.com www.uncle-ebook.com)
rsa_key_size=4096
data_path="./certbot"
email="your-email@example.com" # Change this to your email
staging=0 # Set to 1 for testing

echo "### Preparing directories ..."
mkdir -p "$data_path/conf"
mkdir -p "$data_path/www"

if [ -d "$data_path/conf/live/${domains[0]}" ]; then
  read -p "Existing data found for ${domains[0]}. Continue and replace existing certificate? (y/N) " decision
  if [ "$decision" != "Y" ] && [ "$decision" != "y" ]; then
    exit
  fi
fi

echo "### Creating dummy certificate for ${domains[0]} ..."
path="/etc/letsencrypt/live/${domains[0]}"
mkdir -p "$data_path/conf/live/${domains[0]}"
docker compose --profile prod run --rm --entrypoint "\
  openssl req -x509 -nodes -newkey rsa:$rsa_key_size -days 1\
    -keyout '$path/privkey.pem' \
    -out '$path/fullchain.pem' \
    -subj '/CN=localhost'" certbot
echo

echo "### Starting nginx ..."
docker compose --profile prod up -d nginx
echo

echo "### Deleting dummy certificate for ${domains[0]} ..."
docker compose --profile prod run --rm --entrypoint "\
  rm -Rf /etc/letsencrypt/live/${domains[0]} && \
  rm -Rf /etc/letsencrypt/archive/${domains[0]} && \
  rm -Rf /etc/letsencrypt/renewal/${domains[0]}.conf" certbot
echo

echo "### Requesting Let's Encrypt certificate for ${domains[0]} ..."
domain_args=""
for domain in "${domains[@]}"; do
  domain_args="$domain_args -d $domain"
done

# Select appropriate email arg
case "$email" in
  "") email_arg="--register-unsafely-without-email" ;;
  *) email_arg="--email $email" ;;
esac

# Enable staging mode if needed
if [ $staging != "0" ]; then staging_arg="--staging"; fi

docker compose --profile prod run --rm --entrypoint "\
  certbot certonly --webroot -w /var/www/certbot \
    $staging_arg \
    $email_arg \
    $domain_args \
    --rsa-key-size $rsa_key_size \
    --agree-tos \
    --force-renewal" certbot
echo

echo "### Reloading nginx ..."
docker compose --profile prod exec nginx nginx -s reload

echo "### SSL certificates have been successfully obtained!"
echo "### Your site should now be accessible via HTTPS"
