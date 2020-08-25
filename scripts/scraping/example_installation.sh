# This exact script is the one originally used for
# configuring Chrome and Chromedriver on an Ubuntu
# system on amd64 hardware.
echo "installing chrome beta 84.0.4147.45-1 ... "
wget https://repo.debiancn.org/pool/main/g/google-chrome-beta/google-chrome-beta_84.0.4147.45-1_amd64.deb
sudo dpkg -i google-chrome-beta_84.0.4147.45-1_amd64.deb

echo "getting corresponding version of chromedriver ... "
wget https://chromedriver.storage.googleapis.com/84.0.4147.30/chromedriver_linux64.zip
unzip chromedriver_linux64

echo "installing required packages ... "
pip install -r requirements.txt
