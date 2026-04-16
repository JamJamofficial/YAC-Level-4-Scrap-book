from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Simulated database
fake_db = {
    "count": 0
}

class CounterData(BaseModel):
    value: int


@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI"}


# Endpoint to get the current count
@app.get("/count")
def get_count():
    return fake_db


# Endpoint to update the count
@app.post("/increment")
def increment_count():
    fake_db["count"] += 1
    return fake_db


# Endpoint to reset the count
@app.post("/reset")
def reset_count():
    fake_db["count"] = 0
    return fake_db