from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from enum import Enum

# Enums to match models
class AccountType(str, Enum):
    savings = "savings"
    checking = "checking"

class TransactionType(str, Enum):
    deposit = "deposit"
    withdrawal = "withdrawal"
    transfer = "transfer"

# ----------------------
# Customer Schemas
# ----------------------
class CustomerBase(BaseModel):
    name: str
    email: EmailStr

class CustomerCreate(CustomerBase):
    pass

class CustomerOut(CustomerBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

# ----------------------
# Account Schemas
# ----------------------
class AccountBase(BaseModel):
    account_type: AccountType

class AccountCreate(AccountBase):
    customer_id: int
    account_number: str

class AccountOut(AccountBase):
    id: int
    customer_id: int
    account_number: str
    balance: float
    created_at: datetime

    class Config:
        orm_mode = True

# New schema for Account response including nested customer details
class AccountOutWithCustomer(AccountBase):
    id: int
    customer_id: int
    account_number: str
    balance: float
    created_at: datetime
    customer: CustomerOut  # nested customer schema

    class Config:
        orm_mode = True

# ----------------------
# Transaction Schemas
# ----------------------
class TransactionBase(BaseModel):
    amount: float

class Deposit(TransactionBase):
    to_account_id: int

class Withdraw(TransactionBase):
    from_account_id: int

class Transfer(TransactionBase):
    from_account_id: int
    to_account_id: int

class TransactionOut(TransactionBase):
    id: int
    from_account_id: Optional[int]
    to_account_id: Optional[int]
    transaction_type: TransactionType
    timestamp: datetime

    class Config:
        orm_mode = True

# Authentication system schemas

class UserCreate(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    is_admin: bool

    class Config:
        orm_mode = True
