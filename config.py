import os

# Get the base directory of the project
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """Set Flask configuration variables."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'a_very_secret_key')
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 
        'sqlite:///' + os.path.join(basedir, 'app.db'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False