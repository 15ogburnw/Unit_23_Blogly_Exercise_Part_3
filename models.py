"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
from datetime import datetime

db = SQLAlchemy()


def connect_db(app):

    db.app = app
    db.init_app(app)


class User(db.Model):

    """Model for a user instance in the database. Includes a first name, last name, and profile picture URL"""

    def __repr__(self):
        u = self
        return f'<User {u.first_name} {u.last_name}>'

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    first_name = db.Column(db.Text, nullable=False)

    last_name = db.Column(db.Text, nullable=False)

    image_url = db.Column(db.Text, nullable=True,
                          default='https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png')

    @property
    def full_name(self):
        return self.first_name + ' ' + self.last_name


class Post(db.Model):

    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    title = db.Column(db.String(50), nullable=False, unique=True)

    content = db.Column(db.Text, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.today())

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    author = db.relationship(
        'User', backref=backref('posts', cascade='all, delete'))

    def __repr__(self):
        p = self

        return f'<Post title = {p.title}>'

    @property
    def date_posted(self):

        today = self.created_at

        return today.strftime('%a %b %-d %Y, %-I:%-M %p')


class Tag(db.Model):

    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    name = db.Column(db.String(20), unique=True)

    posts = db.relationship('Post', secondary='posts_tags', backref='tags')


class PostTag(db.Model):

    __tablename__ = 'posts_tags'

    post_id = db.Column(db.Integer, db.ForeignKey(
        'posts.id'), primary_key=True)

    tag_id = db.Column(db.Integer, db.ForeignKey(
        'tags.id'), primary_key=True)
