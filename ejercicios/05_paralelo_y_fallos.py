"""
EJERCICIO 5  --  en paralelo, y cuando algo falla
=================================================

    python ejercicios/05_paralelo_y_fallos.py

Dos cosas que separan un demo que aguanta de uno que se cae en el escenario.

PRIMERA: EN SERIE CONTRA EN PARALELO.

En el ejercicio 3 los subagentes corrian uno detras del otro, porque el
segundo necesitaba lo del primero. Pero cuando dos subagentes NO dependen
uno del otro, esperar al primero para arrancar el segundo es tiempo
regalado. Se arreglan con una linea:

    a, b = await asyncio.gather(
        explorador_codigo.run(pregunta, usage=ctx.usage),
        explorador_docs.run(pregunta, usage=ctx.usage),
    )

Cuesta lo que el mas lento, no la suma de los dos. Ojo: esto NO reduce
peticiones ni tokens. Reduce reloj. Con la cuota gratis sigues pagando
las dos.

SEGUNDA: LOS SUBAGENTES SE CAEN.

La herramienta del orquestador del ejercicio 3 no atrapaba nada. Si el
hijo lanza una excepcion, se muere el padre y se muere la corrida. Y el
sabado, delante del jurado, un subagente SE VA A CAER: un 429, una ruta
mala, un timeout.

La solucion es la misma idea de taller/herramientas.py: devolver el error
como TEXTO en vez de lanzarlo. Si el orquestador lo LEE, decide. Si le
explota, no decide nada.

---------------------------------------------------------------------------
TAREAS  (15 min)
---------------------------------------------------------------------------

1. Corre el archivo. Mira los dos relojes que imprime al final: en serie
   y en paralelo. Con MODO=test la diferencia es chica porque TestModel
   no piensa; en MODO=gemini se ve de verdad.

2. TAREA PRINCIPAL: el bloque `en_paralelo` esta a medias. Completalo con
   asyncio.gather para que los dos exploradores arranquen a la vez.

3. Ahora rompe uno. Descomenta el `raise` que esta en la herramienta
   `buscar_en_docs` y corre. Se cae toda la corrida, no solo el hijo.

4. TAREA 2: atrapa el fallo. Envuelve la llamada al subagente en
   try/except y devuelve el error como texto que empiece con 'ERROR:'.

   OJO, y es el punto entero: tienes que protegerlas LAS DOS, en_serie y
   en_paralelo. Una sola delegacion sin try/except basta para matar la
   corrida completa, y el orquestador llama primero a en_serie. Si solo
   proteges una, no vas a ver ninguna diferencia.

   Corre otra vez con el raise puesto. Ahora el orquestador LEE el fallo
   y sigue con lo que si tiene.

5. Pregunta para el sabado: si un subagente falla y el orquestador sigue,
   quien decide si la respuesta final todavia sirve? (Respuesta: tu, en
   el prompt del orquestador. Dile que hacer con la informacion parcial.)
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


# ===========================================================================
# DOS SUBAGENTES QUE NO DEPENDEN UNO DEL OTRO
# ===========================================================================
# Uno mira el codigo y las notas; el otro mira la carpeta docs/. Ninguno
# necesita lo que encontro el otro: por eso pueden correr a la vez.

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
    # TODO (tarea 3): descomenta esto para simular un subagente que se cae.
    # raise RuntimeError("se cayo la herramienta de docs (simulado)")
    return _listar(ruta)


@explorador_docs.tool_plain
def leer_doc(ruta: str) -> str:
    """Devuelve el contenido de UN archivo, hasta 4000 caracteres.

    NO acepta carpetas. Devuelve texto que empieza con 'ERROR:' si no existe.
    """
    return _leer(ruta)


# ===========================================================================
# EL ORQUESTADOR
# ===========================================================================

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

    a = await explorador_codigo.run(pregunta, usage=ctx.usage)
    b = await explorador_docs.run(pregunta, usage=ctx.usage)

    RELOJ["serie"] = time.perf_counter() - t0
    return "SINTOMA: %s\nCAUSA: %s" % (a.output, b.output)


@orquestador.tool
async def en_paralelo(ctx: RunContext[None], pregunta: str) -> str:
    """Investiga sintoma y causa a la vez. Esta es la que debes usar.

    Devuelve las dos partes. Si una falla, devuelve la otra y lo dice.
    """
    print("   [en paralelo...]")
    t0 = time.perf_counter()

    # -----------------------------------------------------------------------
    # TODO (tarea 2)  --  ARRANCA LOS DOS A LA VEZ
    # -----------------------------------------------------------------------
    # Ahora mismo esto sigue siendo en serie: el segundo await no empieza
    # hasta que termina el primero.
    #
    # Cambialo por asyncio.gather, que recibe las dos corrutinas y devuelve
    # las dos respuestas cuando las dos acabaron:
    #
    #     a, b = await asyncio.gather(
    #         explorador_codigo.run(pregunta, usage=ctx.usage),
    #         explorador_docs.run(pregunta, usage=ctx.usage),
    #     )
    #
    # Fijate que NO lleva await en cada .run(): gather los espera.
    #
    # TODO (tarea 4)  --  Y QUE NO TE MATE UN HIJO
    # Envuelve la llamada en try/except. En el except, devuelve un texto
    # que empiece con 'ERROR:' con lo que fallo. No lo vuelvas a lanzar:
    # el orquestador ya sabe leer errores (mira sus instructions).
    #
    # Y hazlo TAMBIEN en en_serie, ahi arriba. Protege una sola y la
    # corrida se sigue muriendo: el orquestador la llama primero.
    # -----------------------------------------------------------------------

    a = await explorador_codigo.run(pregunta, usage=ctx.usage)
    b = await explorador_docs.run(pregunta, usage=ctx.usage)

    RELOJ["paralelo"] = time.perf_counter() - t0
    return "SINTOMA: %s\nCAUSA: %s" % (a.output, b.output)


OBJETIVO = ("Explica el bug del proyecto: el sintoma y la causa. "
            "Usa en_serie primero y despues en_paralelo, para comparar.")


def main():
    encabezado("Ejercicio 5 - en paralelo, y cuando algo falla")

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
