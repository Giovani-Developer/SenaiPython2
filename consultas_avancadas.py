## Consultas complexas com filtros e JOIN
from app import app
from models import Cliente, Pedido, Produto

if __name__ == "__main__":
    with app.app_context():
        # JOIN automático via relacionamento
        print("▶ JOIN Cliente x Pedido (nome, total):")
        rows = Pedido.query.join(Cliente).add_columns(Cliente.nome, Pedido.valor_total).all()
        for _, nome, total in rows:
            print(" -", nome, total)

        # Filtros compostos
        print("\n▶ Produtos caros (preco > 1000) com estoque > 0:")
        caros = Produto.query.filter(Produto.preco > 1000, Produto.estoque > 0).all()
        for p in caros:
            print(" -", p.nome, p.preco, "estoque:", p.estoque)

        # Ordenação e limite
        print("\n▶ Últimos 5 clientes:")
        ultimos = Cliente.query.order_by(Cliente.id.desc()).limit(5).all()
        for c in ultimos:
            print(" -", c.id, c.nome)
