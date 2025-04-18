echo "Installing system packages..."
sudo apt update -y && sudo apt install -y python3 python3-pip

echo " Now Installing Python dependencies...."
pip3 install requests pyOpenSSL pandas


echo " All dependencies has been installed successfully"
