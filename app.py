from flask import Flask, render_template, request, jsonify
from datetime import datetime
import json
import os
from urllib.parse import urlparse

app = Flask(__name__)

# Configuration
FEEDBACK_FILE = 'feedback_data.json'

def validate_url(url):
    """Validate if a URL is properly formatted."""
    if not url:
        return True
    try:
        result = urlparse(url)
        return all([result.scheme in ('http', 'https'), result.netloc])
    except:
        return False

def load_feedback():
    """Load existing feedback from JSON file."""
    if os.path.exists(FEEDBACK_FILE):
        try:
            with open(FEEDBACK_FILE, 'r') as f:
                return json.load(f)
        except:
            return []
    return []

def save_feedback(feedback_list):
    """Save feedback to JSON file."""
    with open(FEEDBACK_FILE, 'w') as f:
        json.dump(feedback_list, f, indent=2)

@app.route('/')
def index():
    """Render feedback form."""
    return render_template('feedback.html')

@app.route('/api/feedback', methods=['POST'])
def submit_feedback():
    """Handle feedback submission."""
    try:
        data = request.get_json()
        
        # Validation
        if not data:
            return jsonify({'success': False, 'message': 'No data provided'}), 400
        
        name = data.get('name', '').strip()
        suggestion = data.get('suggestion', '').strip()
        email = data.get('email', '').strip()
        link = data.get('link', '').strip()
        
        # Required field validation
        if not name:
            return jsonify({'success': False, 'message': 'Name is required'}), 400
        
        if not suggestion:
            return jsonify({'success': False, 'message': 'Suggestion is required'}), 400
        
        if len(name) > 100:
            return jsonify({'success': False, 'message': 'Name is too long (max 100 characters)'}), 400
        
        if len(suggestion) > 5000:
            return jsonify({'success': False, 'message': 'Suggestion is too long (max 5000 characters)'}), 400
        
        # Email validation
        if email and len(email) > 255:
            return jsonify({'success': False, 'message': 'Email is too long'}), 400
        
        if email and '@' not in email:
            return jsonify({'success': False, 'message': 'Invalid email format'}), 400
        
        # URL validation
        if link and not validate_url(link):
            return jsonify({'success': False, 'message': 'Invalid URL format. Please use http:// or https://'}), 400
        
        # Create feedback entry
        feedback_entry = {
            'id': int(datetime.now().timestamp() * 1000),
            'name': name,
            'email': email if email else None,
            'suggestion': suggestion,
            'link': link if link else None,
            'timestamp': datetime.now().isoformat(),
            'status': 'pending'  # pending, approved, rejected
        }
        
        # Load existing feedback
        feedback_list = load_feedback()
        
        # Add new feedback
        feedback_list.append(feedback_entry)
        
        # Save updated feedback
        save_feedback(feedback_list)
        
        return jsonify({
            'success': True,
            'message': 'Thank you for your feedback! Your suggestion has been submitted and will be reviewed by our team.',
            'id': feedback_entry['id']
        }), 201
    
    except Exception as e:
        app.logger.error(f'Error processing feedback: {str(e)}')
        return jsonify({'success': False, 'message': 'An error occurred while processing your feedback.'}), 500

@app.route('/api/feedback/list', methods=['GET'])
def list_feedback():
    """Get approved feedback (for display on site)."""
    try:
        feedback_list = load_feedback()
        approved = [f for f in feedback_list if f.get('status') == 'approved']
        return jsonify({
            'success': True,
            'total': len(feedback_list),
            'approved_count': len(approved),
            'feedback': approved
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'message': 'Error loading feedback'}), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({'success': False, 'message': 'Endpoint not found'}), 404

@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors."""
    return jsonify({'success': False, 'message': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)
