# main.py
from src.alter_schema import alter_schema

from src.db import Session, metadata, engine
from src.generators.dynamic import insert_fake

def main():
    # aplica alterações de schema antes de inserir os dados
    alter_schema()

    # reflete todas as tabelas (já com id e updated_at garantidos)
    metadata.reflect(bind=engine)

    session = Session()
    insert_fake(session, metadata.tables["customers"], n=5)
    insert_fake(session, metadata.tables["orders"],    n=20)

    print("Dados simulados inseridos com sucesso!")

if __name__ == "__main__":
    main()
