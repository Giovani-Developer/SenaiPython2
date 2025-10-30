## Arquivo central do projeto.
## Ele apenas inicializa o Flask e conecta ao PostgreSQL

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from conexao_bd import conectarSQLAlchemy
import os
from pathlib import Path

app = Flask(__name__)
app.config["SECRET_KEY"] = "dev-secret"  # necessário se usar flash nas rotas
app.config["SQLALCHEMY_DATABASE_URI"] = conectarSQLAlchemy()
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_FOLDER = BASE_DIR / "uploads"
UPLOAD_FOLDER.mkdir(exist_ok=True)

# Configs Flask
app.config["UPLOAD_FOLDER"] = str(UPLOAD_FOLDER)
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024  # 10 MB por request (ajuste se quiser)





db = SQLAlchemy(app)
