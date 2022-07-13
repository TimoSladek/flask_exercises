from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from project.models import User
from project import db, oauth, twitter
from project.users.forms import UserForm, DeleteForm, LoginForm
from sqlalchemy.exc import IntegrityError
from project.decorators import prevent_login_signup, ensure_correct_user
from flask_login import login_user, logout_user, login_required

users_blueprint = Blueprint(
    'users',
    __name__,
    template_folder='templates'
)


@users_blueprint.route('/')
@login_required
def index():
    delete_form = DeleteForm()
    return render_template('users/index.html', users=User.query.all(), delete_form=delete_form)


@users_blueprint.route('/', methods=["POST"])
@prevent_login_signup
def signup():
    form = UserForm(request.form)
    if form.validate():
        try:
            new_user = User(
                form.first_name.data,
                form.last_name.data,
                form.img_url.data,
                form.username.data,
                form.password.data,
                form.email.data)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            flash('User Created!')
            return redirect(url_for('users.index'))
        except IntegrityError:
            flash('Username or email taken!')
            return render_template('users/new.html', form=form)
    return render_template('new.html', form=form)


@users_blueprint.route('/login', methods=["GET", "POST"])
@prevent_login_signup
def login():
    login_form = LoginForm(request.form)
    if request.method == "POST":
        if login_form.validate():
            authenticated_user = User.authenticate(login_form.email.data, login_form.password.data)
            if authenticated_user:
                login_user(authenticated_user)
                flash('You are logged in!')
                return redirect(url_for('users.index'))
            else:
                flash('Invalid credentials')
                return redirect(url_for('users.login'))
    return render_template('users/login.html', form=login_form)


@users_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out!')
    return redirect(url_for('users.login'))


@users_blueprint.route('/new')
@prevent_login_signup
def new():
    user_form = UserForm()
    return render_template('users/new.html', form=user_form)


@users_blueprint.route('/<int:id>/edit')
@login_required
@ensure_correct_user
def edit(id):
    found_user = User.query.get_or_404(id)
    user_form = UserForm(obj=found_user)
    return render_template('users/edit.html', user=found_user, form=user_form)


@users_blueprint.route('/<int:id>', methods=["GET", "POST"])
@login_required
@ensure_correct_user
def show(id):
    found_user = User.query.get_or_404(id)
    if request.method == "POST":
        if request.form['method'] == "PATCH":
            form = UserForm(request.form)
            if form.validate():
                found_user.first_name = form.first_name.data
                found_user.last_name = form.last_name.data
                found_user.img_url = form.img_url.data
                db.session.add(found_user)
                db.session.commit()
                flash('User Updated!')
                return redirect(url_for('users.index'))
            else:
                return render_template('edit.html', user=found_user, form=form)
        elif request.form['method'] == "DELETE":
            delete_form = DeleteForm(request.form)
            if delete_form.validate():
                db.session.delete(found_user)
                db.session.commit()
                logout_user()
                flash('User Deleted!')
                return redirect(url_for('users.index'))
            else:
                return redirect(url_for('index'))
    return render_template('users/show.html', user=found_user)


@users_blueprint.route('/oauth')
def oauth():
    return twitter.authorize(callback=url_for('users.oauth_authorized',
                                              next=request.args.get('next') or request.referrer or None))


@users_blueprint.route('/auth/twitter/callback')
@twitter.authorized_handler
def oauth_authorized(resp):
    next_url = request.args.get('next') or url_for('users.oauth_login')
    if resp is None:
        flash(u'You denied the request to sign in.')
        return redirect(next_url)

    session['twitter_token'] = (
        resp['oauth_token'],
        resp['oauth_token_secret']
    )
    session['twitter_user'] = resp['screen_name']

    return redirect(next_url)


@users_blueprint.route('/oauth-login')
def oauth_login():
    user_exists = User.query.filter_by(username=session['twitter_user']).first()
    if user_exists:
        login_user(user_exists)
        flash('You are logged in!')
    else:
        new_user = User(session['twitter_user'])
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        flash('User Created!')
    return redirect(url_for('users.index'))


@twitter.tokengetter
def get_twitter_token(token=None):
    return session.get('twitter_token')

