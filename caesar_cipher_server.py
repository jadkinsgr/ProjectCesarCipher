#!/usr/bin/env python3
"""
Caesar Cipher Server
A Flask web server that provides Caesar cipher encryption and decryption services.
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import string
import os
import sys

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

class CaesarCipher:
    """
    A class to handle Caesar cipher encryption and decryption operations.
    """
    
    def __init__(self):
        self.alphabet = string.ascii_lowercase
        self.alphabet_upper = string.ascii_uppercase
    
    def encrypt(self, text, shift):
        """
        Encrypt text using Caesar cipher with given shift.
        
        Args:
            text (str): The text to encrypt
            shift (int): The number of positions to shift (1-25)
            
        Returns:
            str: The encrypted text
        """
        return self._process_text(text, shift)
    
    def decrypt(self, text, shift):
        """
        Decrypt text using Caesar cipher with given shift.
        
        Args:
            text (str): The text to decrypt
            shift (int): The number of positions to shift (1-25)
            
        Returns:
            str: The decrypted text
        """
        return self._process_text(text, -shift)
    
    def _process_text(self, text, shift):
        """
        Process text with the given shift value.
        
        Args:
            text (str): The text to process
            shift (int): The shift value (positive for encrypt, negative for decrypt)
            
        Returns:
            str: The processed text
        """
        result = []
        
        for char in text:
            if char.islower():
                # Handle lowercase letters
                shifted_pos = (ord(char) - ord('a') + shift) % 26
                result.append(chr(shifted_pos + ord('a')))
            elif char.isupper():
                # Handle uppercase letters
                shifted_pos = (ord(char) - ord('A') + shift) % 26
                result.append(chr(shifted_pos + ord('A')))
            else:
                # Keep non-alphabetic characters unchanged
                result.append(char)
        
        return ''.join(result)
    
    def analyze_text(self, text):
        """
        Analyze the given text and return statistics.
        
        Args:
            text (str): The text to analyze
            
        Returns:
            dict: Statistics about the text
        """
        stats = {
            'total_chars': len(text),
            'letters': sum(1 for c in text if c.isalpha()),
            'uppercase': sum(1 for c in text if c.isupper()),
            'lowercase': sum(1 for c in text if c.islower()),
            'digits': sum(1 for c in text if c.isdigit()),
            'spaces': sum(1 for c in text if c.isspace()),
            'punctuation': sum(1 for c in text if c in string.punctuation),
            'letter_frequency': {}
        }
        
        # Calculate letter frequency
        for char in text.lower():
            if char.isalpha():
                stats['letter_frequency'][char] = stats['letter_frequency'].get(char, 0) + 1
        
        return stats
    
    def brute_force_decrypt(self, text):
        """
        Attempt to decrypt text using all possible shifts (1-25).
        
        Args:
            text (str): The text to decrypt
            
        Returns:
            list: List of tuples (shift, decrypted_text)
        """
        results = []
        for shift in range(1, 26):
            decrypted = self.decrypt(text, shift)
            results.append((shift, decrypted))
        return results

# Initialize the cipher
cipher = CaesarCipher()

@app.route('/')
def index():
    """Serve the main HTML page."""
    return send_from_directory('.', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    """Serve static files (CSS, JS, etc.)."""
    return send_from_directory('.', filename)

@app.route('/api/caesar-cipher', methods=['POST'])
def process_caesar_cipher():
    """
    Process Caesar cipher encryption or decryption.
    
    Expected JSON payload:
    {
        "text": "Hello World",
        "shift": 3,
        "operation": "encrypt" or "decrypt"
    }
    
    Returns:
        JSON response with the result
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        text = data.get('text', '')
        shift = data.get('shift', 3)
        operation = data.get('operation', 'encrypt')
        
        # Validate input
        if not text:
            return jsonify({'error': 'Text is required'}), 400
        
        if not isinstance(shift, int) or shift < 1 or shift > 25:
            return jsonify({'error': 'Shift must be an integer between 1 and 25'}), 400
        
        if operation not in ['encrypt', 'decrypt']:
            return jsonify({'error': 'Operation must be either "encrypt" or "decrypt"'}), 400
        
        # Process the text
        if operation == 'encrypt':
            result = cipher.encrypt(text, shift)
        else:
            result = cipher.decrypt(text, shift)
        
        # Get text statistics
        original_stats = cipher.analyze_text(text)
        result_stats = cipher.analyze_text(result)
        
        return jsonify({
            'result': result,
            'original_text': text,
            'shift': shift,
            'operation': operation,
            'stats': {
                'original': original_stats,
                'result': result_stats
            }
        })
        
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

@app.route('/api/analyze', methods=['POST'])
def analyze_text():
    """
    Analyze text and return statistics.
    
    Expected JSON payload:
    {
        "text": "Hello World"
    }
    
    Returns:
        JSON response with text analysis
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        text = data.get('text', '')
        
        if not text:
            return jsonify({'error': 'Text is required'}), 400
        
        stats = cipher.analyze_text(text)
        
        return jsonify({
            'text': text,
            'analysis': stats
        })
        
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

@app.route('/api/brute-force', methods=['POST'])
def brute_force_decrypt():
    """
    Attempt to decrypt text using all possible shifts.
    
    Expected JSON payload:
    {
        "text": "Khoor Zruog"
    }
    
    Returns:
        JSON response with all possible decryptions
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        text = data.get('text', '')
        
        if not text:
            return jsonify({'error': 'Text is required'}), 400
        
        results = cipher.brute_force_decrypt(text)
        
        return jsonify({
            'original_text': text,
            'possible_decryptions': [
                {'shift': shift, 'result': result} 
                for shift, result in results
            ]
        })
        
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'service': 'Caesar Cipher Server',
        'version': '1.0.0'
    })

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({'error': 'Internal server error'}), 500

def main():
    """Main function to run the server."""
    print("🔐 Caesar Cipher Server Starting...")
    print("=" * 50)
    print("Features:")
    print("• Encrypt/Decrypt text using Caesar cipher")
    print("• Text analysis and statistics")
    print("• Brute force decryption")
    print("• Modern web interface")
    print("=" * 50)
    
    # Get port from environment variable or use default
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'True').lower() == 'true'
    
    print(f"🌐 Server running on http://localhost:{port}")
    print(f"📊 Debug mode: {debug}")
    print("Press Ctrl+C to stop the server")
    print("=" * 50)
    
    try:
        app.run(host='0.0.0.0', port=port, debug=debug)
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main() 