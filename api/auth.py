import requests
from flask import request, jsonify, current_app
from functools import wraps
import os


def authenticate_with_api(email, password):
    """
    Authenticate user using the university's authentication API
    """
    auth_url = current_app.config.get('AUTH_API_URL', 'https://web.socem.plymouth.ac.uk/COMP2001/auth/api/users')

    try:
        response = requests.post(
            auth_url,
            json={"email": email, "password": password},
            timeout=5
        )

        if response.status_code == 200:
            return {
                "authenticated": True,
                "email": email,
                "data": response.json()
            }
        else:
            return {
                "authenticated": False,
                "error": "Invalid credentials"
            }

    except requests.exceptions.RequestException as e:
        print(f"Auth API error: {e}")
        return {
            "authenticated": False,
            "error": "Authentication service unavailable"
        }


def get_user_from_db(email):
    """
    Get user details from our database (for trail ownership)
    """
    from database.connection import get_db

    try:
        conn = get_db()
        if conn is None:
            return None

        cursor = conn.cursor()
        cursor.execute("""
                       SELECT UserID, Email, DisplayName
                       FROM CW2.[User]
                       WHERE Email = ?
                       """, (email,))

        user = cursor.fetchone()
        cursor.close()

        if user:
            return {
                "UserID": user[0],
                "Email": user[1],
                "DisplayName": user[2]
            }
        return None

    except Exception as e:
        print(f"Database error in get_user_from_db: {e}")
        return None


def authenticate_user(email, password):
    """Authenticate with university API"""
    try:
        response = requests.post(
            'https://web.socem.plymouth.ac.uk/COMP2001/auth/api/users',
            json={'email': email, 'password': password},
            timeout=5
        )
        return response.status_code == 200
    except:
        return False


def auth_required(f):
    """Decorator for protected routes"""

    @wraps(f)
    def decorated(*args, **kwargs):
        email = request.headers.get('X-User-Email')
        password = request.headers.get('X-User-Password')

        if not email or not password:
            return jsonify({'error': 'Missing credentials'}), 401

        if not authenticate_user(email, password):
            return jsonify({'error': 'Invalid credentials'}), 401

        return f(*args, **kwargs)

    return decorated