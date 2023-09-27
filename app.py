"""Blogly application."""

from flask import Flask, render_template, redirect, flash, request, session
from models import db, connect_db, User, Post, Tag, PostTag
from flask_debugtoolbar import DebugToolbarExtension
from datetime import datetime

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
    """shows home page"""
    return render_template("home.html")


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
    print("****************************************************************")
    print(str(post.created_at))
    formatted_datetime = post.created_at.strftime("%a %b %d %Y, %I:%M%p")
    return render_template(
        "post.html", post=post, user=post.user, tags=post.tags, date=formatted_datetime
    )


@app.route("/users/<int:user_id>/posts/new")
def show_new_post_form(user_id):
    """shows new post form"""
    user = User.query.get(user_id)
    tags = Tag.query.all()
    return render_template("post_form.html", user=user, tags=tags)


@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def create_post(user_id):
    """creates a new post from form data"""
    title = request.form["title"]
    content = request.form["content"]
    tags = request.form.getlist("tags")
    post = Post(title=title, content=content, user_id=user_id)
    # is there a way to get post id without making another query? maybe sending it in a response somehow?
    db.session.add(post)
    for tag_id in tags:
        tag = Tag.query.get(tag_id)
        post.tags.append(tag)
    db.session.commit()
    return redirect(f"/users/{user_id}")


@app.route("/posts/<int:post_id>/edit")
def edit_post(post_id):
    """shows edit post form"""
    post = Post.query.get(post_id)
    tags = Tag.query.all()
    return render_template("edit_post.html", post=post, tags=tags)


@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def submit_edit_post(post_id):
    """edits a post from form data"""
    post = Post.query.get(post_id)
    title = request.form["title"]
    content = request.form["content"]
    post.title = title
    post.content = content
    tags = request.form.getlist("tags")
    post.tags = []
    for tag_id in tags:
        tag = Tag.query.get(tag_id)
        post.tags.append(tag)
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


@app.route("/tags/new")
def show_tag_form():
    """Shows new tag form"""
    return render_template("tag_form.html")


@app.route("/tags/new", methods=["POST"])
def create_new_tag():
    """creates new tag from /tags/new"""
    name = request.form["name"]
    new_tag = Tag(name=name)
    db.session.add(new_tag)
    db.session.commit()
    tag = Tag.query.filter(Tag.name == name).one()
    return redirect(f"/tags/{tag.id}")


@app.route("/tags/<int:tag_id>")
def show_tag_details(tag_id):
    """shows tag details"""
    tag = Tag.query.get(tag_id)
    return render_template("tag.html", tag=tag)


@app.route("/tags")
def show_tags():
    """lists all tags"""
    tags = Tag.query.all()
    return render_template("list_tag.html", tags=tags)


@app.route("/tags/<int:tag_id>/edit")
def show_edit_tag(tag_id):
    """shows edit tag form"""
    tag = Tag.query.get(tag_id)
    return render_template("edit_tag.html", tag=tag)


@app.route("/tags/<int:tag_id>/edit", methods=["POST"])
def edit_tag(tag_id):
    """edits tag of tag_id"""
    tag_name = request.form["name"]
    tag = Tag.query.get(tag_id)
    tag.name = tag_name
    db.session.add(tag)
    db.session.commit()
    return redirect(f"/tags/{tag.id}")


@app.route("/tags/<int:tag_id>/delete", methods=["POST"])
def delete_tag(tag_id):
    """deletes tag from tag_id"""
    tag = Tag.query.get(tag_id)
    db.session.delete(tag)
    db.session.commit()
    return redirect("/tags")
