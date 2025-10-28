## Arquivo central do projeto.
## Ele apenas inicializa o Flask e conecta ao PostgreSQL

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from conexao_bd import conectarSQLAlchemy

app = Flask(__name__)
app.config["SECRET_KEY"] = "dev-secret"  # necessário se usar flash nas rotas
app.config["SQLALCHEMY_DATABASE_URI"] = conectarSQLAlchemy()
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
