"""Utility helpers for the ChatBot project."""

# Simple utility function that can be expanded later.
def format_message(message: str) -> str:
    """Add a textual tag to the chatbot's messages (no emojis)."""
    tags = {
        "info":    "[INFO]",
        "success": "[OK]",
        "error":   "[ERROR]",
        "warning": "[WARN]",
    }
    return f"{tags.get(message.split()[0].lower(), '')} {message}"