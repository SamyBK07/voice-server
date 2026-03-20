def ask_mistral(context, proactive=False):

    if proactive:
        system_prompt = """
Comporte toi comme Jarvis.

Tu peux initier la conversation MAIS seulement si c'est pertinent.

Si tu n'as rien d'intéressant à dire :
réponds STRICTEMENT par : SILENCE
"""
    else:
        system_prompt = "Tu réponds normalement."

    response = call_mistral_api(system_prompt, context)

    if "SILENCE" in response:
        return None

    return response.strip()
