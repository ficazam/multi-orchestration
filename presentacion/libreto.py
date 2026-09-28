"""
libreto.py  --  el libreto hablado del taller, palabra por palabra, en PDF.

    pip install reportlab
    python presentacion/libreto.py

Deja el PDF en presentacion/libreto.pdf.

Esto es lo que se dice EN VOZ ALTA, literal. No son notas ni vinetas: es el
texto corrido. Lo demas del repo:

    diapositivas.py   lo que se proyecta
    guion.py          las notas del que presenta (tiempos, trampas, reserva)
    libreto.py        esto: las palabras

El contenido esta en la lista LIBRETO de abajo. Edita ahi y vuelve a correr.
"""

import pathlib

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    CondPageBreak, HRFlowable, KeepTogether, PageBreak, Paragraph,
    SimpleDocTemplate, Spacer, Table, TableStyle,
)

SALIDA = pathlib.Path(__file__).resolve().parent / "libreto.pdf"

TINTA = colors.HexColor("#14181C")
GRIS = colors.HexColor("#6E767D")
ACENTO = colors.HexColor("#0B5C8A")
VERDE = colors.HexColor("#0B6B3A")
ALERTA = colors.HexColor("#8A3B0B")
BANDA = colors.HexColor("#EEF2F4")
LINEA = colors.HexColor("#D9DEE2")


# ===========================================================================
# EL LIBRETO
# ===========================================================================
# Tipos de linea:
#   ("habla",    texto)   LO QUE DICES, literal. <b>negrita</b> = acentua
#   ("pausa",    "")      un beat. Callate y respira
#   ("haz",      texto)   lo que haces mientras hablas (no se dice)
#   ("trabajan", texto)   ellos trabajan, tu te callas y circulas
#   ("pregunta", texto)   lo que preguntas en voz alta
#   ("espera",   texto)   la respuesta que buscas (no se dice)

LIBRETO = [
 {"bloque": "Apertura", "reloj": "0:00 – 4:00", "partes": [

  ("habla",
   "Buenas. En el taller pasado vieron agentes, herramientas y memoria. Ya "
   "saben registrar una funcion con arroba-agente-punto-tool-plain, y ya "
   "vieron un agente decidir cual herramienta usar. Hoy vamos a lo que "
   "sigue: un agente que manda a otros agentes."),

  ("habla",
   "Y les digo de una lo que se llevan, porque esto no es teoria. En setenta "
   "minutos van a tener corriendo, en su maquina, un orquestador con dos "
   "subagentes. Y el ultimo ejercicio es el esqueleto del MVP que presentan "
   "el sabado. No es un ejemplo de juguete que despues botan. Es su punto "
   "de partida."),

  ("pausa", ""),

  ("habla",
   "Antes de escribir una linea, la frase del dia. Si se les olvida toda la "
   "sintaxis de hoy, esta no: <b>un subagente es un agente normal, llamado "
   "desde dentro de una herramienta de otro agente.</b>"),

  ("habla",
   "Eso es todo. No hay una clase especial. No hay framework de "
   "orquestacion. No hay nada magico. Es una funcion que por dentro llama a "
   "otro agente. Cuando lo vean en el ejercicio tres les va a parecer poca "
   "cosa &mdash; y esta bien que les parezca poca cosa. Lo dificil no es "
   "escribirlo. Lo dificil es saber cuando vale la pena."),

  ("pregunta",
   "&iquest;A quien le ha pasado que un agente se queda dando vueltas y le "
   "quema la cuota? Levanten la mano."),
  ("espera",
   "Levanta la tuya primero. Casi todos la levantan. Si no levanta nadie: "
   "\"les va a pasar el sabado\"."),

  ("habla",
   "Eso tambien lo arreglamos hoy. Y no con un truco: con dos numeros que se "
   "ponen antes de la primera corrida."),

  ("habla",
   "Ultima cosa antes de arrancar. Hay dos modos de trabajo. MODO igual "
   "test no usa red ni llave: sirve para comprobar que su codigo corre. MODO "
   "igual gemini da respuestas de verdad y necesita la llave. La regla es: "
   "<b>armen en test, prueben en gemini.</b> Porque la capa gratis de Google "
   "da entre cinco y quince peticiones por minuto, y si prueban cada cambio "
   "contra el modelo real, a mitad del taller se quedan sin cuota."),

  ("habla",
   "Y cada quien necesita SU llave. No la compartan. Una llave entre treinta "
   "personas se muere en el primer ejercicio, y ahi el problema deja de ser "
   "de Google y pasa a ser mio."),
 ]},

 {"bloque": "Ejercicio 1  ·  la descripcion es el prompt",
  "reloj": "4:00 – 20:00", "partes": [

  ("habla",
   "Ejercicio uno. Abran ejercicios, cero-uno, herramientas punto py, y "
   "corranlo. Sin leerlo. Primero corre, despues lee."),

  ("haz", "Proyecta tu propia corrida mientras ellos corren la suya."),

  ("habla",
   "Lo que acaban de ver es un agente con una herramienta que se llama "
   "buscar-texto. Y su docstring dice, completo: \"Busca cosas.\" Dos "
   "palabras."),

  ("habla",
   "Fijense en lo que paso. No dio error. No se cayo. Hizo una llamada "
   "equivocada con total confianza. Y eso es lo peligroso, porque un error "
   "lo ves; una respuesta segura pero mal fundamentada te la crees."),

  ("pausa", ""),

  ("habla",
   "Aqui esta la idea del ejercicio, y es la que mas les va a servir el "
   "sabado: <b>el modelo no ve su codigo.</b> No lee el cuerpo de la "
   "funcion. Ve tres cosas, nada mas. El nombre de la funcion. Los tipos de "
   "los parametros. Y el docstring. Esa es toda la interfaz."),

  ("habla",
   "O sea que su docstring no es documentacion. Es prompt. Y si escriben un "
   "prompt de dos palabras, van a tener el comportamiento que merece un "
   "prompt de dos palabras."),

  ("habla",
   "Ahora arreglenlo. Un docstring que sirve dice tres cosas. Que devuelve, "
   "y en que formato. Que NO hace, o que no acepta. Y que significa el "
   "resultado vacio."),

  ("habla",
   "La tercera es la que nadie escribe y es la que mas cuesta. Si \"Sin "
   "coincidencias\" significa \"no esta\", y no significa \"fallo\", "
   "diganlo. Si no lo dicen, el modelo va a asumir que fallo y va a "
   "reintentar en bucle. Y ahi se les va la cuota."),

  ("trabajan",
   "6 min. Arreglan el docstring y escriben su propia herramienta. Circula. "
   "Si alguien acaba temprano, pidele que lea su docstring en voz alta."),

  ("habla",
   "Una ultima cosa de este ejercicio, y haganla: pidanle un archivo que no "
   "existe."),

  ("pausa", ""),

  ("habla",
   "El agente leyo el error y reintento. No se murio. Y eso no es suerte: es "
   "porque las funciones en taller, herramientas punto py, devuelven el "
   "error como texto en vez de lanzar excepcion. Si la funcion revienta, el "
   "agente se muere. Si devuelve \"ERROR: el archivo no existe\", el agente "
   "lo lee y corrige. Cuando escriban sus herramientas el sabado, devuelvan "
   "el error como texto."),
 ]},

 {"bloque": "Ejercicio 2  ·  que hace run_sync por debajo",
  "reloj": "20:00 – 27:00", "partes": [

  ("habla",
   "Ejercicio dos. Es el mas corto, y es el que mas les va a servir cuando "
   "algo falle el sabado a las dos de la manana."),

  ("haz", "Proyecta el bucle."),

  ("habla",
   "run-sync no es magia. Es este bucle. Armas una lista de mensajes con el "
   "objetivo. Le pasas la lista al modelo. Si el modelo no pide "
   "herramientas, terminaste. Si pide, ejecutas la herramienta, le pegas la "
   "salida a la lista, y vuelves a llamar al modelo con la lista completa."),

  ("habla",
   "De ahi salen dos cosas. La primera: <b>el modelo no tiene memoria.</b> "
   "Ninguna. En cada vuelta se le reenvia el historial entero. Esa lista de "
   "mensajes ES la memoria. No hay nada mas."),

  ("habla",
   "La segunda sale de la primera: el paso diez carga los nueve anteriores. "
   "Por eso el costo de una corrida crece mas rapido que sus pasos. No es "
   "lineal."),

  ("trabajan",
   "3 min. Corren y miran el historial impreso. Que cuenten los "
   "ModelResponse: cada uno es una llamada que pagaron."),

  ("habla",
   "Ahora bajen request-limit a dos, en taller config punto py, y corran "
   "otra vez. Lean el mensaje."),

  ("habla",
   "Eso que acaban de ver es UsageLimits haciendo su trabajo: corto el "
   "agente antes de que siguiera gastando. Ese tope es lo unico que separa "
   "un bug de una factura. Ponganlo antes de la primera corrida, no despues "
   "del susto."),

  ("pregunta",
   "Si su MVP necesita treinta pasos, &iquest;que le pasa al historial? "
   "&iquest;Y al costo?"),
  ("espera",
   "Dejalos contestar. NO contestes tu. La respuesta es la puerta al "
   "ejercicio 3; si la das tu, el ejercicio 3 pierde el porque."),

  ("habla",
   "Exacto. Y esa es la razon por la que existe el ejercicio tres."),
 ]},

 {"bloque": "Ejercicio 3  ·  el bucle multi-agente",
  "reloj": "27:00 – 55:00", "partes": [

  ("habla",
   "Ejercicio tres. Este es el del taller. Si hoy solo se llevan un archivo, "
   "que sea este."),

  ("haz", "Proyecta el patron de cinco lineas y dejalo en pantalla."),

  ("habla",
   "Miren el patron. Son cinco lineas. Es una herramienta del orquestador, "
   "decorada con arroba-orquestador-punto-tool. Y por dentro, en vez de "
   "hacer el trabajo, llama a otro agente y devuelve su salida. Nada mas."),

  ("habla",
   "Y aqui esta lo importante: <b>para el orquestador esto es una "
   "herramienta cualquiera.</b> No sabe que por dentro corrio otro agente "
   "con su propio bucle de diez pasos. Ve una funcion que le devolvio un "
   "texto."),

  ("pausa", ""),

  ("habla",
   "Ahora, por que importa. Y no es porque suene organizado. Hay cuatro "
   "razones, y una es la principal."),

  ("habla",
   "La principal es <b>aislamiento de contexto.</b> El subagente puede "
   "quemar cuarenta mil tokens leyendo archivos, y devolverle doscientas "
   "palabras al padre. Esos cuarenta mil nunca entran al historial del "
   "orquestador."),

  ("habla",
   "Y acuerdense del ejercicio dos: cada paso reenvia todo lo anterior. Si "
   "el orquestador cargara todo lo que leyeron sus hijos, reventaria en tres "
   "pasos. Por eso el aislamiento no es orden. Es lo que hace que la cosa "
   "funcione."),

  ("habla",
   "Las otras tres, rapido. Dos: menos herramientas por decision &mdash; "
   "cada agente elige entre tres opciones, no entre quince, y se equivoca "
   "menos. Tres: modelo por tarea &mdash; lo mecanico puede correr en algo "
   "mas barato. Y cuatro: permisos."),

  ("habla",
   "La de permisos mirenla en el codigo, porque es la que mas les va a "
   "importar el sabado. El explorador no tiene la herramienta "
   "escribir-archivo. No le pedimos que no escriba. <b>No tiene con que.</b>"),

  ("habla",
   "Un prompt que dice \"no borres nada\" es una recomendacion. Una funcion "
   "que no existe es una garantia."),

  ("haz", "Abre taller/herramientas.py y ensena _ruta_segura(). Son seis lineas."),

  ("habla",
   "Lo mismo con el sandbox. Ningun agente de este repo puede tocar un "
   "archivo fuera de la carpeta sandbox. Y no es porque el prompt lo pida: "
   "es porque hay una funcion que resuelve la ruta y la rechaza si se sale. "
   "Seis lineas. Eso es una garantia; el prompt era una sugerencia."),

  ("pausa", ""),

  ("habla",
   "Ahora les toca a ustedes, y es la tarea grande del dia. Van a escribir "
   "el segundo subagente: el escritor."),

  ("habla",
   "Los TODO en el archivo les dicen que tiene que cumplir, no como se "
   "escribe. Eso es a proposito. El explorador que esta justo arriba es su "
   "ejemplo, y esta funcionando: copien la forma, no el texto."),

  ("habla",
   "Tres pasos. Uno: el Agent, con sus instrucciones. Dos: su unica "
   "herramienta, escribir-archivo &mdash; solo esa. Si de paso le dan "
   "leer-archivo, deja de ser un escritor y el aislamiento de permisos se "
   "les cae. Y tres: registrenlo como herramienta del orquestador, con tool, "
   "no con tool-plain, porque necesitan el contexto."),

  ("trabajan",
   "12 min. Es la tarea principal del taller. Si alguien lleva mas de cinco "
   "minutos trabado en un typo, que abra soluciones/ y siga con el grupo: "
   "no se pierde veinte minutos ahi."),

  ("habla",
   "Ahora cambien el OBJETIVO a algo que necesite los dos &mdash; averiguar "
   "el bug y escribir un resumen &mdash; corran, y abran sandbox, reporte "
   "punto md."),

  ("habla",
   "Y fijense en una cosa del sandbox, porque no es casualidad: el bug esta "
   "repartido. Notas punto txt dice el sintoma: el login falla cuando el "
   "correo tiene mayusculas. Y docs, arquitectura punto md, dice la causa: "
   "el correo se guarda sin normalizar. No se puede contestar leyendo un "
   "solo archivo. Eso es lo que justifica tener un explorador."),

  ("habla",
   "Miren tambien el reporte del final. Dice cuantos tokens quemo cada "
   "subagente, y cuantos caracteres devolvio. Esa segunda columna es lo "
   "unico que entro al historial del orquestador. Lo de la primera se quedo "
   "adentro del hijo, y nadie lo paga dos veces."),

  ("espera",
   "En MODO=test la relacion sale AL REVES: TestModel repite la salida de "
   "las herramientas en vez de resumir. El programa lo avisa solo. Si "
   "quieres que se vea de verdad, proyecta tu corrida en MODO=gemini."),

  ("habla",
   "Una mas. Quiten usage igual ctx punto usage de una delegacion, y "
   "corran."),

  ("habla",
   "&iquest;Que le paso al conteo? El gasto del hijo dejo de contar para el "
   "padre. Y eso suena inofensivo hasta que lo dicen al reves: si el gasto "
   "del hijo no cuenta, <b>el limite del padre no esta limitando nada.</b> "
   "Tres subagentes sueltos son tres presupuestos sin techo."),

  ("pausa", ""),

  ("habla",
   "Ultima tarea, y es la que menos se ensena. Van a romper algo que no da "
   "error."),

  ("habla",
   "En la herramienta explorar, antes de llamar al subagente, ignoren lo que "
   "les pidio el orquestador y mandenle un encargo vago: \"Dime que hay en "
   "el proyecto.\" Corran con el objetivo de antes, y abran reporte punto "
   "md."),

  ("pausa", ""),

  ("habla",
   "Vean lo que paso. El explorador no fallo. Contesto bien &mdash; "
   "contesto perfectamente una pregunta que no era la que hacia falta. Y el "
   "orquestador escribio su reporte igual de convencido. Cero errores. "
   "Ningun cuatrocientos veintinueve. Y el resultado esta mal."),

  ("habla",
   "Ese es el costo real de delegar. No son los tokens del salto. Es que "
   "<b>el padre le encarga al hijo algo peor de lo que cree.</b> Cuando su "
   "MVP falle el sabado y los dos agentes \"funcionen\" &mdash; miren el "
   "encargo primero."),
 ]},

 {"bloque": "Ejercicio 4  ·  el esqueleto de tu MVP",
  "reloj": "55:00 – 65:00", "partes": [

  ("habla",
   "Ejercicio cuatro. Este archivo es suyo y se lo llevan."),

  ("habla",
   "Primero en papel. Cinco minutos, sin teclado. Y no copien el ejemplo de "
   "archivos del ejercicio tres: pongan lo que su equipo va a construir de "
   "verdad."),

  ("habla",
   "Cuatro preguntas. Una: &iquest;que hace su MVP, en UNA frase? Dos: que "
   "subagentes necesita, y por cada uno, que herramientas SI tiene y que "
   "herramientas NO tiene. Tres: cual de las cuatro razones justifica "
   "separarlo. Cuatro: cual es su limite de peticiones."),

  ("habla",
   "De las cuatro, la que importa es <b>que herramientas NO tiene.</b> Si no "
   "pueden contestar eso de un subagente, todavia no saben que estan "
   "construyendo. Saben que quieren uno, que no es lo mismo."),

  ("habla",
   "Y el filtro, que es lo que me van a agradecer el sabado: si un subagente "
   "no aisla contexto, no acota permisos, no reduce decisiones y no cambia "
   "de modelo, <b>ese subagente no deberia existir.</b> Haganlo una "
   "herramienta normal del orquestador."),

  ("habla",
   "Porque multi-agente no es gratis. Cada salto son peticiones, latencia, y "
   "una traduccion mas donde se pierde informacion &mdash; la que acabamos "
   "de ver en la ultima tarea."),

  ("trabajan",
   "6 min. Circula. No revises codigo: pregunta \"que hace tu MVP en una "
   "frase\" y \"cuantos subagentes y por que\". Si no contestan en veinte "
   "segundos, ahi esta el trabajo."),
 ]},

 {"bloque": "Cierre", "reloj": "65:00 – 70:00", "partes": [

  ("habla",
   "Vamos a cerrar. Dos ideas. Si se les olvida todo lo demas, estas dos "
   "aguantan."),

  ("habla",
   "La primera: <b>un subagente es una herramienta</b>, y su descripcion es "
   "un prompt. Todo lo del ejercicio uno aplica igual al ejercicio tres."),

  ("habla",
   "Y de ahi sale el diagnostico mas util que les puedo dar hoy: si el "
   "orquestador no esta usando a su subagente, casi siempre el problema no "
   "es el subagente. Es el docstring."),

  ("pausa", ""),

  ("habla",
   "La segunda: <b>lo que garantiza algo es el codigo, no el prompt.</b> El "
   "explorador no escribe porque no tiene la herramienta. Ningun agente se "
   "sale del sandbox porque hay una funcion que rechaza la ruta."),

  ("habla",
   "Cuando le den herramientas de escritura a un agente &mdash; y el sabado "
   "se las van a dar &mdash; esa es la diferencia que mas les va a importar."),

  ("habla",
   "Y una tercera, de regalo: pongan los limites antes de la primera "
   "corrida. No despues del susto."),

  ("pregunta",
   "&iquest;Que van a construir? Una frase por equipo."),
  ("espera",
   "Dos o tres equipos, no mas. Cierra con sus palabras, no con un resumen "
   "tuyo."),
 ]},
]


# ===========================================================================
# ESTILOS Y MOTOR
# ===========================================================================

def estilos():
    e = {}
    e["titulo"] = ParagraphStyle(
        "titulo", fontName="Helvetica-Bold", fontSize=22, leading=26,
        textColor=TINTA, spaceAfter=3)
    e["subtitulo"] = ParagraphStyle(
        "subtitulo", fontName="Helvetica", fontSize=10.5, leading=15,
        textColor=GRIS, spaceAfter=14)
    e["comoleer"] = ParagraphStyle(
        "comoleer", fontName="Helvetica", fontSize=10, leading=15,
        textColor=TINTA, spaceAfter=5, leftIndent=8)
    e["bloque"] = ParagraphStyle(
        "bloque", fontName="Helvetica-Bold", fontSize=15, leading=19,
        textColor=TINTA, spaceAfter=1)
    e["reloj"] = ParagraphStyle(
        "reloj", fontName="Helvetica-Bold", fontSize=9.5, leading=12,
        textColor=ACENTO, spaceAfter=2)
    # el texto hablado: grande y muy aireado, para leerlo de pie
    e["habla"] = ParagraphStyle(
        "habla", fontName="Helvetica", fontSize=12.5, leading=19.5,
        textColor=TINTA, spaceAfter=11)
    e["haz"] = ParagraphStyle(
        "haz", fontName="Helvetica-Oblique", fontSize=10, leading=14,
        textColor=GRIS, spaceAfter=10, leftIndent=16)
    e["pregunta"] = ParagraphStyle(
        "pregunta", fontName="Helvetica-Bold", fontSize=12.5, leading=19,
        textColor=ACENTO, spaceAfter=7)
    e["espera"] = ParagraphStyle(
        "espera", fontName="Helvetica-Oblique", fontSize=10, leading=14,
        textColor=GRIS, spaceAfter=11, leftIndent=16)
    e["trabajan"] = ParagraphStyle(
        "trabajan", fontName="Helvetica-Bold", fontSize=10.5, leading=15,
        textColor=VERDE, spaceAfter=0)
    return e


def banda_trabajan(texto, e):
    """Franja gris: aqui te callas."""
    p = Paragraph("ELLOS TRABAJAN &mdash; tu te callas.  " + texto, e["trabajan"])
    t = Table([[p]], colWidths=[155 * mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), BANDA),
        ("LINEBEFORE", (0, 0), (0, -1), 2.5, VERDE),
        ("LEFTPADDING", (0, 0), (-1, -1), 11),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    return t


def marca_pausa():
    t = Table([[""]], colWidths=[16 * mm], rowHeights=[1.1])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), LINEA),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
    ]))
    return t


def pie(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(GRIS)
    canvas.drawString(27 * mm, 13 * mm, "Libreto  ·  taller multi-agente")
    canvas.drawRightString(183 * mm, 13 * mm, "%d" % doc.page)
    canvas.setStrokeColor(LINEA)
    canvas.setLineWidth(0.4)
    canvas.line(27 * mm, 17 * mm, 183 * mm, 17 * mm)
    canvas.restoreState()


def contar_palabras():
    n = 0
    for b in LIBRETO:
        for tipo, texto in b["partes"]:
            if tipo in ("habla", "pregunta"):
                limpio = texto.replace("<b>", " ").replace("</b>", " ")
                limpio = limpio.replace("&mdash;", " ").replace("&iquest;", "")
                n += len(limpio.split())
    return n


def contar_trabajo():
    """Minutos declarados en las franjas de 'ellos trabajan'."""
    import re
    n = 0
    for b in LIBRETO:
        for tipo, texto in b["partes"]:
            if tipo == "trabajan":
                m = re.match(r"\s*(\d+)\s*min", texto)
                if m:
                    n += int(m.group(1))
    return n


def construir():
    e = estilos()
    doc = SimpleDocTemplate(
        str(SALIDA), pagesize=A4,
        leftMargin=27 * mm, rightMargin=28 * mm,
        topMargin=21 * mm, bottomMargin=23 * mm,
        title="Libreto - taller multi-agente", author="Felipe Icaza")

    palabras = contar_palabras()
    f = []

    f.append(Paragraph("Libreto del taller", e["titulo"]))
    f.append(Paragraph(
        "Sistemas Multi-Agente y Function Calling  ·  Hackathon FISC AI "
        "AGENTS  ·  UTP, salon 3-303", e["subtitulo"]))
    f.append(HRFlowable(width="100%", thickness=1.1, color=TINTA,
                        spaceBefore=0, spaceAfter=12))

    f.append(Paragraph("Como se lee esto", e["bloque"]))
    f.append(Spacer(1, 7))
    for linea in [
        "El <b>texto negro grande es literal</b>: es lo que dices en voz alta. "
        "Lo que esta en <b>negrita</b> dentro de una frase, acentualo.",
        "Lo <i>gris y en cursiva</i> NO se dice: es lo que haces, o la "
        "respuesta que estas buscando.",
        "Lo <font color=\"#0B5C8A\"><b>azul</b></font> son las preguntas que "
        "haces al salon. Despues de cada una, <b>callate</b> y espera.",
        "La <font color=\"#0B6B3A\"><b>franja verde</b></font> es cuando "
        "ellos trabajan y tu no hablas. La mayor parte del taller no es tuya.",
        "La barrita gris corta es una pausa. Respira. No la llenes.",
    ]:
        f.append(Paragraph("&bull;&nbsp;&nbsp;" + linea, e["comoleer"]))

    f.append(Spacer(1, 9))
    hablar = palabras / 140.0
    trabajo = contar_trabajo()
    resto = 70 - hablar - trabajo
    f.append(Paragraph(
        "<b>De donde salen los 70 minutos.</b> Hablando: %d palabras, unos "
        "<b>%.0f min</b> a ritmo de presentacion. Ellos trabajando: <b>%d "
        "min</b> en las franjas verdes. Queda <b>%.0f min</b>, y no son "
        "relleno: son las corridas, la espera del modelo, las preguntas "
        "sueltas y algun 429. Si te oyes hablando mucho mas de %.0f minutos, "
        "le estas quitando el tiempo a lo unico que se llevan puesto."
        % (palabras, hablar, trabajo, resto, hablar), e["comoleer"]))

    for i_b, b in enumerate(LIBRETO):
        f.append(PageBreak() if i_b == 0 else CondPageBreak(62 * mm))
        f.append(Spacer(1, 0 if i_b == 0 else 16))
        f.append(KeepTogether([
            Paragraph(b["reloj"], e["reloj"]),
            Paragraph(b["bloque"], e["bloque"]),
            HRFlowable(width="100%", thickness=0.6, color=LINEA,
                       spaceBefore=5, spaceAfter=11),
        ]))

        for tipo, texto in b["partes"]:
            if tipo == "habla":
                f.append(KeepTogether([Paragraph(texto, e["habla"])]))
            elif tipo == "pregunta":
                f.append(CondPageBreak(26 * mm))
                f.append(Paragraph(texto, e["pregunta"]))
            elif tipo == "espera":
                f.append(Paragraph(texto, e["espera"]))
            elif tipo == "haz":
                f.append(Paragraph("[ " + texto + " ]", e["haz"]))
            elif tipo == "pausa":
                f.append(Spacer(1, 1))
                f.append(marca_pausa())
                f.append(Spacer(1, 12))
            elif tipo == "trabajan":
                f.append(CondPageBreak(34 * mm))
                f.append(banda_trabajan(texto, e))
                f.append(Spacer(1, 13))

    doc.build(f, onFirstPage=pie, onLaterPages=pie)
    return SALIDA, palabras


if __name__ == "__main__":
    ruta, palabras = construir()
    print("PDF generado: %s" % ruta)
    print("%d palabras habladas  (~%.0f min a 140 ppm)  ·  %.0f KB"
          % (palabras, palabras / 140.0, ruta.stat().st_size / 1024))
