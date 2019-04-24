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

def lineNotify(message,type):
    payload = {'message':message}
    return _lineNotify(payload,type)

def notifyFile(filename):
    file = {'imageFile':open(filename,'rb')}
    payload = {'message': 'test'}
    return _lineNotify(payload,file)

def notifyPicture(url,type):
    payload = {'message':" ",'imageThumbnail':url,'imageFullsize':url}
    return _lineNotify(payload,type)

def notifySticker(stickerID,stickerPackageID,type):
    payload = {'message': " ",'stickerPackageId':stickerPackageID,'stickerId':stickerID}
    return _lineNotify(payload,type)

def _lineNotify(payload,type,file=None):
    import requests
    url = 'https://notify-api.line.me/api/notify'
    if type == "admin":
    	token = 'rUVBdKwkDNTvfN5QL5mMCZktU5llOyjk5KLDil5oJ5D'	#EDIT
    elif type == "user":
    	token = 'u5dhlrfoKQYbwDTVXQlo4jA5Wq1x4UShD9GrWpgRQVV'
    else:
    	return "Not Available"
    headers = {'Authorization':'Bearer '+token}
    return requests.post(url, headers=headers , data = payload, files=file)

class smart_soi_status(Resource):
        def get(self, location):
		notifySticker(34,2,"user")
                url = "http://35.208.101.91:8080/sensors/project_id/smart_soi/cie/" + location
                response = requests.get(url)
                smart_soi_status = response.json()
                data = []
                for i in range(len(smart_soi_status)):
                        coming_data = [{'name': location}, {'percentage':traffic_percentage(smart_soi_status[i]["sensor_data"])},{'location': 'soi1'}]
                        print(data)
			#coming_data = {'Alley':'soi1','alley_status':'Heavy_traffic','Location':[20,30]}
                        #data.append(coming_data)
			url1 = "http://35.231.245.160:5000/notify/user/"+smart_soi_status[i]["sensor_data"]
			response2 = requests.get(url1)
                	print(response2)
                        print(smart_soi_status[i]["sensor_data"])
                return jsonify(coming_data)

class line_notify_api(Resource):
	def get(self, msg,type,sticker):
		if msg != "none":
			lineNotify(msg,type)
		if sticker != "none":
			tt = sticker.split(",")
			notifySticker(tt[0],tt[1],type)
		return "sent to: "+type+":"+msg
api.add_resource(smart_soi_status, '/smart_soi/cie/<location>')
api.add_resource(line_notify_api,'/notify/<string:type>/<string:msg>/<string:sticker>')
if __name__ == '__main__':
     app.run(host = '0.0.0.0', port='5000', threaded=True, debug=True)
