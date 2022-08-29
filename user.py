from config import *
from datetime import datetime
from flask import Flask, flash, redirect, render_template, \
     request, url_for

@app.route("/connectPatient")
def connectPatient():
  return render_template('patient_page/connectPatient.html')

@app.route("/patient")
def patient():
    return render_template("patient_page/patient_startData.html", email = pers["email"], nume = pers["nume"])

@app.route("/connect_Patient", methods=['GET', 'POST'])
def connect_Patient():
  if request.method == "POST":
    email = request.form['email']
    password = request.form['parola']  
    try:
      utilizator = auth.sign_in_with_email_and_password(email, password)
      pers["email"] = utilizator["email"]
      pers["uid"] = utilizator["localId"]
      data = db.child("Pacienti").get()
      pers["nume"] = data.val()[pers["uid"]]["Nume"]
      return redirect(url_for('patient'))
    except:
      flash('Datele introduse nu sunt corecte. Încearcă din nou', 'error')
      return redirect(url_for('connectPatient'))

@app.route("/patient/graphs", methods=['GET', 'POST'])
def patient_graphs():
  people = db.child("aplicatie").order_by_child("utilizator").equal_to(pers["nume"]).get()
  data_patient=[]
  for person in people.each():
    data_patient.append(person.val())
  return render_template("patient_page/patient_graphs.html", email = pers["email"], nume = pers["nume"], data_patient = data_patient)
      
@app.route("/patient/patient_data")
def patient_data():
    return render_template('patient_page/patient_data.html', email = pers["email"], nume = pers["nume"])

@app.route("/patient/patient_lastData")
def patient_lastData():
    return render_template('patient_page/patient_lastData.html', email = pers["email"], nume = pers["nume"])

@app.route("/patient/messages")
def patient_messages():
    return render_template('patient_page/patient_messages.html', email = pers["email"], nume = pers["nume"])

@app.route("/patient/send_message")
def patient_send_message():
  return render_template("patient_page/patient_sendMessage.html", nume = pers["nume"])

@app.route("/patient/send_message_ok", methods=['GET', 'POST'])
def patient_send_message_ok():
    if request.method == "POST":
        doctor_email = request.form.get('doctor')
        patient_email = pers["email"]
        patient_nume = pers["nume"]
        subject = request.form['subject']
        message = request.form['message']
        try:
          date_time = datetime.now().strftime("%d-%b-%Y (%H:%M)")
          data = {"Doctor": doctor_email,"Pacient": patient_nume, "Email": patient_email ,"Subiect": subject, "Mesaj": message, "Data": date_time}
          db.child("Mesaje Pacienti").child().push(data)
          flash('Mesajul a fost trimis cu succes.', 'success')
          return render_template("patient_page/patient_sendMessage.html", email = pers["email"], nume = pers["nume"])
        except:
          flash('Mesajul nu a fost trimis cu succes. Încearcă din nou', 'error')
          return render_template("patient_page/patient_sendMessage.html", email = pers["email"], nume = pers["nume"])