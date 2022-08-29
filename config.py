from binascii import rledecode_hqx
import pyrebase
import json
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
from jinja2 import Template
import sshintorasberry

config = {
  "apiKey": "AIzaSyCztAzrFHv3jenF6-uF9I92N-zp1v2Z80U",
  "authDomain": "raspberry-9c43c.firebaseapp.com",
  "databaseURL": "https://raspberry-9c43c-default-rtdb.firebaseio.com",
  "projectId": "raspberry-9c43c",
  "storageBucket": "raspberry-9c43c.appspot.com",
  "messagingSenderId": "337910073952"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()


global pers
pers = {"nume": "", "email": "", "uid": "", "gender": "",  "age": "",  "weight": "",  "phone": "",  "address": "", "details": "", "type": ""}

global doctor
doctor = {"nume": "", "email": "", "uid": "", "gender": "", "phone": "", "type": ""}

global post
post = {"patient": "", "doctor": "", "message": "", "date": ""}

app = Flask(__name__)

@app.route("/Start_Data", methods=['GET', 'POST'])
def Start_Data():
  try:
    sshintorasberry.start_sensors(pers["nume"])
    flash('Datele au fost introduse cu succes în baza de date.', 'success')
    return redirect(url_for('patient'))
  except:
    flash('Datele nu au fost introduse cu succes în baza de date. Încearcă din nou', 'error')
    return redirect(url_for('patient'))