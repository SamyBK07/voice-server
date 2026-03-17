import json

from mistral import ask_mistral
from tasks import load_tasks, save_tasks


def generate_tasks(personality):

    tasks = load_tasks()

    prompt = f"""
Tu es un agent autonome.

Tâches actuelles:
{tasks}

Si aucune tâche n'existe, crée entre 1 et 3 tâches utiles.

Réponds uniquement en JSON:

[
{{"title":"...","description":"..."}}
]
"""

    result = ask_mistral(prompt, personality)

    try:

        new_tasks = json.loads(result)

        for t in new_tasks:

            tasks.append({
                "id":len(tasks)+1,
                "title":t["title"],
                "description":t["description"],
                "status":"pending"
            })

        save_tasks(tasks)

    except:
        pass
