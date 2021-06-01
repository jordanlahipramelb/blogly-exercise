"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

DEFAULT_IMAGE_URL = "https://cdn.icon-icons.com/icons2/1378/PNG/512/avatardefault_92824.png"

# (app) from app.py
def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text, nullable=False, default=DEFAULT_IMAGE_URL)

    posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")

    def __repr__(self):
        u = self
        return f"<User id = {u.id}, first_name = {u.first_name}, last_name = {u.last_name}, image_url = {u.image_url}>"


class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))


class PostTag(db.Model):

    __tablename__ = "posts_tags"
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"), primary_key=True)


class Tag(db.Model):

    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False, unique=True)

    # connects tags to posts (posts.title, posts.content)
    posts = db.relationship("Post", secondary="posts_tags", backref="tags")
