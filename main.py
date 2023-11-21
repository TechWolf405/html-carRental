import re
from typing import Optional
from fastapi import FastAPI, Form, Response, status, HTTPException,Depends,Request
from fastapi.params import Body
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from random import randrange
import mysql.connector as connector
import mysql
import time
from sqlalchemy.orm import Session 
from . import models,schemas
from .database import engine,get_db
from .schemas import Post
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
models.Base.metadata.create_all(bind = engine)


templates = Jinja2Templates(directory="html-carRental/templates")


app = FastAPI()

app.mount("/static", StaticFiles(directory="html-carRental/templates\static"), name="static")

db =get_db()




@app.get('/',response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get('/adminpage')
def admin(request:Request):
    return  templates.TemplateResponse("admin-page.html", {"request": request})



@app.get('/deletecar',response_class=JSONResponse )
def deletecar(request:Request):
    return templates.TemplateResponse("deletecar.html", {"request" : request})




@app.post('/create_car')
def create_car(car: schemas.CarBase, db: Session = Depends(get_db)):

    new_car = models.Car(**car.model_dump())
    

    db.add(new_car)
    db.commit()
    db.refresh(new_car)

    return {"Data" : "Successful"}

@app.get('/create_car',response_class=HTMLResponse)
def home(request:Request ):
    return templates.TemplateResponse("createcar.html", {"request":request})


@app.get('/create_customer')
def admin(request:Request):
    return  templates.TemplateResponse("customer-login.html", {"request": request})

@app.post('/create_customer')
def create_customer(request:Request,customer: schemas.CustomerBase, db: Session = Depends(get_db)):
    new_customer = models.Customer(**customer.model_dump())
    

    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)

    return  templates.TemplateResponse("customer-success.html", {"request": request})


@app.get('/posts/')
def read_posts(request: Request,db:Session = Depends(get_db)):
    
    posts = db.query(models.Post).all()
    return templates.TemplateResponse("posts.html", {"request": request, "posts": posts})


@app.get('/showcar',response_class=HTMLResponse)
def show_car(request: Request,db:Session = Depends(get_db)):
    cars = db.query(models.Car).all()
    return templates.TemplateResponse("display.html", {"request":request, "cars":cars})

@app.delete('/delete_car/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_car(request: Request ,id: int, db:Session = Depends(get_db)):
    cars = db.query(models.Car).filter(models.Car.car_id == id).first()
    if cars == None:
        raise HTTPException ( status_code=status.HTTP_404_NOT_FOUND,
        detail = f"post with id: {id} does not exist")
        
    db.delete(cars)
    db.commit()
    return {"data": "Delete successfull"}
    


@app.get('/updatecar' , response_class=HTMLResponse)
def update_car(request:Request , db:Session = Depends(get_db)):
    return templates.TemplateResponse("updatecar.html", {"request":request})
    


@app.put("/update_car/{id}")
def update_post(id:int,Car: schemas.CarBase, db: Session = Depends(get_db)):
    cars_query = db.query(models.Car).filter(models.Car.car_id == id)
    car = cars_query.first()
    
    if car == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f"post with id: {id} does not exist")
    
    cars_query.update({**Car.model_dump()},synchronize_session=False)
    db.commit()
    return {"data" : 'successful'}