from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os
from datetime import datetime
from services.ChildPubService import ChildPubService
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

app = Flask(__name__)
CORS(app)

def get_latest_json_file(network_code):
    """Get the most recent JSON file for specific network code."""
    pattern = f'child_publishers_{network_code}_*.json'
    files = [f for f in os.listdir('.') if f.startswith(f'child_publishers_{network_code}_') and f.endswith('.json')]
    if not files:
        return None
    return max(files, key=lambda f: os.path.getmtime(f))

def load_json_data(filename):
    """Load data from JSON file."""
    if not filename or not os.path.exists(filename):
        return None
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

def is_data_fresh(fetched_at, max_hours=24):
    """Check if data is less than max_hours old."""
    try:
        fetched_time = datetime.fromisoformat(fetched_at)
        now = datetime.now()
        diff = now - fetched_time
        hours_old = diff.total_seconds() / 3600
        return hours_old < max_hours, hours_old
    except:
        return False, 999

@app.route('/')
def home():
    """API documentation."""
    return jsonify({
        'name': 'GAM Child Publishers API',
        'version': '1.0.0',
        'endpoints': {
            '/': 'API documentation',
            '/fetch?network_code=<code>': 'Fetch child publishers for network (cached)',
            '/fetch?network_code=<code>&refresh=true': 'Force fresh fetch from GAM',
            '/health': 'Health check'
        },
        'usage': {
            'example_1': '/fetch?network_code=23033612553',
            'example_2': '/fetch?network_code=23033612553&refresh=true'
        }
    })

@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/fetch', methods=['GET'])
def fetch_network_data():
    """
    Fetch child publishers data for a GAM network.
    
    Query Parameters:
        network_code (required): 11-digit GAM network code
        refresh (optional): Set to 'true' to force fresh fetch from GAM
    
    Returns:
        JSON with child publishers data
    """
    # Get network code from query parameters
    network_code = request.args.get('network_code') or request.args.get('networkCode')
    
    if not network_code:
        return jsonify({
            'success': False,
            'error': 'Missing required parameter: network_code',
            'usage': '/fetch?network_code=23033612553'
        }), 400
    
    # Validate network code (should be 11 digits)
    if not network_code.isdigit() or len(network_code) != 11:
        return jsonify({
            'success': False,
            'error': 'Invalid network_code. Must be 11 digits.',
            'provided': network_code
        }), 400
    
    # Check if refresh is requested
    force_refresh = request.args.get('refresh', '').lower() == 'true'
    
    # Try to load cached data first
    if not force_refresh:
        cached_file = get_latest_json_file(network_code)
        if cached_file:
            cached_data = load_json_data(cached_file)
            if cached_data:
                is_fresh, hours_old = is_data_fresh(cached_data.get('fetched_at', ''))
                
                if is_fresh:
                    logging.info(f"Returning cached data for network {network_code} ({hours_old:.1f} hours old)")
                    return jsonify({
                        'success': True,
                        'source': 'cache',
                        'cached_hours_ago': round(hours_old, 2),
                        'network_code': cached_data['network_code'],
                        'total_count': cached_data['total_count'],
                        'fetched_at': cached_data['fetched_at'],
                        'children': cached_data['child_publishers'],
                        'message': f'Data from cache ({hours_old:.1f} hours old). Add &refresh=true to force fresh fetch.'
                    })
    
    # Fetch fresh data from GAM
    try:
        logging.info(f"Fetching fresh data from GAM for network {network_code}...")
        result = ChildPubService.fetch_account_status(network_code=network_code)
        
        if isinstance(result, dict):
            logging.info(f"Successfully fetched {result.get('total_count', 0)} publishers for network {network_code}")
            return jsonify({
                'success': True,
                'source': 'fresh',
                'network_code': result['network_code'],
                'total_count': result['total_count'],
                'fetched_at': result['fetched_at'],
                'children': result['child_publishers'],
                'message': 'Data fetched successfully from GAM'
            })
        else:
            logging.error(f"Failed to fetch data for network {network_code}: {result}")
            return jsonify({
                'success': False,
                'error': f'Failed to fetch data: {result}'
            }), 500
            
    except Exception as e:
        logging.error(f"Error fetching data for network {network_code}: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 'Endpoint not found',
        'available_endpoints': ['/', '/fetch', '/health']
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500

if __name__ == '__main__':
    # Run on all interfaces so it's accessible from network
    app.run(host='0.0.0.0', port=5000, debug=True)
