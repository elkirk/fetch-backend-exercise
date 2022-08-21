from datetime import datetime

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from . import models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def check_duplicate_transaction(db: Session, payer: str, timestamp: datetime):
    return db.query(models.Transaction).filter(models.Transaction.payer == payer, 
                                               models.Transaction.timestamp == timestamp).first()
def check_if_enough_points(db: Session, amount: int):
    if db.query(func.sum(models.Transaction.points)).first()[0]:
        total_points = db.query(func.sum(models.Transaction.points)).first()[0]
        return amount > total_points
    else:
        return True

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close


@app.post("/add-transaction", status_code=201)
def add_transaction(data: schemas.Transaction, db: Session = Depends(get_db)):

    if check_duplicate_transaction(db, data.payer, data.timestamp):
        raise HTTPException(status_code=422, detail="This transaction already exists")

    new_transaction = models.Transaction(payer=data.payer, 
                                         points=data.points, 
                                         timestamp=data.timestamp)
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)
    return "Transaction added"


@app.post("/spend", status_code=200)
def spend_points(data: schemas.SpendRequest, db: Session = Depends(get_db)):

    if check_if_enough_points(db, data.points):
        raise HTTPException(status_code=422, detail="Not enough points to cover spend request")

    points = data.points
    spent_points = 0

    transactions = db.query(models.Transaction
            ).order_by(models.Transaction.timestamp.asc()
            ).all()
    
    spend = list()

    for record in transactions:
        if points == spent_points:
            break

        # check if current iteration's payer has already contributed points towards spend request
        payers = [True for transaction in spend if record.payer in transaction.values()]
        
        # if yes, retrieve that payer's spend_transaction dictionary and modify it
        if any(payers):
            idx = next(index for (index, transaction) in enumerate(spend) if transaction['payer'] == record.payer)
            spend_transaction = spend.pop(idx) 

            spend_transaction['points'] -= record.points
            spend.insert(idx, spend_transaction)
            spent_points += record.points
            
        # else, create a new transaction for this payer
        else:    
            spend_transaction = dict()
            spend_transaction['payer'] = record.payer

            if record.points > points:
                spend_transaction['points'] = -(points - spent_points)
                spent_points += (points - spent_points)
            else:
                spend_transaction['points'] = -record.points
                spent_points += record.points
            
            spend.append(spend_transaction)
        
    # write new spend transactions to db
    for transaction in spend:
        new_transaction = models.Transaction(payer=transaction['payer'], points=transaction['points'])
        db.add(new_transaction)
        db.commit()
        db.refresh(new_transaction)

    return spend


@app.get("/balance", status_code=200)
def return_payer_balances(db: Session = Depends(get_db)):

    balances = db.query(models.Transaction.payer,
            func.sum(models.Transaction.points)
            ).group_by(models.Transaction.payer
            ).all()

    response = dict()

    for record in balances:
        response[record[0]] = record[1]

    # does this need to be explicitly converted to json, or is returning a dict fine?
    return response

@app.get("/check", status_code=200)
def check_db_records(db: Session = Depends(get_db)):
    records = db.query(models.Transaction).all()
    return records
