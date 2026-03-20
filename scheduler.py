import time
from planner import should_trigger_proactive
from mistral import ask_mistral
from server import send_to_clients, get_context

COOLDOWN = 30
last_speak = 0

def loop():
    global last_speak

    while True:
        time.sleep(5)

        context = get_context()

        # cooldown
        if time.time() - last_speak < COOLDOWN:
            continue

        decision = should_trigger_proactive(context)

        if not decision:
            continue

        response = ask_mistral(context, proactive=True)

        if response:
            send_to_clients(response)
            last_speak = time.time()
