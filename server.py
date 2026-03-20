from fastapi import FastAPI
from pydantic import BaseModel

from mistral import ask_mistral
from tasks import add_task, load_tasks, save_tasks
from planner import execute_tasks

app = FastAPI()

# Charger personnalité
with open("personality.txt","r",encoding="utf-8") as f:
    PERSONALITY = f.read()


class ChatRequest(BaseModel):
    message: str


@app.post("/chat")
def chat(req: ChatRequest):

    user_msg = req.message.lower()

    # 🎯 1. Ajouter tâche
    if "ajoute une tâche" in user_msg:

        content = req.message.replace("ajoute une tâche", "").strip()

        task = add_task(content, content)

        return {
            "response": f"Tâche ajoutée : {task['title']}"
        }

    # ⚙️ 2. Exécuter tâches
    elif "exécute les tâches" in user_msg:

        tasks = load_tasks()

        results = execute_tasks(tasks, PERSONALITY)

        save_tasks(tasks)

        return {
            "response": results
        }

    # 📋 3. Voir tâches
    elif "liste des tâches" in user_msg:

        tasks = load_tasks()

        return {
            "response": tasks
        }

    # 💬 4. Chat normal
    else:

        reply = ask_mistral(req.message, PERSONALITY)

        return {
            "response": reply
        }


@app.get("/")
def home():
    return {"status":"AI server running"}
