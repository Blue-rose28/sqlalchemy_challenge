from flask import Flask, jsonify
import datetime as dt
from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base


# Create a Flask app
app = Flask(__name__)

# Create engine to connect to the SQLite database
engine = create_engine("sqlite:///hawaii.sqlite")

# Reflect the database tables
Base = automap_base()
Base.prepare(engine, reflect=True)
# Save references to the tables
Measurement = Base.classes.measurement
Station = Base.classes.station
# Define a function to get the most recent date
def get_most_recent_date():
    session = Session(engine)
    most_recent_date = session.query(func.max(Measurement.date)).scalar()
    session.close()
    return most_recent_date

# Define the routes
# Homepage - List available routes
@app.route("/")
def home():
    return (
        f"Available routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;<br/>"
    )

# Precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    most_recent_date = get_most_recent_date()
    one_year_ago = dt.datetime.strptime(most_recent_date, '%Y-%m-%d') - dt.timedelta(days=365)
    
    session = Session(engine)
    precipitation_data = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= one_year_ago).all()
    session.close()
    
    precipitation_dict = {date: prcp for date, prcp in precipitation_data}
    return jsonify(precipitation_dict)

# Stations route
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    station_list = session.query(Station.station).all()
    session.close()
    
    return jsonify(station_list)

# TOBS route
@app.route("/api/v1.0/tobs")
def tobs():
    most_active_station = "USC00519281"  # You can adjust this based on your previous analysis
    
    most_recent_date = get_most_recent_date()
    one_year_ago = dt.datetime.strptime(most_recent_date, '%Y-%m-%d') - dt.timedelta(days=365)
    
    session = Session(engine)
    tobs_data = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == most_active_station).\
        filter(Measurement.date >= one_year_ago).all()
    session.close()
    
    return jsonify(tobs_data)


# Start route
@app.route("/api/v1.0/<start>")
def start_date(start):
    session = Session(engine)
    temperature_stats = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    session.close()
    
    return jsonify(temperature_stats)

# Start and end route
@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):
    session = Session(engine)
    temperature_stats = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    session.close()
    
    return jsonify(temperature_stats)

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
















