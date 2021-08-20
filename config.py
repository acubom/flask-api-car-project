import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY="You will never guess..."
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEPLOY_DATABASE_URI')
    # Decreases unnessary optput in terminal
    SQLALCHEMY_TRACK_MODIFICATIONS = False 