# Chatbot de IA (Parcial 3)

   (\_/)
  ( •_•)   <-- mapache pixel
  / >(o)

Chatbot de IA construido siguiendo el curso **Python for AI** y la
documentación de **Datalumina Functions**.

## Recursos usados
- Video: https://www.youtube.com/watch?v=ygXn5nV5qFc
- Funciones Datalumina: https://python.datalumina.com/functions

## Requisitos
- Python 3.x
- pip
- `datalumina-functions` (y `requests`)

## Instalación

```bash
# 1. Clonar el repositorio
git clone https://github.com/chrisamour/chatbot-parcial3.git
cd chatbot-parcial3

# 2. Crear y activar entorno virtual
python -m venv .venv
source .venv/bin/activate        # Linux / WSL
# .venv\Scripts\activate         # Windows (PowerShell)

# 3. Instalar dependencias
pip install -r requirements.txt
```

## Uso

```bash
python -m src.bot
```

Ejemplos de comandos:

```
/ask clima Madrid
/ask calcular 25*4
/ask traducir hola a inglés
```

Escribe `exit` para salir.

## Estructura

```
chatbot-parcial3/
├── src/
│   ├── __init__.py
│   ├── bot.py          # Motor del chatbot + mapache pixel
│   └── utils.py        # Funciones auxiliares
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

¡Gracias por usar el chatbot! 
   (\_/)
  ( •_•)   <-- mapache pixel
  / >(o)
