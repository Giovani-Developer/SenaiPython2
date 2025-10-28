## Aqui ficam todas as classes que representam as tabelas

from __future__ import annotations
from decimal import Decimal
from app import db

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