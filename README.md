1. Load ec2.micro instance ubuntu

2. 
```
sudo apt update && sudo apt upgrade
```

3. 
```
sudo apt install git docker.io
```

4. 
```
sudo curl -L "https://github.com/docker/compose/releases/download/1.26.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```

5. 
```
sudo chmod +x /usr/local/bin/docker-compose
```

6. 
```
git clone https://github.com/whs2k/stockFries.git && cd stockFries
```

7. 
```
pip install -r requirements.txt
```

8. 
```
crontab -e
```

8.5 (from within crontab)
```
* * 7 * * /usr/bin/python /home/ubuntu/stockFries/app/scraper.py > /var/log/cron.log 2>&1
```

9. Spinup docker instance (run as is to make sure there are no errors thrown. In general you can append the -d flag to run silently in the background)
```
sudo docker-compose up
```

