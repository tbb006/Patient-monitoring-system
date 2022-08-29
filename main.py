from config import *
from doctor import *
from user import *


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.form.get('action1') == 'Pacient':
            return redirect(url_for('connectPatient'))
        elif request.form.get('action2') == 'Doctor':
            return redirect(url_for('connectDoctor'))
    elif request.method == 'GET':
        return render_template('index/homePage.html')
    return render_template("index/homePage.html")


if __name__ == '__main__':
    app.secret_key='1234'
    app.run(host='0.0.0.0')


