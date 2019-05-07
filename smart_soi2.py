
from flask import Flask, request , jsonify
from flask_cors import CORS
from flask_restful import Resource, Api
import json
import random

app = Flask(__name__)
CORS(app)
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
def traffic(data):
	aa = 10
	#x = data["Distance"]
	x = data.split("-")
	lineNotify(x[0],"admin")
	if int(x[0]) > aa:
		lineNotify("No","admin")
		return "No_traffic"
	elif int(x[0]) < aa and int(x[1]) >aa and int(x[2])>aa:
		lineNotify("Light","admin")
		return "Light_traffic"
	elif int(x[0]) < aa and int(x[1]) < aa and int(x[2])>aa:
		lineNotify("Medium","admin")
		return "Medium_traffic"
	elif int(x[0])<aa and int(x[1])<aa and int(x[2])<aa:
		lineNotify("High","admin")
		return "High_traffic"
def sugess(status1,status2):
	if status1 == "High_traffic" and status2 == "High_traffic":
		return "Stay in the lane"
	elif status1 == "High_traffic" and status2 != "High_traffic":
		return "Change to the right lane"
	else:
		return "Stay in the lane"
@app.route('/smart_soi/cie/<location>',methods=['GET','POST'])
def get_soi(location):
        url = "http://35.208.101.91:8080/sensors/project_id/smart_soi/cie/" + location
        response = requests.get(url)
	url1 = "https://www.aismagellan.io/api/things/pull/f91baf10-659e-11e9-96dd-9fb5d8a71344"
	response1 = requests.get(url1)
	rawdata = response1.json()
	print(rawdata)
	rawdatas = rawdata["Distance"]
	rawdatas = rawdatas.split("n")
	statusx = traffic(rawdatas[0])
	statusy = traffic(rawdatas[1])
	sugessx = sugess(statusy,statusx)
        smart_soi_status = response.json()
        data = []
        for i in range(len(smart_soi_status)):
                coming_data = {'name': location, 'percentage':traffic_percentage(smart_soi_status[i]["sensor_data"]),'location': 'soi1','status_soi1': statusx,'status_soi2': statusy,'sugession':sugessx}
                print(data)
		#coming_data = {'Alley':'soi1','alley_status':'Heavy_traffic','Location':[20,30]}
                #data.append(coming_data)
		url1 = "http://35.231.245.160:5000/notify/admin/"+statusy+sugessx+"/none"
		response2 = requests.get(url1)
                print(response2)
                print(smart_soi_status[i]["sensor_data"])
        return json.dumps(coming_data)

if __name__ == '__main__':
     app.run(host = '0.0.0.0', port='5000', threaded=True, debug=True)
