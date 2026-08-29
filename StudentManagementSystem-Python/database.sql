CREATE DATABASE IF NOT EXISTS student_management_db;
USE student_management_db;

CREATE TABLE IF NOT EXISTS users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL,
    full_name VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS students (
    id INT PRIMARY KEY AUTO_INCREMENT,
    roll_no VARCHAR(30) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    phone VARCHAR(20),
    course VARCHAR(100) NOT NULL,
    age INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT IGNORE INTO users (username, password, full_name)
VALUES ('admin', 'admin123', 'Administrator');

INSERT IGNORE INTO students (roll_no, name, email, phone, course, age) VALUES
('STU-001', 'Aarav Sharma', 'aarav@example.com', '9876543210', 'Computer Science', 20),
('STU-002', 'Priya Patel', 'priya@example.com', '9876543211', 'Information Technology', 21),
('STU-003', 'Rohan Verma', 'rohan@example.com', '9876543212', 'Electronics', 19);
