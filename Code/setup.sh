sudo apt update
sudo apt upgrade -y
sudo apt install supervisor -y
sudo apt install python3-pip -y
pip3 install -r bot_req.txt
sudo cp supervisor-bot.conf /etc/supervisor/conf.d/
sudo supervisorctl reload