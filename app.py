import requests
from os import environ
from flask import Flask, render_template, send_from_directory
from datetime import datetime
from math import floor
from json import loads
from flask_talisman import Talisman



# Initialise app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'


# Initialise Flask Talisman
talisman = Talisman(app, content_security_policy=None)
if not environ.get('IN_CONTAINER'): talisman.force_https = False


# Homepage / profile
@app.route('/')
@app.route('/profile/')
def profile():
    # Calculate age to save me updating the site
    age = datetime.today() - datetime(1995, 3, 5)
    age = floor((age.days / 7) / 52)

    # Get data for codewars section
    codewars = loads(requests.get('https://www.codewars.com/api/v1/users/JackieBoyBlue/code-challenges/completed?page={page}').text)
    katas= []
    for i in codewars['data'][:10]:
            if 'python' in i['completedLanguages']:
                date = datetime.strptime(i['completedAt'][:10], '%Y-%m-%d')
                katas.append((i['name'], date.date().strftime('%d/%m/%y')))

    return render_template('profile.html', age=age, katas=katas)


# CV
@app.route('/cv/')
def cv():
    return render_template('cv.html')


# Work experience
@app.route('/work/')
def work():
    return render_template('work.html')


# About me
@app.route('/about-me/')
def about_me():
    return render_template('about-me.html')


# Download CV
@app.route("/uploads/<path:name>")
def download(name):
    return send_from_directory(
        app.config['UPLOAD_FOLDER'], name, as_attachment=True
    )


# 404 handler
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), {"Refresh": "5; url=/"}



# Run flask
if __name__ == '__main__':
    port = int(environ.get('PORT', 5000))
    if environ.get('IN_CONTAINER'):
        from waitress import serve
        serve(app, port=port)
        debug=False
    else: debug=True
    app.run(host='0.0.0.0', port=port, debug=debug)