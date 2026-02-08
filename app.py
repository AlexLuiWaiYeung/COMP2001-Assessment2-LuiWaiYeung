from flask import Flask, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv

# LOAD .env FILE FIRST THING
load_dotenv()


def create_app():
    """
    Creates and configures the Flask application
    """
    # Create the Flask app
    app = Flask(__name__)

    # Enable CORS
    CORS(app)

    # Configuration FROM .env
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')

    # Initialize database
    from database.connection import init_db
    init_db(app)

    # Import and register blueprints
    from api.routes import trails_bp
    app.register_blueprint(trails_bp)

    # Basic routes
    @app.route('/')
    def home():
        return jsonify({
            'message': 'TrailService API',
            'version': '1.0',
            'database': 'connected'  # Add this to verify
        })

    @app.route('/api/health')
    def health():
        return jsonify({
            'status': 'healthy',
            'database': 'checking...'
        })

    return app


# Create the app
app = create_app()

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )