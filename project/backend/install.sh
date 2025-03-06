# Create a virtual environment
python3 -m venv .venv

# Activate the virtual environment
source .venv/bin/activate

# Install the required packages
echo "Installing packages..."
pip install --upgrade pip
pip install python-dotenv spotipy flask flask_cors flask_jwt_extended pymongo werkzeug
echo "Packages installed"