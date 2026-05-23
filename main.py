from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

app = FastAPI() # app is the instance of the fastapi object

@app.get("/") # / means Home endpoint
def read_root():
    return {"Message":"This is the main app"}

@app.get("/greet")
def greet():
    return {"Greet":"hello World"}

# /docs is Swagger UI

# Path & Quyry Parameter

# @app.get("/greet/{name}")
# def greet(name : str, age: Optional[int] = None):
#     return {"Greet":f"Hello {name} are you {age} years old"}

@app.get("/greet/")
def greet(name : str, age: Optional[int] = None):
    return {"Greet":f"Hello {name} are you {age} years old"}
# http://localhost:8000/greet/?name=chiku&age=20

# Post Request - To send the data to the server
class Student(BaseModel):
    name: str
    age: int
    section: str
    roll: int

@app.post("/create_student")
def create_student(student:Student):
    return {
        "name":student.name,
        "age":student.age,
        "section":student.section,
        "roll":student.roll
    }
