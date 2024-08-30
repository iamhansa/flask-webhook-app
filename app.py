from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, Flask is running!"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    # Process the customer data
    customer_email = data.get('email')
    customer_name = data.get('first_name') + " " + data.get('last_name')

    # Here you would add your logic to sync with your software
    print(f"New customer created: {customer_name}, Email: {customer_email}")

    return jsonify({'status': 'success'}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5001)
