from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import random
import json
import os

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Load topics
TOPICS_FILE = "topics.json"
with open(TOPICS_FILE, "r") as f:
    topics = json.load(f)

@app.get("/")
def root():
    return FileResponse("index.html")

@app.get("/api/topics")
def get_topics():
    """Return list of topics"""
    return topics

@app.get("/api/generate_question/{topic_id}")
def generate_question(topic_id: str):
    """Return random question from given topic"""

    # Find the topic by ID
    topic = next((t for t in topics if t["id"] == topic_id), None)
    if not topic:
        return {"error": "Topic not found"}

    # Check if topic file exists
    if not os.path.exists(topic["file"]):
        return {"error": f"File {topic['file']} not found"}

    # Load questions from topic file
    with open(topic["file"], "r") as f:
        questions = json.load(f)

    # Pick random question
    question = random.choice(questions)
    return {
        "question": question["question"],
        "image": question.get("image"),
        "options": question["options"],
        "correct_answer": question["answer"],
        "brief_solution": question["brief"],
        "detailed_explanation": question["detailed"]
    }
