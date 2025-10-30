from app import app, db
from models import User, Role

with app.app_context():
    admin_role = Role.query.filter_by(name="admin").first()
    if not admin_role:
        admin_role = Role(name="admin")
        db.session.add(admin_role)

    email = "admin@admin.com"
    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(email=email)
        user.set_password("123456")
        user.roles.append(admin_role)
        db.session.add(user)

    db.session.commit()
    print("Usuário admin criado com sucesso!")
