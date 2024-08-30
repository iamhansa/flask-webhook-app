from flask import Flask, request, jsonify

app = Flask(__name__)

# Mock customer data storage
customers = []

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'No data received'}), 400

        customer_email = data.get('email', 'No Email Provided')
        customer_name = data.get('first_name', 'No Name Provided') + " " + data.get('last_name', '')

        # Log the data received for debugging purposes
        print(f"New customer created: {customer_name}, Email: {customer_email}")

        # Store the customer in the mock list for GET requests
        customers.append({
            'first_name': data.get('first_name', 'No Name Provided'),
            'last_name': data.get('last_name', ''),
            'email': data.get('email', 'No Email Provided')
        })

        return jsonify({'status': 'success'}), 200
    except Exception as e:
        print(f"Error processing request: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

# Endpoint to retrieve the latest customer
@app.route('/webhook', methods=['GET'])
def get_latest_customer():
    if customers:
        latest_customer = customers[-1]  # Return the last customer in the list
        return jsonify(latest_customer), 200
    else:
        return jsonify({'error': 'No customers found'}), 404

# New endpoint to retrieve all customers
@app.route('/get_customers', methods=['GET'])
def get_customers():
    if customers:
        return jsonify(customers), 200
    else:
        return jsonify({'error': 'No customers found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
