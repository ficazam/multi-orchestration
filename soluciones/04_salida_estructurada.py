"""
SOLUCION 4  --  la salida estructurada
======================================

    python soluciones/04_salida_estructurada.py

Lo que cambia frente al ejercicio: el campo `confianza` en el esquema
(tarea 3) y la comprobacion del orquestador antes de actuar (tarea 2).

Fijate en lo unico que importa de este archivo: la comprobacion son DOS
lineas de Python. Con prosa, comprobar lo mismo habria requerido otra
llamada al modelo preguntandole "oye, encontraste la causa o no?".
"""

import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from pydantic import BaseModel
from pydantic_ai import Agent, RunContext

from taller import modelo, correr, encabezado, LIMITES_ORQ
from taller.herramientas import (
    buscar_texto as _buscar,
    leer_archivo as _leer,
)


class Hallazgo(BaseModel):
    """Lo que el explorador tiene que devolver. Nada mas, nada menos."""

    archivo: str
    linea: int
    sintoma: str
    causa: str | None = None
    confianza: int = 0          # tarea 3: el esquema ES la instruccion


explorador = Agent(
    modelo(),
    output_type=Hallazgo,
    instructions=(
        "Eres un subagente de exploracion. SOLO LEES, nunca escribes.\n"
        "Busca en los archivos el bug que este reportado y devuelvelo "
        "en el esquema Hallazgo.\n"
        "La causa casi nunca esta en el mismo archivo que el sintoma: "
        "si no la encuentras, deja causa en null. No la inventes.\n"
        "En confianza pon de 0 a 10 que tan seguro estas."
    ),
)


@explorador.tool_plain
def buscar_texto(patron: str) -> str:
    """Busca un texto en todos los archivos del sandbox.

    Devuelve lineas 'archivo:numero: contenido', maximo 20.
    Devuelve 'Sin coincidencias' si no hay nada.
    """
    return _buscar(patron)


@explorador.tool_plain
def leer_archivo(ruta: str) -> str:
    """Devuelve el contenido de UN archivo, hasta 4000 caracteres.

    NO acepta carpetas. Devuelve texto que empieza con 'ERROR:' si no existe.
    """
    return _leer(ruta)


orquestador = Agent(
    modelo(),
    instructions=(
        "Coordinas subagentes para resolver una tarea sobre un proyecto.\n"
        "No investigas tu mismo: delegas.\n"
        "Si una herramienta te dice que falta informacion, NO inventes: "
        "dilo en tu respuesta final."
    ),
)


@orquestador.tool
async def investigar(ctx: RunContext[None], pregunta: str) -> str:
    """Investiga el bug del proyecto y devuelve archivo, linea, sintoma y causa.

    Devuelve un texto que empieza con 'INCOMPLETO:' si no pudo determinar
    la causa. En ese caso no te inventes la causa: reportalo.
    """
    print("   [delegando al explorador...]")
    resultado = await explorador.run(pregunta, usage=ctx.usage)
    hallazgo = resultado.output

    print("   [tipo que devolvio el subagente: %s]" % type(hallazgo).__name__)
    print("   [%r]" % (hallazgo,))

    # AQUI ESTA TODO EL EJERCICIO: el padre comprueba en vez de creer.
    if not hallazgo.causa:
        return ("INCOMPLETO: encontre el sintoma en %s:%d pero no la causa. "
                "No la inventes." % (hallazgo.archivo, hallazgo.linea))

    return ("%s:%d  sintoma: %s  |  causa: %s  (confianza %d/10)"
            % (hallazgo.archivo, hallazgo.linea, hallazgo.sintoma,
               hallazgo.causa, hallazgo.confianza))


OBJETIVO = "Averigua que bug esta reportado en el proyecto."


def main():
    encabezado("Solucion 4 - la salida estructurada")

    resultado = correr(orquestador, OBJETIVO, limites=LIMITES_ORQ)

    print("\nRESPUESTA FINAL:")
    print(resultado.output)

    print("\n--- lo que gasto ---")
    print("peticiones al modelo:    %d" % resultado.usage.requests)
    print("herramientas ejecutadas: %d" % resultado.usage.tool_calls)


if __name__ == "__main__":
    main()
