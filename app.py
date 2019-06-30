import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import and_
from flask import Flask, jsonify
import datetime as dt


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date<br/>"
        f"/api/v1.0/start_date/end_date"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    
    # Query all passengers
    results = session.query(Measurement.date, Measurement.prcp).all()
    all_prcp = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict[date] = prcp
        all_prcp.append(prcp_dict)

    return jsonify(all_prcp)

@app.route("/api/v1.0/stations")
def stations():
    """Return a list s"""
    # Query all stations
    results = session.query(Measurement.station).all()
    all_stations = []
    for station in results:
        stations_dict = {}
        stations_dict["station"] = station
        all_stations.append(stations_dict)

    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def tobs():
    """Return a list s"""
    # Query for temps
    results = session.query(Measurement.station, Measurement.tobs, Measurement.date).filter(and_(Measurement.date < '2017-08-24', Measurement.date > '2016-08-22')).all()
    all_tobs = []
    for station, tobs, date in results:
        tobs_dict = {}
        tobs_dict["station"] = station,
        tobs_dict["tobs"] = tobs,
        tobs_dict["date"] = date
        
        all_tobs.append(tobs_dict)

    return jsonify(all_tobs)

@app.route("/api/v1.0/<start_date>")
def temps_by_start_date(start_date):
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= '{start_date}').all()
    values = list(np.ravel(results))
    return jsonify(values)
    

# @app.route("/api/v1.0/<start_date>/<end_date>")
# def temps_by_start_and_end_date(start_date, end_date):
#     results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
#         filter(Measurement.date >= '{start_date}').filter(Measurement.date <= '{end_date}').all()
#     values = list(np.ravel(results))
#     return jsonify(values)

if __name__ == '__main__':
    app.run(debug=True)
