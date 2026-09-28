"""
config.py  --  de donde sale el modelo y cuales son los limites.

Dos modos, se cambian con una variable de entorno:

    MODO=test     TestModel de Pydantic AI. No necesita API key, no usa red.
                  Sirve para verificar que tu codigo corre.
    MODO=gemini   Gemini de verdad. Necesita GEMINI_API_KEY.

    export MODO=gemini
    export GEMINI_API_KEY=tu_llave

En Windows PowerShell:
    $env:MODO="gemini"
    $env:GEMINI_API_KEY="tu_llave"
"""

import os
import pathlib
import sys

from pydantic_ai.usage import UsageLimits


# ---------------------------------------------------------------------------
# .env  --  para que no tengas que exportar las variables en cada terminal
# ---------------------------------------------------------------------------
# Copia .env.ejemplo a .env y pon tu llave ahi. Son diez lineas de codigo
# a proposito: no hace falta instalar nada, y puedes leer que hace.
#
# Lo que YA este en el entorno manda sobre el archivo. Asi un
# `export MODO=test` de un solo uso le gana al .env sin editarlo.

def _cargar_env():
    archivo = pathlib.Path(__file__).resolve().parent.parent / ".env"
    if not archivo.exists():
        return
    for linea in archivo.read_text(encoding="utf-8").splitlines():
        linea = linea.strip()
        if not linea or linea.startswith("#") or "=" not in linea:
            continue
        clave, _, valor = linea.partition("=")
        os.environ.setdefault(clave.strip(), valor.strip().strip("\"'"))


_cargar_env()


# El modelo gratuito de Google AI Studio.
# OJO: confirma el ID exacto en https://aistudio.google.com  --  Google
# cambia los nombres seguido y un ID viejo da 404.
MODELO_GEMINI = os.environ.get("MODELO_GEMINI", "google-gla:gemini-2.5-flash")


def modo():
    return os.environ.get("MODO", "test").lower().strip()


def modelo():
    """Devuelve el modelo que van a usar todos los agentes del taller."""
    m = modo()

    if m == "test":
        from pydantic_ai.models.test import TestModel
        return TestModel()

    if m == "gemini":
        if not (os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")):
            print("ERROR: MODO=gemini pero no hay GEMINI_API_KEY.")
            print("       Saca una gratis en https://aistudio.google.com")
            print("       o usa MODO=test para trabajar sin llave.")
            sys.exit(1)
        return MODELO_GEMINI

    print("ERROR: MODO='%s' no existe. Usa 'test' o 'gemini'." % m)
    sys.exit(1)


# ---------------------------------------------------------------------------
# LIMITES  --  esto no es opcional
# ---------------------------------------------------------------------------
# La capa gratuita de Gemini permite unas 5-15 peticiones POR MINUTO.
# Un agente con un bucle suelto se come eso en una corrida.
#
#   request_limit     cuantas llamadas al modelo como maximo
#   tool_calls_limit  cuantas herramientas puede ejecutar como maximo
#
# Son el MAX_STEPS del que hablamos: sin esto, un bucle roto gasta
# tu cuota (o tu dinero) sin techo.

LIMITES = UsageLimits(request_limit=6, tool_calls_limit=5)

# Para el orquestador con subagentes hace falta mas margen, porque cada
# delegacion suma peticiones al total del padre.
LIMITES_ORQ = UsageLimits(request_limit=12, tool_calls_limit=8)


# ---------------------------------------------------------------------------
# correr()  --  envuelve agent.run_sync y traduce los errores feos
# ---------------------------------------------------------------------------

def correr(agente, prompt, limites=None, **kw):
    """Corre un agente y explica los errores comunes en castellano."""
    try:
        return agente.run_sync(prompt, usage_limits=limites or LIMITES, **kw)

    except Exception as e:
        texto = str(e)

        if "429" in texto or "RESOURCE_EXHAUSTED" in texto or "quota" in texto.lower():
            print("\n--- LIMITE DE TASA ---")
            print("Google te corto por pedir muy rapido. NO es tu codigo.")
            print("Espera unos 60 segundos y vuelve a correr.")
            print("Si sigue, cambia a MODO=test y sigue el taller igual.")
            raise SystemExit(1)

        if "404" in texto and "model" in texto.lower():
            print("\n--- MODELO NO ENCONTRADO ---")
            print("El ID '%s' no existe o no esta en tu cuota." % MODELO_GEMINI)
            print("Revisa el nombre exacto en https://aistudio.google.com")
            print("y exportalo:  export MODELO_GEMINI=google-gla:<id-correcto>")
            raise SystemExit(1)

        if "API key" in texto or "401" in texto or "403" in texto:
            print("\n--- LLAVE INVALIDA ---")
            print("Revisa GEMINI_API_KEY. Si no tienes, usa MODO=test.")
            raise SystemExit(1)

        if "limit" in texto.lower() and "exceed" in texto.lower():
            print("\n--- TOPE ALCANZADO ---")
            print("El agente llego al limite de peticiones o de herramientas.")
            print("Eso es UsageLimits haciendo su trabajo: evito un bucle sin techo.")
            print("Si es legitimo, sube el limite en taller/config.py.")
            raise SystemExit(1)

        raise


def encabezado(titulo):
    print("=" * 60)
    print(titulo)
    print("modo: %s%s" % (modo(), "" if modo() == "test" else "  (%s)" % MODELO_GEMINI))
    print("=" * 60)
