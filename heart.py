# import math
# from turtle import *
# def hearta(k):
#     return 15*math.sin(k)**3
# def heartb(k):
#     return 12*math.cos(k)-5*\
#     math.cos(2*k)-2*\
#                     math.cos(3*k)-\
#                     math.cos(4*k)
# speed(0)
# bgcolor("black")
# for i in range(10000):
#     goto(hearta(i)*20, heartb(i)*20)
#     for j in range(5):
#         color("#f73487")
#     goto(0, 0)
#
# done()
# import random
#
# # a1 = random.randint(len(0, 1))111111
#
# a1 = f"@abc{random.randint(1000, 9999)}"
# a2 = random.randint(1, 19)
#
# print(a1)
# print(a2)

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash
import secrets

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# Configure Flask-Mail settings for sending email
app.config['MAIL_SERVER'] = 'your-mail-server.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'your-mail-username'
app.config['MAIL_PASSWORD'] = 'your-mail-password'
app.config['MAIL_DEFAULT_SENDER'] = 'your-default-sender-email'
mail = Mail(app)

# Example route for resetting password
@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        email = request.form['email']
        # Check if email exists in database
        # ...
        if email_exists:
            # Generate a new random password
            new_password = secrets.token_urlsafe(10)
            # Hash the new password
            hashed_password = generate_password_hash(new_password)
            # Update the hashed password in the database for the given email
            # ...
            # Send the new password to the user's email
            msg = Message('Password Reset', recipients=[email])
            msg.body = f'Your new password is: {new_password}'
            mail.send(msg)
            flash('Password reset successfully. Check your email for the new password.')
            return redirect(url_for('login'))
        else:
            flash('Invalid email address.')
    return render_template('reset_password.html')