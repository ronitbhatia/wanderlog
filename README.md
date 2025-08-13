# Voyagelog – A Lightweight Travel Journal
Keep your memories pinned to the map.


# What it does
1. Add trips (title, location, start/end dates, description).
2. Auto-geocode: latitude & longitude are fetched automatically from the place name.
3. Upload photos and link them to any trip.
4. Interactive Leaflet map with pop-ups for every trip and its photos.
5. Responsive, dark-themed gallery.
6. One-click delete (cleans up photos on disk, too).

# Quick start

1. git clone https://github.com/ronitbhatia/wanderlog.git
2. cd wanderlog
3. python -m venv venv && source venv/bin/activate   # or .\venv\Scripts\activate
4. pip install -r requirements.txt
5. flask --app app run --debug
6. Open http://127.0.0.1:5000

# Folder Structure
voyagelog/
├── app.py                     # Main Flask application
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables (SECRET_KEY)
├── README.md                  # This file
├── instance/
│   └── voyagelog.db           # SQLite database (auto-created)
├── static/
│   ├── css/
│   │   └── style.css          # Dark-theme & glass-morphism styles
│   ├── js/
│   │   ├── map.js             # Leaflet map initialization
│   │   └── fade.js            # Page fade-in animation
│   └── uploads/               # Uploaded photos (auto-created)
└── templates/
    ├── base.html              # Navigation sidebar & global layout
    ├── index.html             # Trip list + delete buttons
    ├── add_trip.html          # Trip creation form
    ├── gallery.html           # Photo grid
    ├── map.html               # Full-screen interactive map
    └── upload.html            # Photo upload form (per trip)
    
# Tech stack
1. Backend: Flask + SQLite (SQLAlchemy)
2. Frontend: Jinja2, vanilla CSS + JS, Leaflet.js
3. Geocoding: OpenStreetMap Nominatim (free)
   
# Transparency & Attribution
This project was developed as an experiment using Kimi K2, an open-source trillion-parameter Mixture-of-Experts model created by Moonshot AI.
I provided high-level architectural prompts (“build a Flask travel journal with interactive map, photo uploads, auto-geocoding…”) and iteratively refined the generated code, debugged edge cases, and enhanced the UI to reach the current functional prototype.
