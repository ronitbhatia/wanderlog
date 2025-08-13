import os
from datetime import date
from pathlib import Path
import requests

from flask import (Flask, render_template, request,
                   redirect, url_for, flash, jsonify)
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()                      # read .env

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///voyagelog.db'
app.config['UPLOAD_FOLDER'] = Path(app.root_path) / 'static' / 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 8 * 1024 * 1024   # 8 MB
app.config['UPLOAD_FOLDER'].mkdir(exist_ok=True)

db = SQLAlchemy(app)

def geocode(place: str):
    """Return (lat, lon) tuple for a human place name using OSM Nominatim."""
    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": place, "format": "json", "limit": 1}
    headers = {"User-Agent": "Voyagelog-localdev"}
    r = requests.get(url, params=params, headers=headers, timeout=5)
    r.raise_for_status()
    data = r.json()
    if not data:
        return None, None
    return float(data[0]["lat"]), float(data[0]["lon"])

# ---------- MODELS ----------
class Trip(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    title       = db.Column(db.String(100), nullable=False)
    location    = db.Column(db.String(120), nullable=False)
    latitude    = db.Column(db.Float, nullable=False)
    longitude   = db.Column(db.Float, nullable=False)
    start_date  = db.Column(db.Date, nullable=False)
    end_date    = db.Column(db.Date, nullable=False)
    description = db.Column(db.Text)

    photos = db.relationship('Photo', backref='trip', cascade='all, delete-orphan')

class Photo(db.Model):
    id       = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200), nullable=False)
    caption  = db.Column(db.String(200))
    trip_id  = db.Column(db.Integer, db.ForeignKey('trip.id'), nullable=False)

# ---------- ROUTES ----------
@app.route('/')
def index():
    trips = Trip.query.order_by(Trip.start_date.desc()).all()
    return render_template('index.html', trips=trips)

@app.route('/add', methods=['GET', 'POST'])
def add_trip():
    if request.method == 'POST':
        location = request.form['location']
        lat, lng = geocode(location)
        if lat is None:
            flash("Location not found – try a more specific name.")
            return redirect(url_for('add_trip'))

        trip = Trip(
            title=request.form['title'],
            location=location,
            latitude=lat,
            longitude=lng,
            start_date=date.fromisoformat(request.form['start']),
            end_date=date.fromisoformat(request.form['end']),
            description=request.form['desc']
        )
        db.session.add(trip)
        db.session.commit()
        flash('Trip added!')
        return redirect(url_for('index'))
    return render_template('add_trip.html')

@app.route('/map')
def map_view():
    return render_template('map.html')

@app.route('/api/trips')
def api_trips():
    trips = Trip.query.all()
    return jsonify([{
        'id': t.id,
        'title': t.title,
        'location': t.location,
        'lat': t.latitude,
        'lng': t.longitude,
        'start': t.start_date.isoformat(),
        'end': t.end_date.isoformat(),
        'desc': t.description,
        'photos': [{'filename': p.filename, 'caption': p.caption} for p in t.photos]
    } for t in trips])

@app.route('/gallery')
def gallery():
    trips = Trip.query.all()
    return render_template('gallery.html', trips=trips)

@app.route('/upload/<int:trip_id>', methods=['GET', 'POST'])
def upload(trip_id):
    trip = Trip.query.get_or_404(trip_id)
    if request.method == 'POST':
        file = request.files['photo']
        if file and file.filename:
            filename = file.filename
            file.save(app.config['UPLOAD_FOLDER'] / filename)
            photo = Photo(filename=filename,
                          caption=request.form['caption'],
                          trip=trip)
            db.session.add(photo)
            db.session.commit()
            flash('Photo uploaded!')
            return redirect(url_for('gallery'))
    return render_template('upload.html', trip=trip)

@app.post('/trips/<int:trip_id>/delete')
def delete_trip(trip_id):
    trip = Trip.query.get_or_404(trip_id)
    # Remove associated photo files from disk
    for p in trip.photos:
        (app.config['UPLOAD_FOLDER'] / p.filename).unlink(missing_ok=True)
    db.session.delete(trip)
    db.session.commit()
    flash('Trip deleted.')
    return redirect(url_for('index'))

# ---------- INIT DB ----------
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)