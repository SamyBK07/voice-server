import time

last_user_time = time.time()

def update_user_activity():
    global last_user_time
    last_user_time = time.time()

def should_trigger_proactive(context):
    now = time.time()

    silence = now - last_user_time

    # événement silence
    if silence > 20:
        return True

    return False
