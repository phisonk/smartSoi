from flask import Flask, request , jsonify
from flask_restful import Resource, Api
import json
import random

app = Flask(__name__)
api = Api(app)

import requests
import time

def smart_soi_sensor_condition(x):
        if x < 250:
                return 'Jam'
        else:
                return 'NotJam'

def alley_status(x):
        if x[0]=='Jam':
        	return 'light_traffic'
	elif x[0]=='Jam'&x[1]=='Jam':
		return 'medium_traffic'
	elif x[0]=='Jam'&x[1]=='Jam'&x[2]=='Jam':
		return 'High_traffic'
	elif x[0]=='Jam'&x[1]=='Jam'&x[2]=='Jam'&x[3]=='Jam':
		return 'Heavy_traffic'
        else:
                return 'No_traffic'
def traffic_percentage(x):
	if x == 'No_traffic':
		return 0
	elif x == 'light_traffic':
		return 25
	elif x == 'medium_traffic':
		return 50
	elif x == 'High_traffic':
		return 75
	else:
		return 100

class smart_soi_status(Resource):
        def get(self, location):
                url = "http://35.208.101.91:8080/sensors/project_id/smart_soi/" + location
                response = requests.get(url)
                smart_soi_status = response.json()
                data = []
                for i in range(len(smart_soi_status)):
                        coming_data = [{'name': location}, {'percentage':traffic_percentage(smart_soi_status[i]["sensor_data"])},{'location': 'soi1'}]
                        print(data)
			#coming_data = {'Alley':'soi1','alley_status':'Heavy_traffic','Location':[20,30]}
                        #data.append(coming_data)
                        print(smart_soi_status[i]["sensor_data"])
                return jsonify(coming_data)

api.add_resource(smart_soi_status, '/smart_soi/<location>')

if __name__ == '__main__':
     app.run(host = '0.0.0.0', port='5000', threaded=True, debug=True)
