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
- `datalumina-functions` (y `requests`)

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
.venv\Scripts\python.exe -m src.bot
```

Nota: no se usa `Activate.ps1` a propósito, porque PowerShell lo
bloquea por defecto. Llamar a `python.exe` directo evita ese error.

Ejemplos de comandos:

```
/ask clima Madrid
/ask calcular 25*4
/ask traducir hola a inglés
```

Escribe `exit` para salir.

Si la librería `datalumina` no está instalada, el bot entra en
**modo demo** y devuelve respuestas simuladas en lugar de crashear.

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
- Las funciones disponibles dependen de lo publicado en
  https://python.datalumina.com/functions; si una no existe, el bot
  devuelve un mensaje de error claro en lugar de crashear.

Gracias quien sea que vea esto :3
