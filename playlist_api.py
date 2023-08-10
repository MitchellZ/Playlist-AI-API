from flask import Flask, jsonify, request

# Import PaLM Service functions
from palm_service import *

app = Flask(__name__)

# Start Enpoint
@app.route('/start', methods=['GET'])

def start():
    # Test value
    (test) = True

    if (test):
        # Success
        response = {
        'message': 'Success!'
        }
        return jsonify(response), 200

    # Error
    response = {
        'message': 'Error!'
    }
    return jsonify(response), 500

# Example Endpoint
@app.route('/endpoint', methods=['GET'])

def endpoint():
    message = request.args.get('message')  # Retrieve the 'message' parameter from the query string

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
            response = {
                'message': 'Unable to generate playlist!'
            }
            return jsonify(response), 501


if __name__ == '__main__':
    initializeConversation()
    app.run(debug=True)