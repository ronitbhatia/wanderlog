import streamlit as st
import sqlite3
import os
from datetime import date, datetime
import requests
from pathlib import Path
import pandas as pd
import folium
from streamlit_folium import st_folium
import base64
from PIL import Image
import io

# Page configuration
st.set_page_config(
    page_title="VoyageLog - Travel Journal",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize database
def init_db():
    conn = sqlite3.connect('voyagelog.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS trip (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            location TEXT NOT NULL,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            start_date DATE NOT NULL,
            end_date DATE NOT NULL,
            description TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS photo (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            caption TEXT,
            trip_id INTEGER NOT NULL,
            FOREIGN KEY (trip_id) REFERENCES trip (id)
        )
    ''')
    conn.commit()
    conn.close()

# Geocoding function
def geocode(place: str):
    """Return (lat, lon) tuple for a human place name using OSM Nominatim."""
    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": place, "format": "json", "limit": 1}
    headers = {"User-Agent": "Voyagelog-streamlit"}
    try:
        r = requests.get(url, params=params, headers=headers, timeout=5)
        r.raise_for_status()
        data = r.json()
        if not data:
            return None, None
        return float(data[0]["lat"]), float(data[0]["lon"])
    except:
        return None, None

# Database operations
def add_trip(title, location, start_date, end_date, description):
    lat, lng = geocode(location)
    if lat is None:
        st.error("Location not found – try a more specific name.")
        return False
    
    conn = sqlite3.connect('voyagelog.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO trip (title, location, latitude, longitude, start_date, end_date, description)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (title, location, lat, lng, start_date, end_date, description))
    conn.commit()
    conn.close()
    return True

def get_trips():
    conn = sqlite3.connect('voyagelog.db')
    trips = pd.read_sql_query("SELECT * FROM trip ORDER BY start_date DESC", conn)
    conn.close()
    return trips

def delete_trip(trip_id):
    conn = sqlite3.connect('voyagelog.db')
    c = conn.cursor()
    c.execute("DELETE FROM trip WHERE id = ?", (trip_id,))
    conn.commit()
    conn.close()

def add_photo(trip_id, image, caption):
    # Create uploads directory if it doesn't exist
    upload_dir = Path("uploads")
    upload_dir.mkdir(exist_ok=True)
    
    # Save image
    filename = f"trip_{trip_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
    filepath = upload_dir / filename
    
    # Convert PIL image to bytes and save
    img_bytes = io.BytesIO()
    image.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    
    with open(filepath, 'wb') as f:
        f.write(img_bytes.getvalue())
    
    # Save to database
    conn = sqlite3.connect('voyagelog.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO photo (filename, caption, trip_id)
        VALUES (?, ?, ?)
    ''', (filename, caption, trip_id))
    conn.commit()
    conn.close()

def get_photos(trip_id):
    conn = sqlite3.connect('voyagelog.db')
    photos = pd.read_sql_query("SELECT * FROM photo WHERE trip_id = ?", conn, params=(trip_id,))
    conn.close()
    return photos

# Initialize database
init_db()

# Main app
def main():
    st.title("✈️ VoyageLog - Your Travel Journal")
    st.markdown("---")
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Choose a page",
        ["🏠 Home", "➕ Add Trip", "🗺️ Map View", "📸 Gallery"]
    )
    
    if page == "🏠 Home":
        show_home()
    elif page == "➕ Add Trip":
        show_add_trip()
    elif page == "🗺️ Map View":
        show_map()
    elif page == "📸 Gallery":
        show_gallery()

def show_home():
    st.header("My Trips")
    
    trips = get_trips()
    
    if trips.empty:
        st.info("No trips yet. Add your first trip using the sidebar!")
    else:
        for _, trip in trips.iterrows():
            with st.container():
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.subheader(trip['title'])
                    st.write(f"**{trip['location']}** ({trip['start_date']} → {trip['end_date']})")
                    if trip['description']:
                        st.write(trip['description'])
                    
                    # Get photos for this trip
                    photos = get_photos(trip['id'])
                    if not photos.empty:
                        st.write("📸 Photos:")
                        photo_cols = st.columns(min(3, len(photos)))
                        for idx, (_, photo) in enumerate(photos.iterrows()):
                            with photo_cols[idx % 3]:
                                try:
                                    img_path = Path("uploads") / photo['filename']
                                    if img_path.exists():
                                        image = Image.open(img_path)
                                        st.image(image, caption=photo['caption'], use_column_width=True)
                                except:
                                    st.write("Photo not found")
                
                with col2:
                    if st.button(f"🗑️ Delete", key=f"delete_{trip['id']}"):
                        delete_trip(trip['id'])
                        st.rerun()
                
                st.markdown("---")

def show_add_trip():
    st.header("Add New Trip")
    
    with st.form("add_trip_form"):
        title = st.text_input("Trip Title")
        location = st.text_input("Location")
        
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start Date")
        with col2:
            end_date = st.date_input("End Date")
        
        description = st.text_area("Description (optional)")
        
        submitted = st.form_submit_button("Add Trip")
        
        if submitted:
            if title and location and start_date and end_date:
                if start_date <= end_date:
                    if add_trip(title, location, start_date, end_date, description):
                        st.success("Trip added successfully!")
                        st.rerun()
                else:
                    st.error("End date must be after start date")
            else:
                st.error("Please fill in all required fields")

def show_map():
    st.header("Trip Map")
    
    trips = get_trips()
    
    if trips.empty:
        st.info("No trips to display on map. Add some trips first!")
    else:
        # Create map centered on first trip
        center_lat = trips.iloc[0]['latitude']
        center_lng = trips.iloc[0]['longitude']
        
        m = folium.Map(location=[center_lat, center_lng], zoom_start=4)
        
        # Add markers for each trip
        for _, trip in trips.iterrows():
            popup_text = f"""
            <b>{trip['title']}</b><br>
            {trip['location']}<br>
            {trip['start_date']} → {trip['end_date']}<br>
            {trip['description'] if trip['description'] else ''}
            """
            
            folium.Marker(
                [trip['latitude'], trip['longitude']],
                popup=folium.Popup(popup_text, max_width=300),
                tooltip=trip['title']
            ).add_to(m)
        
        # Display map
        st_folium(m, width=800, height=600)

def show_gallery():
    st.header("Photo Gallery")
    
    trips = get_trips()
    
    if trips.empty:
        st.info("No trips to display. Add some trips first!")
    else:
        # Select trip
        trip_options = {f"{trip['title']} - {trip['location']}": trip['id'] for _, trip in trips.iterrows()}
        selected_trip_name = st.selectbox("Select a trip:", list(trip_options.keys()))
        selected_trip_id = trip_options[selected_trip_name]
        
        # Show photos for selected trip
        photos = get_photos(selected_trip_id)
        
        if photos.empty:
            st.info("No photos for this trip yet.")
        else:
            st.subheader(f"Photos from {selected_trip_name}")
            
            # Display photos in a grid
            cols = st.columns(3)
            for idx, (_, photo) in enumerate(photos.iterrows()):
                with cols[idx % 3]:
                    try:
                        img_path = Path("uploads") / photo['filename']
                        if img_path.exists():
                            image = Image.open(img_path)
                            st.image(image, caption=photo['caption'], use_column_width=True)
                        else:
                            st.write("Photo not found")
                    except Exception as e:
                        st.write(f"Error loading photo: {e}")
        
        # Upload new photo
        st.subheader("Add New Photo")
        uploaded_file = st.file_uploader("Choose an image...", type=['jpg', 'jpeg', 'png'], key="photo_upload")
        caption = st.text_input("Photo caption (optional)")
        
        if uploaded_file is not None and st.button("Upload Photo"):
            try:
                image = Image.open(uploaded_file)
                add_photo(selected_trip_id, image, caption)
                st.success("Photo uploaded successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"Error uploading photo: {e}")

if __name__ == "__main__":
    main() 