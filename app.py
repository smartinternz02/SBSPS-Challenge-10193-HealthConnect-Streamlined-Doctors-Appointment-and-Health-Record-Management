from flask import Flask,send_from_directory,render_template
from flask import send_from_directory
from flask import Flask, send_from_directory, render_template, request, redirect, url_for
from flask_restful import Resource, Api
from package.patient import Patients, Patient
from package.doctor import Doctors, Doctor
from package.appointment import Appointments, Appointment
from package.common import Common
from package.medication import Medication, Medications
from package.department import Departments, Department
from package.nurse import Nurse, Nurses
from package.room import Room, Rooms
from package.procedure import Procedure, Procedures 
from package.prescribes import Prescribes, Prescribe
from package.undergoes import Undergoess, Undergoes
from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import json
import os
users = [
    {"username": "user1","password": "hashed_password1", "user_type": "patient"},
    {"username": "user2", "password": "hashed_password2", "user_type": "doctor"}
]

with open('config.json') as data_file:
    config = json.load(data_file)

app = Flask(__name__, static_url_path='')
api = Api(app)

api.add_resource(Patients, '/patient')
api.add_resource(Patient, '/patient/<int:id>')
api.add_resource(Doctors, '/doctor')
api.add_resource(Doctor, '/doctor/<int:id>')
api.add_resource(Appointments, '/appointment')
api.add_resource(Appointment, '/appointment/<int:id>')
api.add_resource(Common, '/common')
api.add_resource(Medications, '/medication')
api.add_resource(Medication, '/medication/<int:code>')
api.add_resource(Departments, '/department')
api.add_resource(Department, '/department/<int:department_id>')
api.add_resource(Nurses, '/nurse')
api.add_resource(Nurse, '/nurse/<int:id>')
api.add_resource(Rooms, '/room')
api.add_resource(Room, '/room/<int:room_no>')
api.add_resource(Procedures, '/procedure')
api.add_resource(Procedure, '/procedure/<int:code>')
api.add_resource(Prescribes, '/prescribes')
api.add_resource(Undergoess, '/undergoes')

# Routes

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                          'favicon.ico',mimetype='image/vnd.microsoft.icon')

                          

    


# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Process the form data, authenticate user, and then redirect to index page
        #return redirect(url_for('indeex'))
        username = request.form['username']
        password = request.form['password']
        user_type = request.form['user_type']

        # Here, you would perform authentication and authorization checks
        # and determine where to redirect the user based on their user_type
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        if(user_type=='doctor'):
            cursor.execute("SELECT password FROM doctor WHERE username = ? ", (username,))
        else:
            cursor.execute("SELECT password FROM patient WHERE username = ? ", (username,))
        user = cursor.fetchone()
        
        if user:
            if user[0] == password:  # Compare hashed password (replace with secure hashing)
                if(user_type=='doctor'):
                    return app.send_static_file('indeex.html')
                elif(user_type=='patient'):
                    return app.send_static_file('patient1.html')
 
            else:
                conn.close()
                
                return "usernotfound"
        else:
            conn.close()
            return "User not found"
        return "User not found"
        return app.send_static_file('login.html')
    return app.send_static_file('login.html')
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn
    
@app.route('/doctor_dashboard')
def doctor_dashboard():
    return app.send_static_file('indeex.html')

@app.route('/patient_dashboard')
def patient_dashboard():
    return app.send_static_file('patient1.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        user_type = request.form.get('user_type')
        fname=request.form.get('fname')
        lname=request.form.get('lname')
        number=request.form.get('number')
        addr=request.form.get('Address')
        ins=request.form.get('insurance')
        if password != confirm_password:
            #return "Passwords do not match. Please try again."
            y=0

        # Store user information in the database
        else:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            if(user_type=='doctor'):
                cursor.execute("INSERT INTO doctor (username, password, doc_first_name, doc_last_name, doc_ph_no, doc_address) VALUES (?, ?, ? , ? , ? , ?)",
                        (username, password,fname,lname,number,addr))
            else:
                cursor.execute("INSERT INTO patient (username, password,pat_first_name,pat_last_name,pat_insurance_no,pat_ph_no,pat_address) VALUES (?, ?,?,?,?,?,?)",
                        (username, password,fname,lname,ins,number,addr))
            conn.commit()
            conn.close()

        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/')
def index():
    return app.send_static_file('login.html')
@app.route('/indeex')
def indeex():
    return app.send_static_file('indeex.html')
if __name__ == '__main__':
    app.run(debug=True,host=config['host'],port=config['port'])