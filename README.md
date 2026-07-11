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
- `openai` (opcional: para IA real con OPENAI_API_KEY)

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
```

Escribe `exit` para salir.

Si no hay `OPENAI_API_KEY`, el bot usa un cerebro local
(saludos, nombre, hora, fecha y calculos) y no crashea.

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
  la hora, la fecha y calculos matematicos. Con `OPENAI_API_KEY`
  configurada, usa el modelo de IA real (OpenAI).

Gracias quien sea que vea esto :3
