"""
SOLUCION 1  --  la descripcion ES el prompt
============================================

    python soluciones/01_herramientas.py

Ya sabes registrar herramientas con @agente.tool_plain. Lo que casi nadie
te dijo en el taller pasado: el modelo NO ve tu codigo. Ve el nombre de la
funcion, el docstring y los tipos. Eso es toda la interfaz.

Un docstring vago no produce un error. Produce una llamada equivocada
hecha con total confianza.

---------------------------------------------------------------------------
TAREAS  (20 min)
---------------------------------------------------------------------------

1. Corre el archivo. El agente tiene UNA herramienta con un docstring malo
   a proposito. Mira que hace.

2. Arregla el docstring de buscar_texto. Un docstring util dice:
      - que devuelve y en que formato
      - que NO hace / que no acepta
      - que significa el resultado vacio
   Corre otra vez y compara.

3. ESCRIBE UNA HERRAMIENTA DESDE CERO. Elige una de estas tres:
      a) contar_lineas(ruta)     -> cuantas lineas tiene un archivo
      b) listar_archivos(ruta)   -> que hay en una carpeta
      c) resumir_pendientes()    -> cuantos pendientes hay hechos y cuantos no
   Las implementaciones de (a) y (b) ya existen en taller/herramientas.py;
   tu trabajo es el registro y sobre todo el DOCSTRING.
   Si eliges (c), escribela completa.

4. Cambia OBJETIVO a algo que necesite tus dos herramientas encadenadas.
   Ejemplo: "Busca el ticket 412 y dime cuantas lineas tiene el archivo
   donde aparece."

5. Rompe algo: pide un archivo que no existe. Fijate en que el agente LEE
   el error y reintenta en vez de morirse. Eso pasa porque la funcion
   devuelve el error como texto en lugar de lanzar excepcion.
"""

import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from pydantic_ai import Agent

from taller import modelo, correr, encabezado
from taller.herramientas import buscar_texto as _buscar


agente = Agent(
    modelo(),
    instructions=(
        "Eres un asistente que trabaja sobre los archivos de un proyecto. "
        "Usa las herramientas disponibles para responder. "
        "Si una herramienta devuelve un texto que empieza con ERROR, leelo "
        "y corrige tu siguiente llamada."
    ),
)


# ---------------------------------------------------------------------------
# HERRAMIENTA 1  --  el docstring esta malo a proposito (tarea 2)
# ---------------------------------------------------------------------------

@agente.tool_plain
def buscar_texto(patron: str) -> str:
    """Busca un texto literal en todos los archivos del sandbox.

    Devuelve hasta 20 lineas con formato 'archivo:numero: contenido'.
    La busqueda NO distingue mayusculas. No acepta expresiones regulares.
    Devuelve "Sin coincidencias para 'X'." si no encuentra nada, lo cual
    significa que el texto no esta, no que la llamada fallo.
    """
    return _buscar(patron)


# ---------------------------------------------------------------------------
# HERRAMIENTA 2  --  una version resuelta (opcion a)
# ---------------------------------------------------------------------------

@agente.tool_plain
def contar_lineas(ruta: str) -> str:
    """Cuenta las lineas de UN archivo de texto del sandbox.

    Devuelve solo el numero, como texto. La ruta es relativa al sandbox
    e incluye la extension, por ejemplo 'notas.txt'.
    NO acepta carpetas; para ver que archivos hay usa listar_archivos.
    Devuelve un texto que empieza con 'ERROR:' si la ruta no existe.
    """
    from taller.herramientas import contar_lineas as _contar
    return _contar(ruta)


OBJETIVO = ("Busca el ticket 412 y dime cuantas lineas tiene "
            "el archivo donde aparece.")


def main():
    encabezado("Ejercicio 1 - la descripcion es el prompt")

    resultado = correr(agente, OBJETIVO)

    print("\nRESPUESTA:")
    print(resultado.output)

    print("\n--- lo que gasto ---")
    print("peticiones al modelo: %d" % resultado.usage.requests)
    print("herramientas usadas:  %d" % resultado.usage.tool_calls)


if __name__ == "__main__":
    main()
