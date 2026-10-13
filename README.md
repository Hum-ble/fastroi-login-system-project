# FastROI Login and Registration System

A database-driven registration and login application built with Python, Streamlit and MySQL as part of my MSc Business Analytics coursework at the University of Ghana Business School.

## Project background

The assignment used FastROI Digital Solutions Ltd. as a company scenario. Staff registration and login were handled manually, and the task was to build a simple application backed by a relational database. This project demonstrates database design, input validation and authentication logic.

## What the application does

- Registers users with first name, optional middle name, last name, email, optional phone number, username and password.
- Checks that an email follows the `firstname.lastname@fastroi.com` format.
- Requires passwords with at least 12 characters, an uppercase letter, a lowercase letter, a number and a supported special character.
- Hashes passwords with bcrypt and a generated salt before storage.
- Checks for duplicate email addresses and usernames, supported by database unique constraints.
- Uses parameterised SQL queries for registration and login.
- Verifies login credentials, updates the most recent login time and displays a welcome page.
- Uses Streamlit session state for navigation, login status and logout.

## Tools used

| Tool | Purpose |
| --- | --- |
| Python | Application logic and validation |
| Streamlit | Registration, login and welcome interface |
| MySQL / MariaDB | Relational account storage |
| mysql-connector-python | Database connection and queries |
| bcrypt | Password hashing and verification |
| XAMPP and phpMyAdmin | Original local database setup and administration |
| PyCharm | Original development environment |

## Repository files

| File | Contents |
| --- | --- |
| `app.py` | Interface, validation, registration and login logic |
| `db_connection.py` | Database connection using environment variables |
| `sql/schema.sql` | Empty users table with keys and constraints |
| `requirements.txt` | Python dependencies |
| `fastroi_logo.png` | Branding asset supplied with the project |
| `.gitignore` | Excludes local settings and common development files |

## Database design

The `fastroi_db` database contains one `users` table. `user_id` is an auto-incrementing primary key; `email` and `username` have unique constraints. There are no foreign keys because this version uses a single table.

| Column | Type | Purpose |
| --- | --- | --- |
| user_id | INT | Account identifier |
| first_name | VARCHAR(50) | First name |
| middle_name | VARCHAR(50) | Optional middle name |
| last_name | VARCHAR(50) | Last name |
| email | VARCHAR(100) | Unique email |
| phone | VARCHAR(20) | Optional phone number |
| username | VARCHAR(50) | Unique login name |
| password | VARBINARY(80) | bcrypt hash; original schema permits NULL |
| created_at | DATETIME | Account creation timestamp |
| last_login | DATETIME | Most recent successful login |

## Run locally

1. Install Python and start a local MySQL or MariaDB server.
2. Open a terminal in this project folder and install the dependencies:

   ```bash
   python -m venv .venv
   # Windows PowerShell
   .venv\Scripts\Activate.ps1
   # macOS / Linux
   # source .venv/bin/activate
   python -m pip install -r requirements.txt
   ```

3. Create an empty database and import the schema using MySQL or phpMyAdmin:

   ```sql
   CREATE DATABASE fastroi_db CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
   ```

   ```bash
   mysql -u YOUR_ADMIN_USER -p fastroi_db < sql/schema.sql
   ```

4. Create a local database account with `SELECT`, `INSERT` and `UPDATE` permissions on `fastroi_db.users`. Set its connection details in the same terminal before running the app. For Windows PowerShell:

   ```powershell
   $env:FASTROI_DB_HOST = "localhost"
   $env:FASTROI_DB_PORT = "3306"
   $env:FASTROI_DB_NAME = "fastroi_db"
   $env:FASTROI_DB_USER = "fastroi_app"
   $env:FASTROI_DB_PASSWORD = "YOUR_LOCAL_DATABASE_PASSWORD"
   ```

   On macOS / Linux, use `export VARIABLE="value"` for each setting. The application reads environment variables directly; it does not automatically load a `.env` file.

5. Start the application from the project folder:

   ```bash
   streamlit run app.py
   ```

6. Create an account through the registration form using fictional details for the demonstration. No existing accounts or login passwords are provided.

## What I learned

This project helped me connect a Python interface to a relational database, select suitable field types and constraints, use parameterised queries, implement password hashing and manage database connections. It also gave me practice separating connection settings from the main application.

## Scope and limitations

This is a local academic prototype. Email format validation does not verify ownership or employee status. The welcome page is a basic demonstration rather than a complete employee management dashboard. The application does not implement email verification, password recovery, multi-factor authentication, login rate limiting, account lockout or a complete audit log. It stores only the latest successful login time. Dependencies retain the original unpinned format.

The original coursework included manual interface testing. This portfolio copy has had its Python syntax and privacy checks verified; registration and login still need an end-to-end check with a running local database.

## Privacy in this portfolio version

The database script contains table definitions and constraints only. Account records, phone numbers, personal email addresses, saved password hashes, example passwords and academic identifiers have been excluded. The original submission PDFs and screenshots are omitted because they contain identifiers and account information. Database connection settings are supplied locally and should never be committed.
