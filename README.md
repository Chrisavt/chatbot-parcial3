# Chatbot de IA (Parcial 3)

⠀⠀⢀⡤⢴⠀⠀
⠀⠀⡎⠐⠐⣑⠆
⡤⡖⠁⠀⠀⡇⠀
⠟⠧⠤⠧⠀⠃⠀

Chatbot de IA construido siguiendo el curso **Python for AI** y la
documentación de **Datalumina Functions**.

## Recursos usados
- Video: https://www.youtube.com/watch?v=ygXn5nV5qFc
- Funciones Datalumina: https://python.datalumina.com/functions

## Requisitos
- Python 3.x
- pip
- `openai` (IA real con OpenAI o Groq; Groq usa la misma libreria)
- `huggingface_hub` (opcional: IA gratis con token de Hugging Face)
- Para respuestas de IA metes tu token una vez con el comando `/token`
  (Groq es gratis). Se guarda local en `config.json` y no se sube a GitHub.

## Cómo ejecutarlo (recomendado)

**Doble clic en `ejecutar.bat`** (Windows). Crea el entorno, instala
las dependencias y corre el bot. **No usa PowerShell**, así que no
aparece el error de permisos ("execution of scripts is disabled").

## Instalación manual

```bash
# 1. Clonar el repositorio
git clone https://github.com/Chrisavt/chatbot-parcial3.git
cd chatbot-parcial3

# 2. Crear entorno virtual
python -m venv .venv

# 3. Instalar dependencias (sin activar el entorno)
.venv\Scripts\pip install -r requirements.txt

# 4. Ejecutar el bot (Python directo, sin Activate.ps1)
.venv\Scripts\python.exe src/bot.py
```

Nota: no se usa `Activate.ps1` a propósito, porque PowerShell lo
bloquea por defecto. Llamar a `python.exe` directo evita ese error.
Se ejecuta `src/bot.py` como archivo (no con `-m`) para evitar el
`RuntimeWarning` de importacion del paquete.

Ejemplos de comandos:

```
/ask 25*4
/ask hola
/ask como te llamas?
/ask que hora es
/token gsk_xxxxxxxxxxxxxxxx   (activa la IA con Groq, gratis)
/ask que es una red neuronal?   (responde la IA)
/local                       (usa solo respuestas conocidas, sin IA)
/api                         (vuelve a usar la IA con el token guardado)
```

Escribe `exit` para salir.

## Activar la IA con tu token

El bot no trae token embebido (GitHub bloquea subir secretos), pero lo
activas en segundos. Mete tu token una vez con el comando `/token`
dentro del bot y queda guardado en `config.json`:

```
/token gsk_xxxxxxxxxxxxxxxx   (Groq, gratis)
/token sk-xxxxxxxxxxxxxxxx    (OpenAI)
/token hf_xxxxxxxxxxxxxxxx    (Hugging Face, token GRATIS)
```

- `gsk_...` -> **Groq** (modelo Llama 3.3, gratis).
- `sk-...`  -> **OpenAI** (gpt-4o-mini).
- otro     -> **Hugging Face** (token gratis en
  https://huggingface.co/settings/tokens).
- El token se guarda en `config.json` (archivo local, ignorado por
  git, asi NO se sube a GitHub). La proxima vez que abras el bot ya
  estara conectado.
- Tambien puedes usar variables de entorno: `OPENAI_API_KEY` o `HF_TOKEN`.
- Si quieres usar el bot SIN IA (solo las respuestas que ya conoce:
  saludos, nombre, hora, fecha y calculos), escribe `/local`. Para
  volver a la IA escribe `/api`.

Sin token el bot no crashea: avisa como activarlo y sigue respondiendo
lo local (saludos, nombre, hora, fecha y calculos).

## Estructura

```
chatbot-parcial3/
├── src/
│   ├── __init__.py
│   ├── bot.py          # Motor del chatbot + mapache pixel
│   └── utils.py        # Funciones auxiliares
├── ejecutar.bat        # Lanzador con doble clic (Windows)
├── requirements.txt
├── README.md
├── .gitignore
└── logs.txt            # Generado automáticamente
```

## Notas
- Cada interacción se registra en `logs.txt`.
- El bot funciona sin internet: responde saludos, su nombre,
  la hora, la fecha y calculos matematicos. Con un token de IA
  (Groq/OpenAI/Hugging Face) activado via `/token`, responde
  cualquier pregunta con el modelo real.

Gracias quien sea que vea esto :3
