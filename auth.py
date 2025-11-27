import streamlit as st
import firebase_admin
from firebase_admin import auth, credentials
import requests

# Initialize Firebase if not already initialized
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase_service_account_key.json")
    firebase_admin.initialize_app(cred)

# Custom CSS for better UI
def set_custom_css():
    st.markdown(
        """
        <style>
        .stButton>button {border-radius: 20px; padding: 10px 20px; font-size: 16px;}
        .stButton>button:hover {background-color: #45a049;}
        </style>
        """,
        unsafe_allow_html=True,
    )
set_custom_css()

# Reset password using email
def reset_password():
    st.sidebar.subheader("Reset Password")
    email = st.sidebar.text_input("Enter your registered email:", key="reset_email")
    if st.sidebar.button("Send Reset Email", key="reset_button"):
        if email:
            try:
                link = auth.generate_password_reset_link(email)
                st.sidebar.success("Password reset email sent! Check your inbox.")
                st.sidebar.write(f"Reset link: {link}")  # For debugging purposes, remove in production
            except Exception as e:
                st.sidebar.error(f"Error: {e}")
        else:
            st.sidebar.error("Please enter a valid email address.")
    
    # Add "Go to Login" button
    if st.sidebar.button("Go to Login", key="reset_go_to_login"):
        st.session_state['show_login'] = True
        st.session_state['show_reset_password'] = False
        st.rerun()

# Sign-up function
def sign_up():
    st.sidebar.subheader("Create a New Account")
    email = st.sidebar.text_input("Email", key="signup_email")
    password = st.sidebar.text_input("Password", type="password", key="signup_password")
    confirm_password = st.sidebar.text_input("Confirm Password", type="password", key="signup_confirm_password")
    
    if st.sidebar.button("Sign Up", key="signup_button"):
        if password == confirm_password:
            try:
                user = auth.create_user(email=email, password=password)
                st.sidebar.success("Sign-up successful! Please log in.")
                st.session_state['show_login'] = True  # Switch back to login after sign-up
                st.rerun()  # Refresh the app
            except Exception as e:
                st.sidebar.error(f"Sign-up failed: {e}")
        else:
            st.sidebar.error("Passwords do not match!")
    
    # Add "Go to Login" button
    if st.sidebar.button("Go to Login", key="signup_go_to_login"):
        st.session_state['show_login'] = True
        st.session_state['show_signup'] = False
        st.rerun()

# Login function
def login():
    st.sidebar.subheader("Login to Your Account")
    username_or_email = st.sidebar.text_input("Username or Email", key="login_username_or_email")
    password = st.sidebar.text_input("Password", type="password", key="login_password")
    
    if st.sidebar.button("Login", key="login_button"):
        if username_or_email and password:
            try:
                # Verify user credentials using Firebase REST API
                api_key =   # Your Firebase API key
                url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"
                payload = {
                    "email": username_or_email,  # Allow login with username or email
                    "password": password,
                    "returnSecureToken": True
                }
                response = requests.post(url, json=payload)
                if response.status_code == 200:
                    st.session_state['authenticated'] = True
                    st.session_state['email'] = username_or_email
                    st.sidebar.success("Login successful!")
                    st.rerun()  # Refresh the app
                else:
                    st.sidebar.error("Login failed: Invalid credentials.")
            except Exception as e:
                st.sidebar.error(f"Login failed: {e}")
        else:
            st.sidebar.error("Please enter your credentials.")
    
    if st.sidebar.button("Forgot Password", key="forgot_password_button"):
        st.session_state['show_reset_password'] = True
        st.session_state['show_signup'] = False
        st.session_state['show_login'] = False
        st.rerun()  # Refresh the app
    
    if st.sidebar.button("Sign Up", key="signup_from_login_button"):
        st.session_state['show_signup'] = True
        st.session_state['show_login'] = False
        st.session_state['show_reset_password'] = False
        st.rerun()  # Refresh the app

# Authentication
def authenticate():
    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False
    if 'show_login' not in st.session_state:
        st.session_state['show_login'] = True
    if 'show_signup' not in st.session_state:
        st.session_state['show_signup'] = False
    if 'show_reset_password' not in st.session_state:
        st.session_state['show_reset_password'] = False

    # Show only Logout button if authenticated
    if st.session_state['authenticated']:
        if st.sidebar.button("Logout", key="logout_button"):
            logout()
    else:
        # Show authentication forms if not authenticated
        if st.session_state['show_login']:
            login()
        elif st.session_state['show_signup']:
            sign_up()
        elif st.session_state['show_reset_password']:
            reset_password()

    return st.session_state.get('authenticated', False)

# Logout function
def logout():
    st.session_state.pop('authenticated', None)
    st.session_state.pop('email', None)
    st.session_state['show_login'] = True
    st.session_state['show_signup'] = False
    st.session_state['show_reset_password'] = False
    st.sidebar.success("Logged out successfully!")
    st.rerun()  # Refresh the app