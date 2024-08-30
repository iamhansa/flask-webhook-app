from flask import Flask, request, jsonify

app = Flask(__name__)

customers = []

@app.route('/')
def index():
    return "Flask app is running!"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if data is None:
        print("Received data: None")
        return jsonify({'status': 'failed', 'reason': 'No data received'}), 400
    
    print(f"Received data: {data}")

    customer_email = data.get('email')
    first_name = data.get('first_name')
    last_name = data.get('last_name')

    if not customer_email or not first_name:
        print("Incomplete customer data, skipping...")
        return jsonify({'status': 'failed', 'reason': 'Incomplete data'}), 400

    # Check if this customer already exists
    for customer in customers:
        if customer['email'] == customer_email:
            print(f"Customer with email {customer_email} already exists, skipping...")
            return jsonify({'status': 'failed', 'reason': 'Customer already exists'}), 400

    # Add the new customer
    customer = {
        "email": customer_email,
        "first_name": first_name,
        "last_name": last_name if last_name else ""
    }

    customers.append(customer)
    print(f"New customer created: {first_name} {last_name}, Email: {customer_email}")

    return jsonify({'status': 'success'}), 200

@app.route('/get_customers', methods=['GET'])
def get_customers():
    return jsonify(customers), 200

if __name__ == '__main__':
    app.run(debug=True, port=5001)
