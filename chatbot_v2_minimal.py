#!/usr/bin/env python3
import sys
import ollama

print("🚀 Bot startet...")

def ask(prompt):
    try:
        response = ollama.chat(model="gemma2:2b", messages=[{"role": "user", "content": prompt}])
        return response['message']['content']
    except Exception as e:
        return f"Fehler: {e}"

print("🤖 Bereit. Tippe 'bye' zum Beenden.\n")
while True:
    try:
        user = input("💬 Du: ").strip()
        if not user:
            continue
        if user.lower() in ["bye", "exit", "quit"]:
            print("👋 Tschüss!")
            break
        print("⏳ ...")
        antwort = ask(user)
        print(f"🤖 Bot:\n{antwort}\n")
    except KeyboardInterrupt:
        print("\n👋 Abbruch.")
        break
