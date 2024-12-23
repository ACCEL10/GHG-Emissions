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
            password="3529",  # Replace with your MySQL password
            database="ghg_emissions"  # Database name created in MySQL Workbench
        )
        return connection
    except Error as e:
        st.error(f"Error connecting to MySQL: {e}")
        return None

# Hash the password using SHA-256
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def app():
    st.title("Register Page")

    # Input fields
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("User Information")
        username = st.text_input("Username")
        email = st.text_input("Email")
        phone_number = st.text_input("Phone Number")

    with col2:
        st.subheader("Security Details")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")

    st.markdown("---")

    if st.button("Register"):
        if not username or not email or not phone_number or not password or not confirm_password:
            st.error("Please fill in all fields!")
        elif password != confirm_password:
            st.error("Passwords do not match.")
        else:
            # Hash the password
            password_hash = hash_password(password)

            # Save to MySQL database
            connection = connect_to_db()
            if connection:
                try:
                    cursor = connection.cursor()
                    cursor.execute("""
                        INSERT INTO users (username, email, phone_number, password_hash)
                        VALUES (%s, %s, %s, %s)
                    """, (username, email, phone_number, password_hash))
                    connection.commit()
                    st.success("Registration successful!")
                except Error as e:
                    st.error(f"Error saving to database: {e}")
                finally:
                    connection.close()
