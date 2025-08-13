#!/bin/bash

echo "🚀 Deploying VoyageLog to Streamlit Cloud..."

# Check if streamlit is installed
if ! command -v streamlit &> /dev/null; then
    echo "❌ Streamlit is not installed. Installing now..."
    pip install streamlit
fi

# Install requirements
echo "📦 Installing dependencies..."
pip install -r requirements_streamlit.txt

# Deploy to Streamlit Cloud
echo "🌐 Deploying to Streamlit Cloud..."
streamlit deploy streamlit_app.py

echo "✅ Deployment complete! Check your Streamlit Cloud dashboard for the live link." 