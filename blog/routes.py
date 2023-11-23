from flask import render_template, flash, redirect
from blog import app
from blog.forms import LoginForm, RegistrationForm
from blog.models import User, Post

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
        'content': 'But i got no game lol',
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
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash(f'Welcome back {form.email.data}!', 'success')
            return redirect('/home')  # Using absolute URL using '/'
        else:
            flash(f'Login Failed! Check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect('/home')  # Using absolute URL using '/'
    return render_template('register.html', title='Register', form=form)
