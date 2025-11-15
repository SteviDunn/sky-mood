from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Sky Mood API", version="0.1.0")


class MoodRequest(BaseModel):
    mood: str


@app.get("/healthz")
async def healthcheck():
    return {"status": "ok"}


@app.post("/mood")
async def analyze_mood(payload: MoodRequest):
    mood = payload.mood.strip()
    mood_level = "positive" if mood else "unknown"
    return {"mood": mood, "level": mood_level}


@app.get("/")
async def root():
    return {"message": "Sky Mood API is running"}
