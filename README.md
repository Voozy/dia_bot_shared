# Telegram bot for tracking blood sugar and creation reports

File ***bot.service*** contains setup for **SYSTEMD** application. **SYSTEMD** application allows to keep bot in active status. 
The application will re-start BOT after failure or telegram server re-start.

In order to install **SYSTEMD** app need to run this command:

+ _apt-get install systemd_

File ***bot.service***  should be placed in this folder on server /etc/systemd/system

File ***SugarBot.py*** contains main body of bot. Starting by **SYSTEMD** and running always.
File ***Sugar_DB.py*** contains code for creation Data Base and necessary tables on Server. Need to start only once!
You need to create file ***config.py*** with telegram bot token and place in the same folder when ***SugarBot.py*** stored.
Code of ***config.py*** should be like:
```python
token = 'XXXXXXXXXXXXXXX'
```
Main script will import ***confing.py*** and get token for connection.

File ***SugarSql.py*** contains functions for Insert to DB and Select from DB

In order to setup **Python and TelegramAPI** on Ubuntu server need to run these commands:

+ apt-get update
+ apt-get install python3
+ apt-get install python3-setuptools
+ apt-get install python3-pip
+ pip3 install pyTelegramBotAPI

## PAY YOUR ATTENTION - JUST IN CASE PLEASE UPDATE pyTelegramBotAPI AFTER INSTALATION:

+ pip3 install pyTelegramBotAPI --upgrade
