import email
from config import *
from datetime import datetime

@app.route("/connectDoctor")
def connectDoctor():
  return render_template('doctor/connectDoctor.html')

@app.route("/connect_Doctor", methods=['GET', 'POST'])
def connect_Doctor():
  if request.method == "POST":
    email = request.form['email']
    password = request.form['parola']  
    try:
      utilizator = auth.sign_in_with_email_and_password(email, password)
      pers["email"] = utilizator["email"]
      pers["uid"] = utilizator["localId"]
      data = db.child("Doctori").get()
      pers["nume"] = data.val()[pers["uid"]]["Nume"]
      pers["type"] = data.val()[pers["uid"]]["Tip"]
      return redirect(url_for('doctor'))
    except:
      flash('Datele introduse nu sunt corecte. Încearcă din nou', 'error')
      return redirect(url_for('doctor/connect_Doctor'), email = pers["email"], nume = pers["nume"])

@app.route("/registerDoctor")
def registerDoctor():
  return render_template('doctor/registerDoctor.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
  if request.method == "POST":
    name = request.form['nume']
    email = request.form['email']
    gender = request.form['gender']
    password = request.form['password']
    phone = request.form['phone']
    type = "Doctor"
    code = request.form['code']
    if code == 't1rvfho20mkf5jy28s6':
      try:
        auth.create_user_with_email_and_password(email, password)
        utilizator = auth.sign_in_with_email_and_password(email, password)
        pers["email"] = utilizator["email"]
        pers["gender"] = gender
        pers["uid"] = utilizator["localId"]
        pers["nume"] = name
        pers["phone"] = phone
        pers["type"] = type
        data = {"Nume": name, "Email": email, "Gen": gender, "Telefon": phone, "Tip": type}
        db.child("Doctori").child(pers["uid"]).set(data)
        flash('Datele au fost introduse cu succes în baza de date.', 'success')
        return render_template("doctor/connectDoctor.html", email = pers["email"], nume = pers["nume"])
      except:
        flash('Datele nu au fost introduse cu succes în baza de date. Încearcă din nou', 'error')
        return render_template("doctor/registerDoctor.html", email = pers["email"], nume = pers["nume"])

@app.route("/doctor")
def doctor():
    return render_template("doctor/doctor.html", email = pers["email"], nume = pers["nume"])


@app.route("/doctor/graphs", methods=['GET', 'POST'])
def doctor_graphs():
  selectedvalue=request.args.get("selectedvalue")
  
  people = db.child("aplicatie").order_by_child("utilizator").equal_to(str(selectedvalue)).get()
  data_json=[]
  for person in people.each():
    data_json.append(person.val())

  patient = db.child("Pacienti").order_by_child("Nume").get()
  name_json=[]
  for user in patient.each():
    name_json.append(user.val())

  return render_template("doctor/doctor_graphs.html", email = pers["email"], nume = pers["nume"], name_json = name_json, data_json = data_json, selectedvalue = selectedvalue)


@app.route("/doctor/patient")
def doctor_list_patient():
    return render_template("doctor/doctor_list_patient.html", email = pers["email"], nume = pers["nume"])

@app.route("/doctor/profile")
def doctor_profile():
    email = pers["email"]
    userProfile = db.child("Doctori").order_by_child("Email").equal_to(email).get()
    for user in userProfile.each():
      numeR = user.val()['Adresa']
    return render_template("doctor/doctor_profile.html", email = pers["email"], nume = pers["nume"], numeR=numeR)

@app.route("/doctor/view_messages")
def doctor_view_messages():
  return render_template("doctor/doctor_view_messages.html", nume = pers["nume"])

@app.route("/doctor/messages")
def doctor_message():
  return render_template("doctor/doctor_messages.html", nume = pers["nume"])

@app.route("/doctor/messages/send_message", methods=['GET', 'POST'])
def send_message():
    if request.method == "POST":
        patient = request.form['patient']
        doctor_nume = pers["nume"]
        doctor_email = pers["email"]
        message = request.form['message']
        try:
          date = datetime.now().strftime("%d-%b-%Y (%H:%M:%S)")
          data = {"Pacient": patient, "Doctor": doctor_nume, "Email": doctor_email, "Mesaj": message, "Data": date}
          db.child("Mesaje").child().push(data)
          flash('Mesajul a fost trimis cu succes.', 'success')
          return render_template("doctor/doctor_messages.html", email = pers["email"], nume = pers["nume"])
        except:
          flash('Mesajul nu a fost trimis cu succes. Încearcă din nou', 'error')
          return render_template("doctor/doctor_messages.html", email = pers["email"], nume = pers["nume"])
          
@app.route("/doctor/create_user")
def doctor_create_user():
    return render_template("doctor/doctor_create_user.html", email = pers["email"], nume = pers["nume"])


@app.route("/doctor/create_user/register_user", methods=['GET', 'POST'])
def doctor_register_user():
  if request.method == "POST":
    numeUser = request.form['userName']
    email = request.form['email']
    gender = request.form['gender']
    password = request.form['password']
    age = request.form['age']
    weight = request.form['weight']
    phone = request.form['phone']
    address = request.form['address']
    details = request.form['details']  
    try:
      auth.create_user_with_email_and_password(email, password)
      utilizator = auth.sign_in_with_email_and_password(email, password)
      pers["email"] = utilizator["email"]
      pers["gender"] = gender
      pers["uid"] = utilizator["localId"]
      pers["nume"] = numeUser
      pers["age"] = age
      pers["weight"] = weight
      pers["phone"] = phone
      pers["address"]= address
      pers["details"] = details
      data = {"Nume": numeUser, "Email": email, "Gen": gender, "DataNastere": age, "Greutate": weight + " kg", "Telefon": phone, "Adresa": address, "Detalii": details, "Tip": "Pacient"}
      db.child("Pacienti").child(pers["uid"]).set(data)
      flash('Datele au fost introduse cu succes în baza de date.', 'success')
      return render_template("doctor/doctor_create_user.html", email = pers["email"], nume = pers["nume"])
    except:
      flash('Datele nu au fost introduse cu succes în baza de date. Încearcă din nou', 'error')
      return render_template("doctor/doctor_create_user.html", email = pers["email"], nume = pers["nume"])

@app.route("/doctor/view_users")
def doctor_view_users():
    return render_template("doctor/doctor_view_users.html", email = pers["email"], nume = pers["nume"])


