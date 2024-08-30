from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, Flask is running!"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    
    if not data:
        return jsonify({'status': 'error', 'message': 'No data received'}), 400

    # Fetch the customer details, providing default values if keys are missing
    customer_email = data.get('email', 'No Email Provided')
    first_name = data.get('first_name', '')
    last_name = data.get('last_name', '')
    customer_name = f"{first_name} {last_name}".strip()

    if not customer_name:
        customer_name = "No Name Provided"

    # Here you would add your logic to sync with your software
    print(f"New customer created: {customer_name}, Email: {customer_email}")

    return jsonify({'status': 'success'}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5001)
