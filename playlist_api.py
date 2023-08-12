from flask import Flask, jsonify, request

# Import PaLM Service functions
from palm_service import *

app = Flask(__name__)

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

# Example Endpoint
@app.route('/query', methods=['GET'])

def query():
    message = request.args.get('message')  # Retrieve the 'message' parameter from the query string
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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)