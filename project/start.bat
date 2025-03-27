@echo off
echo "Starting the application..."
cd ./backend
echo "Installing packages"
call .venv/scripts/activate
pip install python-dotenv spotipy flask flask_cors pymongo flask_session flask-restx
echo "Packages installed"
echo "Starting the backend server"
cd src
start cmd /k py -m flask run --host=0.0.0.0 --port=8000
echo "Backend server online"
cd ../../frontend
echo "Starting the frontend server"
start cmd /k npm run dev
echo "Frontend server online"