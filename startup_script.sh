#! /bin/bash

git_path=/bin/smashbot

# Libs for python
sudo apt -y install libssl-dev libncurses5-dev libsqlite3-dev libreadline-dev libgdm-dev libdb4o-cil-dev libpcap-dev libffi-dev zlib1g-dev libbz2-dev libpq-dev liblzma-dev

sudo apt-get -y install wget

# Python
if ! /usr/local/bin/python3 -V | grep -q "Python 3.7.6"; then
    wget https://www.python.org/ftp/python/3.7.6/Python-3.7.6.tgz
    tar -xvf Python-3.7.6.tgz
    cd Python-3.7.6
    sudo apt -y install gcc make
    ./configure
    sudo make
    sudo make install
else
    echo "Python 3.7.6 already installed."
fi

# Git
sudo apt-get -y install git

if [ ! -d "$git_path" ]; then
    sudo mkdir "$git_path"
fi

if [ ! -d "$git_path/.git" ]; then
    sudo gcloud source repos clone github_radolumbo_smashbot $git_path
fi

cd $git_path
sudo git pull

sudo pip3 install --upgrade -r "$git_path/requirements.txt"

sudo cp "$git_path/smashbot.service" /etc/systemd/system/smashbot.service

sudo systemctl daemon-reload

sudo systemctl start smashbot