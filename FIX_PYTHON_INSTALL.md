# 🔧 Fix Python Installation on Server

The server doesn't have Python 3.11 in the default repositories. Let's fix this step by step.

## Option 1: Install Python 3.11 from deadsnakes PPA

Run these commands on your server:

```bash
# Add deadsnakes PPA for Python 3.11
sudo apt update
sudo apt install -y software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update

# Now install Python 3.11
sudo apt install -y python3.11 python3.11-venv python3.11-dev python3.11-distutils

# Install pip for Python 3.11
curl -sS https://bootstrap.pypa.io/get-pip.py | python3.11
```

## Option 2: Use Available Python Version (Simpler)

If Option 1 doesn't work, let's use whatever Python version is available:

```bash
# Check what Python versions are available
python3 --version
ls /usr/bin/python*

# Install the available Python version packages
sudo apt install -y python3 python3-venv python3-dev python3-pip

# Verify installation
python3 --version
pip3 --version
```

## Option 3: Install Python 3.11 from Source (If needed)

If the above options don't work:

```bash
# Install build dependencies
sudo apt update
sudo apt install -y build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev curl libbz2-dev

# Download Python 3.11 source
cd /tmp
wget https://www.python.org/ftp/python/3.11.6/Python-3.11.6.tgz
tar -xf Python-3.11.6.tgz
cd Python-3.11.6

# Configure and install
./configure --enable-optimizations
make -j 8
sudo make altinstall

# Create symlink
sudo ln -sf /usr/local/bin/python3.11 /usr/bin/python3.11
```

## Continue with the Setup

Once Python is installed, continue with the rest of the setup:

```bash
# Install PostgreSQL (this should work)
sudo apt install -y postgresql postgresql-contrib postgresql-client

# Install Node.js 18 LTS
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Install Nginx
sudo apt install -y nginx

# Install PM2 and serve
sudo npm install -g pm2 serve

# Install UFW firewall
sudo apt install -y ufw
```

## Test Python Installation

```bash
# Test Python
python3 --version
python3 -m venv --help

# If you installed Python 3.11 specifically
python3.11 --version
python3.11 -m venv --help
```

Choose the option that works best for your server and continue with the setup!
