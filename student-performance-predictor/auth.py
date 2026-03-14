import requests
import json

# Firebase API Key from firebase.js configuration
API_KEY = "AIzaSyAyn8fpsVqs8PHiyn6NztOsd2THg0p-SlM"

def sign_up(email, password):
    """Sign up a new user with email and password"""
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={API_KEY}"
    data = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }
    try:
        response = requests.post(url, json=data)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def login(email, password):
    """Login user with email and password"""
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={API_KEY}"
    data = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }
    try:
        response = requests.post(url, json=data)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def verify_token(token):
    """Verify if a user token is valid"""
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:lookup?key={API_KEY}"
    data = {"idToken": token}
    try:
        response = requests.post(url, json=data)
        return response.json()
    except Exception as e:
        return {"error": str(e)}
