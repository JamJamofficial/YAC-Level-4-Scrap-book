from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

last_mood = "None"

class Mood(BaseModel):
    mood: str

@app.post("/mood")
def set_mood(m: Mood):
    global last_mood
    last_mood = m.mood
    return {"message": "Saved"}

@app.get("/mood")
def get_mood():
    return {"mood": last_mood}