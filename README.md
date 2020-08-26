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
crontab -e
```

7.5 (from within crontab)
```
* * 7 * * /usr/bin/python /home/ubuntu/stockFries/app/scraper.py > /var/log/cron.log 2>&1
```

8. Spinup docker instance
```
sudo docker-compose -d up
```

