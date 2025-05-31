from fastapi import APIRouter
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas, database

router = APIRouter()



def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[schemas.TransactionOut])
def get_all_transactions(db: Session = Depends(get_db)):
    return crud.get_all_transactions(db)


@router.post("/deposit", response_model=schemas.TransactionOut)
def deposit(deposit: schemas.Deposit, db: Session = Depends(get_db)):
    transaction = crud.create_deposit(db, deposit)
    if not transaction:
        raise HTTPException(status_code=404, detail="Account not found")
    return transaction

@router.post("/withdraw", response_model=schemas.TransactionOut)
def withdraw(withdraw: schemas.Withdraw, db: Session = Depends(get_db)):
    transaction = crud.create_withdrawal(db, withdraw)
    if not transaction:
        raise HTTPException(status_code=400, detail="Insufficient funds or invalid account")
    return transaction

@router.post("/transfer", response_model=schemas.TransactionOut)
def transfer(transfer: schemas.Transfer, db: Session = Depends(get_db)):
    transaction = crud.create_transfer(db, transfer)
    if not transaction:
        raise HTTPException(status_code=400, detail="Transfer failed: Check accounts or balance")
    return transaction
