import os,json, pygal, arrow, lxml
from pygal.style import Style
from bson import json_util, ObjectId
import pymongo
from pymongo import MongoClient
from flask import Flask, render_template
import settings
# import logging
# logging.basicConfig(level=logging.DEBUG)

connection = MongoClient(settings.DB_HOST, settings.DB_PORT)
db = connection[settings.DB_NAME]
db.authenticate(settings.DB_USER, settings.DB_PASS)
collection = db[settings.DB_COLL]

app = Flask(__name__, static_folder='static', template_folder='templates')

@app.route('/')
def chart():
  humidity = []
  temp = []
  outdoorTemp = []
  outdoorHumidity = []
  date = []
  x_labels_major = []

  ### add pagination later ###
  # count = collection.find().count()
  # print(count/21)

  shiftamount = 21
  threeweeksago = arrow.utcnow().shift(days=-shiftamount).datetime

  results = json.loads(json_util.dumps(collection.find({"date" : { "$gte" : threeweeksago}})))
  for result in results:
    humidity.append(result['humidity'])
    temp.append(result['temp'])
    outdoorTemp.append(result['outdoorTemp'])
    outdoorHumidity.append(result['outdoorHumidity'])
    date.append(arrow.get(result['date']['$date']/1000).to('Europe/Stockholm').format('DD MMM HH:00'))
    if (len(x_labels_major) == 0 or x_labels_major[len(x_labels_major)-1][:6] != date[len(date)-1][:6]):
      x_labels_major.append(date[len(date)-1])

  custom_style = Style(
    font_family ='Raleway, sans-serif',
    background='transparent'
  )

  chart = pygal.Line(truncate_legend=50, x_label_rotation=45, height=300, style=custom_style, show_minor_x_labels=False)
  chart.x_labels = date
  chart.x_labels_major = x_labels_major
  chart.title = 'Humidity & Temperature'
  chart.add('Rel Humidity Outdoors (%)', outdoorHumidity)
  chart.add('Rel Humidity Indoors (%)', humidity)
  chart.add('Temp Indoors (C)', temp)
  chart.add('Temp Outdoors (C)', outdoorTemp)
  last = len(humidity) - 1
  current = { 'humidity': humidity[last], 'temp': temp[last], 'outdoorHumidity': outdoorHumidity[last], 'outdoorTemp': outdoorTemp[last], 'date': date[last] }

  chart = chart.render_data_uri()
  return render_template( 'chart.html', chart = chart, current = current, host = settings.HOST)

@app.route('/table')
def table():
  humidity = []
  temp = []
  outdoorTemp = []
  outdoorHumidity = []
  date = []
  x_labels_major = []

  results = json.loads(json_util.dumps(collection.find().sort([("date", pymongo.DESCENDING)])))
  for result in results:
    humidity.append(result['humidity'])
    temp.append(result['temp'])
    outdoorTemp.append(result['outdoorTemp'])
    outdoorHumidity.append(result['outdoorHumidity'])
    date.append(arrow.get(result['date']['$date']/1000).to('Europe/Stockholm').format('DD MMM HH:00'))
    if (date[len(date)-1].find('00:00') != -1):
      x_labels_major.append(date[len(date)-1])

  chart = pygal.Line()
  chart.x_labels = date
  chart.x_labels_major = x_labels_major
  chart.title = 'Humidity & Temperature'
  chart.add('Temp Indoors (C)', temp)
  chart.add('Rel Humidity Indoors (%)', humidity)
  chart.add('Temp Outdoors (C)', outdoorTemp)
  chart.add('Rel Humidity Outdoors (%)', outdoorHumidity)

  return render_template( 'table.html', chart = chart, current = current, host = settings.HOST)


@app.route('/latest')
def current():
    current = json.loads(json_util.dumps(collection.find().sort("date", pymongo.DESCENDING).limit(1)))[0]
    current['date'] = arrow.get(result['date']['$date']/1000).to('Europe/Stockholm').format('DD MMM HH:00')
    return render_template( 'latest.html', current = current)

if __name__ == '__main__':
	app.run()
