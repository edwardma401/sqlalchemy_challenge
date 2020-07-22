import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

engine = create_engine("sqlite:///resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station

app = Flask(__name__)

@app.route("/")
def home():
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp).all()
    session.close()

    all_prcp = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        all_prcp.append(prcp_dict)
    
    return jsonify(all_prcp)


@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(Station.name).all()
    session.close()
    all_stations = list(np.ravel(results))
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def most_active_station_temperature_observed():
    session = Session(engine)
    import datetime as dt
    last_date = session.query(func.max(Measurement.date)).first()
    year_before = dt.datetime(2017,8,23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs, Measurement.date).filter(Measurement.station == Station.station).filter(Station.name == 'WAIHEE 837.5, HI US').filter(Measurement.date >= year_before).order_by(Measurement.date.desc()).all()
    session.close()

    all_tobs = []
    for tobs, date in results:
        tobs_dict = {}
        tobs_dict["tobs"] = tobs
        tobs_dict["date"] = date
        all_tobs.append(tobs_dict)

    return jsonify(all_tobs)

if __name__=='__main__':
    app.run(debug=True)