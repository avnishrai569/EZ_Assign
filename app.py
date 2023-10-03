from flask import Flask, request, jsonify, send_from_directory
import os
import secrets
import smtplib
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///file_share.db'
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your_email@gmail.com'
app.config['MAIL_PASSWORD'] = 'your_password'

db = SQLAlchemy(app)
mail = Mail(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    is_ops_user = db.Column(db.Boolean, default=False)

class UploadedFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Implement User registration, login, and email verification here

# API for Ops User to upload files
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"message": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"message": "No selected file"}), 400

    if not current_user.is_ops_user:
        return jsonify({"message": "Only Ops User can upload files"}), 403

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Store the file information in the database
        uploaded_file = UploadedFile(filename=filename, user_id=current_user.id)
        db.session.add(uploaded_file)
        db.session.commit()
        return jsonify({"message": "File uploaded successfully"}), 200
    else:
        return jsonify({"message": "Invalid file type"}), 400

# API for Client User to download files
@app.route('/download/<file_id>', methods=['GET'])
def download_file(file_id):
    file = UploadedFile.query.get(file_id)

    if not file:
        return jsonify({"message": "File not found"}), 404

    if not current_user.is_authenticated:
        return jsonify({"message": "Access denied"}), 403

    if not current_user.is_ops_user and current_user.id != file.user_id:
        return jsonify({"message": "Access denied"}), 403

    return send_from_directory(app.config['UPLOAD_FOLDER'], file.filename, as_attachment=True)

# Implement API to list all uploaded files

if __name__ == '__main__':
    app.run(debug=True)
