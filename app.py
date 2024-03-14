#################################################
# Import the dependencies.
import sqlalchemy
import numpy as np
from flask import Flask, jsonify
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base

#################################################
# Database Setup

# create function to allow access to SQLite database file
engine = create_engine("sqlite:///Resources/Hawaii.sqlite")

# reflect the database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# set/save the class variables
Station = Base.classes.station
Measurement = Base.classes.measurement

# create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup

app = Flask(__name__)

#################################################
# Flask Routes

#Welcome Route
@app.route("/")
def welcome():
      return(
    '''
    <h1>Welcome to the Climate Analysis API!</h1>
    <h3>Available Routes:</h3>
    <ul>
        <li>/api/v1.0/precipitation</li>
        <li>/api/v1.0/stations</li>
        <li>/api/v1.0/tobs</li>
        <li>/api/v1.0/temp/[start]</li>
        <li>/api/v1.0/temp/[start]/[end]</li>
    </ul>
    ''') 

#Precipitation Route
@app.route("/api/v1.0/precipitation")
def precipitation():
    precipitation = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= '2016-08-23').all()
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)

#Stations Route
@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

#Monthly Temp Route
@app.route("/api/v1.0/tobs")
def tobs():
    results = session.query(Measurement.tobs).\
      filter(Measurement.station == 'USC00519281').filter(Measurement.date >= '2016-08-23').all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

#Statistics Route
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end='2017-08-23'):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    [min,avg,max] = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).first()

    return {'Dates':f'{start} to {end}','Min Temp':min,'Avg Temp':avg,'Max Temp':max}
    

#################################################
# Home route
@app.route('/')
def home():
    return 'Welcome to the Home Page'

# Example route returning JSON data
@app.route('/api/data')
def get_data():
    # Query the database or provide sample data
    data = {'example_key': 'example_value'}
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)