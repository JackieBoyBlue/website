import requests
from os import environ
from flask import Flask, render_template, session
from datetime import datetime
from math import floor
from json import loads
from dotenv import load_dotenv



# Initialise app
app = Flask(__name__)
load_dotenv('.env')
app.secret_key = environ.get('SECRET_KEY')


# Homepage / profile
@app.route('/')
@app.route('/profile')
def profile():
    # Calculate age to save me updating the site
    age = datetime.today() - datetime(1995, 3, 5)
    age = floor((age.days / 7) / 52)

    # Get data for codewars section
    codewars = loads(requests.get('https://www.codewars.com/api/v1/users/JackieBoyBlue/code-challenges/completed?page={page}').text)
    katas= []
    for i in codewars['data']:
        if 'python' in i['completedLanguages']:
            date = datetime.strptime(i['completedAt'][:10], '%Y-%m-%d')
            katas.append((i['name'], date.date().strftime('%d/%m/%y')))

    return render_template('profile.html', age=age, katas=katas)


@app.route('/cv')
def cv():
    return render_template('cv.html')


@app.route('/work')
def work():
    return render_template('work.html')


# Jinja2 functions
@app.context_processor
def cookie_check():
    cookie_check = session.get('cookie_check')
    session['cookie_check'] = True
    return dict(cookie_check=cookie_check)


# # Error handling
# @app.errorhandler(404)
# def page_not_found(e):
#     return render_template('404.html'), {"Refresh": "7; url=/"}

# @app.errorhandler(401)
# def page_not_found(e):
#     return render_template('401.html'), {"Refresh": "7; url=/"}


# Run flask

if __name__ == '__main__':
    app.run(host='0.0.0.0')