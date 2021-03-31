# fake monster creator for mad and pokealarm
# sends an alert to pa and makes an entry into the db for the map
#
# remember i hate python, so this is very hacky
# adjust values that you see fit, if you have to ask you shouldn't bother
#
# tested only on pokealarm
# verified working on March 30, 2021

import json
import requests
from datetime import datetime
from datetime import timedelta
import mysql.connector
import random

#settings
pa_url = 'http://pa_ip:port'

body = {}
body['gender'] = 1
body['encounter_id'] = 123456
body['spawnpoint_id'] = some_id
body['cp'] = 281
body['cp_multiplier'] = 0.69
body['pokemon_id'] = 637
body['latitude'] = some_latitude
body['longitude'] = some_longitude
body['pokestop_id'] = 'some_stop_id'
body['move_1'] = 281
body['move_2'] = 133
body['height'] = 1.6
body['weight'] = 46
body["disappear_time_verified"] = 'true'
body['form'] = 0
body['last_modified_time'] = datetime.now().timestamp()
body["individual_defense"] = 15
body["individual_attack"] = 15
body["individual_stamina"] = 15
body["disappear_time"] = datetime.now().timestamp() + timedelta(minutes=28, seconds=12).total_seconds()
body["disappear_time_utc"] = datetime.utcnow().timestamp() + timedelta(minutes=28, seconds=12).total_seconds()
body["pokemon_level"] = 15
body["costume"] = 0
body["weather"] = 0

data_test = {}
data_test['type'] = "pokemon"
data_test['message'] = body

# send to pokealarm
response = requests.post(url=pa_url, data=json.dumps(data_test), headers={"Content-Type": "application/json"}, timeout=5)
print ("pokelarm response = ",response)

# send to db
mydb = mysql.connector.connect(host="ip", user="username", password="password", database="db_name")

mycursor = mydb.cursor()

sql = 'INSERT INTO pokemon (encounter_id, spawnpoint_id, pokemon_id, latitude, longitude, '\
      'disappear_time, individual_attack, individual_defense, individual_stamina, '\
      'move_1, move_2, cp, cp_multiplier, weight, height, '\
      'gender, form, weather_boosted_condition, last_modified)'\
      'VALUES '\
      '(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'

val = (body['encounter_id'], body['spawnpoint_id'], body['pokemon_id'], body['latitude'], body['longitude'],
       datetime.fromtimestamp(body["disappear_time_utc"]), body["individual_attack"], body["individual_defense"], body["individual_stamina"],
       body['move_1'], body['move_2'], body['cp'], body['cp_multiplier'], body['weight'], body['height'],
       body['gender'], body['form'], 0, datetime.now() )

print (val)

mycursor.execute(sql, val)
mydb.commit()
print(mycursor.rowcount, "record inserted.")
