# FastROI Login and Registration System

I built this login and registration app for my Database Management course as part of my MSc Business Analytics programme at the University of Ghana Business School. I used Python and Streamlit for the interface and MySQL to store user accounts.

## Project background

The project brief described a company, FastROI Digital Solutions Ltd., that wanted to replace its manual staff registration and login process. My task was to design the database and build an app where users could create an account and log in.

I organised the app into registration, login and welcome pages. I kept the database connection in a separate Python file so I could manage the connection settings in one place.

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

I used one table, `users`, in the `fastroi_db` database. I chose an auto-incrementing `user_id` as the primary key so an account keeps the same identifier even if its details change. I added unique constraints to `email` and `username` to prevent duplicate accounts. This version has no foreign keys because it uses only one table.

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

## Run locally on Windows

I developed this project on Windows using PyCharm, XAMPP and phpMyAdmin. The steps below follow that setup.

1. Install Python and XAMPP, then start Apache and MySQL from the XAMPP Control Panel.
2. Open PowerShell in the project folder. Create a virtual environment and install the dependencies:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\python.exe -m pip install -r requirements.txt
   ```

3. Open phpMyAdmin through the XAMPP Control Panel. Create a database called `fastroi_db` with the `utf8mb4_general_ci` collation. Select the database, open the **Import** tab and import `sql/schema.sql`.

4. In phpMyAdmin, create a local database account called `fastroi_app` with a password and give it `SELECT`, `INSERT` and `UPDATE` permissions on `fastroi_db.users`. Set the connection details in the same PowerShell window:

   ```powershell
   $env:FASTROI_DB_HOST = "localhost"
   $env:FASTROI_DB_PORT = "3306"
   $env:FASTROI_DB_NAME = "fastroi_db"
   $env:FASTROI_DB_USER = "fastroi_app"
   $env:FASTROI_DB_PASSWORD = "YOUR_LOCAL_DATABASE_PASSWORD"
   ```

   Replace the password placeholder with the password you set for the database account. The app reads these environment variables directly.

5. Start the app from that PowerShell window:

   ```powershell
   .\.venv\Scripts\python.exe -m streamlit run app.py
   ```

6. Create an account through the registration form using fictional details. No existing accounts or login passwords are provided.

## What I learned

I gained practice connecting a Streamlit app to MySQL and working with database constraints. I also learned how to hash and check passwords with bcrypt, use parameterised queries and close database connections after each operation.

One useful detail was that two users can choose the same password but have different stored hashes because bcrypt generates a separate salt for each password. I also used Streamlit session state to keep track of whether a user was logged in.

## Scope and limitations

I built this as a local coursework project. The welcome page confirms a successful login; it does not include employee management tools.

The email check only validates the format. It does not confirm that the person owns the email address or works for the company. Password recovery, email verification, multi-factor authentication and controls for repeated failed login attempts are not included. The database records the latest successful login time, but there is no separate table for a full login history. The dependency versions are not pinned.

For the coursework, I tested registration and login through the interface, including empty inputs, duplicate accounts and password validation. The cleaned GitHub version has passed Python syntax checks, but it still needs a full registration and login check with a running database after the connection changes.

## About the files shared here

The accounts used for the assignment had fictitious emails and phone numbers. For this public version, I have included an empty database schema so anyone running the app can create their own test accounts.

I have left out my student ID, the original submission PDFs, saved account records and password hashes. The database connection now reads settings from environment variables, so local credentials do not need to be added to the code.
