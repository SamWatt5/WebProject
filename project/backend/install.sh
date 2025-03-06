# Create a virtual environment
python3 -m venv .venv

# Activate the virtual environment
source .venv/bin/activate

# Install the required packages
echo "Installing packages..."
pip intall --upgrade pip
pip install python-dotenv spotipy flask pymongo
echo "Packages installed"