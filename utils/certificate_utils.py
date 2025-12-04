# utils/certificate_utils.py

import hashlib
import json
from datetime import datetime
from pathlib import Path
import base64

class CertificateUtils:
    
    @staticmethod
    def calculate_file_hash(file_path, algorithm='sha256'):
        """Calculate hash of a file"""
        hash_func = hashlib.new(algorithm)
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_func.update(chunk)
        return hash_func.hexdigest()
    
    @staticmethod
    def calculate_text_hash(text, algorithm='sha256'):
        """Calculate hash of text"""
        hash_func = hashlib.new(algorithm)
        hash_func.update(text.encode('utf-8'))
        return hash_func.hexdigest()
    
    @staticmethod
    def validate_certificate_data(data):
        """Validate certificate data structure"""
        required_fields = ['issuer_name', 'recipient_name', 'issue_date']
        
        if not isinstance(data, dict):
            return False, "Certificate data must be a dictionary"
        
        for field in required_fields:
            if field not in data:
                return False, f"Missing required field: {field}"
        
        return True, "Valid certificate data"
    
    @staticmethod
    def generate_certificate_id():
        """Generate unique certificate ID"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
        return f"CERT{timestamp}"
    
    @staticmethod
    def create_metadata(certificate_hash, issuer, recipient):
        """Create certificate metadata"""
        return {
            "certificate_hash": certificate_hash,
            "issuer": issuer,
            "recipient": recipient,
            "issue_date": datetime.now().isoformat(),
            "verification_url": f"/verify/{certificate_hash}",
            "timestamp": datetime.now().timestamp()
        }
    
    @staticmethod
    def save_metadata(metadata, file_path):
        """Save metadata to file"""
        with open(file_path, 'w') as f:
            json.dump(metadata, f, indent=2)
    
    @staticmethod
    def load_metadata(file_path):
        """Load metadata from file"""
        with open(file_path, 'r') as f:
            return json.load(f)
    
    @staticmethod
    def encode_to_base64(data):
        """Encode data to base64"""
        if isinstance(data, str):
            data = data.encode('utf-8')
        return base64.b64encode(data).decode('utf-8')
    
    @staticmethod
    def decode_from_base64(encoded_data):
        """Decode data from base64"""
        return base64.b64decode(encoded_data).decode('utf-8')

class CertificateValidator:
    
    @staticmethod
    def validate_hash_structure(hash_string):
        """Validate if string is a valid hash"""
        if not isinstance(hash_string, str):
            return False
        if len(hash_string) != 64:  # SHA-256 produces 64-character hex string
            return False
        try:
            int(hash_string, 16)
            return True
        except ValueError:
            return False
    
    @staticmethod
    def compare_hashes(hash1, hash2):
        """Compare two hashes securely"""
        if len(hash1) != len(hash2):
            return False
        # Use constant-time comparison to prevent timing attacks
        result = 0
        for x, y in zip(hash1, hash2):
            result |= ord(x) ^ ord(y)
        return result == 0
    
    @staticmethod
    def check_tampering(original_hash, current_hash):
        """Check if certificate has been tampered with"""
        if not CertificateValidator.validate_hash_structure(original_hash):
            return False, "Invalid original hash"
        if not CertificateValidator.validate_hash_structure(current_hash):
            return False, "Invalid current hash"
        
        if CertificateValidator.compare_hashes(original_hash, current_hash):
            return True, "Certificate is authentic"
        else:
            return False, "Certificate has been tampered with"

class QRCodeData:
    
    @staticmethod
    def create_qr_data(certificate_data):
        """Create data string for QR code"""
        return json.dumps({
            "type": "certificate_verification",
            "data": certificate_data,
            "timestamp": datetime.now().isoformat()
        })
    
    @staticmethod
    def parse_qr_data(qr_data):
        """Parse QR code data"""
        try:
            return json.loads(qr_data)
        except json.JSONDecodeError:
            # Try to parse as simple string
            return {"raw_data": qr_data}