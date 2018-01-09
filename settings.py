# check hostname and use configparser on local machine and raspi
# use os.environ on glitch.com

import os, ConfigParser

configParser = ConfigParser.RawConfigParser()
configParser.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'config.ini'))

hostname = os.environ.get('COMPUTERNAME') or os.environ.get('HOSTNAME')

if (hostname == 'MARIGERR-PC' or hostname == 'raspberrypi'):
  DB_HOST = configParser.get('DATABASE', 'DB_HOST')
  DB_PORT = configParser.getint('DATABASE', 'DB_PORT')
  DB_NAME = configParser.get('DATABASE', 'DB_NAME')
  DB_USER = configParser.get('DATABASE', 'DB_USER')
  DB_PASS = configParser.get('DATABASE', 'DB_PASS')
  DB_COLL = configParser.get('DATABASE', 'DB_COLL')
  MY_LAT = configParser.getfloat('LOCATION', 'MY_LAT')
  MY_LON = configParser.getfloat('LOCATION', 'MY_LON')
  OPEN_WEATHER_KEY = configParser.get('APIKEYS', 'OPEN_WEATHER_KEY')
  LOG_FILE_PATH = configParser.get('LOGGING', 'LOG_FILE_PATH')
  HOST = 'RASPI'
else:
  DB_HOST = os.environ.get('DB_HOST')
  DB_PORT = int(os.environ.get('DB_PORT'))
  DB_NAME = os.environ.get('DB_NAME')
  DB_USER = os.environ.get('DB_USER')
  DB_PASS = os.environ.get('DB_PASS')
  DB_COLL = os.environ.get('DB_COLL')
  HOST = 'GLITCH'