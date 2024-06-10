#!/bin/bash
apt-get update
apt install software-properties-common -y
add-apt-repository ppa:freecad-maintainers/freecad-stable -y
apt-get update
apt-get install freecad xvfb  -y
apt install x11-apps -y
apt-get install graphicsmagick-imagemagick-compat -y
apt install curl unzip -y
curl -fsSL https://deb.nodesource.com/setup_20.x -o nodesource_setup.sh
chmod +x nodesource_setup.sh
./nodesource_setup.sh
apt-get install -y nodejs
node -v