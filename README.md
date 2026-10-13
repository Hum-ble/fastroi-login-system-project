# FastROI Login and Registration System

I built this application for my Database Management course during my MSc Business Analytics programme at the University of Ghana Business School. It uses Python, Streamlit and MySQL to register users, check login credentials and record the latest successful login.

## Project background

The coursework scenario involved FastROI Digital Solutions Ltd., a company looking to replace its manual staff registration and login process. My task was to design the database and build a working registration and login interface.

## Main features

- Registration with name, email, optional phone number, username and password.
- Email format validation for `firstname.lastname@fastroi.com`.
- Password validation requiring at least 12 characters, uppercase and lowercase letters, a number and a supported special character.
- Password hashing and verification using bcrypt.
- Duplicate email and username checks, backed by database unique constraints.
- Parameterised SQL queries for registration and login.
- A welcome page after successful login, with session state and logout.
- Account creation and latest successful login timestamps.

## Tools used

| Tool | Role |
| --- | --- |
| Python | Application logic and input validation |
| Streamlit | Registration, login and welcome pages |
| MySQL / MariaDB | User account storage |
| mysql-connector-python | Database queries and connections |
| bcrypt | Password hashing and verification |

I developed the project on Windows using PyCharm, with XAMPP and phpMyAdmin for the local database setup. XAMPP was a convenient way to run the database locally; the app can also connect to a separately installed or hosted MySQL server through its connection settings.

## Design decisions

- **Account identifiers:** I used an auto-incrementing `user_id` as the primary key so an account keeps its identifier when its details change.
- **Duplicate accounts:** Unique constraints on `email` and `username` enforce account uniqueness in the database, alongside checks in the app.
- **Password storage:** bcrypt generates a salt for each password. Two accounts can therefore use the same password and still have different stored hashes.
- **Database queries:** User input is passed as query parameters rather than added directly to SQL strings.
- **Connection handling:** Database settings are kept in `db_connection.py`. Credentials come from environment variables, and connections and cursors are closed after each operation.

## Database structure

The `fastroi_db` database contains one `users` table.

| Column | Type | Purpose |
| --- | --- | --- |
| user_id | INT | Auto-incrementing primary key |
| first_name | VARCHAR(50) | First name |
| middle_name | VARCHAR(50) | Optional middle name |
| last_name | VARCHAR(50) | Last name |
| email | VARCHAR(100) | Unique email address |
| phone | VARCHAR(20) | Optional phone number |
| username | VARCHAR(50) | Unique login name |
| password | VARBINARY(80) | bcrypt password hash |
| created_at | DATETIME | Account creation time |
| last_login | DATETIME | Latest successful login |

The schema contains no account records. Create test accounts through the registration form so passwords are hashed before being stored.

## Project files

| File | Purpose |
| --- | --- |
| `app.py` | Interface, validation, registration and login |
| `db_connection.py` | Database connection settings |
| `sql/schema.sql` | Table definition, primary key and unique constraints |
| `requirements.txt` | Python dependencies |
| `fastroi_logo.png` | Application logo |
| `.gitignore` | Excludes local credentials and development files |

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

6. Create an account through the registration form using fictional details. The database starts empty.

## Testing and current scope

For the coursework, I tested the interface for registration, login, empty inputs, duplicate accounts and password validation. The environment-variable connection settings added for this repository still need a full registration and login check with a running database.

The current app covers registration and login, with a basic welcome page. Email validation checks the format but does not verify email ownership or employee status. Password recovery, multi-factor authentication, login rate limiting and a full login history are possible next improvements.

## Possible extensions

The database design could be adapted to PostgreSQL or another relational database. A PostgreSQL version would need a different Python driver, changes to the schema and database-specific code, and testing. The current implementation uses MySQL.

Other extensions include email verification and a separate login activity table to record successful and failed attempts.
