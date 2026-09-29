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
MODELO_GEMINI = os.environ.get("MODELO_GEMINI", "google:gemini-2.5-flash")


def modo():
    return os.environ.get("MODO", "test").lower().strip()


def modelo():
    """Devuelve el modelo que van a usar todos los agentes del taller."""
    m = modo()

    if m == "test":
        from pydantic_ai.models.test import TestModel
        return TestModel()

    if m == "gemini":
        google = os.environ.get("GOOGLE_API_KEY")
        gemini = os.environ.get("GEMINI_API_KEY")

        if not (gemini or google):
            print("ERROR: MODO=gemini pero no hay GEMINI_API_KEY.")
            print("       Saca una gratis en https://aistudio.google.com")
            print("       o usa MODO=test para trabajar sin llave.")
            sys.exit(1)

        # Pydantic AI usa GOOGLE_API_KEY y DESCARTA GEMINI_API_KEY cuando
        # las dos estan puestas. Es la causa numero uno de "la llave es
        # correcta pero dice que es invalida": una GOOGLE_API_KEY vieja de
        # otro proyecto tapando la nueva.
        if google and gemini and google != gemini:
            print("AVISO: GOOGLE_API_KEY y GEMINI_API_KEY son distintas.")
            print("       Pydantic AI va a usar GOOGLE_API_KEY y a ignorar")
            print("       GEMINI_API_KEY. Si la buena es la de GEMINI:")
            print("         PowerShell:  Remove-Item Env:GOOGLE_API_KEY")
            print("         bash:        unset GOOGLE_API_KEY")

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

        def detalle():
            """El error original. Sin esto no se puede depurar nada."""
            recorte = texto if len(texto) <= 500 else texto[:500] + " [...]"
            print("\nlo que dijo la libreria:")
            print("  %s: %s" % (type(e).__name__, recorte))

        if "429" in texto or "RESOURCE_EXHAUSTED" in texto or "quota" in texto.lower():
            print("\n--- LIMITE DE TASA ---")
            print("Google te corto por pedir muy rapido. NO es tu codigo.")
            print("Espera unos 60 segundos y vuelve a correr.")
            print("Si sigue, cambia a MODO=test y sigue el taller igual.")
            detalle()
            raise SystemExit(1)

        if "404" in texto and "model" in texto.lower():
            print("\n--- MODELO NO ENCONTRADO ---")
            print("El ID '%s' no existe o no esta en tu cuota." % MODELO_GEMINI)
            print("Revisa el nombre exacto en https://aistudio.google.com")
            print("y exportalo:  export MODELO_GEMINI=google:<id-correcto>")
            print("O corre:  python listar_modelos.py")
            detalle()
            raise SystemExit(1)

        if "API key" in texto or "401" in texto or "403" in texto:
            print("\n--- LLAVE INVALIDA ---")
            print("Corre esto, que te dice exactamente cual es el problema:")
            print("    python listar_modelos.py")
            print("")
            print("Lo mas comun, en orden:")
            print("  1. Tienes GOOGLE_API_KEY vieja tapando GEMINI_API_KEY.")
            print("     Pydantic AI prefiere GOOGLE_API_KEY y descarta la otra.")
            print("  2. La llave quedo mal copiada (sobra un espacio, falta")
            print("     un caracter, o se pego con comillas).")
            print("  3. La llave tiene restricciones de API o de IP.")
            detalle()
            raise SystemExit(1)

        if "limit" in texto.lower() and "exceed" in texto.lower():
            print("\n--- TOPE ALCANZADO ---")
            print("El agente llego al limite de peticiones o de herramientas.")
            print("Eso es UsageLimits haciendo su trabajo: evito un bucle sin techo.")
            print("Si es legitimo, sube el limite en taller/config.py.")
            detalle()
            raise SystemExit(1)

        raise


def encabezado(titulo):
    print("=" * 60)
    print(titulo)
    print("modo: %s%s" % (modo(), "" if modo() == "test" else "  (%s)" % MODELO_GEMINI))
    print("=" * 60)
