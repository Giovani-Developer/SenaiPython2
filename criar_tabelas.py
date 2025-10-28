## Executar uma vez para criar as tabelas no PostgreSQL
from app import app, db
from models import *  # garante que TODOS os models estejam carregados

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        print("✅ Tabelas criadas com sucesso!")