1. Load ec2.micro instance ubuntu

2. Add "User Data:" 
```
sudo apt -y update && sudo apt upgrade
sudo apt -y install git docker.io
sudo curl -L "https://github.com/docker/compose/releases/download/1.26.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
git clone https://github.com/whs2k/stockFries.git && cd stockFries
sudo apt -y install python-pip
yes | pip install -r requirements.txt
(crontab -l 2>/dev/null; echo "* * 7 * * /usr/bin/python /home/ubuntu/stockFries/app/scraper.py > /var/log/cron.log 2>&1") | crontab -#https://stackoverflow.com/questions/4880290/how-do-i-create-a-crontab-through-a-script
sudo docker-compose up #Spinup docker instance (run as is to make sure there are no errors thrown. In general you can append the -d flag to run silently in the background) ```

3. Check Docker Containers Running
```sudo docker-compose ps```

4. Stop and Clear Container
```sudo docker-compose down```

5. To test scraping:
cd /home/ubuntu/stockFries/app/ && python scraper.py
