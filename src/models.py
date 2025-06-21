# src/models.py
from sqlalchemy import MetaData
from src.db import engine, metadata

# 1) Reflete todas as tabelas (se ainda não fez isso em db.py)
metadata.reflect(bind=engine)

# 2) Mapear cada tabela pelo nome exato (lower-case)
Customers       = metadata.tables['customers']
Orders          = metadata.tables['orders']
OrderDetails    = metadata.tables['order_details']
Products        = metadata.tables['products']
Employees       = metadata.tables['employees']
Shippers        = metadata.tables['shippers']
Suppliers       = metadata.tables['suppliers']
Categories      = metadata.tables['categories']
# (adicione outras que precise, conforme a lista:)
# 'employee_territories', 'region', 'customer_demographics',
# 'us_states', 'categories', 'territories', 'customer_customer_demo', …

# Pronto: agora você pode importar
# from src.models import Customers, Orders, OrderDetails, …
