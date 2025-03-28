#!/bin/bash

# Print a welcome message
echo "Welcome to the project setup script!"

# Install the required packages
echo "Installing required packages..."
# Navigate to the backend directory, run install.sh, and return to the root directory
cd backend
chmod +x install.sh
./install.sh
cd ..

# Navigate to the backend/src directory and run the Flask application in a new terminal
echo "Starting the Flask backend..."
cd backend/src
osascript -e 'tell application "Terminal" to do script "cd \"'$(pwd)'\" && source .venv/bin/activate && flask run --host=0.0.0.0 --port=8000"'

# Wait for the Flask server to start
echo "Waiting for the Flask backend to start..."
sleep 5

# Run the backend test script in a new terminal
echo "Running backend tests in a new terminal..."
cd ..
osascript -e 'tell application "Terminal" to do script "cd \"'$(pwd)'\" && python3 test_backend_api.py"'

# Wait for the backend tests to complete
echo "Waiting for backend tests to complete..."
sleep 10  # Adjust the sleep time if needed

# Navigate to the frontend directory and run the frontend application in a new terminal
echo "Starting the frontend application..."
cd ../frontend
osascript -e 'tell application "Terminal" to do script "cd \"'$(pwd)'\" && npm install && npm run dev"'

# Print a message indicating that the applications are running
echo "Backend and frontend are running in separate terminals!"