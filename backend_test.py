import sys
import os

# Add the backend/src directory to the Python path
sys.path.insert(0, os.path.join(os.getcwd(), 'backend', 'src'))

# Now try to import the app
try:
    from main import app
    print("Successfully imported the app!")

    # Start the server
    import uvicorn
    print("Starting server on http://0.0.0.0:8000...")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
except ImportError as e:
    print(f"Import error: {e}")
except Exception as e:
    print(f"Error: {e}")