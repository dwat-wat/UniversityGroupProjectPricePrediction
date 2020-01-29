# Created by Dexter Watson DAW35

import requests
import json
import datetime
import numpy as np
from sklearn.svm import SVR, LinearSVR
from sklearn.preprocessing import PolynomialFeatures
import matplotlib.pyplot as plt

# Properties
apikey = "57b9285261bf74807812697d0aa133456f7b0054c5fd040b232003cd4b22de3f"
dates = []
prices = []

# Classes

# Functions
def get_data_thismonth():
    url = "https://min-api.cryptocompare.com/data/v2/histoday?fsym=BTC&tsym=GBP&limit=" + str(datetime.datetime.today().timetuple().tm_yday-1) + "&aggregate=1&api_key=" + apikey
    response = requests.get(url)
    if response.status_code == 200:
        res = json.loads(response.content) 
    
        for data in res["Data"]["Data"]:
            _date = datetime.datetime(1, 1, 1) + datetime.timedelta(seconds=data["time"])
            _date = _date.replace(year=_date.year + 1969)
            date = _date.strftime("%Y-%m-%dT%H:%M:%S.%fZ")[:-3]
            print(_date, data["open"])
            dates.append(_date.day)
            prices.append(float(data["open"]))
    else:
        print("Error: ", response.status_code)
    return

def predict_prices(dates, prices, x):
    dates = np.reshape(dates, (len(dates), 1))
    svr_rbf = SVR(C=1e3, gamma = 0.1)
    svr_lin = LinearSVR(C=1e3, max_iter=1000)
    svr_rbf.fit(dates, prices)
    svr_lin.fit(dates, prices)
    
    plt.scatter(dates, prices, color='blue', label='Data')
    plt.plot(dates, svr_rbf.predict(dates), color='green', label='RBF Model')
    plt.plot(dates, svr_lin.predict(dates), color='red', label='Linear Model')
    
    prediction_rbf = svr_rbf.predict(np.array(x).reshape(1, 1))[0]
    prediction_lin = svr_lin.predict(np.array(x).reshape(1, 1))[0]
    plt.scatter([x], [prediction_rbf], color='green', label='RBF Prediction')
    plt.scatter([x], [prediction_lin], color='red', label='Linear Prediction')
    plt.xlabel('Date (Day)')
    plt.ylabel('Price (£)')
    plt.title('Price Prediction')
    plt.legend()
    plt.show()    
    
    return prediction_rbf, prediction_lin
    
def thismonth():
    get_data_thismonth()
    predictedprices = predict_prices(dates, prices, (datetime.datetime.today()+datetime.timedelta(days=1)).day)
    print("Tomorrows price: ", "\nRBF £", predictedprices[0], "\nLinear £", predictedprices[1])

def get_data_pastdays(ndays):
    url = "https://min-api.cryptocompare.com/data/v2/histoday?fsym=BTC&tsym=GBP&limit=" + str(ndays) + "&aggregate=1&api_key=" + apikey
    response = requests.get(url)
    if response.status_code == 200:
        res = json.loads(response.content)     
        i = 0;
        for data in res["Data"]["Data"]:
            dates.append(i)
            prices.append(float(data["open"]))
            i += 1
            
        print(i)
    else:
        print("Error: ", response.status_code)
    return

def pastdays(ndays):
    get_data_pastdays(ndays)
    predictedprices = predict_prices(dates, prices, ndays+1)
    print("Tomorrows price: ", "\nRBF £", predictedprices[0], "\nLinear £", predictedprices[1])

# Main    

#thismonth()
pastdays(100)



