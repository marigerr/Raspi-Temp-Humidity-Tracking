import json, pygal, ConfigParser, datetime
from pygal.style import Style
from bson import json_util, ObjectId
import pymongo
from pymongo import MongoClient
from flask import Flask, render_template

configParser = ConfigParser.RawConfigParser()   
configParser.read('config.ini')

DB_HOST = configParser.get('DATABASE', 'DB_HOST')
DB_PORT = configParser.getint('DATABASE', 'DB_PORT')
DB_NAME = configParser.get('DATABASE', 'DB_NAME')
DB_USER = configParser.get('DATABASE', 'DB_USER')
DB_PASS = configParser.get('DATABASE', 'DB_PASS')
DB_COLL = configParser.get('DATABASE', 'DB_COLL')

connection = MongoClient(DB_HOST, DB_PORT)
db = connection[DB_NAME]
db.authenticate(DB_USER, DB_PASS)
collection = db[DB_COLL]

app = Flask(__name__)
@app.route('/')
def chart():
  humidity = []
  temp = []
  outdoorTemp = []
  outdoorHumidity = []
  date = []

  results = json.loads(json_util.dumps(collection.find()))

  for result in results:
    humidity.append(result['humidity'])
    temp.append(result['temp'])
    outdoorTemp.append(result['outdoorTemp'])
    outdoorHumidity.append(result['outdoorHumidity'])
    date.append(datetime.datetime.fromtimestamp(result['date']['$date']/1000).strftime('%d %b %H:00'))

  custom_style = Style(
    font_family ='Raleway, sans-serif',
    background='transparent'
  )
  chart = pygal.Line(truncate_legend=50, x_label_rotation=45, height=300, style=custom_style)
  chart.x_labels = date
  chart.title = 'Humidity & Temperature'
  chart.add('Rel Humidity Outdoors (%)', outdoorHumidity)
  chart.add('Rel Humidity Indoors (%)', humidity)
  chart.add('Temp Indoors (C)', temp)
  chart.add('Temp Outdoors (C)', outdoorTemp)
  last = len(humidity) - 1
  current = { 'humidity': humidity[last], 'temp': temp[last], 'outdoorHumidity': outdoorHumidity[last], 'outdoorTemp': outdoorTemp[last], 'date': date[last] }

  chart = chart.render_data_uri()
  return render_template( 'chart.html', chart = chart, current = current)

@app.route('/latest')
def current():
    current = json.loads(json_util.dumps(collection.find().sort("date", pymongo.DESCENDING).limit(1)))[0]
    current['date'] = datetime.datetime.fromtimestamp(current['date']['$date']/1000).strftime('%d %b %H:00')
    return render_template( 'latest.html', current = current)

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')
