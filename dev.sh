#!/bin/bash

# YouTube Script Writer AI - Development Script
# This script helps you manage both frontend and backend development

echo "🎬 YouTube Script Writer AI - Development Manager"
echo "=================================================="

# Function to start React frontend
start_frontend() {
    echo "🚀 Starting React Frontend..."
    echo "Installing dependencies..."
    npm install
    echo "Starting development server..."
    npm start
}

# Function to start Streamlit backend  
start_backend() {
    echo "🐍 Starting Streamlit Backend..."
    echo "Installing Python dependencies..."
    pip install -r streamlit/requirements.txt
    echo "Starting Streamlit server..."
    streamlit run app.py
}

# Function to build for production
build_frontend() {
    echo "🏗️ Building React Frontend for production..."
    npm run build
    echo "✅ Build complete! Files are in the 'build' directory."
}

# Function to deploy to GitHub Pages
deploy_frontend() {
    echo "🚀 Deploying to GitHub Pages..."
    npm run deploy
    echo "✅ Deployed to GitHub Pages!"
}

# Main menu
echo ""
echo "Choose an option:"
echo "1) Start React Frontend (npm start)"
echo "2) Start Streamlit Backend (streamlit run app.py)" 
echo "3) Build Frontend for Production"
echo "4) Deploy to GitHub Pages"
echo "5) Install All Dependencies"
echo "6) Exit"

read -p "Enter your choice (1-6): " choice

case $choice in
    1)
        start_frontend
        ;;
    2)
        start_backend
        ;;
    3)
        build_frontend
        ;;
    4)
        deploy_frontend
        ;;
    5)
        echo "📦 Installing all dependencies..."
        npm install
        pip install -r streamlit/requirements.txt
        echo "✅ All dependencies installed!"
        ;;
    6)
        echo "👋 Goodbye!"
        exit 0
        ;;
    *)
        echo "❌ Invalid option. Please try again."
        ;;
esac
