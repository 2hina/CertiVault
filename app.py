from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_file
from werkzeug.utils import secure_filename
import os
import hashlib
import qrcode
from PIL import Image
import io
import json
from datetime import datetime
import sqlite3
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
import base64

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'pdf', 'txt'}

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('database', exist_ok=True)

# Initialize database
def init_db():
    conn = sqlite3.connect('database/certificates.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS certificates
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  certificate_hash TEXT UNIQUE,
                  issuer_name TEXT,
                  recipient_name TEXT,
                  issue_date TEXT,
                  certificate_data TEXT,
                  digital_signature TEXT,
                  qr_code_path TEXT,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

init_db()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def generate_hash(file_path):
    """Generate SHA-256 hash of file"""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def generate_text_hash(text):
    """Generate SHA-256 hash of text"""
    return hashlib.sha256(text.encode()).hexdigest()

def generate_qr_code(data, filename):
    """Generate QR code from data"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    qr_path = os.path.join('static', 'qrcodes', f"{filename}.png")
    os.makedirs(os.path.dirname(qr_path), exist_ok=True)
    img.save(qr_path)
    return qr_path

def generate_key_pair():
    """Generate RSA key pair for digital signature"""
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    public_key = private_key.public_key()
    
    return private_key, public_key

def create_digital_signature(data, private_key):
    """Create digital signature for data"""
    signature = private_key.sign(
        data.encode(),
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return base64.b64encode(signature).decode()

def verify_signature(data, signature, public_key):
    """Verify digital signature"""
    try:
        public_key.verify(
            base64.b64decode(signature),
            data.encode(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except:
        return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_certificate():
    if request.method == 'POST':
        # Check if file was uploaded
        if 'certificate' not in request.files:
            flash('No file selected')
            return redirect(request.url)
        
        file = request.files['certificate']
        
        if file.filename == '':
            flash('No file selected')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # Get form data
            issuer_name = request.form.get('issuer_name', 'Unknown Issuer')
            recipient_name = request.form.get('recipient_name', 'Unknown Recipient')
            
            # Generate hash
            certificate_hash = generate_hash(file_path)
            
            # Generate QR code
            qr_data = f"Certificate Hash: {certificate_hash}\nIssuer: {issuer_name}\nRecipient: {recipient_name}"
            qr_path = generate_qr_code(qr_data, certificate_hash[:10])
            
            # Generate digital signature (simulated)
            private_key, public_key = generate_key_pair()
            signature_data = f"{certificate_hash}{issuer_name}{recipient_name}"
            digital_signature = create_digital_signature(signature_data, private_key)
            
            # Save to database
            conn = sqlite3.connect('database/certificates.db')
            c = conn.cursor()
            c.execute('''INSERT INTO certificates 
                         (certificate_hash, issuer_name, recipient_name, issue_date, 
                          certificate_data, digital_signature, qr_code_path) 
                         VALUES (?, ?, ?, ?, ?, ?, ?)''',
                     (certificate_hash, issuer_name, recipient_name, 
                      datetime.now().strftime("%Y-%m-%d"), 
                      filename, digital_signature, qr_path))
            conn.commit()
            conn.close()
            
            flash('Certificate uploaded successfully!')
            
            # Return certificate info
            return render_template('upload.html', 
                                 certificate_hash=certificate_hash,
                                 qr_code=qr_path.replace('static/', ''),
                                 issuer_name=issuer_name,
                                 recipient_name=recipient_name)
    
    return render_template('upload.html')

@app.route('/verify', methods=['GET', 'POST'])
def verify_certificate():
    if request.method == 'POST':
        verification_method = request.form.get('verification_method')
        
        if verification_method == 'hash':
            certificate_hash = request.form.get('certificate_hash')
            
            # Search in database
            conn = sqlite3.connect('database/certificates.db')
            c = conn.cursor()
            c.execute('SELECT * FROM certificates WHERE certificate_hash = ?', (certificate_hash,))
            certificate = c.fetchone()
            conn.close()
            
            if certificate:
                return render_template('verify.html', 
                                     found=True,
                                     certificate={
                                         'hash': certificate[1],
                                         'issuer': certificate[2],
                                         'recipient': certificate[3],
                                         'issue_date': certificate[4],
                                         'signature': certificate[6]
                                     })
            else:
                return render_template('verify.html', found=False, message="Certificate not found!")
        
        elif verification_method == 'upload':
            if 'certificate' not in request.files:
                flash('No file selected')
                return redirect(request.url)
            
            file = request.files['certificate']
            
            if file.filename == '':
                flash('No file selected')
                return redirect(request.url)
            
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                
                # Generate hash
                uploaded_hash = generate_hash(file_path)
                
                # Search in database
                conn = sqlite3.connect('database/certificates.db')
                c = conn.cursor()
                c.execute('SELECT * FROM certificates WHERE certificate_hash = ?', (uploaded_hash,))
                certificate = c.fetchone()
                conn.close()
                
                # Clean up uploaded file
                os.remove(file_path)
                
                if certificate:
                    return render_template('verify.html', 
                                         found=True,
                                         certificate={
                                             'hash': certificate[1],
                                             'issuer': certificate[2],
                                             'recipient': certificate[3],
                                             'issue_date': certificate[4],
                                             'signature': certificate[6]
                                         })
                else:
                    return render_template('verify.html', found=False, message="Certificate is not authentic!")
    
    return render_template('verify.html')

@app.route('/dashboard')
def dashboard():
    # Get all certificates from database
    conn = sqlite3.connect('database/certificates.db')
    c = conn.cursor()
    c.execute('SELECT * FROM certificates ORDER BY created_at DESC')
    certificates = c.fetchall()
    conn.close()
    
    # Format certificates
    cert_list = []
    for cert in certificates:
        cert_list.append({
            'id': cert[0],
            'hash': cert[1],
            'issuer': cert[2],
            'recipient': cert[3],
            'issue_date': cert[4],
            'qr_code': cert[7].replace('static/', '') if cert[7] else None
        })
    
    return render_template('dashboard.html', certificates=cert_list)

@app.route('/api/verify/<hash_value>')
def api_verify(hash_value):
    """API endpoint for verification"""
    conn = sqlite3.connect('database/certificates.db')
    c = conn.cursor()
    c.execute('SELECT * FROM certificates WHERE certificate_hash = ?', (hash_value,))
    certificate = c.fetchone()
    conn.close()
    
    if certificate:
        return jsonify({
            'status': 'authentic',
            'certificate': {
                'hash': certificate[1],
                'issuer': certificate[2],
                'recipient': certificate[3],
                'issue_date': certificate[4],
                'digital_signature': certificate[6]
            }
        })
    else:
        return jsonify({'status': 'not_found'})

@app.route('/generate_qr/<hash_value>')
def generate_qr(hash_value):
    """Generate QR code for hash"""
    conn = sqlite3.connect('database/certificates.db')
    c = conn.cursor()
    c.execute('SELECT * FROM certificates WHERE certificate_hash = ?', (hash_value,))
    certificate = c.fetchone()
    conn.close()
    
    if certificate:
        qr_data = f"Certificate Hash: {certificate[1]}\nIssuer: {certificate[2]}\nRecipient: {certificate[3]}"
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        img_io = io.BytesIO()
        img.save(img_io, 'PNG')
        img_io.seek(0)
        
        return send_file(img_io, mimetype='image/png')
    
    return "Certificate not found", 404

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs('static/qrcodes', exist_ok=True)
    app.run(debug=True, port=5000)