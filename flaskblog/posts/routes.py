from flask import Blueprint
from flask import abort, render_template, url_for, flash, redirect, request
from flaskblog.posts.forms import PostForm
from flaskblog.models import Post
from flask_login import current_user, login_required
from flaskblog.db_client import db_posts

posts = Blueprint("posts", __name__)

@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        db_posts.create(title=form.title.data, content=form.content.data, author=current_user)
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template("create_post.html", title="New post", form=form, legend='New post')

@posts.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        db_posts.update(post, title=form.title.data, content=form.content.data)
        flash('Your post has been updated', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == "GET":
        form.title.data = post.title
        form.content.data = post.content
    return render_template("create_post.html", title="Update post", form=form, legend='Update post')

@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db_posts.remove(post)
    flash('Your post has been deleted.', 'success')
    return redirect(url_for("main.home"))