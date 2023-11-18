from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql.sqltypes import Float
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship
from .database import Base
from sqlalchemy.sql.sqltypes import TIMESTAMP
class Car(Base):
    __tablename__ = "Cars"
    
    car_id = Column(Integer, primary_key=True, nullable=False,autoincrement="auto")
    make = Column(String(length=255), nullable=False)
    model = Column(String(length=255), nullable=False)
    year = Column(Integer, nullable=False)
    rental_rate_per_day = Column(Float, nullable=False)
    availability = Column(Boolean, default=True, nullable=False)

class Customer(Base):
    __tablename__ = "Customers"
    
    customer_id = Column(Integer, primary_key=True, nullable=False,autoincrement="auto")
    name = Column(String(length=255), nullable=False)
    email = Column(String(length=255), nullable=False)
    phone = Column(String(length=20), nullable=False)

class Rental(Base):
    __tablename__ = "Rentals"
    
    rental_id = Column(Integer, primary_key=True, nullable=False)
    car_id = Column(Integer, ForeignKey('Cars.car_id'), nullable=False)
    customer_id = Column(Integer, ForeignKey('Customers.customer_id'), nullable=False)
    rental_start_date = Column(DateTime, nullable=False, server_default=text('now()'))
    rental_end_date = Column(DateTime, nullable=False)
    total_cost = Column(Float, nullable=False)

    # Define relationships
    car = relationship("Car", back_populates="rentals")
    customer = relationship("Customer", back_populates="rentals")

# Additional relationships for bi-directional access
Car.rentals = relationship("Rental", order_by=Rental.rental_id, back_populates="car")
Customer.rentals = relationship("Rental", order_by=Rental.rental_id, back_populates="customer")
class Post(Base):
    __tablename__ = "Post"
    
    id = Column(Integer , primary_key=True , nullable=False)
    title = Column(String(length=255), nullable=False)
    content = Column(String(length=255), nullable=False)
    published = Column(Boolean,default=True, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),nullable = False , server_default=text('now()'))