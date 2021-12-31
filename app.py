from flask import Flask,request
import json
from flask.templating import render_template
from flask_cors import CORS, cross_origin
import pandas as pd
from urllib.request import urlopen
import requests
import sys, os
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
# from dotenv import load_dotenv
from geopy.geocoders import Nominatim

# load_dotenv()

app = Flask(__name__)
CORS(app, support_credentials=True)

app.config['SECRET_KEY'] = '123' #our secret key shouldn't be posted on github #os.getenv('key') 
URL = "https://realty-mole-property-api.p.rapidapi.com/saleListings"
PROP_URL = "https://realty-mole-property-api.p.rapidapi.com/properties"

class LocationForm(FlaskForm): #this class is used to process form data into python
    city = StringField('City: ', validators=[DataRequired()])
    state = StringField('State: ', validators=[DataRequired()])
    submit = SubmitField('Submit', validators=[DataRequired()])


@app.route('/findRealEstate/', methods=['GET'])
@cross_origin(supports_credentials=True)

def location():
    url = 'http://ipinfo.io/json'
    response = urlopen(url)
    data = json.load(response)
    city = data['city']
    state = data['region']

    #geolocator can change city and state information into Longitude/Latitude information for use in Realty-Mole

    geolocator = Nominatim(user_agent='user')

    loc = geolocator.geocode(city+','+state)


    #Use Realty-Mole API to get housing data near the IP Address location (note there is some error here).

    querystring = {'latitude': loc.latitude, 'longitude' : loc.longitude, 'radius' : 25 } #25 kilometers a bit over 15 miles.

    #Note the key used in headers shouldn't ever end up on github
    headers = {'x-rapidapi-host': "realty-mole-property-api.p.rapidapi.com", 'x-rapidapi-key': "b8f02b8935msh82f5f902e62342bp149191jsn81acf76d0a8b"}

    response = requests.request("GET", URL, headers=headers, params=querystring)
    response_data = response.json()
    # response_data = pd.DataFrame(response).to_json()

    return json.dumps(response_data)

@app.route('/', methods=['GET','POST'])

def location_from_form():
    error = None
    form = LocationForm()
    return render_template('loc.html', form=form)

#https://stackoverflow.com/questions/42154602/how-to-get-form-data-in-flask

@app.route('/address', methods = ['GET','POST'])

def search_location():
    if(request.method == "POST"):
        city=request.form.get('city')
        state=request.form.get('state')


        geolocator = Nominatim(user_agent='user')

        loc = geolocator.geocode(city+','+state)


        #Use Realty-Mole API to get housing data near the IP Address location (note there is some error here).

        querystring = {'latitude': loc.latitude, 'longitude' : loc.longitude, 'radius' : 25 } #25 kilometers a bit over 15 miles.


        headers = {'x-rapidapi-host': "realty-mole-property-api.p.rapidapi.com", 'x-rapidapi-key': "b8f02b8935msh82f5f902e62342bp149191jsn81acf76d0a8b"}

        response = requests.request("GET", URL, headers=headers, params=querystring)

        res_json = response.json()
        # res_json = pd.DataFrame(response).to_json()

        return json.dumps(res_json)
        #return f'Search for homes near {city}, {state}'
    return 'done'

@app.route('/results', methods=["GET"])
def getResults():
    json_file = open('results.json') # os.path.realpath(os.path.dirname("results.json"))
    result = json.load(json_file)
    return json.dumps(result)


@app.route('/useLocationData', methods=['GET'])

def find_real_estate():
    #first get geographic data from the IP Address
    url = 'http://ipinfo.io/json'
    response = urlopen(url)
    data = json.load(response)
    lat,long=data['loc'].split(',') #get latitude and longitude to use below

    #Use Realty-Mole API to get housing data near the IP Address location (note there is some error here).

    querystring = {'longitude': long, 'latitude' : lat, 'radius' : 25 } #25 kilometers a bit over 15 miles.

    headers = {'x-rapidapi-host': "realty-mole-property-api.p.rapidapi.com", 'x-rapidapi-key': "b8f02b8935msh82f5f902e62342bp149191jsn81acf76d0a8b"}

    response = requests.request("GET", URL, headers=headers, params=querystring).json()
    res_dict = pd.DataFrame(response).set_index('formattedAddress').to_dict()
    #print(response)
    return json.dumps(res_dict)
    #return pd.DataFrame(response).set_index('formattedAddress')
    #sys.stderr.write(f"latitude: {lat} \nlongitude: {long}")
    loc_dict=location()
    html_str='<p>'
    for key,val in loc_dict.items():
        html_str+=f'{key} : {val}<br>'

    print("Response next line")
    print(response)
    return f'{html_str}</p>\ndone'


# Template for more endpoints.  Copy this and change the endpoint_name, function_name, and function implementation
#@app.route('/endpoint_name/', methods=['GET'])
#def function_name():
#    return "some json"
@app.route('/propertyId/<id>', methods = ['GET'])
def find_property_by_id(id):
    querystring = {} 
    headers = {'x-rapidapi-host': "realty-mole-property-api.p.rapidapi.com", 'x-rapidapi-key': "b8f02b8935msh82f5f902e62342bp149191jsn81acf76d0a8b"}
    response = requests.request("GET", PROP_URL + "/" + id, headers=headers, params=querystring)
    res_json = response.json()
    # res_json = pd.DataFrame(response).to_json()

    return json.dumps(res_json)


if __name__ == '__main__':
    # Note using flask run by default will use port 5000
    app.run(debug=True)
    #app.run(host='127.0.0.1', port=5000)