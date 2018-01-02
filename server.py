import json, pygal, ConfigParser, datetime
from bson import json_util, ObjectId
from pymongo import MongoClient
from flask import Flask

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
    date.append(datetime.datetime.fromtimestamp(result['date']['$date']/1000).strftime('%b %d kl %H'))

  chart = pygal.Line(truncate_legend=50, explicit_size = True, x_label_rotation=20)
  chart.x_labels = date
  chart.title = 'Humidity & Temperature'
  chart.add('Humidity Outdoors', outdoorHumidity)
  chart.add('Humidity Indoor', humidity)
  chart.add('Temp Indoor', temp)
  chart.add('Temp Outdoors', outdoorTemp)
  return chart.render_response()

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')
