
import mysql.connector
from flask import Flask, request , jsonify
from flask_cors import CORS
from flask_restful import Resource, Api
import json
import random

app = Flask(__name__)
CORS(app)
api = Api(app)

db = mysql.connector.connect(
        host="104.154.70.132",
        user="root",
        password="12345",
        database="smart_soi"
);

import requests
import time

@app.route('/smart_soi/create/database',methods=['GET','POST'])
def createdb():
    dbcursor = db.cursor()
    dbcursor.execute("CREATE TABLE smartsoi (user VARCHAR(255),magellan VARCHAR(255),data VARCHAR(255))")
    dbcursor.execute("SHOW TABLES")
    for x in dbcursor:
      print(x)
    return "Created"

@app.route('/smart_soi/list',methods=['GET','POST'])
def listUser():
    users = []
    dbcursor = db.cursor()
    dbcursor.execute("SELECT * FROM smartsoi")
    myresult = dbcursor.fetchall()
    for x in myresult:
      users.append(x[0])
    return json.dumps(users)

@app.route('/smart_soi/<string:user>/add/<string:magellan>/<string:data>',methods=['GET','POST'])
def addUser(user,magellan,data):
    sql = "INSERT INTO smartsoi (`user`,`magellan`,`data`)VALUES(%s,%s,%s)"
    dbcursor = db.cursor()
    value = (user,magellan,data)
    dbcursor.execute(sql,value)
    db.commit()
    return str(dbcursor.rowcount)+" record inserted."

@app.route('/smart_soi/<string:user>/delete')
def deleteUser(user):
    dbcursor = db.cursor()
    sql = "DELETE FROM smartsoi WHERE user = %s"
    adr = (user,)
    dbcursor.execute(sql,adr)
    db.commit()
    print(dbcursor.rowcount,"record(s) deleted")
    return str(dbcursor.rowcount)+" record(s) deleted"

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
        requests.get("http://34.74.188.193:5050/notify/admin/"+str(x[0])+"/none")
	if int(x[0]) > aa:
		requests.get("http://34.74.188.193:5050/notify/admin/No/none")
		return "No_traffic"
	elif int(x[0]) < aa and int(x[1]) >aa and int(x[2])>aa:
		requests.get("http://34.74.188.193:5050/notify/admin/Light/none")
		return "Light_traffic"
	elif int(x[0]) < aa and int(x[1]) < aa and int(x[2])>aa:
		requests.get("http://34.74.188.193:5050/notify/admin/Medium/none")
		return "Medium_traffic"
	elif int(x[0])<aa and int(x[1])<aa and int(x[2])<aa:
		requests.get("http://34.74.188.193:5050/notify/admin/High/none")
		return "High_traffic"
def sugess(status1,status2):
	if status1 == "High_traffic" and status2 == "High_traffic":
		return "Stay in the lane"
	elif status1 == "High_traffic" and status2 != "High_traffic":
		return "Change to the right lane"
	else:
		return "Stay in the lane"
@app.route('/smart_soi/<string:user>/cie/<string:location>',methods=['GET','POST'])
def get_soi(location):
        dbcursor = db.cursor()
	sql = "SELECT * FROM lineuser WHERE user = %s"
	adr = (user,)
	dbcursor.execute(sql,adr)
	myresult = dbcursor.fetchall()
	for x in myresult:
		url = x[2]+location
		url1 = x[1]
        response = requests.get(url)
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
		url1 = "http://34.74.188.193:5050/notify/admin/"+statusy+sugessx+"/none"
		response2 = requests.get(url1)
                print(response2)
                print(smart_soi_status[i]["sensor_data"])
        return json.dumps(coming_data)

if __name__ == '__main__':
     app.run(host = '0.0.0.0', port='5000', threaded=True, debug=True)
