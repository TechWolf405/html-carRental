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


templates = Jinja2Templates(directory="app/templates")


app = FastAPI()

app.mount("/static", StaticFiles(directory="app/templates/static"), name="static")

db =get_db()


# @app.get('/')
# def name(request :Request):
#     return templates.TemplateResponse("front.html",{"request":request,"name":"No name"})
# def get_all_posts():
#     try:
#         return db.query(Post).all()
#     finally:
#         db.close()

@app.get('/',response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get('/adminpage')
def admin(request:Request):
    return  templates.TemplateResponse("admin-page.html", {"request": request})
@app.get('/customerlogin')
def admin(request:Request):
    return  templates.TemplateResponse("customer-login.html", {"request": request})


@app.get('/deletecar',response_class=JSONResponse )
def deletecar(request:Request):
    return templates.TemplateResponse("deletecar.html", {"request" : request})




@app.post('/create_car')
def create_car(car: schemas.CarBase, db: Session = Depends(get_db)):
    # Process the form data (car) and save it to the database
    new_car = models.Car(**car.model_dump())
    
    # Your database logic goes here
    db.add(new_car)
    db.commit()
    db.refresh(new_car)
    # For demonstration purposes, just return the received data
    return {"Data" : "Successful"}

@app.get('/create_car',response_class=JSONResponse)
def home(request:Request ):
    return templates.TemplateResponse("createcar.html", {"request":request})

# @app.route('/submit_car', methods=['POST'])
# async def handle_car(
#     request: Request

# ):
#     form = await request.form()
     
#     db:Session = Depends(get_db)
#     # db.add(new_car)
#     # db.commit()
#     # db.refresh(new_car)
#     car = schemas.CarBase(**dict(form))
#     car_dict = car.model_dump()
#     car_dict['car_id'] = 23
#     new_car = models.Car(**car_dict)
#     db.add(new_car)
#     db.commit()
#     db.refresh()
#     return {
#             dict(form)
#     }
    

    
# @app.route('/create_car', methods=['GET', 'POST'])
# def create_car(request: Request, db: Session = Depends(get_db)):
#     if request.method == 'POST':
#         # Process the form data (car) and save it to the database
#         form_data = request.form()
#         print(form_data)
#         car_data = {
#             "make": form_data.get("make"),
#             "model": form_data.get("model"),
#             "year": int(form_data.get("year")),
#             "rental_rate_per_day": float(form_data.get("rental_rate_per_day")),
#             "availability": bool(int(form_data.get("availability"))),
#         }
#         print(car_data)

#         # Assuming your Car model has a Pydantic schema (CarBase)
#         car = schemas.CarBase(**car_data)

#         # Your database logic goes here
#         new_car = models.Car(**car.model_dump())
#         print(new_car)

#         db.add(new_car)
#         db.commit()
#         db.refresh(new_car)

#         # For demonstration purposes, just return the received data
#         return templates.TemplateResponse("createcar.html", {"request": request, "car": car.model_dump()})
#     else:
#         return templates.TemplateResponse("createcar.html", {"request": request})


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