## Aqui ficam todas as classes que representam as tabelas

from __future__ import annotations
from decimal import Decimal
from app import db
from datetime import datetime

# Tabela associativa N:N Produto ↔ Fornecedor
produtos_fornecedores = db.Table(
    "produtos_fornecedores",
    db.Column("produto_id", db.Integer, db.ForeignKey("produtos.id"), primary_key=True),
    db.Column("fornecedor_id", db.Integer, db.ForeignKey("fornecedores.id"), primary_key=True),
)

class Cliente(db.Model):
    __tablename__ = "clientes"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True)
    telefone = db.Column(db.String(20))
    ativo = db.Column(db.Boolean, default=True)
    pedidos = db.relationship("Pedido", backref="cliente", lazy=True)

    def __repr__(self) -> str:
        return f"<Cliente {self.id} {self.nome}>"

class Categoria(db.Model):
    __tablename__ = "categorias"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(60), unique=True, nullable=False)
    produtos = db.relationship("Produto", backref="categoria", lazy=True)

    def __repr__(self) -> str:
        return f"<Categoria {self.id} {self.nome}>"

class Produto(db.Model):
    __tablename__ = "produtos"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Numeric(10, 2), nullable=False)
    estoque = db.Column(db.Integer, default=0)
    categoria_id = db.Column(db.Integer, db.ForeignKey("categorias.id"))

    fornecedores = db.relationship(
        "Fornecedor",
        secondary=produtos_fornecedores,
        backref="produtos",
        lazy="joined",
    )

    def __repr__(self) -> str:
        return f"<Produto {self.id} {self.nome} R${self.preco}>"

class Fornecedor(db.Model):
    __tablename__ = "fornecedores"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)

    def __repr__(self) -> str:
        return f"<Fornecedor {self.id} {self.nome}>"

class Pedido(db.Model):
    __tablename__ = "pedidos"
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey("clientes.id"), nullable=False)
    valor_total = db.Column(db.Numeric(10, 2), default=0)
    status = db.Column(db.String(20), default="aberto")

    itens = db.relationship(
        "ItemPedido",
        backref="pedido",
        lazy=True,
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Pedido {self.id} cliente={self.cliente_id} total={self.valor_total}>"

class ItemPedido(db.Model):
    __tablename__ = "itens_pedido"
    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey("pedidos.id"), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey("produtos.id"), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    preco_unitario = db.Column(db.Numeric(10, 2), nullable=False)

    produto = db.relationship("Produto")

    def subtotal(self) -> Decimal:
        return Decimal(self.quantidade) * Decimal(self.preco_unitario)

    def __repr__(self) -> str:
        return f"<ItemPedido {self.id} pedido={self.pedido_id} produto={self.produto_id}>"
    

class Arquivo(db.Model):
    __tablename__ = "arquivos"
    id = db.Column(db.Integer, primary_key=True)
    nome_original = db.Column(db.String(255), nullable=False)
    nome_armazenado = db.Column(db.String(255), nullable=False, unique=True)
    caminho = db.Column(db.String(512), nullable=False)
    mimetype = db.Column(db.String(120))
    tamanho_bytes = db.Column(db.Integer)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<Arquivo {self.id} {self.nome_original}>"


from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

user_roles = db.Table(
    "user_roles",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id"), primary_key=True),
    db.Column("role_id", db.Integer, db.ForeignKey("roles.id"), primary_key=True),
)

class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=True, nullable=False)

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean, default=True)
    roles = db.relationship("Role", secondary=user_roles, backref="users")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def has_role(self, role_name: str) -> bool:
        return any(r.name == role_name for r in self.roles)