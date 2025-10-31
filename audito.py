from sqlalchemy import event, inspect
from app import db
from models import AuditLog, Cliente, Produto, Categoria, Fornecedor, Pedido, ItemPedido, Arquivo

WATCHED = (Cliente, Produto, Categoria, Fornecedor, Pedido, ItemPedido, Arquivo)

def _dump_columns(obj):
    data = {}
    mapper = inspect(obj).mapper
    for col in mapper.columns:
        name = col.key
        try:
            val = getattr(obj, name)
        except Exception:
            val = None
        # serializa Decimals e afins
        if hasattr(val, "quantize"):
            val = float(val)
        data[name] = val
    return data

def _changes_dict(state):
    """Retorna apenas campos alterados: {campo: [antes, depois]}"""
    changes = {}
    for attr in state.attrs:
        hist = attr.load_history()
        if hist.has_changes():
            before = hist.deleted[0] if hist.deleted else None
            after = hist.added[0] if hist.added else None
            # normaliza Decimal
            if hasattr(before, "quantize"): before = float(before)
            if hasattr(after, "quantize"):  after = float(after)
            # evita ruído de relacionamento
            if attr.key and not hasattr(after, "__dict__"):
                changes[attr.key] = [before, after]
    return changes

# Guardar snapshot de objetos que serão deletados (antes do flush)
@event.listens_for(db.session.__class__, "before_flush")
def before_flush(session, flush_context, instances):
    if not hasattr(session, "_to_audit_deleted"):
        session._to_audit_deleted = []
    session._to_audit_deleted.clear()
    for obj in session.deleted:
        if isinstance(obj, WATCHED):
            state = inspect(obj)
            pk = str(state.identity[0]) if state.identity else "?"
            session._to_audit_deleted.append((
                obj.__class__.__name__, pk, _dump_columns(obj)
            ))

@event.listens_for(db.session.__class__, "after_flush")
def after_flush(session, flush_context):
    user_id = session.info.get("user_id")
    ip = session.info.get("ip")

    # INSERTS
    for obj in session.new:
        if isinstance(obj, WATCHED):
            state = inspect(obj)
            pk = str(state.identity[0]) if state.identity else "?"
            entry = AuditLog(
                action="INSERT",
                entity=obj.__class__.__name__,
                entity_pk=pk,
                user_id=user_id,
                ip=ip,
                changes={"after": _dump_columns(obj)}
            )
            session.add(entry)

    # UPDATES
    for obj in session.dirty:
        if isinstance(obj, WATCHED):
            state = inspect(obj)
            if not state.has_identity or not session.is_modified(obj, include_collections=False):
                continue
            pk = str(state.identity[0]) if state.identity else "?"
            changes = _changes_dict(state)
            if changes:
                entry = AuditLog(
                    action="UPDATE",
                    entity=obj.__class__.__name__,
                    entity_pk=pk,
                    user_id=user_id,
                    ip=ip,
                    changes=changes
                )
                session.add(entry)

    # DELETES (usando snapshot salvo no before_flush)
    for entity_name, pk, snapshot in getattr(session, "_to_audit_deleted", []):
        entry = AuditLog(
            action="DELETE",
            entity=entity_name,
            entity_pk=pk,
            user_id=user_id,
            ip=ip,
            changes={"before": snapshot}
        )
        session.add(entry)

def register_audit_listeners():
    # apenas importar este módulo já registra os event hooks
    return True

