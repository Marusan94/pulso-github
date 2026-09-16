"""Taxonomía compartida: categoría y tipo por nombre/descripción.

Unifica las variantes que vivían duplicadas en fetch_top.py y
fetch_trending.py (la de trending traía "voice"/"tts" de más).
"""

PERMISIVAS = ["MIT", "Apache-2.0", "BSD-2-Clause", "BSD-3-Clause", "ISC", "CC0-1.0"]


def categoria(name, desc):
    t = ((name or "") + " " + (desc or "")).lower()
    if any(k in t for k in ["llm", "gpt", "agent", "ai ", "artificial", "diffusion", "stable",
                            "langchain", "openclaw", "hermes", "mcp", "skill", "transformer",
                            "chatbot", "voice", "tts"]):
        return "IA/LLM"
    if any(k in t for k in ["react", "vue", "angular", "frontend", "css", "tailwind",
                            "ui ", "component"]):
        return "Frontend"
    if any(k in t for k in ["awesome", "list of", "curated", "roadmap", "interview",
                            "tutorial", "book", "course", "learn", "primer", "university"]):
        return "Educación/Recursos"
    if any(k in t for k in ["api", "framework", "server", "database", "kubernetes", "docker",
                            "cli ", "terminal", "linux", "kernel", "self-host"]):
        return "Backend/DevOps"
    if any(k in t for k in ["admin", "dashboard", "template", "boilerplate"]):
        return "Templates"
    if any(k in t for k in ["security", "hack", "cheat", "exploit"]):
        return "Seguridad"
    return "DevTools"


def tipo(name, desc):
    t = ((name or "") + " " + (desc or "")).lower()
    if "awesome" in t or "list of" in t or "curated list" in t:
        return "awesome-list"
    if any(k in t for k in ["tutorial", "course", "book", "roadmap", "university", "primer", "learn"]):
        return "educativo"
    if any(k in t for k in ["framework", "library", "kernel"]):
        return "framework/librería"
    return "herramienta/app"
