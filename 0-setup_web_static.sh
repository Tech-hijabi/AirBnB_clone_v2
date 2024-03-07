#!/usr/bin/env bash
# Script sets up my web servers for the deployment of web_static

if ! command -v nginx &>/dev/null; then
    sudo apt-get update
    sudo apt-get install -y nginx
fi

sudo ufw allow 'Nginx HTTP'

sudo mkdir -p /data/web_static/{releases/test,shared}

cat << EOF | sudo tee /data/web_static/releases/test/index.html >/dev/null
<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>
EOF


sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

sudo chown -R ubuntu:ubuntu /data/

sudo sed -i '/^server {/a \
    location /hbnb_static/ {\
        alias /data/web_static/current/;\
    }' /etc/nginx/sites-available/default

sudo service nginx restart

exit 0
