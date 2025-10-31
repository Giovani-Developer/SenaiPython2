from app import app, db
from sqlalchemy import text

SQL = """
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1
    FROM information_schema.columns
    WHERE table_name='pedidos' AND column_name='data_criacao'
  ) THEN
    ALTER TABLE pedidos
      ADD COLUMN data_criacao TIMESTAMPTZ NOT NULL DEFAULT NOW();
    CREATE INDEX IF NOT EXISTS idx_pedidos_data_criacao ON pedidos(data_criacao);
  END IF;
END$$;
"""

with app.app_context():
    db.session.execute(text(SQL))
    db.session.commit()
    print("✅ Coluna data_criacao adicionada (ou já existia).")