from flask import Flask
from routes.auth import auth_bp
from routes.doctors import doctor_bp
from routes.appointments import appointment_bp
from flask import redirect

app = Flask(__name__)
app.secret_key = "secret"

app.register_blueprint(auth_bp)
app.register_blueprint(doctor_bp)
app.register_blueprint(appointment_bp)

@app.route('/')
def index():
    return redirect('/doctors')

app.run(debug=True)
