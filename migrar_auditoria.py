
from app import app, db
from sqlalchemy import text

SQL = """
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM information_schema.tables WHERE table_name='audit_logs'
  ) THEN
    CREATE TABLE audit_logs (
      id SERIAL PRIMARY KEY,
      action VARCHAR(10) NOT NULL,
      entity VARCHAR(80) NOT NULL,
      entity_pk VARCHAR(120) NOT NULL,
      user_id INTEGER NULL,
      ip VARCHAR(64) NULL,
      created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
      changes JSONB NULL
    );
    CREATE INDEX IF NOT EXISTS idx_audit_logs_created_at ON audit_logs(created_at);
    CREATE INDEX IF NOT EXISTS idx_audit_logs_entity ON audit_logs(entity);
    CREATE INDEX IF NOT EXISTS idx_audit_logs_user ON audit_logs(user_id);
  END IF;
END$$;
"""

with app.app_context():
    db.session.execute(text(SQL))
    db.session.commit()
    print("✅ Tabela de auditoria verificada/criada.")
