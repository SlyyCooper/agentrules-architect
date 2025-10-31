import os

from flask import Flask, send_from_directory

app = Flask(__name__, static_folder=None) # Disable default static folder

# Get the directory where this script is located
base_dir = os.path.abspath(os.path.dirname(__file__))

@app.route('/')
def index():
    """Serves the main HTML file."""
    print(f"Serving index.html from: {base_dir}")
    try:
        return send_from_directory(base_dir, 'index.html')
    except Exception as e:
        print(f"Error serving index.html: {e}")
        return "Error loading game assets.", 500

@app.route('/<path:filename>')
def serve_static(filename):
    """Serves static files like main.js."""
    print(f"Serving static file: {filename} from: {base_dir}")
    # Basic security check: only allow specific files or types if needed
    if filename not in ['main.js']: # Add other allowed files if necessary
         # For more complex apps, you might check file extensions or use a dedicated static dir
         # return "File not allowed", 403
         pass # Allow any file in the base dir for simplicity here
    try:
        return send_from_directory(base_dir, filename)
    except Exception as e:
        print(f"Error serving {filename}: {e}")
        return "Error loading game assets.", 500

if __name__ == '__main__':
    print("Starting Flask server for Flight Simulator...")
    print(f"Serving files from directory: {base_dir}")
    print("Access the game at: http://127.0.0.1:5000")
    # Use host='0.0.0.0' to make it accessible on your network
    app.run(host='0.0.0.0', port=5000, debug=True)
