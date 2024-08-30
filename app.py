from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# A simple route to check if the app is running
@app.route('/')
def index():
    return "Flask app is running!"

# This is the endpoint that WooCommerce will send data to
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    # Process the webhook data here
    print("Webhook received:")
    print(data)
    
    # Perform any action with the received data, like updating your software
    # You can send the data to your local software using requests
    # Example:
    try:
        response = requests.post("http://localhost:5000/update-software", json=data)
        response.raise_for_status()
        print("Data forwarded to the software successfully.")
    except requests.exceptions.RequestException as e:
        print(f"Failed to forward data to the software: {e}")

    return jsonify({'status': 'success'}), 200

# This is a sample route where your software can send data to Flask app
@app.route('/update-software', methods=['POST'])
def update_software():
    data = request.json
    print("Received data from software:")
    print(data)
    
    # Process the data, such as updating your WooCommerce store via REST API

    return jsonify({'status': 'updated'}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5001)
