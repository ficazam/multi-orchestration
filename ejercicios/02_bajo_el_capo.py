"""
EJERCICIO 2  --  que hace Pydantic AI por debajo
================================================

    python ejercicios/02_bajo_el_capo.py

Este es el ejercicio mas corto y el que mas te va a servir cuando algo
falle en el hackathon.

`agente.run_sync()` no es magia. Es este bucle:

    mensajes = [objetivo]
    mientras no termine:
        respuesta = modelo(mensajes, herramientas)
        si respuesta no pide herramientas: listo
        por cada herramienta pedida:
            salida = ejecutar(herramienta)
            mensajes.append(salida)      <-- SIN ESTO no avanza nunca

Dos cosas que hay que entender de ahi:

  1. El modelo NO TIENE MEMORIA entre llamadas. En cada vuelta se le
     reenvia el historial completo. La lista `mensajes` es la memoria.

  2. Por eso el costo crece rapido: el paso 10 carga los 9 anteriores.

---------------------------------------------------------------------------
TAREAS  (10 min)
---------------------------------------------------------------------------

1. Corre el archivo. Mira cuantos mensajes hay en el historial al final.

2. Mira la salida de `mensajes()`: ahi esta todo lo que el modelo recibio.
   Cuenta cuantos ModelRequest y ModelResponse hay. Cada ModelResponse
   es una llamada que pagaste.

3. Cambia el OBJETIVO por uno que necesite tres herramientas encadenadas
   y vuelve a mirar el conteo. Cuanto crecio?

4. Baja el request_limit a 2 en taller/config.py (LIMITES) y corre.
   Lee el mensaje de error. Ese tope es lo unico que separa un bug de
   una factura.

5. Pregunta: si tu MVP necesita 30 pasos, que le pasa
   al historial? Y al costo? Esa respuesta es la razon por la que existen los
   subagentes del ejercicio 3.
"""

import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from pydantic_ai import Agent

from taller import modelo, correr, encabezado
from taller.herramientas import buscar_texto as _buscar, leer_archivo as _leer


agente = Agent(
    modelo(),
    instructions="Responde usando las herramientas. Se breve.",
)


@agente.tool_plain
def buscar_texto(patron: str) -> str:
    """Busca un texto en todos los archivos del sandbox.

    Devuelve lineas con formato 'archivo:numero: contenido', maximo 20.
    Devuelve 'Sin coincidencias' si no encuentra nada.
    """
    return _buscar(patron)


@agente.tool_plain
def leer_archivo(ruta: str) -> str:
    """Devuelve el contenido de UN archivo de texto, hasta 4000 caracteres.

    NO acepta carpetas. La ruta es relativa al sandbox.
    Devuelve un texto que empieza con 'ERROR:' si la ruta no existe.
    """
    return _leer(ruta)


OBJETIVO = "Busca el ticket 412 y leeme el archivo donde aparece."


def main():
    encabezado("Ejercicio 2 - bajo el capo")

    resultado = correr(agente, OBJETIVO)

    print("\nRESPUESTA:")
    print(resultado.output)

    # ----------------------------------------------------------------------
    # Esto es lo que normalmente no ves: el historial completo.
    # ----------------------------------------------------------------------
    historial = resultado.all_messages()

    print("\n--- el historial que se fue armando ---")
    for i, m in enumerate(historial, 1):
        tipo = type(m).__name__
        partes = []
        for p in m.parts:
            nombre = type(p).__name__
            extra = getattr(p, "tool_name", None)
            partes.append(nombre + ("(%s)" % extra if extra else ""))
        print("%2d. %-14s %s" % (i, tipo, ", ".join(partes)))

    print("\n--- lo que gasto ---")
    print("mensajes en el historial: %d" % len(historial))
    print("peticiones al modelo:     %d" % resultado.usage.requests)
    print("herramientas ejecutadas:  %d" % resultado.usage.tool_calls)
    print("tokens de entrada:        %d" % resultado.usage.input_tokens)
    print("\nCada peticion reenvio TODO el historial anterior.")
    print("Por eso el costo de una corrida crece mas rapido que sus pasos.")


if __name__ == "__main__":
    main()
