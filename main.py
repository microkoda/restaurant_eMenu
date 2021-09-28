from fastapi import FastAPI, Depends, status, Response, HTTPException
from sqlalchemy import exc
from . import models, schemas, database
from sqlalchemy.orm import Session
from typing import List
import sqlalchemy
from .database import SessionLocal, engine
from datetime import datetime


models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()


@app.get('/menu', response_model=List[schemas.Menu], status_code=status.HTTP_200_OK)
def get_menus(response : Response, db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    resp = db.query(models.Menu).offset(skip).limit(limit).all()
    if not resp:
        response.status_code = status.HTTP_404_NOT_FOUND
    return resp

@app.get('/menu/{menu_name}', response_model=schemas.Menu, status_code=status.HTTP_200_OK)
def get_menu_by_name(menu_name : str, db: Session = Depends(get_db)):
    resp = db.query(models.Menu).filter(models.Menu.name == menu_name).first()
    if not resp:
        response.status_code = status.HTTP_404_NOT_FOUND
    return resp

@app.post('/menu', status_code = status.HTTP_201_CREATED)
def create_menu(menu: schemas.MenuCreate, response : Response, db: Session = Depends(get_db)):
    new_menu = models.Menu(name = menu.name, description = menu.description, created = datetime.now())
    db.add(new_menu)
    try:
        db.commit()
        db.refresh(new_menu)
    except exc.IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f'Menu with name {new_menu.name} already exists')
    return new_menu

@app.put('/menu/{menu_name}', response_model=schemas.Menu, status_code=status.HTTP_200_OK)
def update_menu(menu: schemas.MenuCreate, response : Response, db: Session = Depends(get_db)):
    pass

@app.delete('/menu/{menu_name}')
def delete_menu_by_name(menu_name : str, db: Session = Depends(get_db)):
    db.query(models.Menu).filter(models.Menu.name == menu_name).delete(synchronize_session=False)
    db.commit()
    return 'ok'

@app.post('/menu/{menu_name}/add_dish', status_code = status.HTTP_201_CREATED)
def add_dish(dish: schemas.Dish, menu_name, response : Response, db: Session = Depends(get_db)):
    new_dish = models.Dish(name = dish.name, description = dish.description, time_to_get_ready = dish.time_to_get_ready, price = dish.price, is_vgetarian = dish.is_vgetarian, owner_id = menu_name)
    q = db.query(models.Menu).filter(models.Menu.name == menu_name)
    if db.query(q.exists()).scalar():
        db.add(new_dish)
        db.commit()
        db.refresh(new_dish)
    else:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No menu with name {menu_name}')
    return new_dish