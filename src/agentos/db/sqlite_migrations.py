"""SQLite-compatible migration scripts for AgentOS.

Ported from the PostgreSQL migrations in ../migrations/. Key adaptations:
- uuid primary key with default: use Python-generated UUIDs or lower(hex(randomblob(16)))
- timestamp with time zone → datetime (stored as ISO string)
- jsonb → text (JSON serialized)
- serial → integer primary key autoincrement
- create extension pgcrypto → removed
- gen_random_uuid() → lower(hex(randomblob(16)))
- numeric(p,s) → real (floating point)
- varchar(n) → text (SQLite is type-flexible)
- partial indexes (WHERE clause) → not supported; use regular indexes
- ON CONFLICT DO NOTHING → INSERT OR IGNORE
- RETURNING clause → not supported; use last_insert_rowid() or re-query
- CREATE INDEX ... WHERE → removed (use application-level filtering)
"""
import re
from pathlib import Path


def port_sql(pg_sql: str, migration_name: str) -> str:
    """Port a single PostgreSQL migration to SQLite-compatible SQL."""
    sql = pg_sql

    # Remove `create extension if not exists pgcrypto;`
    sql = re.sub(r'create\s+extension\s+if\s+not\s+exists\s+pgcrypto;\s*\n?', '', sql, flags=re.IGNORECASE)

    # Replace gen_random_uuid() with lower(hex(randomblob(16)))
    sql = sql.replace('gen_random_uuid()', 'lower(hex(randomblob(16)))')

    # Replace timestamp with time zone → datetime
    sql = re.sub(r'timestamp\s+with\s+time\s+zone', 'datetime', sql, flags=re.IGNORECASE)
    sql = re.sub(r'timestamptz', 'datetime', sql, flags=re.IGNORECASE)

    # Replace jsonb → text
    sql = sql.replace('jsonb', 'text')
    sql = sql.replace("'{}'::jsonb", "'{}'")
    sql = sql.replace("::jsonb", "")

    # Replace serial → integer primary key autoincrement
    sql = re.sub(r'\bserial\b', 'integer primary key autoincrement', sql, flags=re.IGNORECASE)

    # Replace numeric(p,s) → real
    sql = re.sub(r'\bnumeric\s*\(\s*\d+\s*,\s*\d+\s*\)', 'real', sql, flags=re.IGNORECASE)

    # Replace varchar(n) → text (SQLite doesn't enforce length)
    sql = re.sub(r'\bvarchar\s*\(\s*\d+\s*\)', 'text', sql, flags=re.IGNORECASE)

    # Replace bigint → integer (SQLite doesn't have bigint)
    sql = re.sub(r'\bbigint\b', 'integer', sql, flags=re.IGNORECASE)

    # Remove GENERATED ALWAYS AS IDENTITY (PostgreSQL-specific)
    sql = re.sub(r'\s+generated\s+always\s+as\s+identity[^,)*]*', '', sql, flags=re.IGNORECASE)

    # Handle uuid type - SQLite accepts it but stores as text; keep for compatibility
    # Replace uuid → text for strict SQLite compatibility
    sql = re.sub(r'\buuid\b', 'text', sql, flags=re.IGNORECASE)

    # Handle RETURNING clauses - remove them (SQLite doesn't support RETURNING in INSERT)
    # We'll handle version assignment in application code
    sql = re.sub(r'\s+returning\s+[^;]+', '', sql, flags=re.IGNORECASE)

    # Handle partial indexes (CREATE INDEX ... WHERE ...)
    # SQLite doesn't support partial indexes; convert to regular indexes
    partial_idx = re.search(
        r'create\s+(?:unique\s+)?index\s+\w+\s+on\s+\w+\s*\([^)]+\)\s*where\s+[^(]+',
        sql, re.IGNORECASE
    )
    if partial_idx:
        # Extract the index definition and remove the WHERE clause
        idx_sql = partial_idx.group(0)
        idx_sql = re.sub(r'\s+where\s+[^(]+;?\s*$', ';', idx_sql, flags=re.IGNORECASE)
        sql = sql[:partial_idx.start()] + idx_sql + sql[partial_idx.end():]

    # Handle ON CONFLICT DO NOTHING → INSERT OR IGNORE for unique constraints
    # This is handled at the application level for most cases

    # Handle default now() → datetime('now')
    sql = sql.replace("default now()", "default datetime('now')")
    sql = sql.replace("DEFAULT now()", "DEFAULT datetime('now')")

    # Handle INSERT into db_migrations with returning
    # Remove RETURNING from migration insert
    sql = re.sub(r'insert\s+into\s+db_migrations.*?returning[^;]+',
                 'insert into db_migrations (version) values (?)', sql, flags=re.IGNORECASE)

    # Handle information_schema queries → sqlite_master
    # This is handled in migrations.py dump() function

    # Handle format_type(atttypid, atttypmod) → just use type from pragma
    # This is handled in migrations.py dump() function

    # Handle pg_get_expr → removed (handled in dump)
    sql = re.sub(r"pg_get_expr\([^)]+\)", "''", sql, flags=re.IGNORECASE)

    # Handle ::regclass → cast to text
    sql = sql.replace("::regclass", "''")

    # Handle set statement_timeout → not needed in SQLite
    sql = re.sub(r'set\s+statement_timeout.*;', '', sql, flags=re.IGNORECASE)

    # Remove PostgreSQL-specific functions (plpgsql)
    # These are used for triggers and checks that don't translate to SQLite
    sql = re.sub(
        r'create\s+or\s+replace\s+function\s+\w+\s*\([^)]*\)\s*'
        r'returns\s+(?:trigger|[^ ]+)\s+language\s+\w+\s+as\s+'
        r'\$\$.*?\$\$;',
        '', sql, flags=re.IGNORECASE | re.DOTALL
    )

    # Remove PostgreSQL-specific triggers
    sql = re.sub(
        r'create\s+trigger\s+\w+\s+[^;]+;',
        '', sql, flags=re.IGNORECASE | re.DOTALL
    )

    # Remove PostgreSQL GRANT statements
    sql = re.sub(
        r'grant\s+[^;]+;',
        '', sql, flags=re.IGNORECASE
    )

    # Flatten CHECK constraints with multi-line value lists
    # SQLite requires CHECK constraints on a single line or with proper continuation
    sql = re.sub(
        r'check\s*\([^)]*\)',
        lambda m: m.group(0).replace('\n', ' ').strip(),
        sql,
        flags=re.IGNORECASE
    )

    # Remove comment-only lines that reference PostgreSQL features
    lines = sql.split('\n')
    lines = [l for l in lines if not l.strip().startswith('--') or
             'append-only' not in l.lower() or 'trigger' in l.lower()]
    sql = '\n'.join(lines)

    # Clean up extra blank lines
    sql = re.sub(r'\n{3,}', '\n\n', sql)

    return sql.strip() + "\n"


def port_all_migrations(source_dir: Path, dest_dir: Path) -> None:
    """Port all PostgreSQL migrations to SQLite-compatible SQL."""
    dest_dir.mkdir(parents=True, exist_ok=True)

    migration_files = sorted(source_dir.glob("V*.sql"))
    for src in migration_files:
        pg_sql = src.read_text(encoding="utf-8")
        sqlite_sql = port_sql(pg_sql, src.name)
        dest = dest_dir / src.name
        dest.write_text(sqlite_sql, encoding="utf-8")
        print(f"Ported {src.name} → {dest.name}")


if __name__ == "__main__":
    src = Path(__file__).resolve().parent.parent.parent / "migrations"
    dst = Path(__file__).resolve().parent / "sqlite_migrations"
    port_all_migrations(src, dst)
    print(f"\nPorted {len(list(src.glob('V*.sql')))} migrations to {dst}")
