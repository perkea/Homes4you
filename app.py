from flask import Flask
import json
import pandas as pd
from urllib.request import urlopen
import requests

app = Flask(__name__)
URL = "https://realty-mole-property-api.p.rapidapi.com/saleListings"


@app.route('/findRealEstate/', methods=['GET'])
def find_real_estate():
    #Use Realty-Mole API to get housing data near the IP Address location (note there is some error here).

    querystring = {'longitude': -73, 'latitude' : 33, 'radius' : 25 } #25 kilometers a bit over 15 miles.

    headers = {'x-rapidapi-host': "realty-mole-property-api.p.rapidapi.com", 'x-rapidapi-key': "b8f02b8935msh82f5f902e62342bp149191jsn81acf76d0a8b"}

    response = requests.request("GET", URL, headers=headers, params=querystring).json()

    # return pd.DataFrame(response).set_index('formattedAddress')
    print("Response next line")
    print(response)
    return "done"

# Template for more endpoints.  Copy this and change the endpoint_name, function_name, and function implementation
#@app.route('/endpoint_name/', methods=['GET'])
#def function_name():
#    return "some json"

if __name__ == '__main__':
    # Note using flask run by default will use port 5000
    app.run(host='127.0.0.1', port=5000)