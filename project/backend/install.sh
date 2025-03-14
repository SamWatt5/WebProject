# Create a virtual environment
python3 -m venv .venv

# Activate the virtual environment
source .venv/bin/activate

# Install the required packages
echo "Installing packages..."
pip install --upgrade pip
pip install python-dotenv flask_jwt_extended spotipy flask flask_cors pymongo werkzeug
echo "Packages installed"