from flask import render_template, url_for, flash, redirect, request, Blueprint, current_app
from flask_login import login_user, current_user, logout_user, login_required
from main import db, bcrypt
from main.models.users import Users
from main.Auth.forms import RegistractionForm, LoginForm, UpdateAccountForm


from main.Auth.utils import save_picture

auth = Blueprint('auth', __name__)


@auth.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistractionForm()

    if current_user.is_authenticated: # type: ignore
        return redirect(url_for("home.home"))

    if form.validate_on_submit():

        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        user = Users(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('auth.login'))

    return render_template("register.html", title="Register", form=form)



@auth.route("/login", methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated: # type: ignore
        return redirect(url_for("home.home"))


    form = LoginForm()

    if form.validate_on_submit():

        user = Users.query.filter_by(email=form.email.data).first()
        
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)

            next_page = request.args.get('next')

            return redirect(next_page) if next_page else redirect(url_for('home.home'))
        
        else:
            flash('login unsuccessful check your data', 'danger')

    return render_template("login.html", title="Login", form=form)



@auth.route("/account", methods=['GET', 'POST'])
@login_required
def account():

    form = UpdateAccountForm()

    if form.validate_on_submit():
        
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
           
            current_user.img_file = picture_file

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('your account has been updated', 'success')
        return redirect(url_for('auth.account'))
    
    elif request.method == 'GET':
        form.username.data = current_user.username # type: ignore
        form.email.data = current_user.email  # type: ignore

    img_file = url_for('static', filename='profile_pics/'+current_user.img_file) # type: ignore

    return render_template("account.html", title='account', img_file=img_file, form=form)


@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home.home'))