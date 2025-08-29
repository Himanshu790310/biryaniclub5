
from flask import Flask, request, jsonify
from geolocation import LocationService, STORE_LOCATION

app = Flask(__name__)
location_service = LocationService()

@app.route('/calculate-delivery', methods=['POST'])
def calculate_delivery():
    """Calculate delivery charge based on customer address"""
    try:
        data = request.get_json()
        customer_address = data.get('address')
        
        if not customer_address:
            return jsonify({'error': 'Address is required'}), 400
        
        # Get customer coordinates
        customer_coords = location_service.get_coordinates(customer_address)
        
        if not customer_coords:
            return jsonify({'error': 'Could not find location for the provided address'}), 400
        
        # Calculate distance from store
        distance = location_service.calculate_distance(STORE_LOCATION, customer_coords)
        
        # Calculate delivery charge
        delivery_charge = location_service.calculate_delivery_charge(distance)
        
        return jsonify({
            'success': True,
            'distance_km': round(distance, 2),
            'delivery_charge': delivery_charge,
            'customer_coordinates': customer_coords,
            'store_coordinates': STORE_LOCATION
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/delivery-zones', methods=['GET'])
def get_delivery_zones():
    """Get delivery zone pricing information"""
    zones = [
        {'range': '0-5 km', 'charge': 2.99, 'description': 'Local delivery'},
        {'range': '5-10 km', 'charge': 4.99, 'description': 'Nearby delivery'},
        {'range': '10-20 km', 'charge': 7.99, 'description': 'Standard delivery'},
        {'range': '20-50 km', 'charge': 12.99, 'description': 'Extended delivery'},
        {'range': '50+ km', 'charge': 19.99, 'description': 'Long distance delivery'}
    ]
    return jsonify({'delivery_zones': zones})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
