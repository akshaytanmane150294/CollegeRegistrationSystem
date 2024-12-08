import os

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://username:password@localhost/CollegeRegistrationSystem'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = os.urandom(24)
