from flask import Flask, request, jsonify, send_file
from flask_socketio import SocketIO
import subprocess
import time
import os

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Path where generated images are stored
IMAGE_PATH = "/home/pi/infinia-frame/images/output.png"

# Simulated image generation with progress updates
@app.route('/generate', methods=['POST'])
def generate_image():
    try:
        for progress in range(0, 101, 10):  # Fake progress from 0 to 100%
            socketio.emit('progress', {'progress': progress})  # Send progress update
            time.sleep(1)  # Simulate processing time
        
        # Run the actual image generation script
        subprocess.run(["python3", "generate_picture.py", "/home/skalahar/infinia-frame/images"], check=True)
        
        # Notify the client that the image is ready
        socketio.emit('progress', {'progress': 100, 'status': 'completed'})
        
        return jsonify({"status": "Image generated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint to download the generated image
@app.route('/download', methods=['GET'])
def download_image():
    if os.path.exists(IMAGE_PATH):
        return send_file(IMAGE_PATH, mimetype='image/png', as_attachment=True)
    return jsonify({"error": "Image not found"}), 404

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
