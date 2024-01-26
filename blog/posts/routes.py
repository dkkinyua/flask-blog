from flask import Blueprint, request, redirect, render_template, abort, flash, url_for
from blog.posts.forms import PostForm
from blog.models import Post
from blog import db
from flask_login import current_user, login_required

posts = Blueprint('posts', __name__)

#this is a route to create a new post
@posts.route('/posts/new', methods=['POST', 'GET'])
@login_required

def new_post():
    form = PostForm()
    if form.validate_on_submit():
    #Commits and saves posts to the database
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()

        flash('Your post has been created successfully!', 'success')
        return redirect(url_for('main.home'))
        
    return render_template('create_post.html', title='New Post', form=form)

# This is a route to view our post
@posts.route('/posts/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

# This is a route to update our post
@posts.route('/posts/<int:post_id>/update', methods=['POST', 'GET'])
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
        return redirect(url_for('posts.post', post_id=post.id))
    if request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    
    return render_template('update_post.html', title=f'Update Post-{post.author.username}', form=form)

# This is a route to delete your post
@posts.route('/posts/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'danger')
    return redirect(url_for('main.home'))