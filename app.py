from flask import Flask, render_template, url_for, request, redirect, jsonify, session
from flask_session import Session
import json
import hashlib
import datetime

app = Flask(__name__)
app.config['SESSION_OERNABEBT'] = False
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)


@app.route('/')
def index():
    return render_template('main.html')


@app.route('/login/')
@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        marker = False
        login = request.form['login']
        password = request.form['password']

        with open('accounts.json', 'r') as f:
            file = json.load(f)
        new = file.items()

        for key, value in new:
            if value['login'] == login and value['password'] == hashlib.sha256(password.encode()).hexdigest():
                return redirect(f'/profile/{key}')
            else:
                marker = 'Failed Login or Password please try again'

        return render_template('login.html', marker=marker)

    return render_template('login.html')


@app.route('/registration/')
@app.route('/registration/', methods=['POST'])
def registration():
    if request.method == 'POST':

        user_name = request.form['login']
        password = request.form['password']
        sec_password = request.form['sec_password']

        if password == sec_password and user_name and password and sec_password:

            with open('accounts.json', 'r', errors='ignore') as f:
                accounts = json.load(f)

            accounts[f'account_{len(accounts) + 1}'] = {
                "login": user_name,
                "password": hashlib.sha256(password.encode()).hexdigest()
            }

            with open('accounts.json', 'w') as jf:
                json.dump(accounts, jf)

            return render_template('registration.html', f_pass=password, s_pass=sec_password,
                                   warning='The passwords are not the same')

        else:
            return render_template('registration.html', f_pass=password, s_pass=sec_password, login=user_name,
                                   warning='All of the fields is required')

    return render_template('registration.html', f_pass='', s_pass='')



@app.route('/profile/', methods= ['GET'])
def profile():

    return render_template('profile.html')


#     file = json.load(f)
# new = file.items()
#
# for key, value in new:
#     if value['login'] == login and value['password'] == hashlib.sha256(password.encode()).hexdigest():
#         return redirect(f'/profile/{key}')
#     else:
#         marker = 'Failed Login or Password please try again'
# print()
#


@app.route('/createprofile/')
@app.route('/createprofile/', methods=['POST'])
def create_profile():
    if request.method == 'POST':
        user_name = request.form['user_name']
        email = request.form['email']
        text_area = request.form['describe']
        date_of_birth = request.form['date_birth']

    return render_template('create_profile.html')


if __name__ == '__main__':
    app.run(debug=True)
