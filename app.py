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

    customer_email = data.get('email', 'No Email Provided')
    full_name = data.get('first_name', 'No Name Provided')
    phone = data.get('phone', 'No Phone Provided')
    city = data.get('city', 'No City Provided')
    
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
