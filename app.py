#LIBRARIES
import streamlit as st
import bcrypt
import re
import mysql.connector
from db_connection import create_connection

#REUSABLE HELPER FUNCTIONS

def is_valid_company_email(email_address):
    pattern = r"[A-Za-z-]+\.[A-Za-z-]+@fastroi\.com"
    return re.fullmatch(pattern, email_address.strip())


def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed)


def get_password_issues(password):
    validation_errors = []

    if len(password) < 12:
        validation_errors.append("At least 12 characters")

    if not re.search(r"[A-Z]", password):
        validation_errors.append("At least one uppercase letter")

    if not re.search(r"[a-z]", password):
        validation_errors.append("At least one lowercase letter")

    if not re.search(r"\d", password):
        validation_errors.append("At least one number")

    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        validation_errors.append("At least one special character")

    return validation_errors



# HEADER USER INTERFACE (UI)

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    l1, l2, l3 = st.columns([1, 2, 1])
    with l2:
        st.image("fastroi_logo.png", width=170)

    st.markdown(
        "<h2 style='text-align:center; white-space: nowrap; '>FastROI Digital Solutions Ltd</h2>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<p style='text-align:center; color:gray;'>Fast. Precise. Results-Driven.</p>",
        unsafe_allow_html=True
    )

st.divider()


# SESSION STATE INITIALIZATION

if "page" not in st.session_state:
    st.session_state.page = "login"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = None



# LOGIN PAGE

if st.session_state.page == "login":

    if not st.session_state.logged_in:

        st.subheader("Login")

        with st.form("login_form"):

            username = st.text_input("Username")
            login_password = st.text_input("Password", type="password")
            st.caption("Use your assigned FastROI credentials. Password is case-sensitive.")
            submitted = st.form_submit_button("Login", type="primary")

            if submitted:

                if not username.strip() and not login_password.strip():
                    st.error("Please enter username and password")
                elif not username.strip():
                     st.error("Please enter your username.")
                elif not login_password.strip():
                    st.error("Please enter your password.")
                else:
                    conn = None
                    cursor = None

                    try:
                        conn = create_connection()
                        cursor = conn.cursor()

                        cursor.execute(
                            "SELECT user_id, password FROM users WHERE username = %s",
                            (username,)
                        )

                        result = cursor.fetchone()

                        if result:
                            user_id, stored_password = result

                            # Convert bytearray to bytes for bcrypt
                            if isinstance(stored_password, bytearray):
                                stored_password = bytes(stored_password)

                            if verify_password(login_password, stored_password):
                                cursor.execute(
                                    "UPDATE users SET last_login = NOW() WHERE user_id= %s",
                                    (user_id,)
                                )

                                conn.commit()

                                st.session_state.logged_in = True
                                st.session_state.user = username

                                st.rerun()

                            else:
                                st.error("Invalid username or password")
                        else:
                            st.error("Invalid username or password")

                    except mysql.connector.Error:
                        st.error("Unable to process login at this time. Please try again later.")

                    finally:
                        if cursor:
                            cursor.close()
                        if conn:
                            conn.close()

        st.caption("If you forgot your password, please contact the IT department.")

        st.write("Don't have an account yet?")
        if st.button("Create Account"):
            st.session_state.page = "register"
            st.rerun()

    else:

        # DASHBOARD

        st.success(f"Welcome, {st.session_state.user}")

        st.write("You are successfully logged into the FastROI Internal Management System.")
        st.write("Access your assigned resources and internal tools below.")

        st.info(
            "Secure Internal Access Environment. "
            "Access is restricted to authorized FastROI personnel only. "
            "All system activity may be monitored and logged. "
            "Avoid unsecured public networks and log out after each session."
        )

        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.user = None
            st.rerun()



# REGISTRATION PAGE

elif st.session_state.page == "register":
    st.subheader("Create Account")
    st.info("Registration is restricted to official FastROI emails (firstname.lastname@fastroi.com).")

    with st.form("register_form"):

        first_name = st.text_input("First Name")
        middle_name = st.text_input("Middle Name (Optional)")
        last_name = st.text_input("Last Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone Number")
        username = st.text_input("Username")
        reg_password = st.text_input("Password", type="password")

        st.caption(
            "Password must be at least 12 characters and include at least one uppercase, "
            "lowercase, number, and special character."
        )

        submit_register = st.form_submit_button("Register")

        password_issues = []
        if reg_password:
            password_issues = get_password_issues(reg_password)

            if password_issues:
                st.markdown("**Password Requirements:**")
                for issue in password_issues:
                    st.markdown(f"- {issue}")
            else:
                st.success("Password is compliant.")

        if submit_register:

            if not first_name.strip():
                st.error("First Name is required")

            elif not last_name.strip():
                st.error("Last Name is required")

            elif not email.strip():
                st.error("Email is required")



            elif not is_valid_company_email(email):
                st.error("Please use your official FastROI email address.")


            elif not username.strip():
                st.error("Username is required")

            elif not reg_password.strip():
                st.error("Password is required")

            elif password_issues:
                st.error("Password does not meet security requirements.")

            else:
                conn = None
                cursor = None
                try:
                    conn = create_connection()
                    cursor = conn.cursor()

                    cursor.execute("SELECT 1 FROM users WHERE username = %s", (username,))
                    if cursor.fetchone():
                        st.error("Username already exists.")

                    else:
                        cursor.execute("SELECT 1 FROM users WHERE email = %s", (email,))
                        if cursor.fetchone():
                            st.error("Email already registered.")
                        else:
                            hashed_password = hash_password(reg_password)

                            query = """
                                INSERT INTO users
                                (first_name, middle_name, last_name, email, phone, username, password)
                                VALUES (%s,%s,%s,%s,%s,%s,%s)
                            """

                            cursor.execute(query, (
                                first_name,
                                middle_name,
                                last_name,
                                email,
                                phone,
                                username,
                                hashed_password
                            ))

                            conn.commit()
                            st.success("Registration successful. You may now log in.")


                except mysql.connector.Error:
                    st.error("Unable to complete registration at this time. Please try again later.")

                finally:
                    if cursor:
                        cursor.close()
                    if conn:
                        conn.close()

    st.write("Already have an account?")
    if st.button("Back to Login"):
        st.session_state.page = "login"
        st.rerun()
