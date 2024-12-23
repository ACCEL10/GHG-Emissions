import streamlit as st
import mysql.connector
from mysql.connector import Error
import hashlib

# Connect to MySQL
def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",       # Update to your MySQL server host
            user="root",            # Update to your MySQL username
            password="3529",        # Replace with your MySQL password
            database="ghg_emissions"  # Database name created in MySQL Workbench
        )
        return connection
    except Error as e:
        st.error(f"Error connecting to MySQL: {e}")
        return None

# Hash the password using SHA-256
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Check if login credentials are correct
def validate_login(username, password):
    # Hash the entered password
    password_hash = hash_password(password)

    # Connect to the database
    connection = connect_to_db()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()

            if user:
                # Compare the stored password hash with the entered password hash
                if user['password_hash'] == password_hash:
                    return True
                else:
                    return False
            else:
                return False
        except Error as e:
            st.error(f"Error querying the database: {e}")
            return False
        finally:
            connection.close()

def app():
    st.title("Login Page")

    # Input fields
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    st.markdown("---")

    if st.button("Login"):
        if not username or not password:
            st.error("Please enter both username and password.")
        else:
            if validate_login(username, password):
                st.success("Login successful!")
                # After successful login, you can redirect the user to another page or show a message
                # For example: st.write("Welcome to your dashboard!")
            else:
                st.error("Invalid username or password.")
