from flask import Flask, render_template, request
import jsonify
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler

import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "https://eu-de.ml.cloud.ibm.com/ml/v4/deployments/31d4f2a1-cab1-4f2a-9b69-0a29275d39ad/predictions?version=2022-11-14"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}
app = Flask(__name__)


model = pickle.load(open('random_forest_regression_model.pkl', 'rb'))
@app.route('/')
def index():
    return render_template('index1.html')

@app.route('/hai')
def Hai():
    return render_template('index.html')

@app.route('/hello',methods=['GET'])
def Home():
    return render_template('index.html')

standard_to = StandardScaler()
@app.route("/predict", methods=['POST'])
def predict():
    Fuel_Type_Diesel=0
    if request.method == 'POST':
        Year = int(request.form['Year'])
        Present_Price=float(request.form['Present_Price'])
        Kms_Driven=int(request.form['Kms_Driven'])
        Kms_Driven2=np.log(Kms_Driven)
        Owner=int(request.form['Owner'])
        Fuel_Type_Petrol=request.form['Fuel_Type_Petrol']
        if(Fuel_Type_Petrol=='Petrol'):
                Fuel_Type_Petrol=1
                Fuel_Type_Diesel=0
        else:
            Fuel_Type_Petrol=0
            Fuel_Type_Diesel=1
        Year=2020-Year
        Seller_Type_Individual=request.form['Seller_Type_Individual']
        if(Seller_Type_Individual=='Individual'):
            Seller_Type_Individual=1
        else:
            Seller_Type_Individual=0	
        Transmission_Mannual=request.form['Transmission_Mannual']
        if(Transmission_Mannual=='Mannual'):
            Transmission_Mannual=1
        else:
            Transmission_Mannual=0
        prediction=model.predict([[Present_Price,Kms_Driven2,Owner,Year,Fuel_Type_Diesel,Fuel_Type_Petrol,Seller_Type_Individual,Transmission_Mannual]])
        
        
        output=round(prediction[0],2)
        payload_scoring = {"input_data": [{"field": [['Present_Price','Kms_Driven2','Owner','Year','Fuel_Type_Diesel','Fuel_Type_Petrol','Seller_Type_Individual','Transmission_Mannual']], "values":prediction}]}

        response_scoring = requests.post('https://eu-de.ml.cloud.ibm.com/ml/v4/deployments/31d4f2a1-cab1-4f2a-9b69-0a29275d39ad/predictions?version=2022-11-14', json=payload_scoring,
         headers={'Authorization': 'Bearer ' + mltoken})
        print("response_scoring")
        predictions=response_scoring.json()
        predict=predictions['predictions'][0]['values'][0][0]
        if output<0:
            return render_template('index.html',prediction_texts="Sorry you cannot sell this car")
        else:
            return render_template('index.html',prediction_text="You Can Sell The Car at {}".format(output))
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)



