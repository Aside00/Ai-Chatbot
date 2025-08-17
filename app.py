# Simple AI Chatbot with persona selection

import os, time
import gradio as gr
from openai import OpenAI

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
if not OPENAI_API_KEY:
    print("⚠️ Please set your OpenAI key: export OPENAI_API_KEY='...'")
client = OpenAI(api_key=OPENAI_API_KEY)

MODEL = "gpt-4o-mini"

SYSTEM_TEMPLATES = {
    "Study Buddy": "You are a friendly study assistant. Explain concepts step by step and give short examples.",
    "DevOps Coach": "You are a concise DevOps coach. Focus on Docker, Kubernetes, CI/CD best practices.",
    "Recipe Guru": "You are a cooking assistant. Offer practical recipes and cooking tips.",
}

def chat_fn(history, persona):
    system = SYSTEM_TEMPLATES.get(persona, "You are a helpful assistant.")
    messages = [{"role": "system", "content": system}]
    for h in history:
        messages.append({"role": "user", "content": h[0]})
        if h[1]:
            messages.append({"role": "assistant", "content": h[1]})
    resp = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0.6,
    )
    return resp.choices[0].message.content

with gr.Blocks(title="AI Chatbot") as demo:
    gr.Markdown("# 💬 AI Chatbot")
    persona = gr.Dropdown(choices=list(SYSTEM_TEMPLATES.keys()), value="Study Buddy", label="Persona")
    chat = gr.ChatInterface(
        fn=lambda msg, history: chat_fn(history + [[msg, None]], persona.value),
        title="AI Chatbot",
        theme="compact",
    )

if __name__ == "__main__":
    demo.launch()