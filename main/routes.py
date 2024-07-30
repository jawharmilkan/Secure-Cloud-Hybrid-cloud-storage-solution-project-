# main/routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import Message, User
from app import db
from cryptography.fernet import Fernet

main = Blueprint('main', __name__)

@main.route('/')
@login_required
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    messages = Message.query.filter_by(receiver_id=current_user.id).all()
    return render_template('profile.html', messages=messages)

@main.route('/send_message', methods=['POST'])
@login_required
def send_message():
    receiver_username = request.form.get('receiver')
    content = request.form.get('content')
    
    receiver = User.query.filter_by(username=receiver_username).first()
    if not receiver:
        flash('User not found!')
        return redirect(url_for('main.index'))
    
    # Encrypt the message
    key = Fernet.generate_key()
    cipher_suite = Fernet(key)
    encrypted_content = cipher_suite.encrypt(content.encode())
    
    new_message = Message(sender_id=current_user.id, receiver_id=receiver.id, content=encrypted_content)
    db.session.add(new_message)
    db.session.commit()
    
    return redirect(url_for('main.profile'))
