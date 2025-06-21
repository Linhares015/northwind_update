from faker import Faker
from src.db import Session
from src.models import Customers

fake = Faker("pt_BR")

def create_customer():
    return {
      "CustomerID": fake.unique.bothify(text="??#####").upper(),
      "CompanyName": fake.company(),
      "ContactName": fake.name(),
      "ContactTitle": fake.job(),
      "Address": fake.street_address(),
      "City": fake.city(),
      "Region": fake.state(),
      "PostalCode": fake.postcode(),
      "Country": fake.country(),
      "Phone": fake.phone_number(),
      "Fax": fake.phone_number()
    }

def insert_customers(n=10):
    session = Session()
    for _ in range(n):
        data = create_customer()
        session.execute(Customers.insert().values(**data))
    session.commit()
