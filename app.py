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

    if not data:
        return jsonify({'status': 'failed', 'message': 'No data received'}), 400

    # Extract required fields
    customer_email = data.get('email')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    
    # Validate required fields
    if not customer_email or not first_name or not last_name:
        print("Required data missing: email, first name, or last name")
        return jsonify({'status': 'failed', 'message': 'Required data missing'}), 400

    # Optional fields with fallback to empty strings if not provided
    phone = data.get('phone', '')
    city = data.get('city', '')

    customer = {
        "email": customer_email,
        "first_name": first_name,
        "last_name": last_name,
        "phone": phone,
        "city": city
    }

    # Prevent adding the same customer twice
    if customer not in customers:
        customers.append(customer)
        print(f"New customer created: {first_name} {last_name}, Email: {customer_email}, Phone: {phone}, City: {city}")
    else:
        print(f"Duplicate customer detected: {first_name} {last_name}, Email: {customer_email}")

    return jsonify({'status': 'success'}), 200

@app.route('/get_customers', methods=['GET'])
def get_customers():
    return jsonify(customers), 200

if __name__ == '__main__':
    app.run(debug=True, port=5001)
