# main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # ← Add this import
from app.routers import customers, accounts, transactions, auth
from app.database import engine
from app.models import Base
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="Bank System API")

# Allow all origins (for development only)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ← You can specify ["http://localhost:9000"] instead of "*" in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

# Serve static files
#app.mount("/", StaticFiles(directory="frontend", html=True), name="static")  <--- THIS CODE WAS CAUSING ME 405 ERROR !

# Include routers
app.include_router(customers.router, prefix="/customers", tags=["Customers"])
app.include_router(accounts.router, prefix="/accounts", tags=["Accounts"])
app.include_router(transactions.router, prefix="/transactions", tags=["Transactions"])
app.include_router(auth.router, tags=["Auth"])

@app.get("/")
def root():
    return {"message": "Welcome to the Bank System API"}
