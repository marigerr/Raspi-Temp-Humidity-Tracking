#!/usr/bin/python
import traceback, json, time, Adafruit_DHT, datetime, signal
from urllib import urlopen
from pymongo import MongoClient
import settings

path = settings.LOG_FILE_PATH
logfile = open(path, 'a')
now = datetime.datetime.utcnow()

def insertToDatabase(reading):
  try:
    connection = MongoClient(settings.DB_HOST, settings.DB_PORT)
    db = connection[settings.DB_NAME]
    db.authenticate(settings.DB_USER, settings.DB_PASS)
    collection = db[settings.DB_COLL]
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
lat = "lat=" + str(settings.MY_LAT)
lon = "lon=" + str(settings.MY_LON)
units = "units=" + 'metric'
apikey = settings.OPEN_WEATHER_KEY
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
