py -m venv .venv
source .venv/bin/activate
.venv/scripts/activate

echo "Installing packages..."
pip install python-dotenv spotipy flask
echo "Packages installed"