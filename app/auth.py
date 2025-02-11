from flask import Blueprint, redirect, url_for, render_template, flash, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from .model.user_model import User
from . import db
from werkzeug.security import check_password_hash

auth = Blueprint('auth', __name__)

@auth.route('/auth', methods=['GET', 'POST'])
def authentification():
    if request.method == 'POST':
        if 'login' in request.form:
            email = request.form['email']
            password = request.form['password']
            user = User.query.filter_by(email=email).first()

            if not user:
                flash('Aucun compte trouvé avec cet email.', 'error')
            elif not check_password_hash(user.password_hash, password):
                flash('Mot de passe incorrect.', 'error')
            else:
                login_user(user)
                flash('Connexion réussie !', 'success')
                return redirect(url_for('main.index'))

        elif 'register' in request.form:
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']

            if not username or not email or not password:
                flash('Tous les champs sont obligatoires.', 'error')
            elif User.query.filter_by(username=username).first():
                flash('Ce nom d\'utilisateur est déjà pris.', 'error')
            elif User.query.filter_by(email=email).first():
                flash('Un compte avec cet email existe déjà.', 'error')
            else:
                user = User(username=username, email=email)
                user.set_password(password)
                db.session.add(user)
                db.session.commit()
                flash('Compte créé avec succès ! Vous pouvez maintenant vous connecter.', 'success')
                return redirect(url_for('auth.authentification'))

    return render_template('auth.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))