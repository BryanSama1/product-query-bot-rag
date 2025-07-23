def build_prompt(query: str, docs: list[str]) -> str:
    context = "\n\n".join(docs)
    return f"""
Responde la siguiente pregunta del usuario basándote exclusivamente en los siguientes textos sobre productos:

{context}

Pregunta del usuario: {query}

Responde de forma clara y útil como si fuera una conversación de WhatsApp.
"""
