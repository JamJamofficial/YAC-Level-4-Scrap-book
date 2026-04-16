from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:63085"], # Allow your frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Simulated database to store mood history
mood_db = []

# Data model for incoming requests
class MoodRequest(BaseModel):
    mood: str
    emoji: str

@app.get("/")
def read_root():
    return {"message": "Mood Tracker API is running!"}

# Endpoint to record a new mood
@app.post("/mood")
def record_mood(entry: MoodRequest):
    new_entry = {
        "mood": entry.mood,
        "emoji": entry.emoji,
        "timestamp": datetime.now().strftime("%I:%M %p") # e.g., "02:30 PM"
    }
    mood_db.append(new_entry)
    return new_entry

# Endpoint to get the latest mood
@app.get("/mood/latest")
def get_latest_mood():
    if not mood_db:
        return {"mood": "No mood recorded yet", "emoji": "😶", "timestamp": ""}
    return mood_db[-1] # Return the last item in the list

# Endpoint to get the full history
@app.get("/mood/history")
def get_mood_history():
    # Return reversed list so the newest items show up first
    return list(reversed(mood_db))