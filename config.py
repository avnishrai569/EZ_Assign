
import os

class Config:
    SECRET_KEY = 'your_secret_key_here'
    UPLOAD_FOLDER = 'uploads'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///file_share.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'your_email@gmail.com'
    MAIL_PASSWORD = 'your_password'
