#!/bin/bash

# Print a welcome message
echo "Welcome to the project setup script!"

# Install the required packages
echo "Installing required packages..."
cd backend
if [ -f "install.sh" ]; then
    chmod +x install.sh
    ./install.sh
else
    echo "install.sh not found. Exiting..."
    exit 1
fi
cd ..

# Navigate to the backend directory and run the startFlask.sh script
echo "Starting the Flask backend..."
cd backend
if [ -f "startFlask.sh" ]; then
    chmod +x startFlask.sh
    osascript -e 'tell application "Terminal" to do script "cd \"'$(pwd)'\" && ./startFlask.sh"'
else
    echo "startFlask.sh not found. Exiting..."
    exit 1
fi
cd ..

# Wait for the Flask server to start
echo "Waiting for the Flask backend to start..."
sleep 5

# Run the backend test script in a new terminal
echo "Running backend tests in a new terminal..."
cd backend/src
if [ -f "test_backend_api.py" ]; then
    osascript -e 'tell application "Terminal" to do script "cd \"'$(pwd)'\" && source .venv/bin/activate && python3 test_backend_api.py"'
else
    echo "test_backend_api.py not found. Exiting..."
    exit 1
fi
cd ../..

# Wait for the backend tests to complete
echo "Waiting for backend tests to complete..."
sleep 10

# Navigate to the frontend directory and run the frontend application in a new terminal
echo "Starting the frontend application..."
cd frontend
if [ -f "package.json" ]; then
    echo "Installing frontend dependencies..."
    npm install

    echo "Building the frontend application..."
    npm run build

    echo "Starting the frontend preview server in a new terminal..."
    osascript -e 'tell application "Terminal" to do script "cd \"'$(pwd)'\" && npm run preview"'

    echo "Opening the frontend application in the default browser..."
    open "http://localhost:8080"
else
    echo "package.json not found. Exiting..."
    exit 1
fi

# Print a message indicating that the applications are running
echo "Backend and frontend are running in separate terminals!"