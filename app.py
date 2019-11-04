import numpy as np
import pandas as pd
import sqlalchemy
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask Setup
app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Welcome!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

@app.route("/api/v1.0/precipitation")

def precipitation():
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date <'2017-08-23').\
    filter(Measurement.date >'2016-08-23').\
    order_by(Measurement.date).all()
    
    session.close()

#Creating a dictionary
    prcp_total = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        prcp_total.append(prcp_dict)
        
    return jsonify(prcp_total)


@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(Measurement.station).\
    group_by(Measurement.station).all()
    
    session.close()
    
    return jsonify(results)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    results= session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date >= "2016, 8, 23", Measurement.date <= "2017, 8, 23").all()
    
    
    session.close()
    
    all_temps = list(np.ravel(results))

    return jsonify(all_temps)

@app.route("/api/v1.0/<start>")
def start_date(start):
   
    session = Session(engine)
    start_date_one = dt.datetime.strptime(start, "%Y-%m-%d")
    temp_data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= start_date_one).all()
    
    session.close()
    
    all_temps = list(np.ravel(temp_data))
    
    return jsonify(all_temps)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    session = Session(engine)
    start_date = dt.datetime.strptime(start, "%Y-%m-%d")
    end_date = dt.datetime.strptime(end, "%Y-%m-%d")
    temp_date = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= start_date, Measurement.date <= end_date).all()
    
    session.close()
    
    all_temps = list(np.ravel(temp_date))
    
    return jsonify(all_temps)
                   

if __name__ == '__main__':
    app.run(debug=True)
                              
                                      
    
    
   

   
   
    
                         
                                                                      
