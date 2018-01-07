import os, ConfigParser

configParser = ConfigParser.RawConfigParser()
configParser.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'config.ini'))

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
