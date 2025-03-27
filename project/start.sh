#!/bin/bash

# Print a welcome message
echo "Welcome to the project setup script!"

# Install the required packages
echo "Installing required packages..."
# Navigate to the install.sh script and run it
chmod +x backend/install.sh
./backend/install.sh

# Navigate to the backend/src directory and run the Flask application in a new terminal
echo "Starting the Flask backend..."
cd backend/src
osascript -e 'tell application "Terminal" to do script "cd \"'$(pwd)'\" && source .venv/bin/activate && flask run --host=0.0.0.0 --port=8000"'

# Navigate to the frontend directory and run the frontend application in a new terminal
echo "Starting the frontend application..."
cd ../../frontend
osascript -e 'tell application "Terminal" to do script "cd \"'$(pwd)'\" && npm install && npm run dev"'

# Check if the backend command was successful
if [ $? -eq 0 ]; then
    echo "Backend started successfully!"
else
    echo "Failed to start the backend."
fi

# Check if the frontend command was successful
if [ $? -eq 0 ]; then
    echo "Frontend started successfully!"
else
    echo "Failed to start the frontend."
fi
# Wait for a few seconds to allow the applications to start
sleep 5
# Print a message indicating that the applications are running
echo "Backend and frontend are running in separate terminals!"
# Wait for a few seconds to allow the applications to start
sleep 5
# Print a message indicating that the applications are running
echo "Backend and frontend are running in separate terminals!"

# End of script
# This script is used to set up and run the backend and frontend of the project.
# It navigates to the backend/src directory, runs the Flask application, and then navigates to the frontend directory to run the React application.
# The script also checks if each command was successful and prints appropriate messages.        