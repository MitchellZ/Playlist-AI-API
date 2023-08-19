from flask import Flask, jsonify, redirect, request
from flask_cors import CORS

# Import PaLM Service functions
from palm_service import *

app = Flask(__name__)
CORS(app)

# Start Enpoint
@app.route('/ping', methods=['GET'])

def ping():
    # Test value
    (test) = True

    if (test):
        # Success
        response = {
        'message': 'Pong!'
        }
        print('Received ping.\n')
        return jsonify(response), 200

    # Error
    response = {
        'message': 'Error!'
    }
    return jsonify(response), 500

# Playlist generation endpoint
@app.route('/query', methods=['GET'])

def query():
    message = request.args.get('message')  # Retrieve the 'message' parameter from the query string

    # Replace hashtags with spaces
    message = message.replace('#', ' ')
    
    print('Processing request: ' + message + '\n')

    if (message == None):
        # Error
        response = {
            'message': 'No message provided!'
        }
        return jsonify(response), 400

    else:
        playlist = prompt(message)

        if (playlist):
            # Success
            response = {
            'message': 'Received: ' + message,
            'response': playlist
            }
            return jsonify(response), 200
        else:
            # Error
            print('Error: Unable to generate playlist.\n')
            response = {
                'message': 'Unable to generate playlist.'
            }
            return jsonify(response), 500

# Audio endpoint
@app.route('/audio', methods=['GET'])
def get_audio():
    video_id = request.args.get('id')  # Retrieve the 'id' parameter from the query string

    if video_id is None:
        response = {
            'message': 'No video ID provided!'
        }
        return jsonify(response), 400

    audio_url = f"https://vid.puffyan.us/latest_version?id={video_id}&itag=140"

    try:
        return redirect(audio_url)  # Redirect the user to the audio URL
    except Exception as e:
        # Error
        print('Error:', e)
        response = {
            'message': 'Error redirecting to audio URL!'
        }
        return jsonify(response), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)