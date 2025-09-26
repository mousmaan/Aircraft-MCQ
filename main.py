from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import random # ✅ Hum 'random' ka istemal questions ko mix karne ke liye karenge
import json
import os

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

TOPICS_FILE = "topics.json"
with open(TOPICS_FILE, "r") as f:
    topics = json.load(f)

@app.get("/")
def root():
    return FileResponse("index.html")

@app.get("/api/topics")
def get_topics():
    return topics

# ✅✅✅ BADLAV YAHAN HAI ✅✅✅
# Humne purane 'generate_question' function ko is naye function se badal diya hai.
@app.get("/api/start_quiz/{topic_id}")
def start_quiz(topic_id: str):
    """
    Yeh function ek topic ke saare questions dhoondhta hai, 
    unhe mix (shuffle) karta hai, aur poori list browser ko bhej deta hai.
    """

    # Step 1: Topic ki file dhoondo (yeh code waisa hi hai)
    all_sub_topics = []
    for category in topics:
        all_sub_topics.extend(category.get('sub_topics', []))

    topic_info = next((t for t in all_sub_topics if t["id"] == topic_id), None)
    
    if not topic_info:
        return {"error": "Topic (Chapter) not found in topics.json"}

    question_file_path = topic_info.get("file")
    if not question_file_path or not os.path.exists(question_file_path):
        return {"error": f"File not found at path: {question_file_path}"}

    # Step 2: Saare questions load karo (yeh code waisa hi hai)
    try:
        with open(question_file_path, "r") as f:
            questions = json.load(f)
    except json.JSONDecodeError:
        return {"error": f"File is empty or not a valid JSON: {question_file_path}"}

    if not questions:
        return {"error": f"No questions found in file: {question_file_path}"}
        
    # ✅ Step 3: ASLI LOGIC - Poori list ko shuffle (mix) karo
    random.shuffle(questions)
    
    # Step 4: Poori shuffled list frontend ko bhej do
    return questions