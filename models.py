"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.orm import relationship

db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    first_name = db.Column(db.Text, nullable=False)

    last_name = db.Column(db.Text, nullable=False)

    image_url = db.Column(
        db.String(150),
        default="https://img.freepik.com/premium-vector/avatar-profile-icon-vector-illustration_276184-165.jpg?w=826",
    )

    posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")

    def __repr__(self):
        u = self
        return f"<User id={u.id} first_name={u.first_name} last_name={u.last_name} image_url={u.image_url}>"


class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    title = db.Column(db.Text, nullable=False)

    content = db.Column(db.Text, nullable=False)

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    tags = db.relationship("Tag", secondary="posts_tags", backref="posts")


class Tag(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    name = db.Column(db.Text, nullable=False, unique=True)


class PostTag(db.Model):
    __tablename__ = "posts_tags"

    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), primary_key=True)

    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"), primary_key=True)
