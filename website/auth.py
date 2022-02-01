from unicodedata import category
from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from .models import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password, password):
                flash('Logado!', category='success')
                login_user(user, remember=True)

                return redirect(url_for('views.home'))
            else:
                flash('Senha incorreta!', category='error')
        else:
            flash('Email não existe!', category='error')

    return render_template('auth/login.html', user=current_user)


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        email_exists = User.query.filter_by(email=email).first()
        username_exists = User.query.filter_by(username=username).first()

        if username_exists:
            flash('Nome de usuário já cadastrado!', category='error')
        elif email_exists:
            flash('Email já cadastrado!', category='error')
        elif password1 != password2:
            flash('Senhas informadas não conferem!', category='error')
        elif len(username) < 2:
            flash('Nome de usuário muito curto!', category='error')
        elif len(email) < 4:
            flash('Email inválido!', category='error')
        elif len(password1) < 6:
            flash('Senha muito curta!', category='error')
        else:
            new_user = User(username=username, email=email, password=generate_password_hash(password1, method='sha256'))

            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)

            flash('Usuário cadastrado com sucesso!', category='success')

            return redirect(url_for('views.home'))

    return render_template('auth/signup.html', user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.home'))
