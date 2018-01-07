#!/usr/bin/python
import os, traceback, ConfigParser, json, time, Adafruit_DHT, datetime, signal
from urllib import urlopen
from pymongo import MongoClient

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

path = LOG_FILE_PATH
logfile = open(path, 'a')
now = datetime.datetime.utcnow()

def insertToDatabase(reading):
  try:
    connection = MongoClient(DB_HOST, DB_PORT)
    db = connection[DB_NAME]
    db.authenticate(DB_USER, DB_PASS)
    collection = db[DB_COLL]
    collection.insert(reading)
    connection.close()
  except:
    print "Error connecting to mlab"
    reading['date'] = str(reading['date'])

    logfile.write('\n------------------------\n\n')
    logfile.write('ERROR CONNECTING TO MLAB\n')
    logfile.write(now.strftime('%d %b %H:%M'))
    logfile.write('\nData:')
    logfile.write(json.dumps(reading))
    logfile.write('\n')
    logfile.write('\n')
    logfile.write(traceback.format_exc())
    raise

api = "http://api.openweathermap.org/data/2.5/weather?"
lat = "lat=" + str(MY_LAT)
lon = "lon=" + str(MY_LON)
units = "units=" + 'metric'
apikey = OPEN_WEATHER_KEY
urlString = ''.join([api, lat, "&", lon, "&appid=", apikey, "&", units])

outdoorWeather = json.loads(urlopen(urlString).read())
outdoorTemp = outdoorWeather['main']['temp']
outdoorHumidity = outdoorWeather['main']['humidity']
humidity, temperature = Adafruit_DHT.read_retry(11, 4)
data = 'Temp: {0:0.1f} C  Humidity: {1:0.1f} %'.format(temperature, humidity)
print now, data, outdoorTemp, outdoorHumidity
reading = {"temp": temperature,
          "humidity" : humidity,
          "outdoorTemp" : outdoorTemp,
          "outdoorHumidity" : outdoorHumidity,
          "date": now }
insertToDatabase(reading)
