Visitor Management System
Project Overview
This is a web-based Visitor Management System built with Flask, designed to streamline the process of managing visitors entering and exiting a premises. It allows for recording visitor details, tracking their check-in and check-out times, managing hosts and departments, and provides administrative functionalities for user management.

Features
User Authentication: Secure login for admin and sub-users.

Role-Based Access Control:

Admin Users: Full access to manage visitors, departments, hosts, and other admin/sub-users.

Sub-users: Can manage visitors they have added (add, view, edit, delete, check-out).

Visitor Management:

Add new visitor records with details (name, contact, purpose, department, host).

Upload and display visitor photos.

View detailed visitor profiles.

Edit existing visitor information.

Delete visitor records.

Check-out Functionality: Mark visitors as checked out with a timestamp.

Department Management: Admins can add, view, and delete departments.

Host Management: Admins can add, view, and delete hosts, linking them to specific departments.

Responsive Navigation: Modern, mobile-friendly navigation bar with a hamburger menu.

DataTables Integration: Enhanced visitor list with search, pagination, and sorting.

Data Export: Export visitor data (e.g., to CSV).

Custom Confirmation Modals: Improved user experience for delete actions (replaces browser's confirm()).

Technologies Used
Backend: Python, Flask

Database: MySQL

Frontend: HTML5, CSS3, JavaScript, Jinja2 (templating)

Libraries:

Flask-Login (User session management)

Flask-MySQLdb (MySQL integration)

python-dotenv (Environment variable management)

jQuery (JavaScript library)

DataTables.js (Table enhancements)

Font Awesome (Icons)

Setup Instructions
Follow these steps to get the project up and running on your local machine.

Prerequisites
Python 3.8+

MySQL Server


1. Clone the Repository
git clone https://github.com/AjmerAnsari/Visitor-Management-System.git
cd Visitor-Management-System


2. Install Dependencies
Install all required Python packages using pip:

pip install -r requirements.txt

(If requirements.txt doesn't exist, you can create it after installing Flask and other initial dependencies by running pip freeze > requirements.txt while your venv is active.)

3. Database Setup (MySQL)
3.1. Create the Database
Connect to your MySQL server (e.g., using MySQL Workbench, phpMyAdmin, or the command line client) and create a new database:

CREATE DATABASE visitors;
USE visitors;

3.2. Run the Schema
Execute the SQL commands from your schema.sql file to create the necessary tables.

-- Example content of schema.sql (ensure yours matches your current schema)
CREATE TABLE IF NOT EXISTS admin_users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) DEFAULT 'subuser' -- 'admin' or 'subuser'
);

CREATE TABLE IF NOT EXISTS departments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS hosts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    phone VARCHAR(20),
    department_id INT,
    FOREIGN KEY (department_id) REFERENCES departments(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS visitors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    email VARCHAR(100),
    address TEXT,
    purpose VARCHAR(200),
    department_id INT,
    host_id INT,
    check_in DATETIME DEFAULT CURRENT_TIMESTAMP,
    check_out DATETIME,
    created_by INT,
    photo VARCHAR(255),
    FOREIGN KEY (department_id) REFERENCES departments(id) ON DELETE SET NULL,
    FOREIGN KEY (host_id) REFERENCES hosts(id) ON DELETE SET NULL,
    FOREIGN KEY (created_by) REFERENCES admin_users(id) ON DELETE SET NULL
);

-- Insert a default admin user (password 'admin')
INSERT IGNORE INTO admin_users (username, password_hash, role) VALUES ('admin', 'your_hash_password', 'admin');

# Flask Secret Key (REQUIRED for session security)
SECRET_KEY='your_super_long_and_random_secret_key_here'

# MySQL Database Configuration
MYSQL_HOST='localhost'
MYSQL_USER='root'
MYSQL_PASSWORD='your_mysql_root_password'
MYSQL_DB='visitors'

Replace the placeholder values with your actual credentials.
#run in terminal:

python app.py

The application will typically run on http://127.0.0.1:5000/. 

Usage
Login: Access the application in your browser. You will be redirected to the login page. Use the default admin credentials (username: admin, password: admin - if you used the default hash provided in schema.sql).

Dashboard: View all visitors.

Add Visitor: Register new visitors.

Admin Features: If logged in as an admin, use the navigation links to manage departments, hosts, and other users.

Check-out: Mark visitors as checked out from the dashboard.

Project Structure
visitor_management_system/
├── app.py                  # Main Flask application file
├── config.py               # Application configuration (reads from .env)
├── extensions.py           # Initializes Flask extensions (e.g., MySQL)
├── models.py               # Database models/helpers (e.g., User class)
├── requirements.txt        # Python dependencies
├── schema.sql              # Database schema for MySQL
├── auth/                   # Blueprint for authentication routes
│   └── routes.py
├── users/                  # Blueprint for user management (admin, hosts, departments)
│   └── routes.py
├── visitors/               # Blueprint for visitor-related routes
│   └── routes.py
├── static/                 # Static files (CSS, JS, images)
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── main.js
│   └── images/             # Store visitor photos and default-user.png
├── templates/              # Jinja2 HTML templates
│   ├── base.html           # Base template for all pages
│   ├── dashboard.html
│   ├── login.html
│   ├── add_visitor.html
│   ├── view_visitor.html
│   ├── edit_visitor.html
│   ├── export.html
│   ├── manage_departments.html
│   ├── manage_hosts.html
│   └── manage_users.html
              
