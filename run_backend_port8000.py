import sys
import os

# Add the backend src directory to the Python path
backend_src_path = os.path.join(os.path.dirname(__file__), 'backend', 'src')
sys.path.insert(0, backend_src_path)

# Add the backend directory to the Python path as well
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)

# Now try to import and run the app
try:
    from src.main import app
    print("Successfully imported the app!")

    # Start the server using uvicorn on port 8000
    import uvicorn
    print("Starting server on http://0.0.0.0:8000...")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)
except ImportError as e:
    print(f"Import error: {e}")
    import traceback
    traceback.print_exc()
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()