from sqlalchemy.orm import Session
from app import models, schemas
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext

# ----------------------
# Customer CRUD
# ----------------------
def get_all_customers(db: Session):
    return db.query(models.Customer).all()

def get_customer(db: Session, customer_id: int):
    return db.query(models.Customer).filter(models.Customer.id == customer_id).first()

def create_customer(db: Session, customer: schemas.CustomerCreate):
    db_customer = models.Customer(name=customer.name, email=customer.email)
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer
# ----------------------
# Account CRUD
# ----------------------
def create_account(db: Session, account: schemas.AccountCreate):
    db_account = models.Account(**account.dict())
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account

def get_account(db: Session, account_id: int):
    return db.query(models.Account).filter(models.Account.id == account_id).first()

def get_all_accounts(db: Session):
    return db.query(models.Account).all()


# ----------------------
# Transaction CRUD
# ----------------------

def get_all_transactions(db: Session):
    return db.query(models.Transaction).all()
    
def create_deposit(db: Session, deposit: schemas.Deposit):
    account = db.query(models.Account).filter(models.Account.id == deposit.to_account_id).first()
    if not account:
        return None
    account.balance += deposit.amount
    transaction = models.Transaction(
        to_account_id=deposit.to_account_id,
        amount=deposit.amount,
        transaction_type="deposit"
    )
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction

def create_withdrawal(db: Session, withdrawal: schemas.Withdraw):
    account = db.query(models.Account).filter(models.Account.id == withdrawal.from_account_id).first()
    if not account or account.balance < withdrawal.amount:
        return None
    account.balance -= withdrawal.amount
    transaction = models.Transaction(
        from_account_id=withdrawal.from_account_id,
        amount=withdrawal.amount,
        transaction_type="withdrawal"
    )
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction

def create_transfer(db: Session, transfer: schemas.Transfer):
    from_acc = db.query(models.Account).filter(models.Account.id == transfer.from_account_id).first()
    to_acc = db.query(models.Account).filter(models.Account.id == transfer.to_account_id).first()

    if not from_acc or not to_acc or from_acc.balance < transfer.amount:
        return None

    from_acc.balance -= transfer.amount
    to_acc.balance += transfer.amount

    transaction = models.Transaction(
        from_account_id=transfer.from_account_id,
        to_account_id=transfer.to_account_id,
        amount=transfer.amount,
        transaction_type="transfer"
    )
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_username(db, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db, user: schemas.UserCreate):
    hashed_pw = pwd_context.hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_pw)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def verify_password(plain_pw, hashed_pw):
    return pwd_context.verify(plain_pw, hashed_pw)
