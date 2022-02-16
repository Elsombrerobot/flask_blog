from flask import Blueprint
from flask import render_template, url_for, flash, redirect, request
from flaskblog.users.forms import (RegistrationForm, LoginForm,
                             UpdateAccountForm, RequestResetForm, ResetPasswordForm)
from flaskblog import bcrypt
from flaskblog.models import Post, User
from flaskblog.users.utils import save_picture, delete_picture, generate_profile_picture, send_reset_email
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog.db_client import db_users


users = Blueprint("users", __name__)

@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        image_file = generate_profile_picture(form.username.data)
        db_users.create(username=form.username.data, email=form.email.data, password=hashed_password, image_file=image_file)
        flash('Your account has been created! Your are now able to log in.', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("main.home"))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.home"))

@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    if request.form.get('image_reset'):
        delete_picture(current_user.image_file)
        image_file = generate_profile_picture(current_user.username)
        db_users.update(current_user, image_file=image_file)
        flash('Your profile image has been updated!', 'success')
        return redirect(url_for('users.account'))
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            delete_picture(current_user.image_file)
            db_users.update(current_user, image_file=picture_file)
        db_users.update(current_user, username = form.username.data, email = form.email.data)
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username       
        form.email.data = current_user.email 
    return render_template("account.html", title="Account", form=form)


@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)

@users.route("/reset_password/<string:token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    user = User.verify_reset_token(token)
    if not user:
        flash("This is an invalid or expired token.", "warning")
        return redirect(url_for("users.reset_request"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        db_users.update(user=user, password=hashed_password)
        flash('Your password has been updated ! You are now able to login', 'success')
        return redirect(url_for('users.login'))
    return render_template("reset_token.html", title="Reset password", form=form)

@users.route("/home/<string:username>")
def user_posts(username):
    page = request.args.get("page", 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
            .order_by(Post.date_posted.desc())\
            .paginate(page=page, per_page=5)

    return render_template("user_posts.html", posts=posts, user=user)