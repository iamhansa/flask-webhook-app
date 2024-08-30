from flask import Flask, request, jsonify

app = Flask(__name__)

customers = []

@app.route('/')
def index():
    return "Flask app is running!"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print(f"Received data: {data}")  # Log the entire payload for debugging

    if data is None:
        return jsonify({'status': 'error', 'message': 'No data received'}), 400

    customer_email = data.get('email', 'No Email Provided')
    full_name = data.get('first_name', 'No Name Provided')
    
    if 'last_name' in data and data['last_name']:
        full_name += f" {data['last_name']}"

    # Split the full name into first and last name
    name_parts = full_name.split(' ', 1)
    first_name = name_parts[0]
    last_name = name_parts[1] if len(name_parts) > 1 else ""

    customer = {
        "email": customer_email,
        "first_name": first_name,
        "last_name": last_name,
        "phone": data.get('phone', 'No Phone Provided'),
        "city": data.get('city', 'No City Provided')
    }

    # Prevent adding the same customer twice
    if customer not in customers:
        customers.append(customer)
        print(f"New customer created: {first_name} {last_name}, Email: {customer_email}")
    else:
        print(f"Duplicate customer detected: {first_name} {last_name}, Email: {customer_email}")

    return jsonify({'status': 'success'}), 200

@app.route('/get_customers', methods=['GET'])
def get_customers():
    processed_customers = []
    
    for customer in customers:
        full_name = customer.get('first_name', 'No Name Provided')
        
        if 'last_name' in customer and customer['last_name']:
            full_name += f" {customer['last_name']}"
        
        # Split the full name into first and last name
        name_parts = full_name.split(' ', 1)
        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else ""
        
        processed_customers.append({
            "first_name": first_name,
            "last_name": last_name,
            "email": customer.get('email', 'No Email Provided'),
            "phone": customer.get('phone', 'No Phone Provided'),
            "city": customer.get('city', 'No City Provided')
        })
    
    return jsonify(processed_customers), 200

if __name__ == '__main__':
    app.run(debug=True, port=5001)
