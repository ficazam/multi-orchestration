"""
guion.py  --  genera el guion del taller en PDF.

    pip install reportlab
    python presentacion/guion.py

Deja el PDF en presentacion/guion.pdf.

Esto es para EL QUE PRESENTA, no para los estudiantes. El contenido esta
todo en la lista GUION de abajo: edita ahi y vuelve a correr.
"""

import pathlib

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    CondPageBreak, HRFlowable, KeepTogether, PageBreak, Paragraph,
    SimpleDocTemplate, Spacer, Table, TableStyle,
)

SALIDA = pathlib.Path(__file__).resolve().parent / "guion.pdf"

TITULO = "Sistemas Multi-Agente y Function Calling"
SUBTITULO = "Guion del taller  ·  Hackathon FISC AI AGENTS  ·  UTP, salon 3-303"

TINTA = colors.HexColor("#1a1a1a")
GRIS = colors.HexColor("#6b6b6b")
ACENTO = colors.HexColor("#0b5c8a")
FONDO_CODIGO = colors.HexColor("#f4f4f4")
BORDE = colors.HexColor("#d8d8d8")
ALERTA = colors.HexColor("#8a3b0b")


# ---------------------------------------------------------------------------
# EL CONTENIDO
# ---------------------------------------------------------------------------
# Cada bloque es un dict. Tipos de linea dentro de "cuerpo":
#   ("di",     texto)   lo que dices en voz alta
#   ("haz",    texto)   lo que haces o tecleas tu
#   ("codigo", texto)   lo que se ve en pantalla
#   ("pregunta", texto) pregunta abierta al salon
#   ("ojo",    texto)   trampa conocida, adelantate
#   ("nota",   texto)   nota para ti, no se dice

GUION = [
    {
        "titulo": "Antes de que entre nadie",
        "min": "5 min antes",
        "previo": True,   # no cuenta para el total del salon
        "meta": "Que la primera corrida del salon no falle.",
        "cuerpo": [
            ("haz", "Proyecta una terminal con fuente grande. 16pt minimo, "
                    "la gente del fondo tambien existe."),
            ("haz", "Corre <b>python verificar.py</b> en tu maquina delante "
                    "de ellos. Si tu verificador pasa, el suyo tambien deberia."),
            ("haz", "Ten dos terminales abiertas: una en MODO=test y otra en "
                    "MODO=gemini. Vas a saltar entre las dos todo el taller."),
            ("haz", "Escribe en el pizarron las dos lineas del .env. Las van a "
                    "pedir cuatro veces."),
            ("ojo", "El 80% de los problemas de instalacion son Python &lt;3.10 "
                    "o pip apuntando a otro interprete. Preguntalo de entrada: "
                    "<b>python --version</b>."),
            ("nota", "Si alguien llega sin llave de Gemini: MODO=test hace "
                     "todo el taller. No lo dejes bloqueado esperando la llave."),
        ],
    },
    {
        "titulo": "Apertura",
        "min": "4 min",
        "meta": "Encuadre. Que sepan que se llevan y por que no es un tema "
                "de moda.",
        "cuerpo": [
            ("di", "En el taller pasado vieron agentes, tools y memoria. Hoy "
                   "vamos a lo que sigue: un agente que manda a otros agentes. "
                   "Y salen de aqui con el esqueleto del MVP que presentan el "
                   "sabado."),
            ("di", "La frase que quiero que se lleven, y la vamos a repetir "
                   "todo el taller: <b>un subagente es un agente normal, "
                   "llamado desde dentro de una herramienta de otro agente.</b> "
                   "Eso es todo. No hay framework magico."),
            ("pregunta", "&iquest;Quien ha tenido un agente que se queda dando "
                         "vueltas y le quema la cuota? &mdash; Levanten la mano. "
                         "(Casi todos.) Eso tambien lo arreglamos hoy."),
            ("di", "Dos modos: <b>test</b> no usa red ni llave, sirve para "
                   "verificar que tu codigo corre. <b>gemini</b> da respuestas "
                   "de verdad. Armas en test, pruebas en gemini. Esa disciplina "
                   "es la diferencia entre llegar al sabado con cuota y sin cuota."),
            ("ojo", "Deja claro AHORA que cada quien necesita SU llave. Una "
                    "llave compartida entre 30 se muere en el ejercicio 1."),
        ],
    },
    {
        "titulo": "Ejercicio 1  &mdash;  la descripcion ES el prompt",
        "min": "16 min",
        "meta": "Que entiendan que el modelo no ve el codigo: ve el nombre, "
                "el docstring y los tipos.",
        "cuerpo": [
            ("haz", "Que todos corran el archivo tal cual, sin leerlo. "
                    "Primero corre, despues lee."),
            ("codigo", "python ejercicios/01_herramientas.py"),
            ("di", "Esa herramienta tiene un docstring que dice <b>\"Busca "
                   "cosas.\"</b> Miren lo que el agente hace con eso. No da "
                   "error: hace una llamada equivocada con total confianza. "
                   "Eso es lo peligroso."),
            ("di", "El modelo NO VE tu codigo. Ve tres cosas: el nombre de la "
                   "funcion, los tipos y el docstring. Esa es toda la interfaz. "
                   "Tu docstring no es documentacion, es prompt."),
            ("haz", "Ahora que arreglen el docstring. Un docstring util dice "
                    "tres cosas: que devuelve y en que formato, que NO acepta, "
                    "y que significa el resultado vacio."),
            ("nota", "Las tres son importantes pero la tercera es la que nadie "
                     "escribe: si 'Sin coincidencias' significa 'no esta' y no "
                     "'fallo', dilo, o el modelo reintenta en bucle."),
            ("haz", "Tarea 3 es la que importa: escriben una herramienta desde "
                    "cero. El cuerpo es una linea, el trabajo es el docstring."),
            ("pregunta", "&iquest;Alguien tiene un docstring que quiera leer en "
                         "voz alta? &mdash; Lee dos o tres y comparalos en vivo. "
                         "Aqui aprenden mas del de al lado que de ti."),
            ("ojo", "Tarea 5: piden un archivo que no existe. El agente LEE el "
                    "error y reintenta en vez de morirse. Eso pasa porque las "
                    "funciones devuelven el error como texto, no lanzan "
                    "excepcion. Es una decision de diseno, senalala."),
        ],
    },
    {
        "titulo": "Ejercicio 2  &mdash;  que hace run_sync por debajo",
        "min": "7 min",
        "meta": "Desmitificar el bucle. Que sepan por que el costo crece mas "
                "rapido que los pasos.",
        "cuerpo": [
            ("di", "Este es el ejercicio mas corto y el que mas les va a servir "
                   "el sabado cuando algo falle a las dos de la manana."),
            ("codigo", "mensajes = [objetivo]\n"
                       "mientras no termine:\n"
                       "    respuesta = modelo(mensajes, herramientas)\n"
                       "    si respuesta no pide herramientas: listo\n"
                       "    por cada herramienta pedida:\n"
                       "        salida = ejecutar(herramienta)\n"
                       "        mensajes.append(salida)   <-- SIN ESTO no avanza"),
            ("di", "Dos consecuencias. Una: el modelo <b>no tiene memoria</b> "
                   "entre llamadas. En cada vuelta se le reenvia el historial "
                   "completo. La lista es la memoria. Dos: por eso el paso 10 "
                   "carga los 9 anteriores, y el costo crece mas rapido que "
                   "los pasos."),
            ("haz", "Que corran y miren el historial impreso. Cada "
                    "ModelResponse es una llamada que pagaron."),
            ("codigo", "python ejercicios/02_bajo_el_capo.py"),
            ("haz", "Tarea 4: que bajen request_limit a 2 en taller/config.py y "
                    "corran otra vez. Que LEAN el mensaje de error."),
            ("di", "Ese tope es lo unico que separa un bug de una factura. "
                   "UsageLimits no es higiene, con la cuota gratis es "
                   "supervivencia."),
            ("pregunta", "Si su MVP necesita 30 pasos, &iquest;que le pasa al "
                         "historial? &iquest;Y al costo? &mdash; Dejalos "
                         "contestar. Esa respuesta es la puerta al ejercicio 3; "
                         "no la contestes tu."),
            ("nota", "No hay solucion en soluciones/ para este: no hay codigo "
                     "que escribir, es mirar y entender. Si alguien la busca, "
                     "dile eso."),
        ],
    },
    {
        "titulo": "Ejercicio 3  &mdash;  el bucle multi-agente",
        "min": "28 min  (EL CENTRAL)",
        "meta": "Que construyan un orquestador con dos subagentes y VEAN el "
                "aislamiento de contexto en numeros.",
        "cuerpo": [
            ("di", "Este es el ejercicio del taller. Lo que salga de aqui es "
                   "el esqueleto de su MVP."),
            ("codigo", "@orquestador.tool\n"
                       "async def explorar(ctx, pregunta: str) -> str:\n"
                       "    resultado = await explorador.run(pregunta, usage=ctx.usage)\n"
                       "    return resultado.output"),
            ("di", "Eso es todo el patron. Para el orquestador eso es una "
                   "herramienta cualquiera; no sabe que por dentro corrio otro "
                   "agente con su propio bucle."),
            ("haz", "Que corran el archivo tal cual. Ya funciona con UN "
                    "subagente. Que miren el reporte del final."),
            ("codigo", "python ejercicios/03_delegacion.py"),
            ("di", "Cuatro razones para separar un subagente, y solo una es la "
                   "principal. <b>Aislamiento de contexto:</b> el subagente "
                   "puede quemar 40.000 tokens leyendo y devolver 200 palabras; "
                   "esos 40.000 nunca entran al historial del padre. Las otras "
                   "tres: menos herramientas por decision, modelo por tarea, y "
                   "permisos."),
            ("di", "La de permisos miren la en el codigo: el explorador "
                   "<b>no tiene</b> escribir_archivo. No le pedimos que no "
                   "escriba. No tiene como. Un prompt que dice 'no borres nada' "
                   "es una recomendacion; una funcion que no existe es una "
                   "garantia."),
            ("haz", "TAREA PRINCIPAL, dales 12 minutos: que escriban el segundo "
                    "subagente, el escritor. Los TODO dicen que tiene que "
                    "cumplir, no como se escribe. El explorador de arriba es su "
                    "ejemplo funcionando: copian la forma, no el texto."),
            ("nota", "Hay solucion en soluciones/03_delegacion.py. Si alguien "
                     "se traba mas de 5 minutos, que la abra y siga con el "
                     "grupo. No pierdan 20 minutos en un typo."),
            ("haz", "Despues cambian el OBJETIVO a algo que necesite los dos: "
                    "\"Averigua que bug hay y escribe un resumen en "
                    "reporte.md\". Corren y abren sandbox/reporte.md."),
            ("ojo", "El bug del sandbox esta REPARTIDO: notas.txt tiene el "
                    "sintoma (el login falla con mayusculas, ticket 412) y "
                    "docs/arquitectura.md tiene la causa (el correo se guarda "
                    "sin normalizar). No se puede contestar leyendo un solo "
                    "archivo. Eso es lo que justifica al explorador."),
            ("haz", "Tarea 5, hazla tu en vivo: quita <b>usage=ctx.usage</b> de "
                    "una delegacion y corre."),
            ("pregunta", "&iquest;Que le paso al conteo? &iquest;Por que "
                         "conviene que el gasto del hijo cuente para el padre? "
                         "&mdash; Respuesta: si no, el limite del padre no "
                         "esta limitando nada. Tres subagentes sueltos son "
                         "tres presupuestos sin techo."),
            ("haz", "Tarea 6, el traspaso: que le manden al explorador un "
                    "encargo vago a proposito &mdash; <b>\"Dime que hay en el "
                    "proyecto.\"</b> &mdash; y abran reporte.md. Nadie fallo, "
                    "ningun 429, y el resultado esta mal. Ese es el costo real "
                    "de delegar: el padre le encarga al hijo algo peor de lo "
                    "que cree. Cuando su MVP falle el sabado y los dos agentes "
                    "\"funcionen\", que revisen el encargo primero."),
            ("nota", "El reporte del final mide <b>tokens que quemo el hijo</b> "
                     "contra <b>caracteres que devolvio</b>. En MODO=test esa "
                     "relacion sale al reves: TestModel repite la salida de las "
                     "herramientas en vez de resumir, y el explorador devuelve "
                     "mas de lo que quemo. El propio programa lo avisa. Si "
                     "quieres que se VEA, corre este ejercicio en MODO=gemini "
                     "en tu maquina y proyectalo: es el unico momento del taller "
                     "donde vale la pena gastar cuota en publico."),
        ],
    },
    {
        "titulo": "Ejercicio 4  &mdash;  el esqueleto de TU MVP",
        "min": "10 min",
        "meta": "Que salgan con una decision de arquitectura tomada, no con "
                "codigo bonito.",
        "cuerpo": [
            ("di", "Este archivo es suyo y se lo llevan. No copien el ejemplo "
                   "de archivos del ejercicio 3: pongan lo que su equipo va a "
                   "construir de verdad."),
            ("haz", "Primero EN PAPEL, 5 minutos, sin tocar el teclado. Las "
                    "cuatro preguntas del docstring."),
            ("di", "La pregunta que importa de las cuatro es: por cada "
                   "subagente, &iquest;que herramientas <b>NO</b> tiene? Si no "
                   "puedes contestar eso, no sabes que estas construyendo."),
            ("di", "Y el filtro: si un subagente no aisla contexto, no acota "
                   "permisos, no reduce decisiones y no cambia de modelo, "
                   "<b>ese subagente no deberia existir</b>. Hazlo una "
                   "herramienta normal del orquestador. Multi-agente no es "
                   "gratis: cada salto es latencia y peticiones."),
            ("haz", "Pasa por las mesas. No revises codigo: pregunta \"que "
                    "hace tu MVP en una frase\" y \"cuantos subagentes y por "
                    "que\". Si no contestan en 20 segundos, ahi esta el "
                    "trabajo."),
            ("ojo", "Si te queda corto el tiempo, este es el bloque que se "
                    "comprime: el archivo se lo llevan y lo siguen el sabado. "
                    "Lo que NO se comprime es el ejercicio 3."),
        ],
    },
    {
        "titulo": "Cierre",
        "min": "5 min",
        "meta": "Dos ideas que se llevan aunque olviden la sintaxis.",
        "cuerpo": [
            ("di", "Primera: <b>un subagente es una herramienta</b>, y su "
                   "descripcion es un prompt. Todo lo del ejercicio 1 aplica "
                   "igual al ejercicio 3. Si el orquestador no usa a tu "
                   "subagente, casi siempre el problema es el docstring."),
            ("di", "Segunda: <b>lo que garantiza algo es el codigo, no el "
                   "prompt.</b> El explorador no escribe porque no tiene la "
                   "herramienta. Ningun agente sale del sandbox porque hay una "
                   "funcion que rechaza la ruta. Cuando le den herramientas de "
                   "escritura a un agente el sabado, esa es la diferencia que "
                   "mas les va a importar."),
            ("haz", "Ensenales <b>_ruta_segura()</b> en taller/herramientas.py. "
                    "Son seis lineas."),
            ("di", "Y una tercera, gratis: pongan los limites ANTES de la "
                   "primera corrida, no despues del susto."),
            ("pregunta", "&iquest;Que van a construir? &mdash; Dos o tres "
                         "equipos en voz alta, una frase cada uno. Cierra con "
                         "eso, no con un resumen tuyo."),
        ],
    },
]


# --- material de reserva ---------------------------------------------------

EXTRAS = [
    ("Para el equipo que va adelantado: <b>output_type</b>",
     "Lo mas util de Pydantic AI que el taller no cubre. Un subagente que "
     "devuelve <b>output_type=Hallazgo</b> (un BaseModel) en vez de 80 "
     "palabras de prosa le da al padre datos verificables en vez de ingles "
     "que tiene que volver a interpretar. Para un MVP de hackathon es la "
     "mejora de mayor impacto por linea escrita."),
    ("Para el equipo que va adelantado: subagentes en paralelo",
     "Los dos subagentes del ejercicio 3 corren en serie. Si dos subagentes "
     "no dependen uno del otro, <b>asyncio.gather</b> los corre a la vez: son "
     "diez lineas y es el momento en que multi-agente empieza a pagar en "
     "lugar de solo costar un salto mas."),
    ("Si alguien pregunta: &iquest;y si un subagente falla?",
     "La herramienta del orquestador no atrapa nada, asi que una excepcion "
     "del hijo mata la corrida del padre. Para el sabado: envuelve el "
     "<b>await subagente.run(...)</b> en try/except y devuelve el error como "
     "TEXTO, igual que hacen las herramientas de taller/herramientas.py. El "
     "orquestador lo lee y decide, en vez de morirse."),
    ("Si alguien pregunta: &iquest;cuando NO usar subagentes?",
     "Cuando una sola herramienta alcanza. Cada delegacion son peticiones "
     "extra y latencia extra, y ninguna de las cuatro razones del ejercicio 3 "
     "la justifica sola si el trabajo cabe en una funcion. El filtro esta en "
     "el ejercicio 4: si no aisla contexto, no acota permisos, no reduce "
     "decisiones y no cambia de modelo, es una herramienta, no un agente."),
]

TRAMPAS = [
    ("429 / RESOURCE_EXHAUSTED",
     "Limite de tasa de Google, no es su codigo. Esperar 60 s o pasar a "
     "MODO=test. <b>correr()</b> ya lo explica solo; senala que el repo lo "
     "dice con todas sus letras."),
    ("404 model not found",
     "El ID del modelo cambio. Confirmar en aistudio.google.com y exportar "
     "<b>MODELO_GEMINI=google-gla:&lt;id&gt;</b>. Revisa esto la manana del "
     "taller, no la semana antes."),
    ("\"Puse mi llave y sigue dando respuestas raras\"",
     "Esta en MODO=test. El encabezado de cada corrida imprime <b>modo:</b> "
     "&mdash; ensenales donde mirar. Es la pregunta numero uno del dia."),
    ("\"Copie .env.ejemplo a .env y no pasa nada\"",
     "Revisar que el archivo se llame <b>.env</b> exacto y que este en la "
     "raiz del repo. Ojo con Windows escondiendo extensiones y dejando "
     ".env.txt."),
    ("Se acabo la cuota a mitad del taller",
     "MODO=test hace el taller completo. Nadie se queda sin hacer los "
     "ejercicios por esto. Dilo en voz alta cuando pase al primero."),
    ("Limite de UsageLimits alcanzado",
     "Es la red de seguridad haciendo su trabajo, no un bug. Si el caso es "
     "legitimo, se sube en taller/config.py. Buen momento para repetir por "
     "que existe."),
]

CHULETA_BUG = (
    "El bug plantado en sandbox/, para que no lo derives en vivo: "
    "<b>notas.txt</b> dice que el login falla cuando el correo tiene "
    "mayusculas y que es el ticket 412. <b>docs/arquitectura.md</b> dice que "
    "el correo se guarda tal cual lo escribe el usuario, sin normalizar. "
    "Juntando los dos: la comparacion contra la tabla <i>users</i> es "
    "sensible a mayusculas porque nadie normaliza antes de comparar. "
    "<b>pendientes.md</b> confirma que el ticket 412 sigue abierto."
)


# ---------------------------------------------------------------------------
# ESTILOS
# ---------------------------------------------------------------------------

def estilos():
    hoja = getSampleStyleSheet()
    e = {}

    e["titulo"] = ParagraphStyle(
        "titulo", parent=hoja["Title"], fontName="Helvetica-Bold",
        fontSize=23, leading=27, textColor=TINTA, alignment=TA_LEFT,
        spaceAfter=4)
    e["subtitulo"] = ParagraphStyle(
        "subtitulo", parent=hoja["Normal"], fontName="Helvetica",
        fontSize=10.5, leading=15, textColor=GRIS, spaceAfter=16)
    e["tesis"] = ParagraphStyle(
        "tesis", parent=hoja["Normal"], fontName="Helvetica-Oblique",
        fontSize=12, leading=17, textColor=ACENTO, spaceAfter=6,
        leftIndent=10, borderPadding=0)
    e["seccion"] = ParagraphStyle(
        "seccion", parent=hoja["Heading1"], fontName="Helvetica-Bold",
        fontSize=15, leading=19, textColor=TINTA, spaceBefore=2, spaceAfter=2)
    e["min"] = ParagraphStyle(
        "min", parent=hoja["Normal"], fontName="Helvetica-Bold",
        fontSize=9, leading=12, textColor=ACENTO, spaceAfter=1)
    e["meta"] = ParagraphStyle(
        "meta", parent=hoja["Normal"], fontName="Helvetica-Oblique",
        fontSize=9.5, leading=13, textColor=GRIS, spaceAfter=9)
    e["cuerpo"] = ParagraphStyle(
        "cuerpo", parent=hoja["Normal"], fontName="Helvetica",
        fontSize=10, leading=14, textColor=TINTA, spaceAfter=6,
        leftIndent=17, firstLineIndent=-17)
    e["codigo"] = ParagraphStyle(
        "codigo", parent=hoja["Normal"], fontName="Courier",
        fontSize=8.8, leading=12.4, textColor=TINTA)
    e["h2"] = ParagraphStyle(
        "h2", parent=hoja["Heading2"], fontName="Helvetica-Bold",
        fontSize=12.5, leading=16, textColor=TINTA,
        spaceBefore=13, spaceAfter=5)
    e["celda"] = ParagraphStyle(
        "celda", parent=hoja["Normal"], fontName="Helvetica",
        fontSize=9.3, leading=12.6, textColor=TINTA)
    e["celda_b"] = ParagraphStyle(
        "celda_b", parent=hoja["Normal"], fontName="Helvetica-Bold",
        fontSize=9.3, leading=12.6, textColor=TINTA)
    return e


ETIQUETAS = {
    "di":       ("DI",       ACENTO),
    "haz":      ("HAZ",      colors.HexColor("#0b6b3a")),
    "pregunta": ("PREGUNTA", colors.HexColor("#6b2f8a")),
    "ojo":      ("OJO",      ALERTA),
    "nota":     ("nota",     GRIS),
}


def bloque_codigo(texto, e):
    filas = [[Paragraph(l.replace(" ", "&nbsp;") or "&nbsp;", e["codigo"])]
             for l in texto.split("\n")]
    t = Table(filas, colWidths=[152 * mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), FONDO_CODIGO),
        ("BOX", (0, 0), (-1, -1), 0.5, BORDE),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 1.2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 1.2),
    ]))
    return t


def linea(tipo, texto, e):
    etiqueta, color = ETIQUETAS[tipo]
    marca = '<font color="#%s"><b>%s</b></font>' % (color.hexval()[2:], etiqueta)
    estilo = e["cuerpo"]
    if tipo == "nota":
        estilo = ParagraphStyle("n", parent=e["cuerpo"], textColor=GRIS,
                                fontName="Helvetica-Oblique")
        marca = '<font color="#%s">%s</font>' % (GRIS.hexval()[2:], etiqueta)
    return Paragraph("%s&nbsp;&nbsp;%s" % (marca, texto), estilo)


def tabla_dos_columnas(filas, e, ancho_izq=52):
    datos = [[Paragraph(a, e["celda_b"]), Paragraph(b, e["celda"])]
             for a, b in filas]
    t = Table(datos, colWidths=[ancho_izq * mm, (152 - ancho_izq) * mm])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LINEBELOW", (0, 0), (-1, -2), 0.4, BORDE),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 9),
        ("TOPPADDING", (0, 0), (-1, -1), 4.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4.5),
    ]))
    return t


def pie(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(GRIS)
    canvas.drawString(29 * mm, 13 * mm, "Guion del taller  ·  multi-orchestration")
    canvas.drawRightString(181 * mm, 13 * mm, "%d" % doc.page)
    canvas.setStrokeColor(BORDE)
    canvas.setLineWidth(0.4)
    canvas.line(29 * mm, 17 * mm, 181 * mm, 17 * mm)
    canvas.restoreState()


def construir():
    e = estilos()
    doc = SimpleDocTemplate(
        str(SALIDA), pagesize=A4,
        leftMargin=29 * mm, rightMargin=29 * mm,
        topMargin=22 * mm, bottomMargin=24 * mm,
        title="Guion del taller - Sistemas Multi-Agente",
        author="Felipe Icaza",
    )

    f = []

    # --- portada / arranque ------------------------------------------------
    f.append(Paragraph(TITULO, e["titulo"]))
    f.append(Paragraph(SUBTITULO, e["subtitulo"]))
    f.append(HRFlowable(width="100%", thickness=1.1, color=TINTA,
                        spaceBefore=0, spaceAfter=13))
    f.append(Paragraph(
        "&ldquo;Un subagente es un agente normal, llamado desde dentro de una "
        "herramienta del orquestador.&rdquo;", e["tesis"]))
    f.append(Paragraph(
        "Si se llevan una sola frase, es esa. La otra es que lo que garantiza "
        "algo es el codigo, no el prompt.", e["meta"]))

    total = sum(int(b["min"].split()[0]) for b in GUION if not b.get("previo"))
    f.append(Paragraph("Reparto del tiempo", e["h2"]))
    filas = [(b["min"], b["titulo"]) for b in GUION]
    filas.append(("= %d min" % total, "<i>sin contar los 5 min de preparacion "
                                     "antes de que entre nadie</i>"))
    f.append(tabla_dos_columnas(filas, e, ancho_izq=30))
    f.append(Paragraph(
        "70 <b>con apertura y cierre dentro</b>. Los minutos del README suman "
        "70 solo entre los cuatro ejercicios y no dejan nada para abrir ni "
        "cerrar; el margen salio del 2, que no tiene codigo que escribir, y "
        "del 4, que se termina el sabado. Se lo quedo el 3: seis tareas y un "
        "subagente desde cero no caben en 25. Si el slot real es de 60, corta "
        "el 4 &mdash; el 3 no se toca.", e["meta"]))

    # --- bloques -----------------------------------------------------------
    for i, b in enumerate(GUION):
        # Un bloque no arranca si no le quedan 48 mm: evita que el titulo
        # se quede solo al pie con una linea debajo.
        f.append(PageBreak() if i == 0 else Spacer(1, 14))
        if i:
            f.append(CondPageBreak(48 * mm))

        cabeza = [
            Paragraph(b["min"].upper(), e["min"]),
            Paragraph(b["titulo"], e["seccion"]),
            HRFlowable(width="100%", thickness=0.6, color=BORDE,
                       spaceBefore=4, spaceAfter=6),
            Paragraph("Objetivo: %s" % b["meta"], e["meta"]),
        ]
        f.append(KeepTogether(cabeza))

        for tipo, texto in b["cuerpo"]:
            if tipo == "codigo":
                f.append(Spacer(1, 2))
                f.append(bloque_codigo(texto, e))
                f.append(Spacer(1, 8))
            else:
                f.append(linea(tipo, texto, e))

    # --- anexos ------------------------------------------------------------
    f.append(PageBreak())
    f.append(Paragraph("Trampas conocidas", e["seccion"]))
    f.append(HRFlowable(width="100%", thickness=0.6, color=BORDE,
                        spaceBefore=4, spaceAfter=8))
    f.append(Paragraph(
        "Adelantate a estas. Cada una te ahorra cinco manos levantadas.",
        e["meta"]))
    f.append(tabla_dos_columnas(TRAMPAS, e))

    f.append(Paragraph("Chuleta: el bug del sandbox", e["h2"]))
    f.append(Paragraph(CHULETA_BUG, e["celda"]))

    f.append(Paragraph("Material de reserva", e["h2"]))
    f.append(Paragraph(
        "Para el equipo que termina temprano, o para la consulta de "
        "arquitectura del final.", e["meta"]))
    for titulo, texto in EXTRAS:
        f.append(Paragraph(titulo, e["celda_b"]))
        f.append(Spacer(1, 2.5))
        f.append(KeepTogether([Paragraph(texto, e["celda"])]))
        f.append(Spacer(1, 7))

    doc.build(f, onFirstPage=pie, onLaterPages=pie)
    return SALIDA


if __name__ == "__main__":
    ruta = construir()
    print("PDF generado: %s (%.0f KB)" % (ruta, ruta.stat().st_size / 1024))
