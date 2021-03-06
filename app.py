"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///blogly_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "jordaniscool"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
debug = DebugToolbarExtension(app)

connect_db(app)

# running this in ipython creates the tables
db.create_all()


@app.route("/")
def redirect_to_all_users():
    """Redirects to list of users page"""
    return redirect("/users")


######## USER ROUTES #######################


@app.route("/users")
def list_users():
    """Display list of users in database"""

    users = User.query.all()
    return render_template("all_users.html", users=users)


@app.route("/users/new", methods=["GET"])
def show_new_user_page():
    """Create new user page"""
    return render_template("new_user_form.html")


@app.route("/users/new", methods=["POST"])
def create_user():
    """Creates user and redirects to home page"""
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"] or None

    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)

    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")


@app.route("/users/<int:user_id>")
def show_user(user_id):
    """Show info on a single user"""

    user = User.query.get_or_404(user_id)
    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template("details.html", user=user, posts=posts)


@app.route("/users/<int:user_id>/edit")
def show_edit_user(user_id):
    """Display edit user page"""

    user = User.query.get_or_404(user_id)
    return render_template("edit.html", user=user)


@app.route("/users/<int:user_id>/edit", methods=["POST"])
def edit_user(user_id):
    """Sends the form for editing an existing user"""

    user = User.query.get_or_404(user_id)
    user.first_name = request.form["first_name"]
    user.last_name = request.form["last_name"]
    user.image_url = request.form["image_url"]

    db.session.add(user)
    db.session.commit()

    return redirect("/users")


@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    """Delete the user"""

    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")


###########  POST ROUTES ############################


@app.route("/users/<int:user_id>/posts/new")
def show_new_post_form(user_id):
    """Displays the form for creating a new post"""
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template("new_post_form.html", user=user, tags=tags)


@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def add_new_post(user_id):
    """Sends the form for adding a post"""

    user = User.query.get_or_404(user_id)
    title = request.form["title"]
    content = request.form["content"]
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    # user=user due to foreign key (user_id in class User and class Post)
    new_post = Post(title=title, content=content, user=user, tags=tags)

    db.session.add(new_post)
    db.session.commit()
    # ADD FLASH MESSAGE HERE IN FUTURE

    return redirect(f"/users/{user.id}")


@app.route("/posts/<int:post_id>")
def show_post(post_id):
    """Display user's post"""

    post = Post.query.get_or_404(post_id)
    return render_template("post.html", post=post)


@app.route("/posts/<int:post_id>/edit")
def show_edit_post(post_id):
    """Display edit post page"""

    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    return render_template("edit_post_form.html", post=post, tags=tags)


@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def edit_post(post_id):
    """Sends the form for editing an existing post"""

    post = Post.query.get_or_404(post_id)
    post.title = request.form["title"]
    post.content = request.form["content"]

    tag_ids = [int(num) for num in request.form.getlist("tags")]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    db.session.add(post)
    db.session.commit()

    return redirect(f"/users/{post.user_id}")


@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    """Delete the post"""

    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()
    # ADD FLASH MESSAGE

    return redirect(f"/users/{post.user_id}")


################# TAG ROUTES ##################################


@app.route("/tags")
def show_tags():
    """Display list of tags"""

    tags = Tag.query.all()

    return render_template("list_tags.html", tags=tags)


@app.route("/tags/new")
def show_create_tag_form():
    """Display the form for creating a tag"""

    return render_template("create_tag.html")


@app.route("/tags/new", methods=["POST"])
def create_tag():
    """Handle form submission for creating a new tag"""

    post_ids = [int(num) for num in request.form.getlist("posts")]
    posts = Post.query.filter(Post.id.in_(post_ids)).all()
    new_tag = Tag(name=request.form["tag"], posts=posts)

    db.session.add(new_tag)
    db.session.commit()

    return redirect("/tags")


@app.route("/tags/<int:tag_id>")
def show_tag_details(tag_id):
    """Display details of tag"""

    tag = Tag.query.get_or_404(tag_id)

    return render_template("tag_details.html", tag=tag)


@app.route("/tags/<int:tag_id>/edit")
def tags_edit_form(tag_id):
    """Dsiplay a form to edit an existing tag"""

    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.all()
    return render_template("edit_tag.html", tag=tag, posts=posts)


@app.route("/tags/<int:tag_id>/edit", methods=["POST"])
def tags_edit(tag_id):
    """Handle form submission for updating an existing tag"""

    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form["name"]
    post_ids = [int(num) for num in request.form.getlist("posts")]
    tag.posts = Post.query.filter(Post.id.in_(post_ids)).all()

    db.session.add(tag)
    db.session.commit()

    return redirect("/tags")


@app.route("/tags/<int:tag_id>/delete", methods=["POST"])
def tags_destroy(tag_id):
    """Handle form submission for deleting an existing tag"""

    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()

    return redirect("/tags")