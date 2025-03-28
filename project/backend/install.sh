# Navigate to the src directory
cd src

# Create a virtual environment inside the src directory
python3 -m venv .venv

# Activate the virtual environment
source .venv/bin/activate

# Install the required packages
echo "Installing packages..."
pip install --upgrade pip
pip install python-dotenv spotipy flask flask_cors requests flask_jwt_extended pymongo flask_session flask-restx
echo "Packages installed"