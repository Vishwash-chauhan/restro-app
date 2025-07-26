
import os
from flask import Flask
from models.models import db
from config import DevelopmentConfig, ProductionConfig, TestingConfig

app = Flask(__name__)

# Load config based on FLASK_ENV environment variable
env = os.environ.get('FLASK_ENV', 'development')
if env == 'production':
    app.config.from_object(ProductionConfig)
elif env == 'testing':
    app.config.from_object(TestingConfig)
else:
    app.config.from_object(DevelopmentConfig)

db.init_app(app)

with app.app_context():
    db.create_all()

from routes.routes import admin_bp
app.register_blueprint(admin_bp)

if __name__ == '__main__':
    app.run()
