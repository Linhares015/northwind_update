import random
from datetime import datetime, timedelta
from faker import Faker
from src.db import Session
from src.models import Orders, OrderDetails, Products, Customers, Employees, Shippers

fake = Faker()

def create_order(customer_ids, employee_ids, shipper_ids, product_rows):
    order_date = fake.date_between(start_date="-30d", end_date="today")
    ship_date  = order_date + timedelta(days=random.randint(1,10))
    data_order = {
      "CustomerID": random.choice(customer_ids),
      "EmployeeID": random.choice(employee_ids),
      "OrderDate": order_date,
      "RequiredDate": order_date + timedelta(days=7),
      "ShippedDate": ship_date,
      "ShipVia": random.choice(shipper_ids),
      "Freight": round(random.uniform(10,200), 2),
      "ShipName": fake.company(),
      "ShipAddress": fake.street_address(),
      "ShipCity": fake.city(),
      "ShipRegion": fake.state(),
      "ShipPostalCode": fake.postcode(),
      "ShipCountry": fake.country(),
    }
    details = []
    for _ in range(random.randint(1,5)):
        prod = random.choice(product_rows)
        qty = random.randint(1,10)
        details.append({
          "ProductID": prod.ProductID,
          "UnitPrice": prod.UnitPrice,
          "Quantity": qty,
          "Discount": random.choice([0, 0.05, 0.1, 0.15])
        })
    return data_order, details

def insert_orders(n=20):
    session = Session()
    # buscar chaves existentes
    customer_ids = [r.CustomerID for r in session.query(Customers.c.CustomerID)]
    employee_ids = [r.EmployeeID for r in session.query(Employees.c.EmployeeID)]
    shipper_ids  = [r.ShipperID  for r in session.query(Shippers.c.ShipperID)]
    product_rows = session.query(Products).all()

    for _ in range(n):
        o, details = create_order(customer_ids, employee_ids, shipper_ids, product_rows)
        result = session.execute(Orders.insert().values(**o))
        order_id = result.inserted_primary_key[0]
        for d in details:
            d["OrderID"] = order_id
            session.execute(OrderDetails.insert().values(**d))
    session.commit()
