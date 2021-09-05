#Importin Packages
from flask import Flask, render_template, request, session, redirect
import json
from flask_mail import Mail
import os
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

#Opening A File And Connecting The Website To A Server
with open('config.json','r') as c:
    params = json.load(c)["params"]

local_server = True

#Creating Our Website
app = Flask(__name__)

#Connecting Our Website With Gmail
app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME = params['gmail-user'],
    MAIL_PASSWORD = params['gmail-password']   
)

mail = Mail(app)

#Connectin Our Website With phpMyAdmin
if(local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']

else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']

db = SQLAlchemy(app)

#Creatin Class For Storing The Values Of Contact Form
class Contact(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(12), nullable=False)
    message = db.Column(db.String(100), nullable=False)

#Importing Webpages For Our Website
@app.route('/',methods= ['GET', 'POST'])
def home():
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        email = request.form.get('email')
        message = request.form.get('message')
        entry = Contact(name=name, email=email, phone=phone, message=message)
        db.session.add(entry)
        db.session.commit()
        mail.send_message('New message from ' + name, sender=email, recipients=[params['gmail-user']], body=message + "\n" + phone)

    return render_template('index.html')

@app.route('/feature')
def feature():
    return render_template('feature.html')

#Running Our Website On A Deployment Server
app.run(debug=True)