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
    first_name = data.get('first_name', 'No Name Provided')
    last_name = data.get('last_name', '')
    
    # Retrieve phone and city from billing or shipping address
    phone = data.get('phone', '')
    city = data.get('city', '')

    if 'billing' in data:
        phone = data['billing'].get('phone', 'No Phone Provided')
        city = data['billing'].get('city', 'No City Provided')
    elif 'shipping' in data:
        phone = data['shipping'].get('phone', 'No Phone Provided')
        city = data['shipping'].get('city', 'No City Provided')

    customer = {
        "email": customer_email,
        "first_name": first_name,
        "last_name": last_name,
        "phone": phone,
        "city": city
    }

    # Prevent adding the same customer twice
    if not any(cust['email'] == customer_email for cust in customers):
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
