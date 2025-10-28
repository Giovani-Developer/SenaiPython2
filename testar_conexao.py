from app import db, app

with app.app_context():
    try:
        db.session.execute(db.text("SELECT version();"))
        print("✅ Conexão com o PostgreSQL funcionando!")
    except Exception as e:
        print("❌ Erro ao conectar:", e)