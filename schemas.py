from pydantic import BaseModel
from typing import List
class BasePost(BaseModel):
    title: str
    content: str
    published: bool = True
    
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    
    class Config:
        orm_mode = True
        


class CarBase(BaseModel):
    make: str
    model: str
    year: int
    rental_rate_per_day: float
    availability: bool

class CarCreate(CarBase):
    pass

class Car(CarBase):
    car_id: int

    class Config:
        orm_mode = True

class CustomerBase(BaseModel):
    name: str
    email: str
    phone: str

class CustomerCreate(CustomerBase):
    pass

class Customer(CustomerBase):
    customer_id: int

    class Config:
        orm_mode = True

class RentalBase(BaseModel):
    car_id: int
    customer_id: int
    rental_start_date: str
    rental_end_date: str
    total_cost: float

class RentalCreate(RentalBase):
    pass

class Rental(RentalBase):
    rental_id: int

    class Config:
        orm_mode = True

class CarWithRentals(Car):
    rentals: List[Rental] = []

class CustomerWithRentals(Customer):
    rentals: List[Rental] = []
