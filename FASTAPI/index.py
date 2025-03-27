from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# User model
class User(BaseModel):
    id: int
    name: str
    phone_no: str
    address: str

# In-memory storage with initial data
users_db = [
    User(id=1, name="Alice Johnson", phone_no="1112223333", address="10 Elm St"),
    User(id=2, name="Bob Smith", phone_no="4445556666", address="20 Oak Ave"),
    User(id=3, name="Charlie Brown", phone_no="7778889999", address="30 Pine Rd")
]

# Create a new user
@app.post("/users/", status_code=201)
def create_user(user: User):
    for existing_user in users_db:
        if existing_user.id == user.id:
            raise HTTPException(status_code=400, detail="User ID already exists")
    users_db.append(user)
    return {"message": "User created successfully"}

# Read user by ID
@app.get("/users/{id}")
def get_user(id: int):
    for user in users_db:
        if user.id == id:
            return user
    raise HTTPException(status_code=404, detail="User not found")

# Read users by name
@app.get("/users/", response_model=List[User])
def search_users(name: str = Query(...)):
    result = [user for user in users_db if user.name.lower() == name.lower()]
    return result

# Update user details
@app.put("/users/{id}")
def update_user(id: int, updated_user: User):
    for index, user in enumerate(users_db):
        if user.id == id:
            users_db[index] = updated_user
            return {"message": "User updated successfully"}
    raise HTTPException(status_code=404, detail="User not found")

# Delete user by ID
@app.delete("/users/{id}")
def delete_user(id: int):
    for index, user in enumerate(users_db):
        if user.id == id:
            users_db.pop(index)
            return {"message": "User deleted successfully"}
    raise HTTPException(status_code=404, detail="User not found")

