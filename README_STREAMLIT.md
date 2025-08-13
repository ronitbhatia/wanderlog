# WanderLog - Streamlit Version

A beautiful travel journal application built with Streamlit that allows users to log their trips, add photos, and view them on an interactive map.

## Features

- ✈️ **Trip Management**: Add, view, and delete trips with location, dates, and descriptions
- 📍 **Interactive Map**: View all your trips on an interactive map with markers
- 📸 **Photo Gallery**: Upload and view photos for each trip
- 🗺️ **Geocoding**: Automatic location coordinates using OpenStreetMap
- 📱 **Responsive Design**: Works great on desktop and mobile devices

## Quick Demo

To run a quick demo locally:

1. Install dependencies:
```bash
pip install -r requirements_streamlit.txt
```

2. Run the app:
```bash
streamlit run streamlit_app.py
```

3. Open your browser to `http://localhost:8501`

## Deploy to Streamlit Cloud

### Option 1: Deploy from GitHub

1. **Push your code to GitHub**:
   - Create a new repository on GitHub
   - Push your code including `streamlit_app.py` and `requirements_streamlit.txt`

2. **Deploy on Streamlit Cloud**:
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with your GitHub account
   - Click "New app"
   - Select your repository
   - Set the main file path to `streamlit_app.py`
   - Click "Deploy"

### Option 2: Deploy from Local Files

1. **Install Streamlit**:
```bash
pip install streamlit
```

2. **Create a `.streamlit/config.toml` file** (optional):
```toml
[theme]
primaryColor = "#FF6B6B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
```

3. **Deploy using Streamlit Cloud CLI**:
```bash
streamlit deploy streamlit_app.py
```

## File Structure

```
wanderlog/
├── streamlit_app.py          # Main Streamlit application
├── requirements_streamlit.txt # Python dependencies
├── README_STREAMLIT.md       # This file
├── wanderlog.db             # SQLite database (created automatically)
└── uploads/                 # Photo uploads directory (created automatically)
```

## How to Use

1. **Add a Trip**:
   - Navigate to "Add Trip" in the sidebar
   - Fill in trip details (title, location, dates, description)
   - Click "Add Trip"

2. **View Trips**:
   - The home page shows all your trips
   - Each trip displays with photos and details
   - Use the delete button to remove trips

3. **Map View**:
   - Go to "Map View" to see all trips on an interactive map
   - Click markers to see trip details

4. **Photo Gallery**:
   - Visit "Gallery" to view and upload photos
   - Select a trip to see its photos
   - Upload new photos with captions

## Customization

### Styling
You can customize the appearance by modifying the `st.set_page_config()` call in `streamlit_app.py`:

```python
st.set_page_config(
    page_title="Your Custom Title",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)
```

### Adding Features
The modular structure makes it easy to add new features:
- Add new pages by creating functions and adding them to the sidebar navigation
- Extend the database schema in the `init_db()` function
- Add new UI components using Streamlit widgets

## Troubleshooting

### Common Issues

1. **Location not found**: Try using more specific location names (e.g., "Paris, France" instead of just "Paris")

2. **Photos not loading**: Make sure the `uploads/` directory exists and has proper permissions

3. **Database errors**: Delete `wanderlog.db` to reset the database

### Performance Tips

- The app uses SQLite for simplicity, but for production consider PostgreSQL
- Large photo uploads may slow down the app - consider image compression
- The geocoding service has rate limits, so avoid rapid successive requests

## License

This project is open source and available under the MIT License.

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review Streamlit documentation at [docs.streamlit.io](https://docs.streamlit.io)
3. Open an issue on the GitHub repository 