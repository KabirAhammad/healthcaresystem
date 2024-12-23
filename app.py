from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS  # Import CORS to handle cross-origin requests
import threading
import webbrowser  # To open URLs
import os  # For working with file paths
import server  # Ensure server.py contains the necessary voice assistant logic

# Initialize the Flask application
app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

# Serve static files (like CSS, JS, images) from the static folder
app.config['STATIC_FOLDER'] = 'static'

@app.route('/voice_assistant', methods=['GET'])
def voice_assistant():
    print("Voice Assistant triggered")  # Log when the route is accessed

    def run_voice_assistant():
        """Runs the voice assistant logic from server.py."""
        try:
            server.voice_google_search()  # Call the function from server.py to handle voice assistant logic
        except Exception as e:
            print(f"Error in voice assistant thread: {e}")

    assistant_thread = threading.Thread(target=run_voice_assistant)
    assistant_thread.daemon = True  # Ensure the thread exits with the main program
    assistant_thread.start()

    return jsonify({"status": "Voice assistant triggered"}), 200

@app.route('/voice_assistant_process', methods=['POST'])
def voice_assistant_process():
    data = request.get_json()  # Get the command sent from the frontend
    command = data.get('command', '').lower()  # Get the command text

    print(f"Received command: {command}")

    # Check if the command is health-related
    if "health" in command or "symptom" in command or "fever" in command or "pain" in command:
        # Open NHS website with a health search
        nhs_url = f"https://www.nhs.uk/search/results?q={command}"
        webbrowser.open(nhs_url)
        return jsonify({"status": f"Searching for health-related info: {command}"}), 200
    elif "appointment" in command or "schedule" in command:
        # Respond with scheduling action, for example
        return jsonify({"status": "Scheduling an appointment."}), 200
    else:
        # For all other queries, perform a Google search
        google_url = f"https://www.google.com/search?q={command}"
        webbrowser.open(google_url)
        return jsonify({"status": f"Searching on Google for: {command}"}), 200

# Serve the index.html file from the root folder
@app.route('/', methods=['GET'])
def home():
    """Serve the index.html file from the root folder."""
    return send_from_directory(os.getcwd(), 'index.html')

@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors for undefined routes."""
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(500)
def internal_server_error(e):
    """Handle 500 errors for server issues."""
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    try:
        print("Starting Flask server...")
        # Allow external access by setting host='0.0.0.0' and running on port 5001
        app.run(host='0.0.0.0', port=5001, debug=True)
    except KeyboardInterrupt:
        print("Server shutting down gracefully.")