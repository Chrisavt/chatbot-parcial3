import os
import re
import ast
import json
import operator
from datetime import datetime

# La IA externa (OpenAI) es opcional. Si hay una API key en la variable
# de entorno OPENAI_API_KEY, el bot responde con el modelo real; si no,
# usa un cerebro local que sigue funcionando al 100%.
try:
    from openai import OpenAI
    _client = OpenAI() if os.getenv("OPENAI_API_KEY") else None
except Exception:  # noqa: BLE001
    _client = None

# Pixel-art mapache (raccoon) para la interfaz de inicio
MAPACHE = r"""
   (\_/)
  ( o_o )
  / >(o)
"""

# --- Calculadora segura (sin usar eval) ---
_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.USub: operator.neg,
}


def _eval_node(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp):
        return _OPS[type(node.op)](_eval_node(node.left), _eval_node(node.right))
    if isinstance(node, ast.UnaryOp):
        return _OPS[type(node.op)](_eval_node(node.operand))
    raise ValueError("Expresion no valida")


def calcular(expr: str):
    """Evalua una expresion matematica de forma segura."""
    tree = ast.parse(expr, mode="eval")
    return _eval_node(tree.body)


def responder(query: str) -> str:
    """Cerebro del chatbot: devuelve una respuesta a la pregunta."""
    q = query.strip()
    low = q.lower()

    # 1) Calculo matematico
    expr = q.replace("^", "**")
    if any(c.isdigit() for c in expr) and re.fullmatch(r"[0-9\.\s\+\-\*\/\%\(\)]+", expr):
        try:
            return f"El resultado es {calcular(expr)}"
        except Exception:  # noqa: BLE001
            pass

    # 2) Respuestas locales
    if any(w in low for w in ["hola", "buenos dias", "buenas", "que tal"]):
        return "Hola, soy Mapache Bot. Como te puedo ayudar?"
    if "como te llamas" in low or "tu nombre" in low or "quien eres" in low:
        return "Me llamo Mapache Bot, tu asistente de IA para el Parcial 3."
    if "hora" in low:
        return f"Son las {datetime.now().strftime('%H:%M:%S')}."
    if "fecha" in low or "que dia es" in low:
        return f"Hoy es {datetime.now().strftime('%d/%m/%Y')}."

    # 3) Modelo de IA real (si hay API key configurada)
    if _client is not None:
        try:
            resp = _client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": q}],
            )
            return resp.choices[0].message.content.strip()
        except Exception as e:  # noqa: BLE001
            return f"[ERROR] No pude contactar el modelo de IA: {e}"

    # 4) Fallback (sin API key)
    return (
        "Puedo responder saludos, mi nombre, la hora, la fecha y calculos "
        "matematicos (ej: /ask 25*4). Para respuestas de IA general, "
        "configura la variable OPENAI_API_KEY."
    )


class ChatBot:
    """Chatbot de IA para el Parcial 3."""

    def __init__(self, log_path: str = "logs.txt"):
        self.log_path = log_path

    def ask(self, question: str) -> str:
        """Procesa un comando /ask y devuelve la respuesta."""
        if not question.startswith("/ask"):
            return "[X] Solo acepto comandos del tipo '/ask [pregunta]'"
        query = question[4:].strip()
        if not query:
            return "[!] Escribe algo despues de /ask. Ej: /ask hola"
        return responder(query)

    def run(self):
        """Bucle principal interactivo."""
        print(MAPACHE)
        if _client is None:
            print("[INFO] Modo local (sin OPENAI_API_KEY): respuestas basicas + calculos.")
        else:
            print("[INFO] Modo IA conectado (OpenAI).")
        print("Chatbot de IA listo. Escribe '/ask <pregunta>' o 'exit' para salir.")
        while True:
            try:
                user_input = input("> ").strip()
                if user_input.lower() in {"exit", "salir", "quit"}:
                    print("Hasta luego!")
                    break
                response = self.ask(user_input)
                print(response)
                self.log_interaction(user_input, response)
            except (KeyboardInterrupt, EOFError):
                print("\nHasta luego!")
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


def main():
    ChatBot().run()


if __name__ == "__main__":
    main()
