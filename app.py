from flask import Flask, request, jsonify

app = Flask(__name__)

# Store customer data in a simple list for example purposes
customers = []

@app.route('/')
def index():
    return "Hello, Flask is running!"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    customer_email = data.get('email', 'No Email Provided')
    customer_name = data.get('first_name', 'No Name Provided') + " " + data.get('last_name', '')
    
    # Save the customer to our list
    customers.append({
        'email': customer_email,
        'name': customer_name,
        'first_name': data.get('first_name', 'No First Name Provided'),
        'last_name': data.get('last_name', 'No Last Name Provided')
    })

    print(f"New customer created: {customer_name}, Email: {customer_email}")
    return jsonify({'status': 'success'}), 200

# Route to fetch customer data
@app.route('/customers', methods=['GET'])
def get_customers():
    return jsonify(customers)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
