"""
SOLUCION 5  --  en paralelo, y cuando algo falla
================================================

    python soluciones/05_paralelo_y_fallos.py

Lo que cambia frente al ejercicio: `en_paralelo` usa asyncio.gather
(tarea 2) y atrapa el fallo del hijo devolviendolo como texto (tarea 4).

Para ver la tarea 3 y 4 de verdad, descomenta el raise de buscar_en_docs
y corre: el orquestador LEE el error y sigue con lo que si tiene.
"""

import asyncio
import sys
import pathlib
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from pydantic_ai import Agent, RunContext
from pydantic_ai.usage import UsageLimits

from taller import modelo, modo, correr, encabezado
from taller.herramientas import (
    buscar_texto as _buscar,
    leer_archivo as _leer,
    listar_archivos as _listar,
)


explorador_codigo = Agent(
    modelo(),
    instructions=(
        "Buscas SINTOMAS en las notas y los archivos de la raiz del "
        "proyecto. No mires docs/. Maximo 50 palabras."
    ),
)


@explorador_codigo.tool_plain
def buscar_en_notas(patron: str) -> str:
    """Busca un texto en los archivos del sandbox.

    Devuelve lineas 'archivo:numero: contenido', maximo 20.
    Devuelve 'Sin coincidencias' si no hay nada.
    """
    return _buscar(patron)


explorador_docs = Agent(
    modelo(),
    instructions=(
        "Buscas CAUSAS TECNICAS en la carpeta docs/. No mires las notas. "
        "Maximo 50 palabras."
    ),
)


@explorador_docs.tool_plain
def buscar_en_docs(ruta: str = "docs") -> str:
    """Lista lo que hay en una carpeta del sandbox. Usa 'docs' para la de docs.

    Devuelve un nombre por linea. Devuelve texto que empieza con 'ERROR:'
    si la ruta no existe.
    """
    # Descomenta para probar la tarea 3 y 4:
    # raise RuntimeError("se cayo la herramienta de docs (simulado)")
    return _listar(ruta)


@explorador_docs.tool_plain
def leer_doc(ruta: str) -> str:
    """Devuelve el contenido de UN archivo, hasta 4000 caracteres.

    NO acepta carpetas. Devuelve texto que empieza con 'ERROR:' si no existe.
    """
    return _leer(ruta)


orquestador = Agent(
    modelo(),
    instructions=(
        "Coordinas dos exploradores para explicar un bug.\n"
        "Uno te da el sintoma y el otro la causa.\n"
        "Si una herramienta te devuelve un texto que empieza con ERROR, "
        "NO te detengas: usa lo que si tengas y di explicitamente que "
        "parte falta."
    ),
)

# Este ejercicio corre CUATRO subagentes (dos en serie y dos en paralelo),
# asi que LIMITES_ORQ le queda corto. Los topes no son decoracion: si los
# dejas en 8 herramientas, este archivo los toca justo y revienta al
# primer paso extra.
LIMITES_EJ5 = UsageLimits(request_limit=20, tool_calls_limit=16)

RELOJ = {}


@orquestador.tool
async def en_serie(ctx: RunContext[None], pregunta: str) -> str:
    """Investiga sintoma y causa, uno despues del otro. Mas lento.

    Usala solo si te lo piden explicitamente; normalmente usa en_paralelo.
    """
    print("   [en serie...]")
    t0 = time.perf_counter()

    # Toda delegacion va protegida, no solo la de abajo. Una sola sin
    # try/except basta para matar la corrida entera.
    try:
        a = await explorador_codigo.run(pregunta, usage=ctx.usage)
        b = await explorador_docs.run(pregunta, usage=ctx.usage)
    except Exception as e:
        RELOJ["serie"] = time.perf_counter() - t0
        return ("ERROR: uno de los exploradores se cayo (%s: %s). "
                "No tengo las dos partes." % (type(e).__name__, e))

    RELOJ["serie"] = time.perf_counter() - t0
    return "SINTOMA: %s\nCAUSA: %s" % (a.output, b.output)


@orquestador.tool
async def en_paralelo(ctx: RunContext[None], pregunta: str) -> str:
    """Investiga sintoma y causa a la vez. Esta es la que debes usar.

    Devuelve las dos partes. Si una falla, devuelve la otra y lo dice.
    """
    print("   [en paralelo...]")
    t0 = time.perf_counter()

    try:
        # tarea 2: los dos arrancan a la vez. gather los espera a los dos.
        a, b = await asyncio.gather(
            explorador_codigo.run(pregunta, usage=ctx.usage),
            explorador_docs.run(pregunta, usage=ctx.usage),
        )
    except Exception as e:
        # tarea 4: el error se DEVUELVE, no se lanza. El padre lo lee.
        RELOJ["paralelo"] = time.perf_counter() - t0
        return ("ERROR: uno de los exploradores se cayo (%s: %s). "
                "No tengo las dos partes." % (type(e).__name__, e))

    RELOJ["paralelo"] = time.perf_counter() - t0
    return "SINTOMA: %s\nCAUSA: %s" % (a.output, b.output)


OBJETIVO = ("Explica el bug del proyecto: el sintoma y la causa. "
            "Usa en_serie primero y despues en_paralelo, para comparar.")


def main():
    encabezado("Solucion 5 - en paralelo, y cuando algo falla")

    resultado = correr(orquestador, OBJETIVO, limites=LIMITES_EJ5)

    print("\nRESPUESTA FINAL:")
    print(resultado.output)

    print("\n--- reloj de pared ---")
    for nombre in ("serie", "paralelo"):
        if nombre in RELOJ:
            print("%-9s %6.2f s" % (nombre + ":", RELOJ[nombre]))
    if len(RELOJ) == 2 and RELOJ["paralelo"] > 0:
        print("paralelo fue %.1fx mas rapido de reloj"
              % (RELOJ["serie"] / RELOJ["paralelo"]))
    print("\nOJO: el reloj baja, el gasto NO. Son las mismas peticiones.")

    print("\n--- lo que gasto ---")
    print("peticiones al modelo:    %d" % resultado.usage.requests)
    print("herramientas ejecutadas: %d" % resultado.usage.tool_calls)
    if modo() == "test":
        print("\n(En MODO=test la diferencia de reloj es chica: TestModel")
        print(" responde de inmediato. Corre en MODO=gemini para verla.)")


if __name__ == "__main__":
    main()
