from fastapi import FastAPI
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from databases import Database
from contextlib import asynccontextmanager

# Database Configuration
DATABASE_URL = "sqlite:///./test.db"
database = Database(DATABASE_URL)
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define the table
class Calculation(Base):
    __tablename__ = "calculations"
    id = Column(Integer, primary_key=True, index=True)
    operation = Column(String)
    num1 = Column(Integer)
    num2 = Column(Integer)
    result = Column(Integer)

# Create the database table
Base.metadata.create_all(bind=engine)

# FastAPI App with Database Connection
@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()

app = FastAPI(lifespan=lifespan)

# Addition endpoint
@app.get("/add/{num1}/{num2}")
async def add(num1: int, num2: int):
    result = num1 + num2
    query = "INSERT INTO calculations (operation, num1, num2, result) VALUES ('add', :num1, :num2, :result)"
    await database.execute(query=query, values={"num1": num1, "num2": num2, "result": result})
    return {"result": result}

# Subtraction endpoint
@app.get("/subtract/{num1}/{num2}")
async def subtract(num1: int, num2: int):
    result = num1 - num2
    query = "INSERT INTO calculations (operation, num1, num2, result) VALUES ('subtract', :num1, :num2, :result)"
    await database.execute(query=query, values={"num1": num1, "num2": num2, "result": result})
    return {"result": result}

# Multiplication endpoint
@app.get("/multiply/{num1}/{num2}")
async def multiply(num1: int, num2: int):
    result = num1 * num2
    query = "INSERT INTO calculations (operation, num1, num2, result) VALUES ('multiply', :num1, :num2, :result)"
    await database.execute(query=query, values={"num1": num1, "num2": num2, "result": result})
    return {"result": result}

# Endpoint to get history
@app.get("/history")
async def get_history():
    query = "SELECT * FROM calculations"
    results = await database.fetch_all(query=query)
    return results
