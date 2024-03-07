#!/usr/bin/env bash
# Script sets up my web servers for the deployment of web_static

if ! command -v nginx &>/dev/null; then
    sudo apt-get update
    sudo apt-get install -y nginx
fi

sudo mkdir -p /data/web_static/{releases/test,shared}

echo "<!DOCTYPE html><html><head><title>Test Page</title></head><body><h1>Holberton School</h1></body></html>" | sudo tee /data/web_static/releases/test/index.html >/dev/null

sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

sudo chown -R ubuntu:ubuntu /data/

sudo sed -i '/^server {/a \
    location /hbnb_static/ {\
        alias /data/web_static/current/;\
    }' /etc/nginx/sites-available/default

sudo service nginx restart

exit 0
