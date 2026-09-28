"""
diapositivas.py  --  genera las diapositivas del taller en PDF.

    pip install reportlab
    python presentacion/diapositivas.py

Deja el PDF en presentacion/diapositivas.pdf, en 16:9, para proyectar.

El contenido esta todo en la lista DIAPOS de abajo: edita ahi y vuelve a
correr. El guion del que presenta va aparte, en guion.py.
"""

import pathlib

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfgen import canvas as canvas_mod
from reportlab.platypus import Paragraph

SALIDA = pathlib.Path(__file__).resolve().parent / "diapositivas.pdf"

# 16:9 en puntos  ->  13.33 x 7.5 pulgadas, lo mismo que un PowerPoint
ANCHO, ALTO = 960.0, 540.0
MARGEN = 62.0
UTIL = ANCHO - 2 * MARGEN

FONDO = colors.HexColor("#FBFBF9")
TINTA = colors.HexColor("#14181C")
GRIS = colors.HexColor("#6E767D")
ACENTO = colors.HexColor("#0B5C8A")
ALERTA = colors.HexColor("#8A3B0B")
VERDE = colors.HexColor("#0B6B3A")
CODIGO_BG = colors.HexColor("#EDF0F2")
LINEA = colors.HexColor("#D9DEE2")


# ===========================================================================
# EL CONTENIDO
# ===========================================================================
# Tipos de diapositiva:
#   portada   titulo grande + subtitulo
#   seccion   separador de bloque: numero, titulo, minutos
#   idea      una sola frase, a tamano grande. Una idea por diapositiva.
#   lista     titulo + vinetas
#   codigo    titulo + bloque monoespaciado (+ pie opcional)
#   tabla     titulo + filas de dos columnas
#   turno     "tu turno": lo que hacen ellos, con barra de color
#   cierre    frase final

DIAPOS = [
    {"tipo": "portada",
     "titulo": "Sistemas Multi-Agente<br/>y Function Calling",
     "subtitulo": "Hackathon FISC AI AGENTS  ·  UTP, salon 3-303",
     "pie": "Hoy: un orquestador con subagentes. Y sales con el esqueleto "
            "de tu MVP."},

    {"tipo": "idea",
     "texto": "Un subagente es un agente normal,<br/>"
              "llamado desde <b>dentro de una herramienta</b><br/>"
              "de otro agente.",
     "pie": "Eso es todo. No hay framework magico."},

    {"tipo": "tabla",
     "titulo": "Dos modos",
     "filas": [("MODO=test",
                "No usa red ni llave. Verifica que tu codigo corre."),
               ("MODO=gemini",
                "Respuestas de verdad. Necesita GEMINI_API_KEY.")],
     "pie": "<b>Armas en test, pruebas en gemini.</b> Esa disciplina es la "
            "diferencia entre llegar al sabado con cuota y sin cuota."},

    {"tipo": "idea",
     "texto": "Cada quien necesita<br/><b>SU PROPIA llave.</b>",
     "pie": "La capa gratis da 5-15 peticiones por minuto. Una llave "
            "compartida entre 30 se muere en el primer ejercicio.",
     "color": ALERTA},

    # --- 1 ----------------------------------------------------------------
    {"tipo": "seccion", "numero": "1", "titulo": "La descripcion ES el prompt",
     "min": "16 min"},

    {"tipo": "lista",
     "titulo": "El modelo no ve tu codigo",
     "items": ["El nombre de la funcion",
               "Los tipos de los parametros",
               "El docstring"],
     "pie": "Esa es <b>toda</b> la interfaz. Tu docstring no es "
            "documentacion: es prompt."},

    {"tipo": "codigo",
     "titulo": "Esto no da error",
     "lineas": ['@agente.tool_plain',
                'def buscar_texto(patron: str) -> str:',
                '    """Busca cosas."""',
                '    return _buscar(patron)'],
     "pie": "Da una llamada equivocada hecha con total confianza. "
            "Eso es lo peligroso."},

    {"tipo": "lista",
     "titulo": "Un docstring util dice tres cosas",
     "items": ["Que devuelve, y en que formato",
               "Que <b>NO</b> hace / que no acepta",
               "Que significa el resultado vacio"],
     "pie": "La tercera es la que nadie escribe. Si 'Sin coincidencias' "
            "significa <i>no esta</i> y no <i>fallo</i>, dilo, o el modelo "
            "reintenta en bucle."},

    {"tipo": "turno",
     "titulo": "Tu turno  ·  ejercicio 1",
     "items": ["Corre el archivo. Mira que hace con el docstring malo.",
               "Arreglalo. Corre otra vez y compara.",
               "Escribe una herramienta desde cero. El cuerpo es una linea; "
               "el trabajo es el docstring.",
               "Pide un archivo que no existe. Fijate: el agente LEE el "
               "error y reintenta."],
     "pie": "python ejercicios/01_herramientas.py"},

    # --- 2 ----------------------------------------------------------------
    {"tipo": "seccion", "numero": "2", "titulo": "Que hace run_sync por debajo",
     "min": "7 min"},

    {"tipo": "codigo",
     "titulo": "run_sync no es magia. Es este bucle.",
     "lineas": ['mensajes = [objetivo]',
                'mientras no termine:',
                '    respuesta = modelo(mensajes, herramientas)',
                '    si respuesta no pide herramientas: listo',
                '    por cada herramienta pedida:',
                '        salida = ejecutar(herramienta)',
                '        mensajes.append(salida)   <-- SIN ESTO no avanza'],
     "pie": ""},

    {"tipo": "lista",
     "titulo": "Dos consecuencias",
     "items": ["El modelo <b>no tiene memoria</b> entre llamadas. En cada "
               "vuelta se le reenvia el historial completo. La lista es la "
               "memoria.",
               "El paso 10 carga los 9 anteriores. El costo crece mas rapido "
               "que los pasos."],
     "pie": ""},

    {"tipo": "idea",
     "texto": "El tope de peticiones es lo unico<br/>"
              "que separa un bug de una factura.",
     "pie": "UsageLimits(request_limit=6, tool_calls_limit=5). "
            "Ponlo antes de la primera corrida, no despues del susto.",
     "color": ALERTA},

    {"tipo": "turno",
     "titulo": "Tu turno  ·  ejercicio 2",
     "items": ["Corre y mira el historial completo impreso.",
               "Cuenta los ModelResponse. Cada uno es una llamada que pagaste.",
               "Baja request_limit a 2 y corre. Lee el error."],
     "pie": "python ejercicios/02_bajo_el_capo.py"},

    {"tipo": "idea",
     "texto": "Si tu MVP necesita 30 pasos,<br/>"
              "&iquest;que le pasa al historial?<br/>"
              "&iquest;Y al costo?",
     "pie": "Esa respuesta es por que existen los subagentes."},

    # --- 3 ----------------------------------------------------------------
    {"tipo": "seccion", "numero": "3", "titulo": "El bucle multi-agente",
     "min": "28 min  ·  el central"},

    {"tipo": "codigo",
     "titulo": "El patron completo",
     "lineas": ['@orquestador.tool',
                'async def explorar(ctx, pregunta: str) -> str:',
                '    resultado = await explorador.run(',
                '        pregunta, usage=ctx.usage)',
                '    return resultado.output'],
     "pie": "Para el orquestador es una herramienta cualquiera. No sabe que "
            "por dentro corrio otro agente con su propio bucle."},

    {"tipo": "lista",
     "titulo": "Cuatro razones para separar un subagente",
     "items": ["<b>Aisla contexto.</b> Quema 40.000 tokens y devuelve 200 "
               "palabras. Esos 40.000 nunca entran al padre. &larr; la "
               "principal",
               "<b>Menos herramientas por decision.</b> Elegir entre 3, no "
               "entre 15.",
               "<b>Modelo por tarea.</b> Lo mecanico, en algo mas barato.",
               "<b>Permisos.</b> No puede hacer lo que no tiene."],
     "pie": ""},

    {"tipo": "codigo",
     "titulo": "El aislamiento, en numeros",
     "lineas": ['explorador  quemo   344 tokens  ->  devolvio  796 caracteres',
                'escritor    quemo   166 tokens  ->  devolvio   48 caracteres'],
     "pie": "Al historial del orquestador solo entro la segunda columna. "
            "En MODO=test la relacion sale al reves: TestModel repite en vez "
            "de resumir."},

    {"tipo": "idea",
     "texto": "El explorador no escribe<br/>"
              "porque <b>no tiene la herramienta.</b>",
     "pie": "Un prompt que dice 'no borres nada' es una recomendacion. "
            "Una funcion que no existe es una garantia.",
     "color": VERDE},

    {"tipo": "turno",
     "titulo": "Tu turno  ·  ejercicio 3",
     "items": ["Corre tal cual. Ya funciona con UN subagente.",
               "<b>Construye el escritor:</b> el Agent, su unica herramienta, "
               "y registralo con @orquestador.tool.",
               "Cambia el OBJETIVO a algo que necesite los dos. Abre "
               "sandbox/reporte.md.",
               "Empeora el docstring de explorar. &iquest;Lo sigue usando?",
               "Quita usage=ctx.usage y corre. &iquest;Que le paso al conteo?"],
     "pie": "python ejercicios/03_delegacion.py"},

    {"tipo": "idea",
     "texto": "El costo real de delegar no es el token.<br/>"
              "Es que el padre le encarga al hijo<br/>"
              "<b>algo peor de lo que cree.</b>",
     "pie": "Tarea 6: mandale un encargo vago. Nadie falla, ningun 429, y el "
            "reporte sale mal. Cuando tu MVP falle el sabado y los dos "
            "agentes \"funcionen\", revisa el encargo primero.",
     "color": ALERTA},

    # --- 4 ----------------------------------------------------------------
    {"tipo": "seccion", "numero": "4", "titulo": "El esqueleto de TU MVP",
     "min": "10 min"},

    {"tipo": "lista",
     "titulo": "Primero en papel. Sin teclado.",
     "items": ["&iquest;Que hace tu MVP, en UNA frase?",
               "Por cada subagente: que hace, que herramientas SI tiene, y "
               "<b>que herramientas NO tiene.</b>",
               "&iquest;Que razon de las cuatro lo justifica?",
               "&iquest;Cual es tu limite de peticiones?"],
     "pie": "La tercera pregunta del segundo punto es la que importa. Si no "
            "la puedes contestar, todavia no sabes que vas a construir."},

    {"tipo": "idea",
     "texto": "Si no aisla contexto, no acota permisos,<br/>"
              "no reduce decisiones y no cambia de modelo:<br/>"
              "<b>no es un subagente. Es una funcion.</b>",
     "pie": "Multi-agente no es gratis. Cada salto son peticiones, latencia, "
            "y una traduccion mas donde se pierde informacion."},

    {"tipo": "turno",
     "titulo": "Tu turno  ·  ejercicio 4",
     "items": ["Contesta las cuatro preguntas en papel.",
               "Llena los TODO con TU MVP, no con el ejemplo de archivos.",
               "Pon MIS_LIMITES antes de la primera corrida."],
     "pie": "python ejercicios/04_mi_mvp.py   ·   esto se lo llevan y lo "
            "siguen el sabado"},

    # --- cierre -----------------------------------------------------------
    {"tipo": "lista",
     "titulo": "Las dos ideas que se llevan",
     "items": ["<b>Un subagente es una herramienta</b>, y su descripcion es "
               "un prompt. Si el orquestador no lo usa, casi siempre el "
               "problema es el docstring.",
               "<b>Lo que garantiza algo es el codigo, no el prompt.</b> "
               "Ningun agente sale del sandbox porque hay una funcion que "
               "rechaza la ruta."],
     "pie": ""},

    {"tipo": "cierre",
     "texto": "&iquest;Que van a construir?",
     "pie": "Una frase cada equipo."},
]


# ===========================================================================
# MOTOR
# ===========================================================================

def estilo(tam, color=TINTA, fuente="Helvetica", lider=None,
           alineacion=TA_LEFT, espacio=0):
    return ParagraphStyle(
        "s%d%s%s" % (tam, fuente, alineacion), fontName=fuente, fontSize=tam,
        leading=lider or tam * 1.22, textColor=color, alignment=alineacion,
        spaceAfter=espacio)


def poner(c, html, x, arriba, ancho, est):
    """Dibuja un parrafo con su borde superior en `arriba`. Devuelve su alto."""
    p = Paragraph(html, est)
    _, alto = p.wrapOn(c, ancho, 10000)
    p.drawOn(c, x, arriba - alto)
    return alto


def medir(c, html, ancho, est):
    p = Paragraph(html, est)
    _, alto = p.wrapOn(c, ancho, 10000)
    return alto


def fondo(c):
    c.setFillColor(FONDO)
    c.rect(0, 0, ANCHO, ALTO, stroke=0, fill=1)


def numerar(c, n, total, etiqueta=""):
    c.setFont("Helvetica", 10)
    c.setFillColor(GRIS)
    if etiqueta:
        c.drawString(MARGEN, 28, etiqueta)
    c.drawRightString(ANCHO - MARGEN, 28, "%d / %d" % (n, total))


def bloque_codigo(c, lineas, arriba, tam=19):
    """Caja monoespaciada centrada horizontalmente. Devuelve el alto usado."""
    lider = tam * 1.45
    pad = 22
    alto = len(lineas) * lider + pad * 2
    ancho_texto = max(c.stringWidth(l, "Courier-Bold", tam) for l in lineas)
    ancho = min(UTIL, ancho_texto + pad * 2)
    x = (ANCHO - ancho) / 2

    c.setFillColor(CODIGO_BG)
    c.setStrokeColor(LINEA)
    c.setLineWidth(0.8)
    c.roundRect(x, arriba - alto, ancho, alto, 8, stroke=1, fill=1)

    c.setFillColor(TINTA)
    c.setFont("Courier-Bold", tam)
    y = arriba - pad - tam
    for l in lineas:
        c.drawString(x + pad, y, l)
        y -= lider
    return alto


# --- una funcion por tipo de diapositiva -----------------------------------

def dib_portada(c, d):
    poner(c, d["titulo"], MARGEN, ALTO - 118, UTIL,
          estilo(54, TINTA, "Helvetica-Bold", lider=64))
    c.setStrokeColor(ACENTO)
    c.setLineWidth(3)
    c.line(MARGEN, 232, MARGEN + 120, 232)
    poner(c, d["subtitulo"], MARGEN, 208, UTIL, estilo(20, GRIS))
    poner(c, d["pie"], MARGEN, 158, UTIL * 0.8,
          estilo(17, ACENTO, "Helvetica-Oblique"))


def dib_seccion(c, d):
    c.setFillColor(colors.HexColor("#E8EDF1"))
    c.setFont("Helvetica-Bold", 210)
    c.drawString(MARGEN - 6, ALTO / 2 - 68, d["numero"])
    poner(c, d["titulo"], MARGEN + 150, ALTO / 2 + 66, UTIL - 150,
          estilo(44, TINTA, "Helvetica-Bold", lider=52))
    poner(c, d["min"], MARGEN + 150, ALTO / 2 - 34, UTIL - 150,
          estilo(19, ACENTO, "Helvetica-Bold"))


def dib_idea(c, d):
    color = d.get("color", TINTA)
    est = estilo(37, color, "Helvetica-Bold", lider=50, alineacion=TA_CENTER)
    alto_t = medir(c, d["texto"], UTIL, est)
    pie = d.get("pie", "")
    est_pie = estilo(17, GRIS, "Helvetica", lider=25, alineacion=TA_CENTER)
    alto_p = medir(c, pie, UTIL * 0.82, est_pie) if pie else 0

    total = alto_t + (48 + alto_p if pie else 0)
    arriba = (ALTO + total) / 2
    poner(c, d["texto"], MARGEN, arriba, UTIL, est)
    if pie:
        y = arriba - alto_t - 30
        c.setStrokeColor(LINEA)
        c.setLineWidth(1)
        c.line(ANCHO / 2 - 46, y, ANCHO / 2 + 46, y)
        poner(c, pie, MARGEN + UTIL * 0.09, y - 18, UTIL * 0.82, est_pie)


def dib_lista(c, d):
    y = ALTO - 92
    y -= poner(c, d["titulo"], MARGEN, y, UTIL,
               estilo(38, TINTA, "Helvetica-Bold", lider=45))
    y -= 34
    est = estilo(21, TINTA, "Helvetica", lider=29)
    for item in d["items"]:
        c.setFillColor(ACENTO)
        c.circle(MARGEN + 6, y - 11, 4.2, stroke=0, fill=1)
        y -= poner(c, item, MARGEN + 28, y, UTIL - 28, est)
        y -= 21
    pie = d.get("pie", "")
    if pie:
        # normalmente va anclado abajo; si las vinetas crecen, cede el sitio
        poner(c, pie, MARGEN, min(108.0, y - 16), UTIL * 0.9,
              estilo(16, GRIS, "Helvetica-Oblique", lider=23))


def dib_codigo(c, d):
    y = ALTO - 92
    y -= poner(c, d["titulo"], MARGEN, y, UTIL,
               estilo(34, TINTA, "Helvetica-Bold", lider=41))
    y -= 40
    # el tamano se ajusta para que la linea mas larga quepa
    largo = max(len(l) for l in d["lineas"])
    tam = 19 if largo <= 58 else (16 if largo <= 70 else 13.5)
    y -= bloque_codigo(c, d["lineas"], y, tam)
    pie = d.get("pie", "")
    if pie:
        poner(c, pie, MARGEN, max(y - 34, 112), UTIL * 0.92,
              estilo(16, GRIS, "Helvetica-Oblique", lider=23))


def dib_tabla(c, d):
    y = ALTO - 92
    y -= poner(c, d["titulo"], MARGEN, y, UTIL,
               estilo(38, TINTA, "Helvetica-Bold", lider=45))
    y -= 40
    izq = 250.0
    for clave, valor in d["filas"]:
        a1 = poner(c, clave, MARGEN, y, izq - 26,
                   estilo(21, ACENTO, "Courier-Bold", lider=28))
        a2 = poner(c, valor, MARGEN + izq, y, UTIL - izq,
                   estilo(21, TINTA, "Helvetica", lider=28))
        y -= max(a1, a2) + 15
        c.setStrokeColor(LINEA)
        c.setLineWidth(0.7)
        c.line(MARGEN, y + 6, ANCHO - MARGEN, y + 6)
        y -= 15
    pie = d.get("pie", "")
    if pie:
        poner(c, pie, MARGEN, max(y - 12, 112), UTIL * 0.92,
              estilo(16, GRIS, "Helvetica-Oblique", lider=23))


def dib_turno(c, d):
    c.setFillColor(VERDE)
    c.rect(0, 0, 13, ALTO, stroke=0, fill=1)
    y = ALTO - 92
    y -= poner(c, d["titulo"], MARGEN, y, UTIL,
               estilo(34, VERDE, "Helvetica-Bold", lider=41))
    y -= 30
    est = estilo(19.5, TINTA, "Helvetica", lider=27)
    for i, item in enumerate(d["items"], 1):
        c.setFillColor(GRIS)
        c.setFont("Helvetica-Bold", 16)
        c.drawString(MARGEN, y - 19, "%d." % i)
        y -= poner(c, item, MARGEN + 30, y, UTIL - 30, est)
        y -= 16
    pie = d.get("pie", "")
    if pie:
        c.setFillColor(CODIGO_BG)
        c.setStrokeColor(LINEA)
        c.roundRect(MARGEN, 84, UTIL, 40, 7, stroke=1, fill=1)
        c.setFillColor(TINTA)
        c.setFont("Courier-Bold", 15)
        c.drawString(MARGEN + 16, 98, pie)


def dib_cierre(c, d):
    est = estilo(52, TINTA, "Helvetica-Bold", lider=62, alineacion=TA_CENTER)
    alto_t = medir(c, d["texto"], UTIL, est)
    arriba = (ALTO + alto_t) / 2 + 22
    poner(c, d["texto"], MARGEN, arriba, UTIL, est)
    poner(c, d.get("pie", ""), MARGEN, arriba - alto_t - 30, UTIL,
          estilo(19, GRIS, "Helvetica-Oblique", alineacion=TA_CENTER))


DIBUJAR = {
    "portada": dib_portada,
    "seccion": dib_seccion,
    "idea": dib_idea,
    "lista": dib_lista,
    "codigo": dib_codigo,
    "tabla": dib_tabla,
    "turno": dib_turno,
    "cierre": dib_cierre,
}

# etiqueta al pie, para saber en que bloque vas
ETIQUETA = ""


def construir():
    global ETIQUETA
    c = canvas_mod.Canvas(str(SALIDA), pagesize=(ANCHO, ALTO))
    c.setTitle("Sistemas Multi-Agente y Function Calling - taller")
    c.setAuthor("Felipe Icaza")

    total = len(DIAPOS)
    etiqueta = ""
    for i, d in enumerate(DIAPOS, 1):
        fondo(c)
        if d["tipo"] == "seccion":
            etiqueta = "%s · %s" % (d["numero"], d["titulo"])
        DIBUJAR[d["tipo"]](c, d)
        if d["tipo"] not in ("portada",):
            numerar(c, i, total, etiqueta if d["tipo"] != "seccion" else "")
        c.showPage()

    c.save()
    return SALIDA, total


if __name__ == "__main__":
    ruta, n = construir()
    print("PDF generado: %s  (%d diapositivas, %.0f KB)"
          % (ruta, n, ruta.stat().st_size / 1024))
