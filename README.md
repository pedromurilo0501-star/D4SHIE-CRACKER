--Downloader
# Arch Linux / BlackArch / CachyOS
sudo pacman -S --noconfirm python python-pip
pip install figlet --break-system-packages
chmod +x painel.py && python painel.py

# Debian / Ubuntu / Kali / Mint
sudo apt update && sudo apt install -y python3 python3-pip
pip3 install figlet --break-system-packages
chmod +x painel.py && python3 painel.py

# Fedora / RHEL
sudo dnf install -y python3 python3-pip
pip3 install figlet --break-system-packages
chmod +x painel.py && python3 painel.py

# openSUSE
sudo zypper install -y python3 python3-pip
pip3 install figlet --break-system-packages
chmod +x painel.py && python3 painel.py

# Alpine Linux
sudo apk add --no-cache python3 py3-pip
pip3 install figlet --break-system-packages
chmod +x painel.py && python3 painel.py

# Gentoo
sudo emerge --ask dev-lang/python dev-python/pip
pip3 install figlet --break-system-packages
chmod +x painel.py && python3 painel.py
# CRAKER p1
chmod +x D4shieCrak.py.py
# CRAKER p2
cd Downloads && python3 D4shieCrak.py.py
