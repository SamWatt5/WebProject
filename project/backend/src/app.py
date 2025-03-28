from . import create_app

# Create the Flask application instance
app = create_app()

if __name__ == "__main__":
    """
    Entry point for the application.

    This script runs the Flask application in debug mode.
    """
    app.run(debug=True)
