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
            if user:
                if check_password_hash(user.password_hash, password):
                    login_user(user)
                    return redirect(url_for('main.index'))
                else:
                    flash('Mot de passe incorrect.', 'error')
            else:
                flash('Aucun compte associé à cet email.', 'error')
        elif 'register' in request.form:
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']

            # Validation
            if not username or not email or not password:
                flash('Veuillez remplir tous les champs.', 'error')
                return redirect(url_for('auth.authentification'))

            if User.query.filter_by(username=username).first():
                flash('Ce nom d\'utilisateur est déjà pris.', 'error')
            elif User.query.filter_by(email=email).first():
                flash('Un compte avec cet email existe déjà.', 'error')
            else:
                user = User(username=username, email=email)
                user.set_password(password)
                db.session.add(user)
                db.session.commit()
                flash('Compte créé avec succès. Veuillez vous connecter.', 'success')
                return redirect(url_for('auth.authentification'))
    return render_template('auth.html')


# @auth.route('/check-email', methods=['POST'])
# def check_email():
#     email = request.json.get('email')
#     user = User.query.filter_by(email=email).first()
#     return jsonify(exists=bool(user))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))