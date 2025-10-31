from app import app, db
from models import User, Role

def ensure_role(name):
    r = Role.query.filter_by(name=name).first()
    if not r:
        r = Role(name=name)
        db.session.add(r)
        db.session.flush()
    return r

def ensure_user(email, password, roles):
    u = User.query.filter_by(email=email).first()
    if not u:
        u = User(email=email)
        u.set_password(password)
        db.session.add(u)
        db.session.flush()
    # sincroniza roles
    u.roles.clear()
    for r in roles:
        u.roles.append(r)
    return u

with app.app_context():
    admin = ensure_role("admin")
    operador = ensure_role("operador")
    leitor = ensure_role("leitor")

    ensure_user("admin@admin.com", "123456", [admin])
    ensure_user("operador@admin.com", "123456", [operador])
    ensure_user("leitor@admin.com", "123456", [leitor])

    db.session.commit()
    print("✅ Usuários criados:")
    print(" - admin@admin.com / 123456 (admin)")
    print(" - operador@admin.com / 123456 (operador)")
    print(" - leitor@admin.com / 123456 (leitor)")
