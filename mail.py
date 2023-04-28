from flask import Flask
from flask_mail import Mail, Message
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
app = Flask(__name__)


# Configure Flask-Mail settings for sending email
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'petstellonstudios@gmail.com'
app.config['MAIL_PASSWORD'] = "szsboybheujzjvxo"
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)


@app.route('/')
def send_email():
    # Create the message object
    msg = Message('Test Email', sender='petstellonstudios@gmail.com', recipients=['fayoseayomipo170@gmail.com'])

    # Add the message body
    msg.body = "Hello, this is a test email sent from Flask-Mail!"

    # Send the email
    mail.send(msg)

    # Return a message to the user
    return "Email sent!"

@app.route('/send')
def sender():
    import smtplib

    sender = 'petstellonstudios@gmail.com'
    receivers = ['rouspet62@gmail.com']
    message = """From: From Person <petstellonstudios@gmail.com>
    To: To Person <rouspet62@gmail.com.com>
    Subject: SMTP email example


    This is a test message.
    """


    smtpObj = smtplib.SMTP('smtp.gmail.com')
    smtpObj.sendmail(sender, receivers, message)
    return "Successfully sent email"


if __name__ == '__main__':
    app.run(debug=True)




