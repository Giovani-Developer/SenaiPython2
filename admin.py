from flask_admin import Admin
import admin
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from app import app, db
from models import Cliente, Produto, Categoria, Fornecedor, Pedido, ItemPedido, Arquivo, User, Role

class SecureModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.has_role("admin")
    def inaccessible_callback(self, name, **kwargs):
        from flask import redirect, url_for, flash
        flash("Acesso restrito ao administrador.", "error")
        return redirect(url_for("login"))

admin = Admin(app, name="Painel Administrativo")

for model in [Cliente, Produto, Categoria, Fornecedor, Pedido, ItemPedido, Arquivo, User, Role]:
    admin.add_view(SecureModelView(model, db.session))


class SecureModelView(ModelView):
    def is_accessible(self):
        try:
            return current_user.is_authenticated and current_user.has_role("admin")
        except Exception:
            return False
    def inaccessible_callback(self, name, **kwargs):
        from flask import redirect, url_for, flash
        flash("Acesso restrito ao administrador.", "error")
        return redirect(url_for("login"))
		
# ✅ Removido template_mode para evitar o TypeError
#admin = Admin(app, name="Painel Administrativo")

