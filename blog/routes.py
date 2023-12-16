# This file contains routes for the app, imports from 'blog' package
from flask import render_template, flash, redirect, url_for, request
from blog import app, db, bcrypt
from blog.forms import LoginForm, RegistrationForm
from blog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required


posts = [
    {
        'author': 'D. Kinyua',
        'title': 'First post here, any welcome?',
        'content': 'I am new here, whats up gang',
        'date_posted': 'November 22, 2023'
    },
    {
        'author': 'Eren Yeager',
        'title': 'AOT over, now over for ya women',
        'content': 'But I got no game lol',
        'date_posted': 'November 18, 2023'
    },
    {
        'author': 'Gojo Satoru',
        'title': 'Haha, I am sealed now, no more trouble for Geto-kun',
        'content': 'How did this happen G?',
        'date_posted': 'November 11, 2023'
    }
]

@app.route("/")
@app.route('/home')
def home():
    return render_template('home.html', posts=posts)


@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash(f'Welcome {form.username.data}!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home')) # Itinenary conditionals
        else:
            flash('Login Failed! Check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)
    
    if current_user.is_authenticated:
        return redirect(url_for('home'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Hello {form.username.data}, your account has been created. Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/account')
@login_required
def account():
    return render_template('account.html', title='Account')