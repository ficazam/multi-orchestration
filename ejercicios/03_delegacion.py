"""
EJERCICIO 3  --  el bucle multi-agente
======================================

    python ejercicios/03_delegacion.py

ESTE ES EL EJERCICIO CENTRAL DEL TALLER. Lo que salgas construyendo aqui
es el esqueleto de tu MVP.

La idea, en una frase: un subagente es un agente normal, llamado desde
DENTRO de una herramienta del orquestador.

    @orquestador.tool
    async def explorar(ctx, pregunta: str) -> str:
        resultado = await explorador.run(pregunta, usage=ctx.usage)
        return resultado.output

Para el orquestador eso es una herramienta cualquiera. No sabe que por
dentro corrio otro agente con su propio bucle.

POR QUE IMPORTA (y no es porque "suene organizado"):

  1. AISLAMIENTO DE CONTEXTO. El subagente puede quemar 40.000 tokens
     leyendo archivos y devolver 200 palabras. Esos 40.000 NUNCA entran
     al historial del orquestador. Es la razon principal.

  2. MENOS HERRAMIENTAS POR AGENTE. Cada agente elige entre 2 o 3 opciones
     en vez de 15. Menos decisiones equivocadas por paso.

  3. MODELO POR TAREA. El trabajo mecanico puede correr en un modelo mas
     barato que el razonamiento.

  4. PERMISOS. El explorador NO tiene escribir_archivo. No puede escribir
     aunque el modelo lo decida. Garantia del codigo, no del prompt.

---------------------------------------------------------------------------
TAREAS  (25 min)
---------------------------------------------------------------------------

1. Corre el archivo tal cual. Ya funciona con UN subagente (explorador).
   Mira el reporte del final: lo que quemo el subagente frente a lo
   que le devolvio al orquestador.

2. TAREA PRINCIPAL: agrega el segundo subagente, el `escritor`.
   Esta todo marcado con TODO abajo. Son tres pasos:
      a) crear el Agent
      b) darle su herramienta (escribir_archivo)
      c) registrarlo como herramienta del orquestador con @orquestador.tool

3. Cambia el OBJETIVO a algo que necesite los dos:
   "Averigua que bug hay y escribe un resumen en reporte.md"
   Corre y revisa sandbox/reporte.md.

4. Empeora la descripcion (el docstring) de la herramienta `explorar`.
   El orquestador deja de usarla? Es el ejercicio 1 otra vez: un subagente
   es una herramienta, y su descripcion es un prompt.

5. Quita `usage=ctx.usage` de una delegacion y corre. Que pasa con el
   conteo? Por que conviene que el uso del hijo cuente para el padre?

6. EL TRASPASO. Aqui se pierde la informacion, y no da ningun error.
   En `explorar`, ignora lo que te pidio el orquestador y mandale al
   subagente un encargo vago:

       pregunta = "Dime que hay en el proyecto."
       print("   [encargo que recibio el hijo: %r]" % pregunta)

   Corre con el OBJETIVO de la tarea 3 y abre sandbox/reporte.md. El
   explorador no fallo: contesto bien una pregunta que no era la que hacia
   falta, y el orquestador escribio su reporte igual de convencido. Cero
   errores, cero 429, y el resultado esta mal.

   Ese es el costo real de delegar: no son los tokens del salto, es que el
   padre le encarga al hijo algo peor de lo que cree. Cuando tu MVP falle
   el sabado y los dos agentes "funcionen", revisa el encargo primero.
"""

import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from pydantic_ai import Agent, RunContext

from taller import modelo, modo, correr, encabezado, LIMITES_ORQ
from taller.herramientas import (
    buscar_texto as _buscar,
    leer_archivo as _leer,
    listar_archivos as _listar,
    escribir_archivo as _escribir,
)


# ===========================================================================
# SUBAGENTE 1  --  EXPLORADOR   (solo lectura)
# ===========================================================================

explorador = Agent(
    modelo(),
    instructions=(
        "Eres un subagente de exploracion. SOLO LEES, nunca escribes.\n"
        "Tu respuesta se la entregas a otro agente, asi que se breve: "
        "maximo 80 palabras. Estructura:\n"
        "- Archivos relevantes (ruta + una linea)\n"
        "- Que NO encontraste"
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


@explorador.tool_plain
def listar_archivos(ruta: str = ".") -> str:
    """Lista archivos y carpetas de una ruta. Usa '.' para la raiz del sandbox."""
    return _listar(ruta)


# Fijate: el explorador NO tiene escribir_archivo.
# No puede escribir. No es que le pedimos que no lo haga: no tiene como.


# ===========================================================================
# TAREA 2  --  SUBAGENTE 2: EL ESCRITOR      (te toca escribirlo)
# ===========================================================================
#
# El explorador de arriba es tu ejemplo, y esta funcionando. Copia la FORMA,
# no el texto: un Agent con sus instructions, y debajo sus herramientas
# registradas con @escritor.tool_plain.
#
# a) EL AGENTE. Sus instructions tienen que contestar tres cosas:
#       - que hace: escribe el archivo que le pasan, y nada mas
#       - que NO hace: no investiga. Si le falta informacion, lo dice y para
#       - cuanto mide su respuesta: la va a leer el orquestador, se breve
#
# b) SU UNICA HERRAMIENTA: escribir_archivo(ruta, contenido).
#    La implementacion ya existe: es `_escribir`, importado arriba. Lo que
#    escribes tu es el registro y el DOCSTRING, que es lo que el modelo lee
#    para decidir. Como en el ejercicio 1: que devuelve, que pasa si el
#    archivo ya existe, que no acepta.
#
#    Dale SOLO esa. Si de paso le das leer_archivo, deja de ser un escritor
#    y el aislamiento de permisos se te cae.
#
# (el paso c va mas abajo, con las herramientas del orquestador)
# ===========================================================================


# ===========================================================================
# EL ORQUESTADOR
# ===========================================================================

orquestador = Agent(
    modelo(),
    instructions=(
        "Coordinas subagentes para resolver una tarea sobre un proyecto.\n"
        "No investigas ni escribes tu mismo: delegas.\n"
        "Primero explora, y solo despues actua con lo que te devolvieron."
    ),
)


@orquestador.tool
async def explorar(ctx: RunContext[None], pregunta: str) -> str:
    """Investiga los archivos del proyecto y devuelve un resumen corto.

    Usar ANTES de intentar cualquier otra cosa. Devuelve maximo 80 palabras
    con rutas y hallazgos, nunca el contenido completo de los archivos.
    NO escribe ni modifica nada.
    """
    print("   [delegando al explorador...]")

    # OJO: resultado.usage ES el contador del padre, no el del hijo (le
    # pasamos usage=ctx.usage). Para saber lo que gasto EL HIJO hay que
    # medir antes y despues.
    antes = ctx.usage.input_tokens
    resultado = await explorador.run(pregunta, usage=ctx.usage)

    CONTEO["explorador"] = (ctx.usage.input_tokens - antes, len(resultado.output))
    return resultado.output


# ---------------------------------------------------------------------------
# TAREA 2, PASO C  --  registra el escritor como herramienta del orquestador
# ---------------------------------------------------------------------------
#
# Mira `explorar` ahi arriba: es el patron completo en siete lineas. El tuyo
# se llama `escribir` y recibe (ctx, ruta, contenido).
#
# Cuatro cosas tiene que tener, y las cuatro importan:
#
#   1. @orquestador.tool  --  `tool`, no `tool_plain`. Necesitas el ctx.
#   2. Un docstring que le diga al orquestador CUANDO usarlo. Pista: solo
#      sirve si ya tiene el contenido final. Este subagente no investiga.
#   3. usage=ctx.usage en el .run()  --  asi lo que gasta el hijo cuenta
#      para el limite del padre. Sin eso, LIMITES_ORQ no lo esta frenando.
#   4. CONTEO["escritor"] = len(resultado.all_messages())  --  alimenta el
#      reporte del final. Es la linea que te deja VER el aislamiento.
#
# Devuelve resultado.output, no el resultado completo.
# ---------------------------------------------------------------------------


CONTEO = {}

OBJETIVO = "Averigua que bug esta reportado en el proyecto y explicalo en una frase."


def main():
    encabezado("Ejercicio 3 - el bucle multi-agente")

    resultado = correr(orquestador, OBJETIVO, limites=LIMITES_ORQ)

    print("\nRESPUESTA FINAL:")
    print(resultado.output)

    print("\n--- contexto: el punto entero del patron ---")
    for nombre, (tokens, chars) in CONTEO.items():
        print("%-11s quemo %5d tokens de entrada  ->  devolvio %4d caracteres"
              % (nombre, tokens, chars))
    print("\nAl historial del orquestador solo entro la segunda columna.")
    print("Lo de la primera se quedo en el subagente y nadie lo paga dos veces.")
    if modo() == "test":
        print("\n(En MODO=test la relacion no dice nada: TestModel no resume,")
        print(" repite la salida de las herramientas. Corre esto en MODO=gemini")
        print(" y mira como la primera columna se despega de la segunda.)")

    print("\n--- lo que gasto en total ---")
    print("peticiones al modelo:    %d" % resultado.usage.requests)
    print("herramientas ejecutadas: %d" % resultado.usage.tool_calls)
    print("(incluye las de los subagentes, por usage=ctx.usage)")


if __name__ == "__main__":
    main()
