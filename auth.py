from flask import render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from app import app, db
from models import User, Role
from functools import wraps
from flask_login import current_user
from flask import redirect, url_for, flash
from functools import wraps
from flask_login import current_user
from flask import redirect, url_for, flash

login_manager = LoginManager(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        pwd = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(pwd):
            login_user(user)
            flash("Bem-vindo(a)!", "success")
            return redirect(url_for("home"))
        flash("Credenciais inválidas.", "error")
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Sessão encerrada.", "success")
    return redirect(url_for("login"))


def role_required(*roles):
    """
    Ex.: @role_required("admin") ou @role_required("admin", "operador")
    """
    def deco(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated:
                flash("Faça login para continuar.", "error")
                return redirect(url_for("login"))
            if "admin" in roles and hasattr(current_user, "has_role") and current_user.has_role("admin"):
                return fn(*args, **kwargs)
            # qualquer outro papel listado
            for r in roles:
                if hasattr(current_user, "has_role") and current_user.has_role(r):
                    return fn(*args, **kwargs)
            flash("Você não tem permissão para acessar esta página.", "error")
            return redirect(url_for("home"))
        return wrapper
    return deco
