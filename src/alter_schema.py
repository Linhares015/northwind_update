# src/alter_schema.py
import os
from sqlalchemy import create_engine, inspect, text
from dotenv import load_dotenv

load_dotenv()  # carrega DB_URL de .env
DB_URL = os.getenv("DB_URL")
engine = create_engine(DB_URL)
inspector = inspect(engine)


def alter_schema(tables_to_alter=None):
    """
    Garante que cada tabela em tables_to_alter tenha colunas 'id' (serial)
    e 'updated_at' (timestamp com default CURRENT_TIMESTAMP).
    """
    if tables_to_alter is None:
        tables_to_alter = ["customers", "orders"]

    with engine.begin() as conn:
        for table in tables_to_alter:
            cols = [col_info["name"] for col_info in inspector.get_columns(table)]

            # Adiciona coluna 'id' se não existir (sem tornar PK para não conflitar)
            if "id" not in cols:
                print(f"Adicionando coluna 'id' em '{table}'...")
                conn.execute(text(
                    f"ALTER TABLE {table} ADD COLUMN id SERIAL"
                ))
            else:
                print(f"Tabela '{table}' já possui coluna 'id'.")

            # Adiciona coluna 'updated_at' se não existir
            if "updated_at" not in cols:
                print(f"Adicionando coluna 'updated_at' em '{table}'...")
                conn.execute(text(
                    f"ALTER TABLE {table} ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
                ))
            else:
                print(f"Tabela '{table}' já possui coluna 'updated_at'.")

    print("Alterações de schema concluídas.")
