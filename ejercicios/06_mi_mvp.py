"""
EJERCICIO 6  --  el esqueleto de TU MVP
=======================================

    python ejercicios/06_mi_mvp.py

Este archivo es tuyo. Sale del taller contigo y lo sigues el sabado.

No copies el ejemplo de archivos del ejercicio 3: pon aqui lo que tu
equipo va a construir de verdad.

---------------------------------------------------------------------------
PRIMERO, EN PAPEL (5 min, antes de escribir codigo)
---------------------------------------------------------------------------

Contesta estas cuatro. Si no puedes, todavia no sabes que vas a construir.

  1. Que hace tu MVP, en UNA frase?

  2. Que subagentes necesita? Por cada uno:
        nombre:
        que hace:
        herramientas que SI tiene:
        herramientas que NO tiene:   <-- esta es la importante

  3. Por cada subagente, cual de estas razones justifica separarlo?
        [ ] aisla contexto (quema muchos tokens y devuelve poco)
        [ ] acota permisos (no debe poder hacer X)
        [ ] menos herramientas por decision
        [ ] modelo distinto
     Si no marcaste ninguna, ese subagente no deberia existir: haz que
     sea una herramienta normal del orquestador.

  4. Cual es el limite de peticiones que le pones? (Acuerdate de la cuota
     gratis: 5-15 por minuto.)

---------------------------------------------------------------------------
DESPUES, EL CODIGO
---------------------------------------------------------------------------

La estructura esta abajo. Llena los TODO. Corre en MODO=test mientras
armas la forma, y cambia a MODO=gemini cuando quieras respuestas reales
(asi no quemas cuota probando).
"""

import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from pydantic_ai import Agent, RunContext
from pydantic_ai.usage import UsageLimits

from taller import modelo, correr, encabezado


# ===========================================================================
# 1. TUS SUBAGENTES
# ===========================================================================

# ---- subagente A ----------------------------------------------------------
# TODO: cambiale el nombre y las instrucciones a lo que TU necesitas.

subagente_a = Agent(
    modelo(),
    instructions=(
        "TODO: que hace este subagente. Se especifico. "
        "Di tambien el formato y el largo maximo de su respuesta, porque "
        "eso es lo que protege el contexto del orquestador."
    ),
)


# TODO: sus herramientas. Solo las que necesita.
#
# @subagente_a.tool_plain
# def mi_herramienta(parametro: str) -> str:
#     """Que devuelve. Que no acepta. Que significa vacio."""
#     return "..."


# ---- subagente B ----------------------------------------------------------
# TODO: el segundo. Si tu MVP solo necesita uno, borra este bloque
#       y dilo en la consulta de arquitectura al final del taller.

subagente_b = Agent(
    modelo(),
    instructions="TODO",
)


# ===========================================================================
# 2. EL ORQUESTADOR
# ===========================================================================

orquestador = Agent(
    modelo(),
    instructions=(
        "TODO: como coordina. Normalmente: no hace el trabajo el mismo, "
        "delega; en que orden llama a los subagentes; cuando se detiene."
    ),
)


CONTEO = {}


@orquestador.tool
async def llamar_a(ctx: RunContext[None], tarea: str) -> str:
    """TODO: el docstring que lee el orquestador para decidir si usar esto.

    Acuerdate del ejercicio 1: di que devuelve, que no hace, y que pasa
    si no encuentra nada.
    """
    antes = ctx.usage.input_tokens
    resultado = await subagente_a.run(tarea, usage=ctx.usage)
    CONTEO["subagente_a"] = (ctx.usage.input_tokens - antes, len(resultado.output))
    return resultado.output


# TODO: registra el subagente B igual que el A.


# ===========================================================================
# 3. LIMITES  --  ponlos antes de la primera corrida, no despues
# ===========================================================================

MIS_LIMITES = UsageLimits(
    request_limit=12,      # TODO: ajusta segun cuantos pasos necesitas
    tool_calls_limit=8,
)


OBJETIVO = "TODO: la tarea que tu MVP tiene que resolver."


def main():
    encabezado("Ejercicio 6 - mi MVP")

    if OBJETIVO.startswith("TODO"):
        print("\nTodavia no llenaste el OBJETIVO.")
        print("Contesta primero las cuatro preguntas del docstring de arriba.")
        return

    resultado = correr(orquestador, OBJETIVO, limites=MIS_LIMITES)

    print("\nRESPUESTA:")
    print(resultado.output)

    print("\n--- contexto ---")
    for nombre, (tokens, chars) in CONTEO.items():
        print("%-12s quemo %5d tokens  ->  devolvio %4d caracteres"
              % (nombre, tokens, chars))

    print("\n--- gasto ---")
    print("peticiones: %d" % resultado.usage.requests)
    print("tools:      %d" % resultado.usage.tool_calls)


if __name__ == "__main__":
    main()
