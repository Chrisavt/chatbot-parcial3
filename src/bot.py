import os
import re
import ast
import json
import operator
from datetime import datetime

# --- Clientes de IA opcionales (no bloquean el arranque si faltan) ---
try:
    from openai import OpenAI
except Exception:  # noqa: BLE001
    OpenAI = None

try:
    from huggingface_hub import InferenceClient
except Exception:  # noqa: BLE001
    InferenceClient = None

# Pixel-art mapache para la interfaz de inicio
MAPACHE = r"""
   (\_/)
  ( o_o )
  / >(o)
"""

CONFIG_PATH = "config.json"
GROQ_URL = "https://api.groq.com/openai/v1"
GROQ_MODEL = "llama-3.3-70b-versatile"
OPENAI_MODEL = "gpt-4o-mini"
HF_MODEL = "HuggingFaceH4/zephyr-7b-beta"

# Token por defecto: None. El token se pone en config.json (local, no se
# sube a GitHub) o con el comando /token. Asi el secreto no queda en el codigo.
TOKEN_POR_DEFECTO = None

# Estado global del cliente de IA
_cliente = None
_proveedor = None


def cargar_config():
    try:
        with open(CONFIG_PATH, encoding="utf-8") as f:
            return json.load(f)
    except Exception:  # noqa: BLE001
        return {}


def guardar_config(cfg):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)


def _crear_cliente(token):
    """Devuelve (cliente, proveedor) segun el prefijo del token."""
    t = (token or "").strip()
    if t.lower().startswith("gsk_") and OpenAI is not None:
        return OpenAI(api_key=t, base_url=GROQ_URL), "groq"
    if t.lower().startswith("sk-") and OpenAI is not None:
        return OpenAI(api_key=t), "openai"
    if InferenceClient is not None:
        return InferenceClient(token=t or None), "huggingface"
    return None, None


def configurar_token(token):
    """Guarda el token, detecta el proveedor y crea el cliente de IA."""
    global _cliente, _proveedor
    token = (token or "").strip()
    if not token:
        return ("[!] Escribe el token despues de /token. Ej:\n"
                "      /token gsk_xxxx  (Groq)\n"
                "      /token sk-xxxx   (OpenAI)\n"
                "      /token hf_xxxx   (Hugging Face, gratis)")
    cfg = cargar_config()
    cliente, prov = _crear_cliente(token)
    if cliente is None:
        return ("[X] No se pudo crear el cliente de IA. Instala las "
                "dependencias: .venv\\Scripts\\pip install -r requirements.txt")
    _cliente, _proveedor = cliente, prov
    cfg["token"] = token
    cfg["proveedor"] = prov
    guardar_config(cfg)
    nombres = {"openai": "OpenAI", "groq": "Groq", "huggingface": "Hugging Face"}
    return f"[OK] Token listo. El bot ahora responde con IA ({nombres[prov]})."


def cargar_token_guardado():
    """Al arrancar usa: config.json > variable de entorno > token por defecto."""
    global _cliente, _proveedor
    cfg = cargar_config()
    token = (cfg.get("token")
             or os.getenv("OPENAI_API_KEY")
             or os.getenv("HF_TOKEN")
             or TOKEN_POR_DEFECTO)
    cliente, prov = _crear_cliente(token)
    if cliente is not None:
        _cliente, _proveedor = cliente, prov


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
    return _eval_node(ast.parse(expr, mode="eval").body)


def _preguntar_ia(q: str) -> str:
    """Llama al modelo de IA configurado y devuelve la respuesta."""
    try:
        if _proveedor in ("openai", "groq"):
            model = OPENAI_MODEL if _proveedor == "openai" else GROQ_MODEL
            resp = _cliente.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": q}],
            )
            return resp.choices[0].message.content.strip()
        # Hugging Face (modelo de chat gratuito via Inference API)
        prompt = (f"Eres Mapache Bot, un asistente de IA util y amable. "
                  f"Responde en espanol.\nUsuario: {q}\nAsistente:")
        out = _cliente.text_generation(
            prompt, model=HF_MODEL, max_new_tokens=250, temperature=0.7,
        )
        return out.strip()
    except Exception as e:  # noqa: BLE001
        return f"[ERROR] La IA fallo: {e}"


def responder(query: str) -> str:
    """Cerebro del chatbot: devuelve una respuesta a la pregunta."""
    q = query.strip()
    low = q.lower()

    # 1) Calculo matematico (local, exacto y rapido)
    expr = q.replace("^", "**")
    if any(c.isdigit() for c in expr) and re.fullmatch(r"[0-9\.\s\+\-\*\/\%\(\)]+", expr):
        try:
            return f"El resultado es {calcular(expr)}"
        except Exception:  # noqa: BLE001
            pass

    # 2) Respuestas locales rapidas
    if any(w in low for w in ["hola", "buenos dias", "buenas", "que tal"]):
        return "Hola, soy Mapache Bot. Como te puedo ayudar?"
    if "como te llamas" in low or "tu nombre" in low or "quien eres" in low:
        return "Me llamo Mapache Bot, tu asistente de IA para el Parcial 3."
    if "hora" in low:
        return f"Son las {datetime.now().strftime('%H:%M:%S')}."
    if "fecha" in low or "que dia es" in low:
        return f"Hoy es {datetime.now().strftime('%d/%m/%Y')}."

    # 3) IA real (si hay token configurado)
    if _cliente is not None:
        return _preguntar_ia(q)

    # 4) Sin token: avisa como activarla
    return ("Todavia no tengo IA configurada. Activala asi:\n"
            "  /token <tu_token>\n"
            "  - 'gsk_...' -> Groq\n"
            "  - 'sk-...'  -> OpenAI\n"
            "  - otro      -> Hugging Face (gratis en huggingface.co/settings/tokens)\n"
            "Mientras tanto respondo saludos, mi nombre, la hora,\n"
            "la fecha y calculos (ej: /ask 25*4).")


class ChatBot:
    """Chatbot de IA para el Parcial 3."""

    def __init__(self, log_path: str = "logs.txt"):
        self.log_path = log_path

    def ask(self, command: str) -> str:
        """Procesa los comandos /token y /ask."""
        # Comando para meter el token de IA en caliente
        if command.startswith("/token"):
            return configurar_token(command[6:].strip())
        if not command.startswith("/ask"):
            return ("[X] Comandos:\n"
                    "      '/ask <pregunta>'  -> pregunta al bot\n"
                    "      '/token <tu_token>' -> activa la IA\n"
                    "      'exit'             -> salir")
        query = command[4:].strip()
        if not query:
            return "[!] Escribe algo despues de /ask. Ej: /ask hola"
        return responder(query)

    def run(self):
        """Bucle principal interactivo."""
        cargar_token_guardado()
        print(MAPACHE)
        if _cliente is None:
            print("[INFO] Modo local. Activa la IA con: /token <tu_token>")
        else:
            print(f"[INFO] IA conectada ({_proveedor}). Listo para responder.")
        print("Escribe '/ask <pregunta>', '/token <tu_token>' o 'exit'.")
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
