"""
EJERCICIO 4  --  la salida estructurada
=======================================

    python ejercicios/04_salida_estructurada.py

En el ejercicio 3 el explorador devolvia PROSA: ochenta palabras en espanol.
El orquestador tenia que leerlas y creerselas. No podia comprobar nada.

Aqui el subagente devuelve un OBJETO. Se declara asi:

    class Hallazgo(BaseModel):
        archivo: str
        linea: int
        sintoma: str
        causa: str | None = None

    explorador = Agent(modelo(), output_type=Hallazgo, instructions=...)

Y entonces `resultado.output` ya no es un string: es un Hallazgo, validado
por Pydantic antes de que tu codigo lo vea.

POR QUE ESTO CAMBIA TODO PARA TU MVP:

  1. EL PADRE PUEDE COMPROBAR. Con prosa, "no encontre la causa" y "la
     causa es X" son los dos un string; hay que leerlos. Con un objeto,
     `if not hallazgo.causa` es una linea de Python. El orquestador deja
     de creer y empieza a verificar.

  2. EL MODELO YA NO ELIGE EL FORMATO. Sin output_type le pides "responde
     en este formato" en el prompt y a veces obedece. Con output_type no
     es una peticion: si no encaja en el esquema, Pydantic AI lo hace
     reintentar. El formato deja de ser suerte.

  3. SE ACABAN LOS PARSEOS. Nadie tiene que sacar el numero de linea de
     una frase con una expresion regular a las dos de la manana.

  4. ES MAS BARATO. Un objeto de cuatro campos ocupa menos tokens en el
     historial del padre que ochenta palabras de prosa.

---------------------------------------------------------------------------
TAREAS  (18 min)
---------------------------------------------------------------------------

1. Corre el archivo. Fijate en el tipo que imprime: no es str, es Hallazgo.

2. TAREA PRINCIPAL: el orquestador tiene que COMPROBAR antes de actuar.
   Esta marcado con TODO abajo. La idea: si el hallazgo viene sin causa,
   no sigas: devuelve que falta y deja que el orquestador decida.
   Con prosa esto no se puede escribir.

3. Agregale un campo a Hallazgo. Por ejemplo:

       confianza: int      # de 0 a 10

   Corre otra vez. No tocaste el prompt y el modelo ya llena el campo:
   el esquema ES la instruccion.

4. Rompe el esquema a proposito: pon `linea: int` y en las instrucciones
   pidele que devuelva la linea como texto ("linea cuarenta y dos").
   Mira lo que hace Pydantic AI: no te pasa basura, reintenta.

5. Compara el costo. Imprime len(str(hallazgo)) y compara con los ~400
   caracteres de prosa del ejercicio 3. Eso es lo que entra al historial
   del padre en cada vuelta.

6. Cual de tus subagentes deberia devolver un objeto en vez
   de un parrafo? Pista: todos los que alimentan una decision del padre.
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


# ===========================================================================
# EL ESQUEMA  --  esto es el contrato, y tambien es el prompt
# ===========================================================================

class Hallazgo(BaseModel):
    """Lo que el explorador tiene que devolver. Nada mas, nada menos."""

    archivo: str
    linea: int
    sintoma: str
    causa: str | None = None

    # TODO (tarea 3): agregale un campo y corre otra vez sin tocar el prompt.


# ===========================================================================
# EL SUBAGENTE  --  igual que antes, pero con output_type
# ===========================================================================

explorador = Agent(
    modelo(),
    output_type=Hallazgo,
    instructions=(
        "Eres un subagente de exploracion. SOLO LEES, nunca escribes.\n"
        "Busca en los archivos el bug que este reportado y devuelvelo "
        "en el esquema Hallazgo.\n"
        "La causa casi nunca esta en el mismo archivo que el sintoma: "
        "si no la encuentras, deja causa en null. No la inventes."
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


# ===========================================================================
# EL ORQUESTADOR
# ===========================================================================

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

    # -----------------------------------------------------------------------
    # TODO (tarea 2)  --  COMPRUEBA ANTES DE ACTUAR
    # -----------------------------------------------------------------------
    # Esto es lo que la prosa no te deja hacer. El hallazgo puede venir
    # sin causa: el subagente hizo su trabajo y no la encontro.
    #
    # Escribe la comprobacion:
    #   - si hallazgo.causa esta vacia, devuelve un texto que empiece con
    #     'INCOMPLETO:' explicando que falta (el docstring de arriba ya se
    #     lo prometio al orquestador: cumplelo)
    #   - si esta, devuelve las cuatro cosas en una linea
    #
    # Dos lineas de Python. Con un parrafo de prosa harian falta un modelo
    # y una oracion.
    # -----------------------------------------------------------------------

    return str(hallazgo)   # <-- reemplaza esto por tu comprobacion


OBJETIVO = "Averigua que bug esta reportado en el proyecto."


def main():
    encabezado("Ejercicio 4 - la salida estructurada")

    resultado = correr(orquestador, OBJETIVO, limites=LIMITES_ORQ)

    print("\nRESPUESTA FINAL:")
    print(resultado.output)

    print("\n--- lo que gasto ---")
    print("peticiones al modelo:    %d" % resultado.usage.requests)
    print("herramientas ejecutadas: %d" % resultado.usage.tool_calls)


if __name__ == "__main__":
    main()
