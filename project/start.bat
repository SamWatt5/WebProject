@echo off

:: Print a welcome message
echo Welcome to the project setup script!

:: Install the required packages
echo Installing required packages...
cd backend
if exist install.bat (
    call install.bat
) else (
    echo install.bat not found. Exiting...
    exit /b 1
)
cd ..

:: Navigate to the backend directory and run the startFlask.bat script
echo Starting the Flask backend...
cd backend
if exist startFlask.bat (
    start cmd /k "call startFlask.bat"
) else (
    echo startFlask.bat not found. Exiting...
    exit /b 1
)
cd ..

:: Wait for the Flask server to start
echo Waiting for the Flask backend to start...
timeout /t 5 >nul

:: Run the backend test script in a new terminal
echo Running backend tests in a new terminal...
cd backend\src
if exist test_backend_api.py (
    start cmd /k "cd /d %cd% && .venv\Scripts\activate && python test_backend_api.py"
) else (
    echo test_backend_api.py not found. Exiting...
    exit /b 1
)
cd ..\..

:: Wait for the backend tests to complete
echo Waiting for backend tests to complete...
timeout /t 30 >nul

:: Navigate to the frontend directory and run the frontend application in a new terminal
echo Starting the frontend application...
cd frontend
if exist package.json (
    npm install
    start cmd /k "npm run dev"
) else (
    echo package.json not found. Exiting...
    exit /b 1
)

:: Print a message indicating that the applications are running
echo Backend and frontend are running in separate terminals!