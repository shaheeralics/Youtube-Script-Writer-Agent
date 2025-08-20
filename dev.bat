@echo off
:: YouTube Script Writer AI - Development Script for Windows
:: This script helps you manage both frontend and backend development

echo 🎬 YouTube Script Writer AI - Development Manager
echo ==================================================

:menu
echo.
echo Choose an option:
echo 1) Start React Frontend (npm start)
echo 2) Start Streamlit Backend (streamlit run app.py)
echo 3) Build Frontend for Production
echo 4) Push to GitHub (Auto-Deploy)
echo 5) Install All Dependencies
echo 6) Exit

set /p choice="Enter your choice (1-6): "

if "%choice%"=="1" goto frontend
if "%choice%"=="2" goto backend
if "%choice%"=="3" goto build
if "%choice%"=="4" goto deploy
if "%choice%"=="5" goto install
if "%choice%"=="6" goto exit
echo ❌ Invalid option. Please try again.
goto menu

:frontend
echo 🚀 Starting React Frontend...
echo Installing dependencies...
call npm install
echo Starting development server...
call npm start
goto menu

:backend
echo 🐍 Starting Streamlit Backend...
echo Installing Python dependencies...
call pip install -r streamlit/requirements.txt
echo Starting Streamlit server...
call streamlit run app.py
goto menu

:build
echo 🏗️ Building React Frontend for production...
call npm run build
echo ✅ Build complete! Files are in the 'build' directory.
goto menu

:deploy
echo 🚀 Pushing to GitHub (Auto-Deploy)...
echo Adding all changes...
git add .
set /p message="Enter commit message: "
git commit -m "%message%"
git push origin main
echo ✅ Pushed to GitHub! Check Actions tab for deployment status.
goto menu

:install
echo 📦 Installing all dependencies...
call npm install
call pip install -r streamlit/requirements.txt
echo ✅ All dependencies installed!
goto menu

:exit
echo 👋 Goodbye!
pause
