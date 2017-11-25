# coding=utf-8
from flask import Flask, render_template, url_for, request, session, redirect
from flask_pymongo import PyMongo
import bcrypt  # to hash the password

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'web_mongodb'
app.config['MONGO_URI'] = 'mongodb://hugo:hugohugohugo@ds040877.mlab.com:40877/web_mongodb'

mongo = PyMongo(app)


@app.route('/')
def index():
    if 'email' in session:
        return render_template('index.html', blank=session['email'])
        # return 'You are logged in as ' + session['email']
    return render_template('index.html', blank='登录')
    # return render_template('sign_login.html')


@app.route('/sign_login', methods=['GET', 'POST'])
def sign_login():
    if request.method == 'GET':
        return render_template('sign_login.html')

    users = mongo.db.users
    if request.form.get('email_login') is not None:
        login_user = users.find_one({'email': request.form.get('email_login')})
        if login_user and bcrypt.hashpw(request.form['password_login'].encode('utf-8'),
                                        login_user['password']) == login_user['password']:
            session['email'] = request.form['email_login']
            return redirect(url_for('index'))
    else:
        existing_user = users.find_one({'email': request.form.get('email_signup')})
        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['password_signup'].encode('utf-8'), bcrypt.gensalt())
            users.insert({'email': request.form['email_signup'], 'password': hashpass,
                          'username': request.form.get('username_signup'), 'intro': request.form.get('intro_signup')})
            session['email'] = request.form['email_signup']
            return redirect(url_for('index'))
        return 'That email already exists!'
    return render_template('sign_login.html')


@app.route('/user_info')
def user_info():
    users = mongo.db.users
    login_user = users.find_one({'email': session['email']})
    return render_template('user_info.html', username=login_user['username'], email=login_user['email'],
                           intro=login_user['intro'])


@app.route('/spider', methods=['POST', 'GET'])
def spider():
    return redirect('https://www.baidu.com/s?wd=%ssite:tieba.baidu.com' % request.form.get('search'))
    # return render_template('spider.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=True)
