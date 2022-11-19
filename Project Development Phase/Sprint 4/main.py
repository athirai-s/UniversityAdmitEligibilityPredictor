from flask import Flask,flash,render_template,request,session,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user,logout_user,login_manager,LoginManager
from flask_login import login_required,current_user
import requests

#db connection
local_server = True
app = Flask(__name__)

#326, 110, 2, 3.5, 4, 9.23, 1

@app.route('/',methods=['POST','GET'])
def homepage():
	if request.method == 'POST':
		gre = request.form.get('gre')
		toefl = request.form.get('toefl')
		univ = request.form.get('univ')
		sop = request.form.get('sop')
		lor = request.form.get('lor')
		cgpa = request.form.get('cgpa')
		research = request.form.get('research')
		API_KEY = "lGCP5Vh5MbNgiAv9NqmgEfCbZ0ILlFdhuIYROAGPurry"
		token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
		mltoken = token_response.json()["access_token"]

		header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

# NOTE: manually define and pass the array(s) of values to be scored in the next line
		payload_scoring = {"input_data": [{"field": [["GRE Score","TOEFL Score","University Rating","SOP","LOR ","CGPA", "Research"]], "values": [[gre,toefl,univ,sop,lor,cgpa,research]]}]}

		response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/1b71fd07-9daf-42eb-a620-453452c7e5a7/predictions?version=2022-11-18', json=payload_scoring,
 headers={'Authorization': 'Bearer ' + mltoken})
		print("Scoring response")
		print(response_scoring.json())
		probability = response_scoring.json()['predictions'][0]['values'][0][0][0]
		print(probability)
		temp = probability
		message = "Good Luck, You have great chances of getting selected!!, Pecentage = {}%".format(temp)
		if probability<0.5:
			message = "Better Luck Next Time :/ Pecentage = {}%".format(temp)
		return render_template('success.html',prediction_text="Admission chances: {}% ".format(probability),message = message)
	return render_template('index.html')



if __name__ == '__main__':
	app.run(debug=True)
