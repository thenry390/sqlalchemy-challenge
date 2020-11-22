import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
import numpy as np
import pandas as pd
import datetime as dt
import psycopg2
from sqlalchemy import create_engine, func, inspect
from sqlalchemy.ext.declarative import declarative_base
# Allow us to declare column types
from sqlalchemy import Column, Integer, String, Float 
from sqlalchemy.sql.expression import bindparam
from sqlalchemy import Interval
from datetime import timedelta

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect an existing database into a new model
# Declare a Base using `automap_base()`
Base = automap_base()

# reflect the tables
# Use the Base class to reflect the database tables
Base.prepare(engine, reflect=True)
Base.classes.keys()
# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

def mergeDictionary(dis1,dis2):
    finalDis=dis1.copy() #copy dis1 to finalDis
    finalDis.update(dis2) # concate the ds1 with ds2
    return finalDis # return the final dictionary

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List of all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precip<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
    )

@app.route("/precip_info")
def precip_info():
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >='2016-08-23').filter(Measurement.date <= '2017-08-23').all()
    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_precip_rows = []
    for date, prcp in results:
        precip_dict = {}
        precip_dict["date"] = date
        precip_dict["prcp"] = prcp
        all_precip_rows.append(precip_dict)

    return jsonify(all_precip_rows)    

@app.route("/stations")
def stations():
    session = Session(engine)
    results = session.query(Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).all()
    session.close()

    all_station_rows =[]   
    for station, name, latitude, longitude, elevation in results:
        station_dict = {}
        station_dict["station"]=station
        station_dict["name"]=name
        station_dict["latitude"]=latitude
        station_dict["longitude"]=longitude
        station_dict["elevation"]=elevation
        all_station_rows.append(station_dict)
        
    return jsonify(all_station_rows)

@app.route("/tobs")
def tobs():
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >='2016-08-23').filter(Measurement.date <= '2017-08-23').filter(Measurement.station=='USC00519281').all()
    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_tobs_rows = []
    for date, tobs in results:
        precip_dict = {}
        precip_dict["date"] = date
        precip_dict["tobs"] = tobs
        all_tobs_rows.append(precip_dict)

    return jsonify(all_tobs_rows)    


@app.route("/startdate")
def startdate():
    session = Session(engine)
    startdate = '2016-08-23'
    results=session.query(Measurement).filter(Measurement.station=='USC00519281').filter(Measurement.date >=startdate)
    query_max = results.with_entities(func.max(Measurement.tobs)).all()
    query_min = results.with_entities(func.min(Measurement.tobs)).all()
    query_avg = results.with_entities(func.avg(Measurement.tobs)).all()   
    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_tobs_rows = []
    tobs_dict = {}
    tobs_dict["max"] = query_max
    tobs_dict["min"] = query_min
    tobs_dict["avg"] = query_avg
    all_tobs_rows.append(tobs_dict)

    return jsonify(all_tobs_rows)    

@app.route("/startenddate")
def startenddate():

    session = Session(engine)
    startdate = '2016-08-23'
    enddate='2017-08-23'
    results=session.query(Measurement).filter(Measurement.station=='USC00519281').filter(Measurement.date >=startdate).filter(Measurement.date <= enddate)
    query_max = results.with_entities(func.max(Measurement.tobs)).all()
    query_min = results.with_entities(func.min(Measurement.tobs)).all()
    query_avg = results.with_entities(func.avg(Measurement.tobs)).all()   

    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_tobs_rows = []
    tobs_dict = {}
    tobs_dict["max"] = query_max
    tobs_dict["min"] = query_min
    tobs_dict["avg"] = query_avg
    all_tobs_rows.append(tobs_dict)

    return jsonify(all_tobs_rows)    


if __name__ == '__main__':
    app.run(debug=True)
