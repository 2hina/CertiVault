-- database/schema.sql

-- Certificates table
CREATE TABLE IF NOT EXISTS certificates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    certificate_hash TEXT UNIQUE NOT NULL,
    issuer_name TEXT NOT NULL,
    recipient_name TEXT NOT NULL,
    issue_date TEXT NOT NULL,
    certificate_data TEXT,
    digital_signature TEXT,
    qr_code_path TEXT,
    ipfs_hash TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Issuers table
CREATE TABLE IF NOT EXISTS issuers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    public_key TEXT,
    contact_email TEXT,
    institution_type TEXT,
    verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Verifications table
CREATE TABLE IF NOT EXISTS verifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    certificate_hash TEXT NOT NULL,
    verifier_ip TEXT,
    verification_result TEXT,
    verification_method TEXT,
    verified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (certificate_hash) REFERENCES certificates(certificate_hash)
);

-- API keys table
CREATE TABLE IF NOT EXISTS api_keys (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    key_hash TEXT UNIQUE NOT NULL,
    issuer_id INTEGER,
    permissions TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,
    FOREIGN KEY (issuer_id) REFERENCES issuers(id)
);

-- Indexes for better performance
CREATE INDEX idx_certificates_hash ON certificates(certificate_hash);
CREATE INDEX idx_verifications_hash ON verifications(certificate_hash);
CREATE INDEX idx_certificates_issuer ON certificates(issuer_name);
CREATE INDEX idx_certificates_recipient ON certificates(recipient_name);