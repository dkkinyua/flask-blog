from flask import Blueprint, redirect, render_template, request, flash, url_for
from flask_login import current_user, logout_user, login_user, login_required
from blog import db, bcrypt
from blog.models import User, Post
from blog.users.forms import LoginForm, RegistrationForm, UpdateAccountForm, RequestPasswordForm, ResetPasswordForm
from blog.users.utils import save_picture, send_reset_email
from sqlalchemy.exc import IntegrityError

users = Blueprint('users', __name__)

# The 'LOGIN' route, to the 'LOGIN' route
@users.route('/login', methods=['GET', 'POST'])
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
            flash('Login Failed! Check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)
    
    if current_user.is_authenticated:
        return redirect(url_for('home'))

# The 'REGISTER' route, to the 'REGISTER' route
@users.route('/register', methods=['GET', 'POST'])
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
    
# The 'LOGOUT' route, to the 'LOGOUT' and other routes   
@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@users.route('/account', methods=['POST', 'GET'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        try:
            db.session.commit() # Commits the saved username and email to the db
            flash(f'Hi {current_user.username}, your account has been updated!', 'success') # Flashes the success message
            return redirect(url_for('account'))
        # It solves the user exists error
        except IntegrityError:
            db.session.rollback() 
            flash('This email or username is taken.', 'danger')
    
    elif request.method == 'GET':
        # Populates the form with the current user's details
        form.username.data = current_user.username
        form.email.data = current_user.email
        
    if current_user.image_file:
        image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    else:
       image_file = url_for('static', filename='profile_pics/default.jpg')  # Provide a default image file
    return render_template('account.html', title='Account', image_file=image_file, form=form)

# A route to show the user's posts and profile
@users.route('/user/<username>')
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)     
    return render_template('user_posts.html', posts=posts, user=user)

# This is a route to request for a pass reset
@users.route('/reset_password', methods=['POST', 'GET'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        send_reset_email(user)
        flash('An email with instructions on how to reset your password has been sent to your email', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset password', form=form)

# This is a route to actually reset your password
@users.route('/reset_password/<token>', methods=['POST', 'GET'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_user_token(token)
    if user is None:
        flash('This is an invalid or expired token, try again.', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash(f'Hello {form.username.data}, your password has been updated! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset your password', form=form)