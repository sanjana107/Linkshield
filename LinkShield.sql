-- 1. Create the Database
CREATE DATABASE IF NOT EXISTS linkshield_db;
USE linkshield_db;

-- 2. Drop tables if they exist to start fresh (Be careful with this in production!)
DROP TABLE IF EXISTS url_intelligence;
DROP TABLE IF EXISTS training_data;

-- 3. Create the Training Data table
-- This table stores a large list of known Good and Bad URLs for the AI model
CREATE TABLE training_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    url_text TEXT NOT NULL,
    is_phishing TINYINT(1) NOT NULL, -- 1 for Phishing, 0 for Safe
    source VARCHAR(100) DEFAULT 'Manual Entry'
);

-- 4. Create the Live Intelligence table
-- This table stores the results of every scan performed by your Streamlit app
CREATE TABLE url_intelligence (
    id INT AUTO_INCREMENT PRIMARY KEY,
    url_scanned TEXT NOT NULL,
    predicted_label ENUM('SAFE', 'PHISHING') NOT NULL,
    confidence_score FLOAT, -- The probability percentage from the AI
    scanned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 5. Insert Sample Training Data
-- Adding a mix of legitimate sites and common phishing patterns
INSERT INTO training_data (url_text, is_phishing, source) VALUES
('https://www.google.com', 0, 'Seed List'),
('https://www.amazon.com/gp/cart', 0, 'Seed List'),
('http://secure-login-amazon-verify.net/login.php', 1, 'PhishTank'),
('https://www.facebook.com', 0, 'Seed List'),
('http://update-your-paypal-account-now.info/access', 1, 'PhishTank'),
('https://github.com/trending', 0, 'Seed List'),
('http://bit.ly/3x8sk2k_fake_login', 1, 'Manual Entry'),
('https://www.microsoft.com/en-us/security', 0, 'Seed List'),
('http://account-verification-required.top/security', 1, 'Manual Entry');

-- 6. Verification Query
SELECT * FROM training_data;
