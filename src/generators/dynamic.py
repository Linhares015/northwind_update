from random import choice
from faker import Faker
from sqlalchemy import (
    String, Integer, Date, DateTime, Float, Boolean,
    select, func
)

fake = Faker("pt_BR")

def truncate(value, length):
    if not isinstance(value, str) or length is None:
        return value
    return value[:length]


def generate_row(table, session):
    data = {}
    for col in table.columns:
        # 0) pular colunas 'id' e 'updated_at', que usam default do DB
        if col.name in ('id', 'updated_at'):
            continue

        # 1) PK numérico: gera via max(pk)+1
        if col.primary_key and isinstance(col.type, Integer):
            max_val = session.execute(select(func.max(col))).scalar() or 0
            data[col.name] = max_val + 1
            continue

        # 2) PK texto: máscara coerente e truncar
        if col.primary_key:
            length = getattr(col.type, "length", 5) or 5
            pattern = "?" * 2 + "#" * (length - 2)
            val = fake.unique.bothify(text=pattern).upper()
            data[col.name] = truncate(val, length)
            continue

        # 3) Foreign keys: valor existente
        if col.foreign_keys:
            fk = list(col.foreign_keys)[0]
            parent = fk.column.table
            parent_col = fk.column.name
            res = session.execute(select(parent.c[parent_col])).scalars().all()
            data[col.name] = choice(res) if res else None
            continue

        # 4) NOT NULL sem default, não-string: pular
        if not col.nullable and col.default is None and not col.server_default:
            if not isinstance(col.type, String):
                continue

        # 5) Geração por tipo com truncamento
        length = getattr(col.type, "length", None)
        if isinstance(col.type, String):
            name = col.name.lower()
            if name in ("company_name", "ship_name"):
                val = fake.company()
            elif name == "contact_name":
                val = fake.name()
            elif name == "contact_title":
                val = fake.job()
            elif "address" in name:
                val = fake.street_address()
            elif "city" in name:
                val = fake.city()
            elif "region" in name:
                val = fake.state()
            elif "postal_code" in name:
                val = fake.postcode()
            elif "country" in name:
                val = fake.country()
            elif "phone" in name or "fax" in name:
                val = fake.phone_number()
            else:
                val = fake.text(max_nb_chars=length or 20).strip()
            data[col.name] = truncate(val, length)
        elif isinstance(col.type, Integer):
            data[col.name] = fake.random_int(min=1, max=30000)
        elif isinstance(col.type, Float):
            data[col.name] = abs(round(fake.pyfloat(left_digits=3, right_digits=2), 2))
        elif isinstance(col.type, Boolean):
            data[col.name] = fake.boolean()
        elif isinstance(col.type, Date):
            data[col.name] = fake.date_between(start_date="-2y", end_date="today")
        elif isinstance(col.type, DateTime):
            data[col.name] = fake.date_time_between(start_date="-1y", end_date="now")
        else:
            data[col.name] = fake.word()

    return data


def insert_fake(session, table, n=10):
    """
    Insere n linhas “realistas” em `table`, respeitando PKs, FKs e tipos.
    """
    for _ in range(n):
        row = generate_row(table, session)
        session.execute(table.insert().values(**row))
    session.commit()
