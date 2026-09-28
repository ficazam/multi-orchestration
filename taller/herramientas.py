"""
herramientas.py  --  las funciones que los agentes pueden ejecutar.

Son funciones normales de Python. Lo que las convierte en herramientas es
registrarlas con @agente.tool_plain, y eso lo haces tu en los ejercicios.

Fijate en dos cosas:

1. Ninguna lanza excepciones hacia afuera. Devuelven el error como TEXTO.
   Es a proposito: si la funcion revienta, el agente se muere. Si devuelve
   "ERROR: el archivo no existe", el agente lo LEE y puede corregir.

2. Todas pasan por _ruta_segura(). Un agente no puede tocar nada fuera de
   sandbox/, aunque el modelo lo decida. Eso es una garantia del CODIGO.
   Un prompt que dice "no borres nada" es solo una recomendacion.
"""

import pathlib

SANDBOX = (pathlib.Path(__file__).resolve().parent.parent / "sandbox").resolve()


def _ruta_segura(ruta):
    """Resuelve una ruta contra el sandbox y falla si se sale de el.

    Compara por CONTENCION de rutas, no por prefijo de texto. Un prefijo
    de texto dejaria pasar una carpeta hermana llamada 'sandbox_malo':
    su ruta empieza con la del sandbox pero esta afuera.
    """
    destino = (SANDBOX / ruta).resolve()
    try:
        destino.relative_to(SANDBOX)
    except ValueError:
        raise ValueError("fuera del sandbox")
    return destino


def listar_archivos(ruta: str = ".") -> str:
    try:
        destino = _ruta_segura(ruta)
    except ValueError:
        return "ERROR: esa ruta esta fuera del sandbox."
    if not destino.exists():
        return "ERROR: la ruta '%s' no existe." % ruta
    if not destino.is_dir():
        return "ERROR: '%s' no es una carpeta, es un archivo." % ruta
    nombres = sorted(p.name + ("/" if p.is_dir() else "") for p in destino.iterdir())
    return "\n".join(nombres) if nombres else "(carpeta vacia)"


def leer_archivo(ruta: str) -> str:
    try:
        destino = _ruta_segura(ruta)
    except ValueError:
        return "ERROR: esa ruta esta fuera del sandbox."
    if not destino.exists():
        return "ERROR: el archivo '%s' no existe." % ruta
    if destino.is_dir():
        return "ERROR: '%s' es una carpeta. Usa listar_archivos." % ruta
    return destino.read_text(encoding="utf-8")[:4000]


def escribir_archivo(ruta: str, contenido: str) -> str:
    try:
        destino = _ruta_segura(ruta)
    except ValueError:
        return "ERROR: esa ruta esta fuera del sandbox."
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(contenido, encoding="utf-8")
    return "Escrito %s (%d caracteres)." % (ruta, len(contenido))


def buscar_texto(patron: str) -> str:
    """Busca un texto en todos los archivos del sandbox."""
    hits = []
    for p in sorted(SANDBOX.rglob("*")):
        if not p.is_file():
            continue
        try:
            for i, linea in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
                if patron.lower() in linea.lower():
                    rel = p.relative_to(SANDBOX)
                    hits.append("%s:%d: %s" % (rel, i, linea.strip()[:90]))
        except Exception:
            continue
    if not hits:
        return "Sin coincidencias para '%s'." % patron
    return "\n".join(hits[:20])


def contar_lineas(ruta: str) -> str:
    try:
        destino = _ruta_segura(ruta)
    except ValueError:
        return "ERROR: esa ruta esta fuera del sandbox."
    if not destino.is_file():
        return "ERROR: '%s' no es un archivo." % ruta
    return str(len(destino.read_text(encoding="utf-8").splitlines()))
