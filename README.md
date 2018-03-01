## Track Humidity and Temperature with Raspberry Pi and DHT11 sensor

Run ```Tracker.py``` script as cron task  
Setup with ```crontab -e```  
View existing tasks with ```crontab -l```

Example below runs every 4 hours everyday  
More info at https://www.raspberrypi.org/documentation/linux/usage/cron.md

```
0 0 * * *  python ~/Absolute/Path/To/tracker.py   
0 4 * * *  python ~/Absolute/Path/To/tracker.py  
0 8 * * *  python ~/Absolute/Path/To/tracker.py  
0 12 * * *  python ~/Absolute/Path/To/tracker.py  
0 16 * * *  python ~/Absolute/Path/To/tracker.py  
0 20 * * *  python ~/Absolute/Path/To/tracker.py  
```

## View Chart of data
Start dev server that reloads with saves by navigating to project folderin bash terminal thens
```
$ export FLASK_APP=server.py
$ export FLASK_DEBUG=1
$ flask run
```
Start server with ```python server.py```  
Can run server on Rasp Pi and then view chart from other machines on local network using Rasp Pi's ip address and default port 5000.

## Start chart server at Raspberry Pi boot

Add service to systemd to run ```server.py``` when starting up Rasp Pi and restart if fails.  
Instructions at:  https://www.raspberrypi.org/documentation/linux/usage/systemd.md

Example of chartserver.service
```
[Unit]
Description=ChartHumidityTempData
After=network.target

[Service]
ExecStart=/usr/bin/python2.7 -u server.py
WorkingDirectory=/Absolute/Path/To/Server/Folder
StandardOutput=inherit
StandardError=inherit
Restart=always
RestartSec=10
User=pi

[Install]
WantedBy=multi-user.target
```

After copying into systemd folder and enabling, will receive confirmation msg:   
```Created symlink /etc/systemd/system/multi-user.target.wants/chartserver.service → /lib/systemd/system/chartserver.service.```