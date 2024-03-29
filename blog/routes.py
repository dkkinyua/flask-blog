# This file contains routes for the app, imports from 'blog' package
import os
import secrets
from PIL import Image
from flask import render_template, flash, redirect, url_for, request, abort
from blog import app, db, bcrypt, mail
from blog.forms import LoginForm, RegistrationForm, UpdateAccountForm, PostForm, RequestPasswordForm, ResetPasswordForm
from blog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy.exc import IntegrityError
from flask_mail import Message



# The 'HOME' route, to the 'HOME' route
@app.route("/")
@app.route('/home')
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts)

# The 'ABOUT' route, to the 'ABOUT' route
@app.route('/about')
def about():
    return render_template('about.html', title='About')

# The 'LOGIN' route, to the 'LOGIN' route
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
            flash('Login Failed! Check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)
    
    if current_user.is_authenticated:
        return redirect(url_for('home'))

# The 'REGISTER' route, to the 'REGISTER' route
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
    
# The 'LOGOUT' route, to the 'LOGOUT' and other routes   
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

# The 'ACCOUNT' route, to the 'ACCOUNT' and other routes

# A function that saves the profile picture uploaded by the user
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext= os.path.splitext(form_picture.filename) #Splits the filename and filetype i.e. 'jpg', 'png'
    picture_fn = random_hex + f_ext # Adds the random_hex created above and the file_extension
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    # Resizing the selected picture
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn



@app.route('/account', methods=['POST', 'GET'])
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

#this is a route to create a new post
@app.route('/posts/new', methods=['POST', 'GET'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
    #Commits and saves posts to the database
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()

        flash('Your post has been created successfully!', 'success')
        return redirect(url_for('home'))
        
    return render_template('create_post.html', title='New Post', form=form)

# This is a route to view our post
@app.route('/posts/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

# This is a route to update our post
@app.route('/posts/<int:post_id>/update', methods=['POST', 'GET'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()

    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been successfully been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    if request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    
    return render_template('update_post.html', title=f'Update Post-{post.author.username}', form=form)

# This is a route to delete your post
@app.route('/posts/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'danger')
    return redirect(url_for('home'))

# A route to show the user's posts and profile
@app.route('/user/<username>')
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)     
    return render_template('user_posts.html', posts=posts, user=user)

# a function to send reset emails to the user
def send_reset_email(user):
    user = User()
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='no-reply@demo.com', recipients=[user.email])
    msg.body = f''' To reset your password, please follow the link: {url_for('reset_token', token=token, _external=True)}
If you did not request for a password change, please ignore this mail as no changes will be made to your profile.
This message has been sent by admin.
'''
    mail.send(msg)


# This is a route to request for a pass reset
@app.route('/reset_password', methods=['POST', 'GET'])
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
@app.route('/reset_password/<token>', methods=['POST', 'GET'])
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