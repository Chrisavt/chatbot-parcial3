import os
import json
from datetime import datetime

from datalumina import Functions

# Pixel-art mapache (raccoon) para la interfaz de inicio
MAPACHE = r"""
   (\_/)
  ( •_•)   <-- mapache pixel
  / >(o)
"""


class ChatBot:
    """Chatbot de IA que usa Datalumina Functions para responder consultas."""

    def __init__(self, log_path: str = "logs.txt"):
        # Cliente oficial de Datalumina (según el video / documentación)
        self.functions = Functions()
        self.log_path = log_path

    def ask(self, question: str):
        """Procesa un comando /ask y devuelve la respuesta de la función."""
        if not question.startswith("/ask"):
            return "[X] Solo acepto comandos del tipo '/ask [pregunta]'"
        query = question[5:].strip()
        try:
            # Datalumina expone las funciones como atributos/índices.
            # Ejemplo de uso real (ver python.datalumina.com/functions):
            #   self.functions.clima("Madrid")
            #   self.functions.calcular("25 * 4")
            result = self.functions[query]()
            return result
        except KeyError:
            return {"error": f"[!] No hay una función llamada '{query}' disponible"}
        except Exception as e:  # noqa: BLE001
            return {"error": f"[!] Error al procesar la solicitud: {e}"}

    def run(self):
        """Bucle principal interactivo (estilo Claude Code)."""
        print(MAPACHE)
        print("Chatbot de IA listo. Escribe '/ask <pregunta>' o 'exit' para salir.")
        while True:
            try:
                user_input = input("> ").strip()
                if user_input.lower() in {"exit", "salir", "quit"}:
                    print("¡Hasta luego!")
                    break
                response = self.ask(user_input)
                print(response)
                self.log_interaction(user_input, response)
            except (KeyboardInterrupt, EOFError):
                print("\n¡Hasta luego!")
                break

    def log_interaction(self, user, bot_response):
        """Guarda cada consulta/respuesta en logs.txt."""
        entry = {
            "time": datetime.now().isoformat(),
            "user": user,
            "bot": str(bot_response),
        }
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    ChatBot().run()
