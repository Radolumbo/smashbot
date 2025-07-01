pye# Idempotent bootstrapping script -- Note, as of 7/1/2025, this is pretty out of date, I think.

# If not using desktop docker, uncomment:
# NOTE: this might be out of date, not bothering updating it (7/1/2025)
# if [ -f "/usr/share/keyrings/docker-archive-keyring.gpg" ]; then
#     echo "Docker keyring already downloaded"
# else
#     curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
# fi

# echo \
# "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
# $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get -y update
sudo apt-get -y install build-essential
sudo apt-get -y install python3.13
# commenting out DB stuff for now (7/1/2025)
sudo apt-get -y install python3-dev # libpq-dev postgresql-client-common
# sudo apt-get -y install postgresql-client

# Added on 7/1/2025, but not really super tested. Taken from https://github.com/pyenv/pyenv/wiki#suggested-build-environment
sudo apt update; sudo apt install make build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev curl git \
libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev

sudo apt-get -y install \
    apt-transport-https \
    ca-certificates \
    curl \
    # gnupg \
    lsb-release
# If not using desktop docker, uncomment:
# sudo apt-get -y install docker-ce docker-ce-cli containerd.io


if [ -d "venv/" ]; then
    echo "venv/ already exists"
else
    python3 -m venv venv/
fi

# Database instructions are super out of date, and I don't want to host a DB
# for now, anyway.  (7/1/2025)

# sudo mkdir -p ~/tmpsmashdb/data
# sudo docker pull postgres:alpine
# docker rm smashdb
# sudo docker run --name smashdb -d -p 5432:5432 -v postgres-volume:/var/lib/postgresql/data -e POSTGRES_PASSWORD=smash postgres:alpine

# PGPASSWORD=smash psql -h localhost -U postgres -tc \
#   "SELECT 1 FROM pg_database WHERE datname = 'smashdb'" | grep -q 1 || \
#    PGPASSWORD=smash psql -h localhost -U postgres -c "CREATE DATABASE smashdb"

# PGPASSWORD=smash psql -h localhost -d smashdb -U postgres -f sql/schemas.sql
# PGPASSWORD=smash psql -h localhost -d smashdb -U postgres -f sql/player.sql
# PGPASSWORD=smash psql -h localhost -d smashdb -U postgres -f sql/fighter.sql
# PGPASSWORD=smash psql -h localhost -d smashdb -U postgres -f sql/player_fighter.sql
# PGPASSWORD=smash psql -h localhost -d smashdb -U postgres -f sql/player_fighter_mod1.sql
# PGPASSWORD=smash psql -h localhost -d smashdb -U postgres -f sql/guild_member.sql
# PGPASSWORD=smash psql -h localhost -d smashdb -U postgres -f sql/fighter_alias.sql

# filepath="sql/fighter_dlc*.sql"
# for file in $filepath
# do
#   PGPASSWORD=smash psql -h localhost -d smashdb -U postgres -f $file
# done

# filepath="sql/fighter_alias_dlc*.sql"
# for file in $filepath
# do
#   PGPASSWORD=smash psql -h localhost -d smashdb -U postgres -f $file
# done

# PGPASSWORD=smash psql -h localhost -U postgres -tc \
#   "SELECT 1 FROM pg_roles WHERE rolname='smashbot'" | grep -q 1 || \
#    PGPASSWORD=smash psql -h localhost -U postgres -c "CREATE USER smashbot"

# PGPASSWORD=smash psql -h localhost -d smashdb -U postgres -c "GRANT USAGE ON SCHEMA player TO smashbot"
# PGPASSWORD=smash psql -h localhost -d smashdb -U postgres -c "GRANT USAGE ON SCHEMA fighter TO smashbot"
# PGPASSWORD=smash psql -h localhost -d smashdb -U postgres -c "GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA player TO smashbot"
# PGPASSWORD=smash psql -h localhost -d smashdb -U postgres -c "GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA fighter TO smashbot"
# PGPASSWORD=smash psql -h localhost -d smashdb -U postgres -c "GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA player TO smashbot;"
# PGPASSWORD=smash psql -h localhost -d smashdb -U postgres -c "GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA fighter TO smashbot;"

source venv/bin/activate
pip install -r requirements.txt
