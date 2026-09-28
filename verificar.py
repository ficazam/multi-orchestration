"""
verificar.py  --  corre esto ANTES del taller.

    python verificar.py

Si sale todo OK, llegas el lunes listo para trabajar.
Si algo falla, escribe al canal con lo que imprime esto.
"""

import os
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

OK, MAL, AVISO = "  OK   ", " FALLA ", " AVISO "
fallas = 0


def check(etiqueta, cond, ayuda="", critico=True):
    global fallas
    print("[%s] %s" % (OK if cond else (MAL if critico else AVISO), etiqueta))
    if not cond:
        if ayuda:
            print("         -> %s" % ayuda)
        if critico:
            fallas += 1
    return cond


print("\n=== Verificacion del entorno ===\n")

v = sys.version_info
check("Python %d.%d.%d (se necesita 3.10+)" % v[:3], v >= (3, 10),
      "Instala Python 3.10 o mas nuevo.")

raiz = pathlib.Path(__file__).resolve().parent
for c in ("taller", "ejercicios", "soluciones", "sandbox"):
    check("carpeta %s/" % c, (raiz / c).is_dir(), "Vuelve a clonar el repo.")

try:
    import pydantic_ai
    check("pydantic-ai instalado (%s)" % pydantic_ai.__version__, True)
except ImportError:
    check("pydantic-ai instalado", False,
          "pip install -r requirements.txt")

try:
    from taller import modelo, modo, correr
    from taller.herramientas import buscar_texto
    check("import de taller/", True)
except Exception as e:
    check("import de taller/", False, "Error: %s" % e)

try:
    salida = buscar_texto("412")
    check("las herramientas locales corren", "notas.txt" in salida,
          "Salida inesperada: %r" % salida[:100])
except Exception as e:
    check("las herramientas locales corren", False, "Error: %s" % e)

# Dos formas de intentar salirse: subir un nivel, y una carpeta hermana
# cuyo nombre EMPIEZA igual que el sandbox. La segunda es la que se cuela
# si la comprobacion compara texto en vez de rutas.
try:
    from taller.herramientas import leer_archivo
    escapes = ["../taller/config.py", "../sandbox_malo/x.txt", "../../secreto.txt"]
    malas = [r for r in escapes if not str(leer_archivo(r)).startswith("ERROR")]
    check("el sandbox bloquea rutas de afuera", not malas,
          "Estas rutas se colaron: %s -- avisa en el canal." % malas)
except Exception as e:
    check("el sandbox bloquea rutas de afuera", False, "Error: %s" % e)

# Un agente completo, sin red y sin llave.
try:
    os.environ["MODO"] = "test"
    from pydantic_ai import Agent
    from taller import modelo as _modelo
    a = Agent(_modelo(), instructions="prueba")

    @a.tool_plain
    def eco(texto: str) -> str:
        """Devuelve el mismo texto."""
        return texto

    r = a.run_sync("di hola")
    check("un agente corre de punta a punta (MODO=test, sin llave)",
          r.usage.requests >= 1)
except Exception as e:
    check("un agente corre de punta a punta", False, "Error: %s" % e)

print()

llave = bool(os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY"))
check("GEMINI_API_KEY definida", llave,
      "Sacala gratis en https://aistudio.google.com  "
      "(sin llave puedes trabajar en MODO=test)", critico=False)

print("\n" + "=" * 52)
if fallas == 0:
    print("Todo lo critico esta OK. Prueba:")
    print("    python ejercicios/01_herramientas.py")
    if not llave:
        print("\nSin llave vas a trabajar en MODO=test (respuestas de prueba).")
        print("Consigue la llave de Google AI Studio antes del lunes:")
        print("es gratis, no pide tarjeta, y toma dos minutos.")
else:
    print("Hay %d problema(s) critico(s). Resuelvelos antes del taller." % fallas)
print("=" * 52 + "\n")

sys.exit(1 if fallas else 0)
