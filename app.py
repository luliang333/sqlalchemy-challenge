import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext import automap
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
from flask import Flask, jsonify
from werkzeug.exceptions import RequestHeaderFieldsTooLarge

engine = create_engine('sqlite:///Resources/hawaii.sqlite')
Base = automap_base()
Base.prepare(engine,reflect = True)

Station = Base.classes.station
Measurement = Base.classes.measurement
session = Session(engine)

last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
query_date = dt.date(2017,8,23) - dt.timedelta(days=365)

data = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= query_date).all()
df = pd.DataFrame(data, columns=['date', 'prcp']).set_index('date')
prcp_dict = df.to_dict('data')

data = session.query(Measurement.station, Measurement.date, Measurement.tobs).filter(Measurement.station == 'USC00519281').all()
stations = session.query(Station.station, Station.name).all()
stations_df = pd.DataFrame(stations, columns=['station', 'name'])
stations_dict = stations_df.to_dict('data')
print(stations_dict)

tobs_df = pd.DataFrame(data, columns=['station', 'date', 'temperature'])
tobs_dict = tobs_df.to_dict('data')  



app = Flask(__name__)
@app.route("/")
def home():
    return(
        f"API Routes<br>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
    )


@app.route("/api/v1.0/precipatation")
def precipitation():
    return jsonify(prcp_dict)

@app.route('/api/v1.0/stations')
def stations():
    return jsonify(stations_dict)

@app.route("/api/v1.0/tobs")
def tobs():
    return jsonify(tobs_dict)

if __name__ == '__main__':
    app.run(debug=True)
