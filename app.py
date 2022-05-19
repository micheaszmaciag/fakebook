from flask import Flask, render_template, url_for, request, redirect, jsonify, session
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
import json
import hashlib
from flask_session import Session
import datetime

app = Flask(__name__)
app.config['SESSION_OERNABEBT'] = False
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)


@app.route('/')
def index():
    return render_template('main.html')


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
                session["name"] = key
                return redirect(f'/profile/')
            else:
                marker = 'Failed Login or Password please try again'

        return render_template('login.html', marker=marker)

    return render_template('login.html')


@app.route('/registration/', methods=['GET', 'POST'])
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


@app.route('/profile/', methods=['GET', 'POST'])
def profile():
    if not session.get("name"):
        return render_template('profile.html')
    return render_template('profile.html')


@app.route('/logout/')
def logout():
    session["name"] = None
    return redirect('/')


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


@app.route('/createprofile/', methods=['GET', 'POST'])
def create_profile():
    if request.method == 'POST':
        user_name = request.form['user_name']
        email = request.form['email']
        text_area = request.form['describe']
        date_of_birth = request.form['date_birth']

        with open('accounts.json', 'r', errors='ignore') as f:
            file = json.load(f)
            login = ''
            password = ''
            for key, value in file.items():
                if key == session["name"]:
                    login = value['login']
                    password = value['password']

            file[f'{session["name"]}'] = {
                "login": login,
                "password": password,
                "user_name": user_name,
                "email": email,
                "describe": text_area,
                "date_of_birth": date_of_birth
            }
        with open('accounts.json', 'w') as f:
            json.dump(file, f)

    if request.method == 'GET':
        with open('accounts.json', 'r') as f:
            account = json.load(f)
            for key, value in account.items():
                if session['name'] == key:
                    data = value['login']

        return render_template('create_profile.html', user=data)

    return render_template('create_profile.html')


if __name__ == '__main__':
    app.run(debug=True)
