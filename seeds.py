# Arquivo para adicionar Clientes, Produtos, Categorias e Fornecedores no direto no banco de dados via terminal
from app import app, db
from models import Cliente, Categoria, Produto, Fornecedor

if __name__ == "__main__":
    with app.app_context():
        print("🧹 Limpando e recriando tabelas...")
        db.drop_all()
        db.create_all()

        # Clientes
        clientes = [
            Cliente(nome="João Silva", email="joao@email.com"),
            Cliente(nome="Maria Souza", email="maria@email.com"),
            Cliente(nome="Carlos Pereira", email="carlos@email.com"),
        ]
        db.session.add_all(clientes)
        print("👥 Clientes adicionados.")

        # Categorias
        cat1 = Categoria(nome="Informática")
        cat2 = Categoria(nome="Móveis")
        cat3 = Categoria(nome="Eletrodomésticos")
        db.session.add_all([cat1, cat2, cat3])
        db.session.flush()
        print("📂 Categorias criadas.")

        # Produtos
        produtos = [
            Produto(nome="Notebook Dell", preco=3500.00, estoque=10, categoria=cat1),
            Produto(nome="Mouse Sem Fio", preco=120.00, estoque=40, categoria=cat1),
            Produto(nome="Cadeira Gamer", preco=1500.00, estoque=6, categoria=cat2),
            Produto(nome="Mesa de Escritório", preco=700.00, estoque=5, categoria=cat2),
            Produto(nome="Cafeteira Elétrica", preco=300.00, estoque=12, categoria=cat3),
        ]
        db.session.add_all(produtos)
        db.session.flush()
        print("📦 Produtos cadastrados.")

        # Fornecedores
        f1 = Fornecedor(nome="Tech Distribuidora")
        f2 = Fornecedor(nome="Moveis BR")
        db.session.add_all([f1, f2])
        db.session.flush()

        # Relacionamentos N:N
        produtos[0].fornecedores.append(f1)  # Notebook -> Tech
        produtos[1].fornecedores.append(f1)  # Mouse -> Tech
        produtos[2].fornecedores.append(f2)  # Cadeira -> Moveis BR
        produtos[3].fornecedores.append(f2)  # Mesa -> Moveis BR
        produtos[4].fornecedores.append(f1)  # Cafeteira -> Tech

        db.session.commit()
        print("🤝 Fornecedores e relações adicionadas.")
        print("✅ Banco populado com sucesso!")
