 **CertiVault** 
 
My Individual Implementation of the Certificate Verification System

Developer: Urvee Sharma

Project: CertiVault (Individual Contribution)

🌐 Live Website : https://certivault-production.up.railway.app/

• 💻 Source Code : https://github.com/2hina/certivault

• 👔 LinkedIn : www.linkedin.com/in/urvee-sharma

</div>
📋 About My Project
This is my individual implementation of CertiVault, developed as part of a dual-project collaboration. While working on the same problem statement with another team member, I built this complete, production-ready certificate verification system from scratch.

🎯 My Solution Approach

Architecture :	Full-stack Flask application with modular design

Security :	SHA-256 hashing + simulated digital signatures

User Experience :	Modern responsive UI with intuitive workflow

Deployment :	Production-ready on Railway with CI/CD

🚀 Live Deployment

🌐 Live Website: https://certivault-production.up.railway.app

Status: ✅ Fully Operational

Platform: Railway

Uptime: 24/7

SSL: Enabled (HTTPS)

✨ My Features

🔐 Core Features

Smart Certificate Upload with drag & drop interface

SHA-256 Cryptographic Hashing for tamper-proof verification

Dynamic QR Code Generation for each certificate

Three Verification Methods: Hash, File Upload, and QR Scan

Real-time Dashboard with certificate management

🎨 UI/UX Excellence

Modern Glass Morphism Design

Fully Responsive across all devices

Interactive Animations and smooth transitions

Intuitive Workflow with guided steps

🛡️ Security Implementation 

File integrity validation

Secure session management

Input sanitization and validation

Database protection against injection

🛠️ Tech Stack I Used

Backend Development
Python 3.9+ with Flask framework

SQLite for lightweight database

Cryptography Library for security features

Pillow & qrcode for image processing

Frontend Development
HTML5 with semantic markup

CSS3 with Flexbox/Grid layouts

Vanilla JavaScript for interactivity

Font Awesome icons

DevOps & Deployment
Railway for cloud deployment

Gunicorn as production WSGI server

Git/GitHub for version control

Cross-platform compatibility

📦 Installation (All Platforms)

**Windows**

powershell-

# Clone my repository
git clone https://github.com/2hina/certivault.git
cd certivault

# Setup virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run my application
python app.py

**macOS/Linux**

bash-

# Clone repository
git clone https://github.com/2hina/certivault.git
cd certivault

# Setup environment
python3 -m venv venv
source venv/bin/activate

# Install packages
pip3 install -r requirements.txt

# Launch application
python3 app.py

🎮 Quick Usage Guide

📤 Upload a Certificate

Visit the Upload page

Fill in issuer & recipient details

Upload any certificate file

Get unique hash & QR code instantly

🔍 Verify Authenticity

Method 1: Enter the 64-character hash

Method 2: Upload the certificate file

Method 3: Scan the generated QR code

📊 Manage Certificates

View all uploaded certificates

Access verification history

Generate new QR codes

Monitor system status

🏗️ Project Structure

text

certivault-urvee/
├── app.py                    # Main Flask application
├── requirements.txt          # Python dependencies
├── Procfile                 # Railway deployment config
├── runtime.txt              # Python version spec
│
├── templates/               # UI Templates (My Design)
│   ├── layout.html         # Base template with navigation
│   ├── index.html          # Landing page with animations
│   ├── upload.html         # Certificate upload interface
│   ├── verify.html         # Multi-method verification
│   └── dashboard.html      # Admin dashboard
│
├── static/                  # Frontend Assets
│   ├── css/
│   │   └── style.css       # Custom CSS with animations
│   └── js/
│       └── main.js         # Interactive features
│
├── uploads/                 # Temporary file storage
└── database/               # SQLite database
    └── certificates.db     # Certificate records
    
🔧 Troubleshooting

Common Issues & Solutions:

Issue                   	Platform	                 Solution
Port 5000 in use	          All	                 Change port in app.py or kill process
Module not found	         Windows	             Run as Admin: pip install --user -r requirements.txt
SQLite errors           	macOS/Linux	           Check file permissions: chmod 755 database/
QR not generating	           All	               Install Pillow: pip install Pillow --upgrade

Need Help?

Check the deployment logs on Railway

Verify Python version (python --version)

Ensure all dependencies are installed

Clear browser cache if UI issues occur

🎯 What Makes My Implementation Unique

Technical Excellence

Clean, modular code architecture

Comprehensive error handling

Production-ready deployment pipeline

Cross-platform compatibility

User-Centric Design

Intuitive user interface

Real-time feedback mechanisms

Mobile-responsive design

Accessibility considerations

Innovative Features

Simulated blockchain principles

Future-ready architecture for Web-3 integration

Scalable database design

API-ready endpoints
