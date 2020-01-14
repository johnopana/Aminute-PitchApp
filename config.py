import os

class Config:
    '''
    general configuration
    '''
    # SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://moringa:john@localhost/pitchapp'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    # SECRET_KEY = os.environ.get('SECRET_KEY')
    SECRET_KEY = 'kfnwkjnfewfkqewlf;renfoiq;rhgreqhgou;ire'

    @staticmethod
    def init_app(app):
        pass
