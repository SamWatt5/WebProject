py -m venv .venv
@REM source .venv/bin/activate
call .venv/scripts/activate

echo "Installing packages..."
pip install python-dotenv spotipy flask flask_cors flask_jwt_extended pymongo
echo "Packages installed"