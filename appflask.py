import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Passenger = Base.classes.passenger

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
        f"/api/v1.0/station
        f"/api/v1.0/tobs"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a list of precipitation"""
    # Convert the query results to a Dictionary using date as the key and prcp as the value.
    results = session.query(Measurement.date,Measurememt.prcp).all()
    new_results = { Measurement.date: Measurement.prcp
        
        
    }
    

    # Return the JSON representation of your dictionary
    return jsonify(new_results)


@app.route("/api/v1.0/station")
def station():
    """Return a JSON list of stations from the dataset"""
    # Query all stations
    results = session.query(Measurement.station).all()

    # Create a list and run a for loop to add it to a list 
    all_stations = []
    for stations in results:
    all_stations.append(results)
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    """query for the dates and temperature observations from a year from the last data point."""
    # Query fort the dates 
    results = session.query(Measurement.dates).order by(Measurement.dates)filter(Measurement.dates>= year).all()

    # Return a JSON list of Temperature Observations (tobs) for the previous year.
    temp_obs = session.query(Measurement.tobs, Measurement.dates)filter(Measurement.dates>=year).all()
    return jsonify(temp_obs)


@app.route("/api/v1.0/<start>")
def start():
    """When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date."""

    start = session.query(Measurement.dates, fun.min(Measurement.tobs), func.avg(Measurement.tobs),func.max(Measurement.tobs))filter(Measurement.dates>= year).all()
    return jsonify(start)



if __name__ == '__main__':
    app.run()
