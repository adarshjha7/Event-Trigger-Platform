from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint
from .extensions import db, scheduler
from .job_scheduler import cleanup_old_logs
import os

def create_app():
    app = Flask(__name__)

    # Configure the SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'events.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass  # Folder already exists

    # Initialize the database
    db.init_app(app)

    # Initialize the scheduler
    scheduler.start()

    # Schedule the cleanup_old_logs job
    scheduler.add_job(
        func=cleanup_old_logs,
        trigger='interval',
        hours=1,
        args=[app]  # Pass the Flask app to the cleanup_old_logs function
    )

    # Swagger UI configuration
    SWAGGER_URL = '/api/docs'  # URL for accessing Swagger UI
    API_URL = '/static/swagger.json'  # URL for your OpenAPI/Swagger spec

    # Create Swagger UI blueprint
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "Event Trigger Platform API"
        }
    )

    # Register Swagger UI blueprint
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    # Import and initialize routes
    from .routes import init_routes
    init_routes(app)  # Ensure this is called only once

    # Create the database tables
    with app.app_context():
        db.create_all()  # This creates the database and tables if they don't exist

    # Pass the Flask app to the scheduler
    scheduler.app = app

    return app