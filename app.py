"""Blogly application."""

from email.mime import image
import re
from flask_debugtoolbar import DebugToolbarExtension
from flask import Flask, request, redirect, render_template, flash
from models import db, connect_db, User, Post, Tag, PostTag
from sqlalchemy import desc

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

app.config['SECRET_KEY'] = "SECRET!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


@app.route('/')
def homepage():

    posts = Post.query.order_by(desc('created_at')).limit(5).all()
    return render_template('homepage.html', posts=posts)


@app.route('/users')
def show_users():
    """Renders the a page with a list of all users"""

    users = User.query.order_by('last_name', 'first_name').all()
    return render_template('user_list.html', users=users)


@app.route('/users/<int:user_id>')
def user_details(user_id):
    """Renders the details page for the user, given a user id"""

    user = User.query.get_or_404(user_id)

    posts = Post.query.filter_by(user_id=user.id)

    return render_template('user_details.html', user=user, posts=posts)


@app.route('/users/new')
def new_user_form():
    """Renders the new user form page"""

    return render_template('new_user.html')


@app.route('/users/new', methods=["POST"])
def create_user():
    """Takes data from the new user form and adds the user to the database, then redirects the user to the user list page"""

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']

    if not image_url:
        image_url = None

    # If no first or last name are entered, the user is redirected back to the same page with an alert message flashed on the screen

    if not first_name or not last_name:
        flash('You must enter a first and last name!', 'danger')
        return redirect('/users/new')

    user = User(first_name=first_name,
                last_name=last_name, image_url=image_url)

    db.session.add(user)
    db.session.commit()

    flash('New user has been created!', 'success')
    return redirect('/users')


@app.route('/users/<int:user_id>/edit')
def edit_user_form(user_id):
    """Renders the edit user form with prepopulated fields, given a user id"""

    user = User.query.get_or_404(user_id)

    return render_template('edit_user.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=["POST"])
def edit_user(user_id):
    """Takes data from the edit user form and updates the user info in the database"""

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']

    # If no first or last name are entered, the user is redirected back to the same page with an alert message flashed on the screen

    if not first_name or not last_name:
        flash('You must enter a first and last name!', 'danger')
        return redirect(f'/users/{user_id}/edit')

    user = User.query.get_or_404(user_id)
    user.first_name = first_name
    user.last_name = last_name
    user.image_url = image_url

    db.session.add(user)
    db.session.commit()

    flash('User info has been modified!', 'success')
    return redirect('/users')


@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """Deletes a user from the database"""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    flash('User has been successfully deleted!', 'success')
    return redirect('/users')


@app.route('/users/<int:user_id>/posts/new')
def new_post_form(user_id):

    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()

    return render_template('new_post_form.html', user=user, tags=tags)


@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def submit_new_post(user_id):

    title = request.form['post_title']
    content = request.form['post_content']
    tags = request.form.getlist('tags')

    if not title or not content:
        flash('You must enter a title and content for your post!', 'danger')
        return redirect(f'/users/{user_id}/posts/new')

    post = Post(title=title, content=content, user_id=user_id)

    db.session.add(post)
    db.session.commit()

    for tag in tags:
        post.tags.append(Tag.query.filter_by(name=tag).one())

    db.session.commit()

    flash('Post has been successfully published!', 'success')
    return redirect(f'/users/{user_id}')


@app.route('/posts/<post_id>')
def show_post(post_id):

    post = Post.query.get_or_404(post_id)
    tags = post.tags

    return render_template('post.html', post=post, tags=tags)


@app.route('/posts/<post_id>/edit')
def edit_post_form(post_id):

    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    current_tags = post.tags

    return render_template('edit_post_form.html', post=post, user=post.author, tags=tags, current_tags=current_tags)


@app.route('/posts/<post_id>/edit', methods=["POST"])
def edit_post(post_id):

    title = request.form['post_title']
    content = request.form['post_content']
    tags = request.form.getlist('tags')

    if not title or not content:
        flash('You must enter a title and content for your post!', 'danger')
        return redirect(f'/posts/{post_id}')

    post = Post.query.get_or_404(post_id)

    post.title = title
    post.content = content

    db.session.add(post)
    PostTag.query.filter(post_id == post_id).delete()
    db.session.commit()

    for tag in tags:
        post.tags.append(Tag.query.filter_by(name=tag).one())

    db.session.commit()

    ('Post modifications have been saved!', 'success')
    return redirect(f'/posts/{post_id}')


@app.route('/posts/<post_id>/delete', methods=['POST'])
def delete_post(post_id):

    post = Post.query.get_or_404(post_id)
    user_id = post.author.id

    db.session.delete(post)
    db.session.commit()

    flash('Post has been successfully deleted!', 'success')
    return redirect(f'/users/{user_id}')


@app.route('/tags')
def show_tag_list():

    tags = Tag.query.all()

    return render_template('tag_list.html', tags=tags)


@app.route('/tags/<int:tag_id>')
def tag_details(tag_id):

    tag = Tag.query.get_or_404(tag_id)
    posts = tag.posts

    return render_template('tag_details.html', tag=tag, posts=posts)


@app.route('/tags/new')
def new_tag_form():
    posts = Post.query.all()
    return render_template('new_tag_form.html', posts=posts)


@app.route('/tags/new', methods=["POST"])
def create_tag():

    tag_name = request.form['tag_name']
    post_ids = request.form.getlist('posts')
    posts = Post.query.filter(Post.id.in_(post_ids)).all()

    if not tag_name:

        flash('You must enter a name for your Tag!', 'danger')
        return redirect('/tags/new')

    new_tag = Tag(name=tag_name)

    db.session.add(new_tag)
    db.session.commit()

    for post in posts:
        post.tags.append(new_tag)

    db.session.commit()

    flash('New Tag has been successfully created!', 'success')
    return redirect('/tags')


@app.route('/tags/<int:tag_id>/edit')
def edit_tag_form(tag_id):

    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.all()
    tagged_posts = tag.posts

    return render_template('edit_tag_form.html', tag=tag, posts=posts, tagged_posts=tagged_posts)


@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def edit_tag(tag_id):

    tag_name = request.form['tag_name']
    post_ids = request.form.getlist['posts']
    posts = Post.query.filter(Post.id.in_(post_ids)).all()

    if not tag_name:
        flash('You must enter a name for your Tag!', 'danger')
        return redirect(f'/tags/{tag_id}/edit')

    tag = Tag.query.get_or_404(tag_id)
    tag.name = tag_name

    db.session.add(tag)
    db.session.delete(PostTag.query.filter(tag_id == tag_id))
    db.session.commit()

    for post in posts:
        post.tags.append(tag)

    db.session.commit()

    flash('Tag modifications have been saved!', 'success')
    return redirect(f'/tags/{tag_id}')


@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def delete_tag(tag_id):

    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()

    flash('Tag successfully deleted', 'success')
    return redirect('/tags')
