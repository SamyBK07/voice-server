from mistral import ask_mistral

def execute_tasks(tasks, personality):

    results = []

    for task in tasks:

        if task["status"] == "pending":

            prompt = f"""
Exécute cette tâche :

Titre: {task['title']}
Description: {task['description']}
"""

            result = ask_mistral(prompt, personality)

            task["status"] = "done"
            task["result"] = result

            results.append({
                "task": task["title"],
                "result": result
            })

    return results
