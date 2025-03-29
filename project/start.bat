@echo off

:: Print a welcome message
echo Welcome to the project setup script!

:: Install the required packages
echo Installing required packages...
:: Navigate to the backend directory, run install.bat, and return to the root directory
cd backend
if exist install.bat (
    call install.bat
) else (
    echo install.bat not found. Exiting...
    exit /b 1
)
cd ..

:: Navigate to the backend/src directory and run the Flask application in a new terminal
echo Starting the Flask backend...
cd backend\src
start cmd /k "cd /d %cd% && .venv\Scripts\activate && flask run --host=0.0.0.0 --port=8000"

:: Wait for the Flask server to start
echo Waiting for the Flask backend to start...
timeout /t 5 >nul

:: Run the backend test script in a new terminal
echo Running backend tests in a new terminal...
cd ..
start cmd /k "cd /d %cd% && .venv\Scripts\activate && python test_backend_api.py"

:: Wait for the backend tests to complete
echo Waiting for backend tests to complete...
timeout /t 10 >nul

:: Navigate to the frontend directory and run the frontend application in a new terminal
echo Starting the frontend application...
cd ..\frontend
start cmd /k "cd /d %cd% && npm install && npm run dev"

:: Print a message indicating that the applications are running
echo Backend and frontend are running in separate terminals!