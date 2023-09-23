"""Blogly application."""

from flask import Flask, render_template, redirect, flash, request, session
from models import db, connect_db, User, Post
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///blogly"
# app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///blogly_test"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = False
app.config["SECRET_KEY"] = "chickenzarecool21837"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
debug = DebugToolbarExtension(app)


connect_db(app)
with app.app_context():
    db.create_all()


@app.route("/")
def home_page():
    """redirects to /users"""
    return redirect("/users")


@app.route("/users")
def list_users():
    """Shows list of all users in db"""
    users = User.query.all()
    return render_template("list_users.html", users=users)


@app.route("/users/new", methods=["GET"])
def new_user_form():
    """shows form to create new user"""
    return render_template("create_user.html")


@app.route("/users/new", methods=["POST"])
def new_user():
    """creates a new user from form data"""
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]
    image_url = image_url if image_url else None

    user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(user)
    db.session.commit()
    return redirect(f"/users/{user.id}")


@app.route("/users/<int:user_id>")
def user_details(user_id):
    """shows user details page"""
    user = User.query.get_or_404(user_id)
    posts = user.posts
    return render_template("details.html", user=user, posts=posts)


@app.route("/users/<int:user_id>/edit")
def edit_user(user_id):
    """shows edit user form"""
    user = User.query.get(user_id)
    return render_template("edit_user.html", user=user)


@app.route("/users/<int:user_id>/edit", methods=["POST"])
def save_edit_user(user_id):
    """edits user based on form data"""
    user = User.query.get(user_id)
    user.first_name = request.form["first_name"]
    user.last_name = request.form["last_name"]
    user.image_url = request.form["image_url"]
    db.session.add(user)
    db.session.commit()
    return redirect(f"/users/{user_id}")


@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    """deletes user and all of their posts"""
    user = User.query.get_or_404(user_id)
    for post in user.posts:
        db.session.delete(post)
    db.session.commit
    db.session.delete(user)
    db.session.commit()
    return redirect("/users")


@app.route("/posts/<int:post_id>")
def show_post(post_id):
    """shows post of post_id"""
    post = Post.query.get_or_404(post_id)
    return render_template("post.html", post=post, user=post.user)


@app.route("/users/<int:user_id>/posts/new")
def show_new_post_form(user_id):
    """shows new post form"""
    user = User.query.get(user_id)
    return render_template("post_form.html", user=user)


@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def create_post(user_id):
    """creates a new post from form data"""
    title = request.form["title"]
    content = request.form["content"]
    post = Post(title=title, content=content, user_id=user_id)
    db.session.add(post)
    db.session.commit()
    return redirect(f"/users/{user_id}")


@app.route("/posts/<int:post_id>/edit")
def edit_post(post_id):
    """shows edit post form"""
    post = Post.query.get(post_id)
    return render_template("edit_post.html", post=post)


@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def submit_edit_post(post_id):
    """edits a post from form data"""
    post = Post.query.get(post_id)
    title = request.form["title"]
    content = request.form["content"]
    post.title = title
    post.content = content
    db.session.commit()
    return redirect(f"/posts/{post.id}")


@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    """deletes post with using post_id"""
    post = Post.query.get_or_404(post_id)
    user_id = post.user.id
    db.session.delete(post)
    db.session.commit()
    return redirect(f"/users/{user_id}")
