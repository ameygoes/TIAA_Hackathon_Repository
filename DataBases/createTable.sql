USE tiaa; 

CREATE TABLE transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    userId INT,
    transactionCategory VARCHAR(255),
    transactionAmount INT
);

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    karma_points INT,
    retirement_age INT,
    retirement_amt INT,
    birth_year INT,
    monthly_burn_rate INT,
    transactionId INT,
    FOREIGN KEY (transactionId) REFERENCES transactions(id)
);


