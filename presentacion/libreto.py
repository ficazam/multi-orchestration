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

Taller de DOS HORAS: ~69 min hablando, ~51 min de teclado.

El contenido esta en la lista LIBRETO de abajo. Edita ahi y vuelve a correr:
el PDF recalcula solo los minutos de charla a partir de las palabras, asi
que no se queda desfasado.
"""

import pathlib
import re

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    CondPageBreak, HRFlowable, KeepTogether, PageBreak, Paragraph,
    SimpleDocTemplate, Spacer, Table, TableStyle,
)

SALIDA = pathlib.Path(__file__).resolve().parent / "libreto.pdf"

MINUTOS_TALLER = 120
PALABRAS_POR_MINUTO = 135      # ritmo de presentacion, con sus pausas

TINTA = colors.HexColor("#14181C")
GRIS = colors.HexColor("#6E767D")
ACENTO = colors.HexColor("#0B5C8A")
VERDE = colors.HexColor("#0B6B3A")
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

 # =========================================================================
 {"bloque": "Apertura", "reloj": "0:00 – 10:00", "partes": [

  ("habla",
   "Buenas. En el taller pasado vieron tres cosas: agentes, herramientas y "
   "memoria. Ya saben registrar una funcion con arroba-agente-punto-tool-"
   "plain, y ya vieron un agente decidir cual herramienta usar. Hoy vamos a "
   "lo que sigue: un agente que manda a otros agentes."),

  ("habla",
   "Son dos horas. Y les digo de una lo que se llevan, porque esto no es "
   "teoria. Al final van a tener corriendo, en su maquina, un orquestador "
   "con subagentes, con salida estructurada, corriendo en paralelo, y que no "
   "se cae cuando un hijo se cae. Y el ultimo ejercicio es el esqueleto del "
   "MVP que presentan el sabado. No es un ejemplo de juguete que despues "
   "botan. Es su punto de partida."),

  ("pausa", ""),

  ("habla",
   "Antes de escribir una linea, la frase del dia. Si se les olvida toda la "
   "sintaxis de hoy, esta no: <b>un subagente es un agente normal, llamado "
   "desde dentro de una herramienta de otro agente.</b>"),

  ("habla",
   "Eso es todo. No hay una clase especial. No hay framework de "
   "orquestacion. No hay nada magico. Es una funcion que por dentro llama a "
   "otro agente. Cuando lo vean les va a parecer poca cosa, y esta bien que "
   "les parezca poca cosa. Lo dificil no es escribirlo. Lo dificil es saber "
   "cuando vale la pena, y eso es la mitad del taller."),

  ("pausa", ""),

  ("habla",
   "Empecemos por el problema, no por el patron. Porque si les enseno el "
   "patron primero, lo van a usar en todo, y la mitad de las veces va a "
   "estar de mas."),

  ("habla",
   "Imaginense un solo agente. Uno. Le dan quince herramientas: leer "
   "archivos, escribir, buscar, llamar a una API, consultar la base de "
   "datos, mandar correo. Y le dan una tarea que necesita treinta pasos. "
   "&iquest;Que se rompe?"),

  ("habla",
   "Se rompen cuatro cosas, y las van a ver todas hoy, en este orden."),

  ("habla",
   "Una: <b>el contexto.</b> Cada paso le reenvia al modelo todo lo "
   "anterior. En el paso treinta esta cargando veintinueve pasos de basura, "
   "incluidos archivos completos que leyo en el paso tres y que ya no "
   "importan. Se vuelve lento, caro, y en algun momento no cabe."),

  ("habla",
   "Dos: <b>las decisiones.</b> Con quince herramientas, en cada paso el "
   "modelo elige entre quince. Se equivoca mas que eligiendo entre tres. Y "
   "los errores se acumulan: un paso mal elegido contamina todo lo que "
   "viene detras."),

  ("habla",
   "Tres: <b>los permisos.</b> Si el agente tiene escribir-archivo, la "
   "tiene SIEMPRE. En los treinta pasos. Y basta uno raro para que te "
   "sobreescriba algo."),

  ("habla",
   "Y cuatro: <b>el costo.</b> Un solo modelo, normalmente el bueno y el "
   "caro, haciendo tanto el razonamiento duro como el trabajo mecanico de "
   "listar una carpeta."),

  ("pausa", ""),

  ("habla",
   "Los subagentes son la respuesta a esas cuatro. No a una idea de orden. A "
   "esas cuatro. Y esa es la razon por la que hoy vamos a medir cosas en vez "
   "de hablar de arquitectura: si no puedo mostrarles el numero, no les "
   "estoy dando una razon, les estoy dando una moda."),

  ("habla",
   "Y ya que estamos: <b>multi-agente esta de moda y la mayoria de la gente "
   "lo usa mal.</b> La mitad de los \"sistemas multi-agente\" que van a ver "
   "en internet deberian ser un agente con tres herramientas. Al final del "
   "taller les doy un filtro de cuatro preguntas para saber cuando NO "
   "hacerlo. Si el sabado el filtro les dice que no hace falta, no lo "
   "hagan. Un MVP simple que corre le gana a una arquitectura bonita que se "
   "cae en el demo."),

  ("pausa", ""),

  ("habla",
   "Una cosa mas antes de la logistica, para los que llegaron hoy sin haber "
   "venido al taller pasado. Un agente, en una frase, es un modelo dentro de "
   "un bucle con permiso para llamar funciones. Eso es. El modelo no ejecuta "
   "nada: dice \"quiero llamar a buscar-texto con este argumento\", y su "
   "codigo es el que ejecuta y le devuelve el resultado. Todo el poder de un "
   "agente son las funciones que ustedes le dieron. Ni una mas."),

  ("habla",
   "Y por eso todo el taller de hoy es, en realidad, sobre <b>que funciones "
   "le das, como se las describes, y a quien se las das.</b> No hay otra "
   "palanca."),

  ("pausa", ""),

  ("habla",
   "Dejenme contarles como se ve esto el sabado, para que sepan hacia donde "
   "vamos. El patron de MVP que se cae es siempre el mismo: un agente, doce "
   "herramientas, un prompt de dos paginas que dice \"eres un asistente "
   "experto, no cometas errores, no borres archivos\". Funciona en la prueba "
   "con el caso facil. Y en el demo, con el jurado mirando, elige la "
   "herramienta equivocada, o se queda en un bucle, o se come la cuota en el "
   "minuto dos."),

  ("habla",
   "El que aguanta se ve distinto: pocas herramientas por agente, "
   "descripciones aburridas y precisas, limites puestos desde el principio, "
   "y respuestas que el codigo puede verificar. Menos impresionante de "
   "explicar, mucho mas dificil de romper. Eso es lo que vamos a construir "
   "hoy, en seis pasos."),

  ("pausa", ""),

  ("habla",
   "Ahora, logistica, y pongan atencion aqui porque de esto depende que "
   "lleguen al final del taller con cuota."),

  ("habla",
   "Hay dos modos de trabajo. MODO igual test no usa red ni llave: usa el "
   "TestModel de Pydantic AI, que llama a todas sus herramientas con datos "
   "de relleno y no razona. Sirve para comprobar que su codigo corre. Y "
   "MODO igual gemini da respuestas de verdad y necesita la llave."),

  ("habla",
   "La regla es: <b>armen en test, prueben en gemini.</b> Escriban, "
   "verifiquen la forma en test, y solo cuando ya corre, cambien a gemini "
   "para ver el comportamiento real. Porque la capa gratis de Google da "
   "entre cinco y quince peticiones por minuto. Si prueban cada cambio "
   "contra el modelo real, a la mitad del taller se quedan sin cuota y "
   "terminan mirando la pantalla del vecino."),

  ("habla",
   "Y cada quien necesita SU llave. No la compartan. Una llave entre treinta "
   "personas se muere en el primer ejercicio, y ahi el problema deja de ser "
   "de Google y pasa a ser mio."),

  ("pregunta",
   "&iquest;A quien le falta la llave? Levanten la mano."),
  ("espera",
   "Los que levanten: diles que trabajen en MODO=test todo el taller, que "
   "funciona completo, y que saquen la llave en aistudio.google.com mientras "
   "corren el ejercicio 1. No los dejes bloqueados esperando."),

  ("haz", "Escribe en el pizarron las dos lineas del .env. Las van a pedir "
          "cuatro veces."),

  ("habla",
   "Si algo no les corre, lo primero es python verificar punto py. Les dice "
   "exactamente que falta. Y si les sale un cuatrocientos veintinueve en "
   "cualquier momento del taller: es el limite de tasa de Google, no es su "
   "codigo. El repo se los dice con todas sus letras. Esperan un minuto o "
   "se pasan a test y siguen."),
 ]},

 # =========================================================================
 {"bloque": "Ejercicio 1  ·  la descripcion es el prompt",
  "reloj": "10:00 – 28:00", "partes": [

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
   "funcion. Nunca. Ve tres cosas, nada mas. El nombre de la funcion. Los "
   "tipos de los parametros. Y el docstring. Esa es toda la interfaz."),

  ("habla",
   "O sea que su docstring no es documentacion. <b>Es prompt.</b> Es la "
   "unica instruccion que el modelo tiene para decidir si usa esa "
   "herramienta, cuando, y con que argumentos. Y si escriben un prompt de "
   "dos palabras, van a tener el comportamiento que merece un prompt de dos "
   "palabras."),

  ("habla",
   "Las tres partes cuentan, no solo el docstring. El <b>nombre</b> es lo "
   "primero que el modelo lee: buscar-texto le dice algo; func-dos o "
   "helper-final no le dicen nada. Los <b>tipos</b> son restricciones "
   "reales: si ponen linea dos puntos int, el modelo no les va a mandar "
   "\"cuarenta y dos\" en letras, porque Pydantic no se lo permite. Los "
   "tipos no son adorno, son la primera validacion."),

  ("pausa", ""),

  ("habla",
   "Ahora arreglen ese docstring. Y un docstring que sirve dice tres cosas."),

  ("habla",
   "Uno: <b>que devuelve, y en que formato.</b> No \"devuelve los "
   "resultados\". Devuelve lineas con formato archivo, dos puntos, numero, "
   "dos puntos, contenido, maximo veinte. Asi el modelo sabe que va a "
   "recibir antes de llamarla, y sabe como leerlo cuando llegue."),

  ("habla",
   "Dos: <b>que NO hace, o que no acepta.</b> Esta es la que evita la mitad "
   "de las llamadas malas. Si su herramienta no acepta carpetas, diganlo. Si "
   "no entiende expresiones regulares, diganlo. Porque si no lo dicen, el "
   "modelo lo va a intentar &mdash; no por tonto, sino porque nada se lo "
   "prohibio."),

  ("habla",
   "Y tres, la que nadie escribe y la que mas cuesta: <b>que significa el "
   "resultado vacio.</b> Si \"Sin coincidencias\" significa \"no esta\", y "
   "no significa \"la llamada fallo\", diganlo explicitamente. Porque si no, "
   "el modelo asume que fallo, y reintenta. Y vuelve a reintentar. Y ahi se "
   "les va la cuota, en un bucle que ustedes causaron con una omision de "
   "seis palabras."),

  ("habla",
   "Ese es el patron que quiero que se lleven: <b>los agentes no fallan "
   "tanto por lo que les dices; fallan por lo que no les dijiste.</b>"),

  ("pausa", ""),

  ("habla",
   "Y ya que estamos en herramientas, tres decisiones de diseno que van a "
   "tener que tomar el sabado y que casi nadie les va a explicar."),

  ("habla",
   "La primera: <b>que tan grande hacen cada herramienta.</b> Tienen dos "
   "extremos. Una sola herramienta gigante que hace todo &mdash; buscar, "
   "leer y resumir &mdash; o tres chiquitas. La grande le quita decisiones "
   "al modelo, y eso suena bien, pero tambien le quita informacion: si "
   "falla, no sabes en que parte fallo, y el modelo tampoco. Las chiquitas "
   "le dan control y te dan visibilidad. La regla practica: <b>una "
   "herramienta, un verbo.</b> Si el nombre de su funcion necesita un \"y\", "
   "probablemente son dos."),

  ("habla",
   "La segunda: <b>cuanto devuelven.</b> Miren leer-archivo en el repo: "
   "corta a cuatro mil caracteres. No es pereza, es presupuesto. Si una "
   "herramienta devuelve un archivo de cincuenta mil caracteres, eso entra "
   "al historial, y a partir de ahi <b>se reenvia en cada vuelta</b> del "
   "bucle. Una sola llamada descuidada les puede triplicar el costo de toda "
   "la corrida. Devolver de mas es tan malo como devolver de menos, y es "
   "mas caro."),

  ("habla",
   "La tercera: <b>que las llamen dos veces sin miedo.</b> Los agentes "
   "reintentan. Se equivocan y repiten. Si su herramienta manda un correo o "
   "cobra una tarjeta, que la llamen dos veces es un problema de verdad, no "
   "un detalle. En el sandbox de hoy todo es leer y escribir archivos y no "
   "pasa nada. El sabado, si le dan al agente algo que toca el mundo real, "
   "esa pregunta la tienen que contestar antes."),

  ("habla",
   "Fijense que ninguna de las tres es sobre el prompt. Son de diseno. El "
   "prompt del ejercicio uno se arregla en un minuto; estas tres se arreglan "
   "cuando decides la forma de la herramienta."),

  ("pausa", ""),

  ("habla",
   "Y una cosa mas sobre los tipos, porque es la validacion mas barata que "
   "existe y casi nadie la usa a fondo."),

  ("habla",
   "Cuando ustedes escriben ruta dos puntos str, Pydantic AI le manda al "
   "modelo un esquema que dice \"este parametro es texto\". Si escriben "
   "linea dos puntos int, el modelo no puede mandarles \"cuarenta y dos\" en "
   "letras: no pasa la validacion. Eso es una restriccion que ustedes "
   "consiguieron gratis, sin escribir una sola linea de comprobacion."),

  ("habla",
   "Y se puede apretar mucho mas. En vez de un string libre para un modo, "
   "usen un tipo cerrado con las tres opciones validas. En vez de un int "
   "suelto, un int con minimo y maximo. Cada vez que aprietan el tipo, le "
   "quitan al modelo una manera de equivocarse."),

  ("habla",
   "La forma de pensarlo es esta: <b>el docstring es persuasion, el tipo es "
   "ley.</b> El docstring le explica al modelo lo que deberia hacer y "
   "normalmente hace caso. El tipo decide lo que <b>puede</b> llegar a su "
   "codigo. Y es la misma idea que vamos a repetir tres veces hoy: si algo "
   "tiene que cumplirse, no lo pidan. Hagan que sea imposible incumplirlo."),

  ("trabajan",
   "9 min. Arreglan el docstring y escriben su propia herramienta desde "
   "cero. Circula. A quien acabe temprano, pidele que lea su docstring en "
   "voz alta; se aprende mas del de al lado que de ti."),

  ("habla",
   "Una ultima cosa de este ejercicio, y haganla ahora mismo: pidanle un "
   "archivo que no existe."),

  ("pausa", ""),

  ("habla",
   "El agente leyo el error y reintento. No se murio. Y eso no es suerte: es "
   "una decision de diseno, y esta en taller, herramientas punto py. Todas "
   "esas funciones devuelven el error <b>como texto</b> en vez de lanzar "
   "excepcion."),

  ("habla",
   "Piensenlo desde el agente. Si la funcion revienta, la excepcion sube y "
   "mata la corrida: el agente no se enteró de nada, simplemente dejo de "
   "existir. Si la funcion devuelve \"ERROR: el archivo no existe\", eso "
   "entra al historial como un mensaje mas, el modelo lo LEE, y corrige en "
   "el siguiente paso."),

  ("habla",
   "Apuntense esto para el sabado, porque es de las cosas mas utiles del "
   "taller: <b>en las herramientas de un agente, un error no es una "
   "excepcion. Es un dato.</b> Y lo vamos a volver a usar en el ejercicio "
   "cinco, con subagentes enteros en vez de funciones."),
 ]},

 # =========================================================================
 {"bloque": "Ejercicio 2  ·  que hace run_sync por debajo",
  "reloj": "28:00 – 42:00", "partes": [

  ("habla",
   "Ejercicio dos. Es el mas corto de escribir &mdash; no tiene nada que "
   "escribir &mdash; y es el que mas les va a servir cuando algo falle el "
   "sabado a las dos de la manana."),

  ("haz", "Proyecta el bucle y dejalo en pantalla todo el bloque."),

  ("habla",
   "run-sync no es magia. Es este bucle, y son seis lineas. Armas una lista "
   "de mensajes con el objetivo. Le pasas la lista al modelo. Si el modelo "
   "no pide herramientas, terminaste. Si pide, ejecutas la herramienta, le "
   "pegas la salida a la lista, y vuelves a llamar al modelo con la lista "
   "completa. Y otra vez."),

  ("habla",
   "Fijense en la linea que dice mensajes punto append. Sin esa linea el "
   "bucle no avanza nunca: el modelo volveria a pedir la misma herramienta "
   "eternamente, porque nadie le dijo el resultado."),

  ("pausa", ""),

  ("habla",
   "De ahi salen dos cosas, y las dos importan mas de lo que parecen."),

  ("habla",
   "La primera: <b>el modelo no tiene memoria.</b> Ninguna. Cero. No "
   "\"recuerda\" el paso anterior. En cada vuelta se le reenvia el historial "
   "entero, desde el principio. Esa lista de mensajes ES la memoria. No hay "
   "nada mas. Cuando alguien dice que su agente \"se acuerda\", lo que pasa "
   "es que alguien esta reenviando texto."),

  ("habla",
   "La segunda sale de la primera, y es de plata. El paso uno manda un "
   "mensaje. El paso dos manda tres. El paso diez manda los nueve "
   "anteriores mas el nuevo. O sea que el costo de una corrida <b>no crece "
   "con los pasos: crece mas rapido que los pasos.</b>"),

  ("habla",
   "Hagan la cuenta gruesa conmigo. Digamos que cada paso agrega mil tokens. "
   "En el paso diez no pagaron diez mil: pagaron mil, mas dos mil, mas tres "
   "mil... hasta diez mil. Cincuenta y cinco mil tokens para diez pasos que "
   "\"generaron\" diez mil. Y en treinta pasos son casi medio millon."),

  ("habla",
   "Y hay un segundo techo, que no es de plata: la <b>ventana de "
   "contexto.</b> En algun punto el historial ya no cabe en la peticion. Ahi "
   "no te sale una factura mas alta: te sale un error, o el modelo empieza a "
   "olvidar el principio. Los subagentes del proximo ejercicio existen "
   "sobre todo por esto."),

  ("habla",
   "Antes de que corran, les explico que van a ver, porque el archivo imprime "
   "el historial completo y a la primera parece sopa de letras."),

  ("habla",
   "Van a ver dos tipos de mensaje alternandose. <b>ModelRequest</b> es lo "
   "que ustedes le mandaron al modelo. <b>ModelResponse</b> es lo que "
   "contesto. Y adentro de cada uno hay partes: una ToolCallPart es el "
   "modelo pidiendo una herramienta, y una ToolReturnPart es el resultado "
   "que su codigo le devolvio."),

  ("habla",
   "Cuenten los ModelResponse. <b>Cada ModelResponse es una peticion que "
   "pagaron.</b> Y si hay cuatro, es porque el bucle dio cuatro vueltas, no "
   "porque hicieron cuatro cosas. Esta es la pantalla que van a querer mirar "
   "el sabado cuando su agente \"se tarde mucho\" o \"gaste mucho\": casi "
   "siempre la respuesta esta ahi, en una vuelta de mas que nadie pidio."),

  ("trabajan",
   "4 min. Corren y miran el historial impreso. Que cuenten los "
   "ModelResponse. Despues bajan request_limit a 2 en taller/config.py y "
   "corren otra vez."),

  ("habla",
   "Lo que acaban de ver con el limite en dos es UsageLimits haciendo su "
   "trabajo: corto el agente antes de que siguiera gastando."),

  ("habla",
   "Y hay dos topes distintos, no uno. <b>request-limit</b> cuenta llamadas "
   "al modelo: te protege del bucle de razonamiento, del agente que piensa "
   "en circulos. <b>tool-calls-limit</b> cuenta ejecuciones de "
   "herramientas: te protege del agente que lee cuatrocientos archivos "
   "porque no encontro lo que buscaba. Son fallos distintos y hacen falta "
   "los dos."),

  ("habla",
   "Ese par de numeros es lo unico que separa un bug de una factura. Con "
   "cuota gratis no es higiene, es supervivencia. <b>Ponganlos antes de la "
   "primera corrida, no despues del susto.</b>"),

  ("pausa", ""),

  ("habla",
   "Y una pregunta que siempre sale aqui: si el problema es que el historial "
   "crece, &iquest;por que no lo cortamos y ya? Se puede, y hay tres "
   "maneras, con sus costos."),

  ("habla",
   "Una: <b>truncar.</b> Botan los mensajes viejos. Es gratis y es "
   "peligroso: si botan el que tenia el dato que hacia falta, el agente se "
   "vuelve a poner a buscarlo, y gastan mas de lo que ahorraron."),

  ("habla",
   "Dos: <b>resumir.</b> Cada tantos pasos, le piden al modelo que "
   "comprima lo anterior. Funciona, pero cuesta una peticion, y cada resumen "
   "pierde detalle. Resumen de resumen de resumen y ya no queda nada "
   "concreto."),

  ("habla",
   "Y tres: <b>no meterlo nunca.</b> Que el trabajo sucio pase en otro "
   "historial, y que al principal solo llegue la conclusion. Eso es un "
   "subagente, y es la unica de las tres que no pierde nada del historial "
   "principal, porque nunca lo ensucio."),

  ("pregunta",
   "Si su MVP necesita treinta pasos, &iquest;que le pasa al historial? "
   "&iquest;Y al costo? &iquest;Y a la ventana de contexto?"),
  ("espera",
   "Dejalos contestar. NO contestes tu. La respuesta es la puerta al "
   "ejercicio 3; si la das tu, el ejercicio 3 pierde el porque."),

  ("habla",
   "Exacto. Y esa es la razon por la que existe el ejercicio tres."),

  ("pausa", ""),

  ("habla",
   "Y antes de pasar, dos minutos sobre algo que no esta en ningun tutorial "
   "y que el sabado les va a salvar la noche: <b>como se depura un "
   "agente.</b>"),

  ("habla",
   "El problema es que un agente que falla casi nunca tira un error. Les "
   "devuelve una respuesta razonable que esta mal. Y entonces la gente hace "
   "lo unico que se le ocurre: le cambia el prompt. Le agrega \"por favor se "
   "preciso\", lo corre otra vez, sale distinto, y creen que lo arreglaron. "
   "No arreglaron nada: movieron la ruleta."),

  ("habla",
   "Hay tres cosas que mirar, y las tres estan en este repo."),

  ("habla",
   "La primera: <b>el historial.</b> El que acabamos de imprimir. Ahi se ve "
   "que herramienta pidio, con que argumentos, y que le devolvio. El noventa "
   "por ciento de los \"el modelo esta tonto\" son en realidad un argumento "
   "mal armado que esta escrito ahi, en texto plano, esperando que alguien lo "
   "lea."),

  ("habla",
   "La segunda: <b>el uso.</b> Peticiones y herramientas. Si esperaban tres "
   "pasos y gastaron nueve, hubo un bucle. Ese numero les dice que hay un "
   "problema antes de que la factura se los diga."),

  ("habla",
   "Y la tercera, que es una costumbre mas que una herramienta: <b>impriman "
   "lo que le mandan a cada subagente.</b> Fijense que las delegaciones del "
   "ejercicio tres imprimen \"delegando al explorador\". En su MVP, impriman "
   "tambien <b>el encargo</b>. Una linea. Y cuando algo salga raro, van a "
   "ver con sus ojos lo que el hijo recibio en vez de suponerlo. Van a "
   "entender por que insisto en esto en unos veinte minutos."),
 ]},

 # =========================================================================
 {"bloque": "Ejercicio 3  ·  el bucle multi-agente",
  "reloj": "42:00 – 72:00", "partes": [

  ("habla",
   "Ejercicio tres. Este es el del taller. Si hoy solo se llevan un archivo, "
   "que sea este."),

  ("haz", "Proyecta el patron de cinco lineas y dejalo en pantalla."),

  ("habla",
   "Miren el patron. Son cinco lineas. Es una herramienta del orquestador, "
   "decorada con arroba-orquestador-punto-tool. Y por dentro, en vez de "
   "hacer el trabajo, llama a otro agente y devuelve su salida. Nada mas."),

  ("habla",
   "Una diferencia de sintaxis que importa: aqui es punto-tool, no "
   "punto-tool-plain. La version sin plain te pasa un contexto como primer "
   "parametro, el ctx. Lo necesitan para una cosa que vamos a ver en un "
   "rato, y es la que mas gente olvida."),

  ("habla",
   "Y aqui esta lo importante: <b>para el orquestador esto es una "
   "herramienta cualquiera.</b> No sabe que por dentro corrio otro agente "
   "con su propio bucle de diez pasos. Ve una funcion que le devolvio un "
   "texto. Igualito que buscar-texto en el ejercicio uno."),

  ("pausa", ""),

  ("habla",
   "Ahora, las cuatro razones. Son las cuatro cosas que se rompian con el "
   "agente unico de hace media hora, en el mismo orden."),

  ("habla",
   "La primera, y la principal: <b>aislamiento de contexto.</b> El "
   "subagente puede quemar cuarenta mil tokens leyendo archivos, y "
   "devolverle doscientas palabras al padre. Esos cuarenta mil <b>nunca "
   "entran</b> al historial del orquestador."),

  ("habla",
   "Y acuerdense de la cuenta del ejercicio dos: cada paso del padre "
   "reenvia todo lo suyo. Si el padre cargara todo lo que leyeron sus hijos, "
   "reventaria en tres pasos. Por eso el aislamiento no es orden ni "
   "elegancia: es lo que hace que la cosa <b>funcione</b> a treinta pasos."),

  ("habla",
   "La segunda: <b>menos herramientas por decision.</b> El orquestador "
   "elige entre dos: explorar o escribir. El explorador elige entre tres. "
   "Nadie elige entre quince. Y menos opciones por paso es menos errores "
   "por paso."),

  ("habla",
   "La tercera: <b>modelo por tarea.</b> El orquestador razona, y puede "
   "necesitar el modelo bueno. El que lista una carpeta y copia texto no "
   "necesita razonar nada, y puede correr en el mas barato y mas rapido. "
   "Hoy los dos corren en el mismo porque estamos en cuota gratis, pero el "
   "sabado eso es plata real."),

  ("habla",
   "Y la cuarta: <b>permisos.</b> Esta mirenla en el codigo, porque es la "
   "que mas les va a importar el sabado."),

  ("haz", "Ensena el explorador: sus tres herramientas, y que no esta "
          "escribir_archivo."),

  ("habla",
   "El explorador tiene tres herramientas: buscar, leer y listar. No tiene "
   "escribir-archivo. Y no es que le pedimos amablemente que no escriba. "
   "<b>No tiene con que.</b> Aunque el modelo decida que lo mejor del mundo "
   "seria sobreescribir un archivo, no hay funcion que llamar."),

  ("habla",
   "Digan esto conmigo, porque es la idea mas importante del taller despues "
   "de la del principio: <b>un prompt que dice \"no borres nada\" es una "
   "recomendacion. Una funcion que no existe es una garantia.</b>"),

  ("haz", "Abre taller/herramientas.py y ensena _ruta_segura(). Son seis "
          "lineas."),

  ("habla",
   "Lo mismo con el sandbox. Ningun agente de este repo puede tocar un "
   "archivo fuera de la carpeta sandbox. Y no es porque el prompt lo pida: "
   "es porque hay una funcion que resuelve la ruta y la rechaza si se sale. "
   "Seis lineas de Python."),

  ("habla",
   "Y fijense en el detalle, que es donde casi todo el mundo se equivoca: "
   "compara <b>rutas</b>, no texto. Si compararan el texto del principio, "
   "una carpeta hermana llamada sandbox-guion-malo pasaria el filtro, porque "
   "su ruta empieza igual que la del sandbox. Esa clase de error es "
   "exactamente la que uno no ve hasta que alguien la busca."),

  ("habla",
   "Esa es la idea general: <b>lo que garantiza algo es el codigo, no el "
   "prompt.</b> El prompt es para que se porte bien. El codigo es para "
   "cuando no."),

  ("pausa", ""),

  ("habla",
   "Ahora, la pregunta que de verdad importa y que nadie contesta: "
   "&iquest;<b>donde ponen la linea?</b> &iquest;Como deciden que dos "
   "agentes y no uno, o cuatro?"),

  ("habla",
   "Mi respuesta practica: <b>corten donde el contexto se puede tirar.</b> "
   "Si despues de un pedazo de trabajo se puede botar todo lo que se leyo y "
   "quedarse solo con la conclusion, ahi hay un subagente. Si el siguiente "
   "paso necesita todo el detalle del anterior, ahi no hay frontera y "
   "partirlo solo les agrega una traduccion."),

  ("habla",
   "Miren nuestro caso con ese lente. El explorador lee tres archivos "
   "completos y de todo eso lo unico que hace falta despues es \"el bug es "
   "este\". Se puede tirar el resto. Frontera clarisima. El escritor, en "
   "cambio, recibe el texto y lo escribe: no genera contexto que valga la "
   "pena tirar. &iquest;Y por que lo separamos, entonces? No por contexto. "
   "<b>Por permisos.</b> Es el unico que tiene escribir-archivo. Razon "
   "distinta, misma decision."),

  ("habla",
   "Y una que les va a picar: &iquest;puede un subagente tener sus propios "
   "subagentes? Si. Tecnicamente no hay nada que lo impida. Y para el "
   "sabado, mi consejo es: <b>no pasen de un nivel.</b> Cada nivel es otra "
   "traduccion, y ya van a ver en un rato lo que cuesta una sola. Dos "
   "niveles de delegacion en un MVP de hackathon es casi siempre una forma "
   "elegante de no saber por que salio mal."),

  ("pausa", ""),

  ("habla",
   "Otra cosa, y tomenle foto al codigo porque es facil de pasar por alto: "
   "miren las instrucciones del explorador. Dicen \"maximo ochenta "
   "palabras\" y le dan una estructura."),

  ("habla",
   "&iquest;Por que? Porque <b>la respuesta del subagente es lo unico que "
   "entra al padre.</b> Si el hijo contesta con quinientas palabras, "
   "acabamos de perder la mitad del aislamiento que nos costo tanto "
   "conseguir. El limite de largo del hijo no es cortesia: es la puerta por "
   "donde entra el costo al padre. Ponganselo a todos sus subagentes."),

  ("habla",
   "Y al reves, en el orquestador: sus instrucciones dicen que no investiga "
   "ni escribe el mismo, que delega, y en que orden. Un orquestador sin esa "
   "frase tiende a intentar hacer el trabajo solo, y entonces no tienen un "
   "orquestador: tienen un agente con pasos extra."),

  ("pausa", ""),

  ("habla",
   "Y el sintoma numero uno con el que van a pelear el sabado: <b>el "
   "orquestador no llama a su subagente.</b> Simplemente no lo usa, contesta "
   "cualquier cosa y termina. Van a pensar que el subagente esta roto."),

  ("habla",
   "Casi nunca esta roto. Revisen en este orden. Uno: el <b>docstring</b> de "
   "la herramienta &mdash; &iquest;dice cuando usarla? Si dice \"explora "
   "cosas\", estamos en el ejercicio uno otra vez. Dos: las "
   "<b>instrucciones del orquestador</b> &mdash; &iquest;le dijeron que "
   "delegue? Tres: &iquest;se quedo sin <b>limite</b> antes de llegar? Y "
   "cuatro, ya de ultimo, el subagente."),

  ("habla",
   "Ese orden les va a ahorrar horas. El problema casi siempre esta del lado "
   "del que decide, no del que ejecuta."),

  ("pausa", ""),

  ("habla",
   "Y el sintoma numero dos, que es el contrario: <b>el orquestador no "
   "para.</b> Delega, le devuelven algo, y en vez de contestar vuelve a "
   "delegar. Otra vez. Hasta que se acaba el limite."),

  ("habla",
   "Eso pasa porque nadie le dijo <b>cuando terminar.</b> Y no hay una "
   "funcion para eso: es una frase en sus instrucciones. Digan "
   "explicitamente que hacer cuando ya tenga la informacion: \"cuando el "
   "explorador te devuelva el hallazgo, escribe tu respuesta final y "
   "detente\". Sin eso, un modelo servicial va a seguir buscando mas "
   "contexto para siempre, porque mas contexto siempre parece mejor."),

  ("habla",
   "Y ahi es donde el limite del ejercicio dos se gana el sueldo: cuando el "
   "prompt falla, el tope corta. El prompt es la intencion; el limite es la "
   "red. Necesitan los dos, y por razones distintas."),

  ("pausa", ""),

  ("habla",
   "Ahora les toca, y es la tarea grande del dia. Van a escribir el segundo "
   "subagente: el escritor."),

  ("habla",
   "Los TODO en el archivo les dicen que tiene que cumplir, no como se "
   "escribe. Eso es a proposito &mdash; no les puse el codigo comentado "
   "para que lo descomenten. El explorador que esta justo arriba es su "
   "ejemplo, y esta funcionando: copien la forma, no el texto."),

  ("habla",
   "Tres pasos. Uno: el Agent, con sus instrucciones. Diganle que hace, que "
   "NO hace, y cuanto mide su respuesta. Dos: su unica herramienta, "
   "escribir-archivo. Solo esa &mdash; si de paso le dan leer-archivo, deja "
   "de ser un escritor y el aislamiento de permisos se les cae, que es lo "
   "que acabamos de decir que importaba. Y tres: registrenlo como "
   "herramienta del orquestador, con tool, no con tool-plain."),

  ("trabajan",
   "12 min. Es la tarea principal del taller. Si alguien lleva mas de cinco "
   "minutos trabado en un typo, que abra soluciones/ y siga con el grupo: "
   "no se pierde veinte minutos ahi."),

  ("habla",
   "Ahora cambien el OBJETIVO a algo que necesite los dos &mdash; averiguar "
   "el bug y escribir un resumen en reporte punto md &mdash; corran, y abran "
   "el archivo."),

  ("habla",
   "Y fijense en una cosa del sandbox, porque no es casualidad: <b>el bug "
   "esta repartido.</b> Notas punto txt dice el sintoma: el login falla "
   "cuando el correo tiene mayusculas, ticket cuatrocientos doce. Y docs, "
   "arquitectura punto md, dice la causa: el correo se guarda tal cual, sin "
   "normalizar."),

  ("habla",
   "No se puede contestar leyendo un solo archivo. Eso es lo que justifica "
   "tener un explorador: si la respuesta estuviera en un archivo, esto "
   "seria una herramienta, no un subagente."),

  ("pausa", ""),

  ("habla",
   "Miren ahora el reporte del final. Dice cuantos tokens de entrada quemo "
   "cada subagente, y cuantos caracteres devolvio. Esa segunda columna es lo "
   "unico que entro al historial del orquestador. Lo de la primera se quedo "
   "adentro del hijo, y nadie lo paga dos veces."),

  ("espera",
   "En MODO=test la relacion sale AL REVES: TestModel repite la salida de "
   "las herramientas en vez de resumir, y el explorador devuelve mas de lo "
   "que quemo. El programa lo avisa solo. Si quieres que se vea de verdad, "
   "proyecta TU corrida en MODO=gemini: es el mejor momento del taller para "
   "gastar cuota en publico."),

  ("habla",
   "Una cosa mas, y es la que olvida todo el mundo. Quiten usage igual ctx "
   "punto usage de una delegacion, y corran."),

  ("habla",
   "&iquest;Que le paso al conteo? El gasto del hijo dejo de contar para el "
   "padre. Y eso suena inofensivo hasta que lo dicen al reves: si el gasto "
   "del hijo no cuenta, <b>el limite del padre no esta limitando nada.</b> "
   "Ustedes creen que pusieron un techo de doce peticiones, y en realidad "
   "pusieron doce para el padre y ninguno para los hijos. Tres subagentes "
   "sueltos son tres presupuestos sin techo. Por eso necesitaban el ctx."),

  ("habla",
   "Y fijense en la consecuencia, que esta en config punto py: hay dos juegos "
   "de limites. LIMITES, para un agente solo, con seis peticiones. Y "
   "LIMITES-ORQ, para el orquestador, con doce. <b>No es que el orquestador "
   "sea mas importante: es que su cuenta incluye a sus hijos.</b> Si delegan "
   "tres veces y cada hijo da tres vueltas, el padre ya lleva nueve "
   "peticiones sin haber pensado casi nada el mismo."),

  ("habla",
   "O sea que cuando agreguen un subagente al MVP, tienen que subir el techo "
   "del padre. Y si no lo suben, el sintoma que van a ver no es \"me quede "
   "sin limite\": es que <b>el ultimo subagente nunca corre</b>, porque la "
   "cuota del padre se acabo antes de llegar a el. Ese es de los bugs mas "
   "confusos que hay, porque el codigo de ese subagente esta perfecto."),

  ("pausa", ""),

  ("habla",
   "Y ahora la ultima tarea de este bloque, que es la que menos se ensena en "
   "ningun lado. Van a romper algo que no da error."),

  ("habla",
   "En la herramienta explorar, antes de llamar al subagente, ignoren lo que "
   "les pidio el orquestador y mandenle un encargo vago: \"Dime que hay en "
   "el proyecto.\" Corran con el objetivo de antes, y abran reporte punto "
   "md."),

  ("trabajan", "3 min. Que lo hagan y que abran el reporte."),

  ("habla",
   "Vean lo que paso. El explorador <b>no fallo.</b> Contesto bien. "
   "Contesto perfectamente una pregunta que no era la que hacia falta. Y el "
   "orquestador tomo esa respuesta y escribio su reporte igual de "
   "convencido. Cero errores. Ningun cuatrocientos veintinueve. Ningun "
   "limite alcanzado. Y el resultado esta mal."),

  ("habla",
   "Ese es el costo real de delegar, y no es el que la gente cuenta. No son "
   "los tokens del salto. No es la latencia. Es que <b>el padre le encarga "
   "al hijo algo peor de lo que cree.</b> Cada delegacion es una traduccion, "
   "y en cada traduccion se pierde algo."),

  ("habla",
   "Guardense esto para el sabado: cuando su MVP falle y los dos agentes "
   "\"funcionen\" &mdash; los dos corren, ninguno tira excepcion, los logs "
   "estan limpios &mdash; <b>miren el encargo primero.</b> No el prompt del "
   "hijo, no el del padre: lo que el padre le paso al hijo."),

  ("pausa", ""),

  ("habla",
   "Y ya que les ensene como se rompe, les digo como se arregla, porque si "
   "no esto es solo una anecdota triste."),

  ("habla",
   "Un buen encargo lleva tres cosas. La primera: <b>el objetivo original, "
   "no la version resumida del padre.</b> Suena obvio y es el error mas "
   "comun: el orquestador \"interpreta\" lo que le pidieron y le manda al "
   "hijo su interpretacion. Si el objetivo era \"averigua el bug y escribe un "
   "resumen\", el explorador necesita saber que hay un resumen al final, "
   "porque eso cambia lo que le conviene recoger."),

  ("habla",
   "La segunda: <b>que va a hacer el padre con la respuesta.</b> \"Necesito "
   "esto para escribir un reporte de una frase\" produce una respuesta "
   "distinta a \"dime todo lo que encuentres\". El hijo no puede optimizar lo "
   "que no sabe."),

  ("habla",
   "Y la tercera: <b>que NO hace falta.</b> Igual que en los docstrings del "
   "ejercicio uno. \"No me listes todos los archivos, solo los que tengan "
   "que ver con el login.\" Sin eso, el hijo hace lo razonable, que es "
   "traerte todo, y ahi se te va el aislamiento."),

  ("habla",
   "Fijense que es el ejercicio uno otra vez, un nivel arriba. Ahi el "
   "docstring era el prompt de la herramienta. Aqui <b>el encargo es el "
   "prompt del subagente.</b> Y las dos cosas las escribe el padre, en "
   "tiempo de ejecucion, sin que nadie las revise."),
 ]},

 # =========================================================================
 {"bloque": "Ejercicio 4  ·  la salida estructurada",
  "reloj": "72:00 – 90:00", "partes": [

  ("habla",
   "Ejercicio cuatro. Y esto es lo que mas les va a cambiar el MVP por linea "
   "escrita, asi que aunque se lleven medio taller, llevense esto."),

  ("habla",
   "Hasta ahora nuestro explorador devolvia <b>prosa.</b> Ochenta palabras "
   "en espanol. Y el orquestador tenia que leerlas y creerselas. No podia "
   "comprobar nada. Piensenlo: \"no encontre la causa\" y \"la causa es que "
   "no se normaliza el correo\" son los dos un string. Para distinguirlos "
   "hay que entender espanol."),

  ("haz", "Proyecta la clase Hallazgo."),

  ("habla",
   "Aqui declaramos un esquema: una clase que hereda de BaseModel, con "
   "cuatro campos. Archivo, un string. Linea, un entero. Sintoma, un string. "
   "Y causa, que puede ser un string o puede ser nulo. Y despues le pasamos "
   "output-type igual Hallazgo al agente."),

  ("habla",
   "Con eso, resultado punto output ya no es un string. <b>Es un "
   "Hallazgo</b>, validado por Pydantic antes de que su codigo lo vea."),

  ("pausa", ""),

  ("habla",
   "Para que se vea la diferencia, pensemos en lo que el orquestador tendria "
   "que hacer con prosa. Le llega: \"Encontre que el login falla con "
   "mayusculas, esta reportado en notas punto txt como ticket cuatrocientos "
   "doce, aunque no pude confirmar la causa exacta.\""),

  ("habla",
   "Ahora ustedes, desde el codigo del padre, quieren saber tres cosas: "
   "&iquest;hay causa o no? &iquest;en que archivo? &iquest;en que linea? "
   "Con ese parrafo tienen tres opciones, y las tres son malas. Escriben "
   "expresiones regulares sobre espanol libre. O le piden a otro modelo que "
   "lo interprete, y pagan otra peticion para entender la respuesta que ya "
   "pagaron. O &mdash; y esto es lo que hace todo el mundo &mdash; no "
   "comprueban nada, le pasan el parrafo al siguiente paso, y rezan."),

  ("habla",
   "La tercera opcion es la que produce los MVP que funcionan en la prueba y "
   "se caen en el demo. Porque funcionan mientras el modelo conteste "
   "parecido a como contestaba ayer."),

  ("pausa", ""),

  ("habla",
   "Cuatro cosas cambian, y la primera es la grande."),

  ("habla",
   "Una: <b>el padre puede comprobar.</b> Si no hallazgo punto causa, dos "
   "puntos. Es una linea de Python. El orquestador deja de creer y empieza "
   "a verificar. Con prosa, para saber si el hijo encontro la causa, "
   "tendrian que preguntarle a otro modelo &mdash; o sea, pagar otra "
   "peticion para interpretar la respuesta que ya pagaron."),

  ("habla",
   "Dos: <b>el modelo ya no elige el formato.</b> Sin output-type, ustedes "
   "le piden en el prompt \"responde con archivo, linea y causa\", y a veces "
   "obedece, y a veces les mete una introduccion amable antes. Con "
   "output-type no es una peticion: si la respuesta no encaja en el esquema, "
   "Pydantic AI lo hace <b>reintentar</b>. El formato deja de ser suerte."),

  ("habla",
   "Tres: <b>se acaban los parseos.</b> Nadie tiene que sacar un numero de "
   "linea de una frase con una expresion regular a las dos de la manana. Y "
   "les prometo que eso, a las dos de la manana, no sale bien."),

  ("habla",
   "Y cuatro: <b>es mas barato.</b> Un objeto de cuatro campos ocupa menos "
   "tokens en el historial del padre que ochenta palabras de prosa. O sea "
   "que refuerza el aislamiento del ejercicio tres."),

  ("pausa", ""),

  ("habla",
   "Y hay una cosa que me gusta especialmente de esto, que es que <b>el "
   "esquema ES la instruccion.</b> Cuando agreguen un campo &mdash; por "
   "ejemplo confianza, de cero a diez &mdash; no van a tocar el prompt, y el "
   "modelo lo va a llenar igual. El esquema se le manda como parte de la "
   "definicion. Es la misma leccion del ejercicio uno: la interfaz es el "
   "prompt. Antes era el docstring; ahora es el tipo."),

  ("habla",
   "Su tarea principal aqui es la comprobacion. El docstring de la "
   "herramienta ya le promete al orquestador que va a devolver algo que "
   "empieza con INCOMPLETO si falta la causa. Cumplanlo: si el hallazgo "
   "viene sin causa, no sigan, devuelvan que falta, y dejen que el "
   "orquestador decida. Son dos lineas."),

  ("pausa", ""),

  ("habla",
   "Dos detalles del esquema que valen oro y que se ven en tres minutos."),

  ("habla",
   "El primero: <b>los campos opcionales son una decision de producto.</b> "
   "Fijense que causa puede ser nulo, a proposito, y que las instrucciones "
   "le dicen \"si no la encuentras, dejala en null, no la inventes\". Si "
   "hubieramos puesto causa como obligatoria, el modelo <b>tiene</b> que "
   "llenarla &mdash; y cuando un modelo tiene que llenar un campo que no "
   "sabe, se lo invents. Ustedes convirtieron un campo obligatorio en una "
   "alucinacion garantizada. Lo opcional es lo que le da permiso de no "
   "saber."),

  ("habla",
   "El segundo: para clasificar, usen tipos cerrados. Un Literal o un Enum "
   "&mdash; alto, medio, bajo &mdash; en vez de un string libre. Con string "
   "libre les va a llegar \"alto\", \"Alto\", \"muy alto\" y \"high\", y van "
   "a terminar escribiendo un if con cuatro casos. Con un tipo cerrado, o "
   "llega uno de los tres o Pydantic AI lo hace reintentar."),

  ("habla",
   "Y la letra chica, para que no los sorprenda: <b>los reintentos "
   "cuestan.</b> Cada vez que la respuesta no encaja en el esquema, hay otra "
   "peticion. Un esquema con quince campos obligatorios y descripciones "
   "vagas puede reintentar tres veces por llamada. O sea que un esquema "
   "demasiado exigente se les convierte en una factura. Pidan lo que "
   "necesitan para decidir. Nada mas."),

  ("trabajan",
   "7 min. Escriben la comprobacion y agregan un campo al esquema. En "
   "MODO=test la causa sale nula, asi que la rama de INCOMPLETO se ve sin "
   "gastar llave: eso es una ventaja, no un problema."),

  ("habla",
   "Y para que quede claro cuando NO usar esto: si lo que quieren del "
   "subagente es de verdad un resumen libre, para que lo lea una persona, "
   "dejenlo en prosa. El esquema es para lo que <b>alimenta una decision de "
   "codigo.</b> La regla practica: si el padre va a hacer un if con la "
   "respuesta, que sea un objeto."),
 ]},

 # =========================================================================
 {"bloque": "Ejercicio 5  ·  en paralelo, y cuando algo falla",
  "reloj": "90:00 – 105:00", "partes": [

  ("habla",
   "Ejercicio cinco. Dos cosas que separan un demo que aguanta de uno que se "
   "cae en el escenario. Y la segunda les va a pasar el sabado, se lo "
   "garantizo."),

  ("habla",
   "Primera: en serie contra en paralelo. En el ejercicio tres los "
   "subagentes corrian uno detras del otro, y estaba bien, porque el "
   "escritor necesitaba lo que encontro el explorador. Habia dependencia."),

  ("habla",
   "Pero cuando dos subagentes <b>no dependen uno del otro</b>, esperar al "
   "primero para arrancar el segundo es tiempo regalado. Aqui tenemos dos "
   "exploradores: uno busca el sintoma en las notas, el otro busca la causa "
   "en docs. Ninguno necesita lo del otro. Se arregla con una linea: "
   "asyncio punto gather."),

  ("habla",
   "Le pasan las dos corrutinas &mdash; y fijense, sin await en cada una "
   "&mdash; y gather las espera a las dos. La corrida cuesta lo que el mas "
   "lento, no la suma de los dos."),

  ("habla",
   "Y ahora la letra chica, que es importante con cuota gratis: <b>el reloj "
   "baja, el gasto no.</b> Son las mismas dos peticiones. Paralelizar no les "
   "ahorra ni un token; les ahorra segundos. Para un demo de tres minutos "
   "delante de un jurado, esos segundos valen. Para su cuota, no cambian "
   "nada. No confundan las dos cosas."),

  ("habla",
   "Y hay una trampa con el paralelo que tienen que oir hoy, porque con "
   "cuota gratis les va a morder: <b>el paralelo hace que el limite de tasa "
   "sea peor, no mejor.</b>"),

  ("habla",
   "Piensenlo. En serie, sus dos peticiones estan separadas por unos "
   "segundos. En paralelo, salen las dos <b>en el mismo instante.</b> Si "
   "Google les da cinco por minuto, dos rafagas simultaneas se acercan mucho "
   "mas rapido al techo que las mismas dos espaciadas. Ganaron segundos de "
   "reloj y compraron mas probabilidad de un cuatrocientos veintinueve."),

  ("habla",
   "Asi que el consejo para el sabado es concreto: <b>paralelicen de dos en "
   "dos, no de diez en diez.</b> Si tienen cinco subagentes independientes y "
   "los lanzan todos a la vez con cuota gratis, el gather les va a devolver "
   "cinco errores de limite en lugar de cinco respuestas. Y va a ser mas "
   "lento que haberlos hecho en serie, porque van a tener que reintentarlos "
   "todos."),

  ("habla",
   "Y la otra cosa que el paralelo no perdona: <b>si dos subagentes escriben, "
   "no los paralelicen.</b> Dos escritores sobre el mismo archivo, "
   "arrancando al mismo tiempo, es una carrera, y el que gana es el que "
   "termine ultimo. En paralelo van los que <b>leen.</b> Los que escriben, en "
   "serie, y con la escritura en un solo sitio."),

  ("pausa", ""),

  ("habla",
   "Segunda cosa, y la mas util: <b>los subagentes se caen.</b>"),

  ("habla",
   "La herramienta del orquestador que escribieron en el ejercicio tres no "
   "atrapa nada. Si el hijo lanza una excepcion, sube, y se muere el padre, "
   "y se muere la corrida completa. Y el sabado un subagente se va a caer: "
   "un cuatrocientos veintinueve, una ruta mala, un timeout, una respuesta "
   "que no encaja en el esquema."),

  ("habla",
   "Y la solucion ya la saben, porque la vieron en el ejercicio uno: "
   "<b>devolver el error como texto en vez de lanzarlo.</b> Ahi era una "
   "funcion que devolvia \"ERROR: el archivo no existe\". Aqui es un "
   "subagente entero. La idea es la misma: si el orquestador lo LEE, decide. "
   "Si le explota, no decide nada."),

  ("habla",
   "Y miren las instrucciones del orquestador de este archivo: le decimos "
   "explicitamente que si una herramienta devuelve algo que empieza con "
   "ERROR, no se detenga, use lo que si tiene, y diga que parte falta. Sin "
   "esa frase, atrapar la excepcion no sirve de nada: el padre se queda con "
   "un error en la mano y sin saber que hacer con el."),

  ("habla",
   "Hay un detalle en el que van a tropezar, y les aviso antes: tienen que "
   "proteger <b>las dos</b> delegaciones, la de en-serie y la de "
   "en-paralelo. Una sola delegacion sin try-except basta para matar la "
   "corrida, y el orquestador llama primero a en-serie. Si solo protegen "
   "una, van a jurar que su codigo no funciona."),

  ("habla",
   "Y esa es la regla general, no un detalle de este archivo: <b>toda "
   "delegacion va protegida.</b> No la que creen que es riesgosa. Todas."),

  ("pausa", ""),

  ("habla",
   "Y aprovechen que estamos aqui para pensar en todo lo que se puede caer, "
   "porque no es solo una excepcion de Python."),

  ("habla",
   "Se puede caer el <b>limite de tasa</b> a mitad de corrida: el paso uno "
   "pasa y el paso cuatro les da cuatrocientos veintinueve. Se puede caer un "
   "<b>timeout</b>, que es el peor porque no falla rapido: se queda ahi "
   "mientras el jurado los mira. Se puede caer la <b>validacion</b> del "
   "esquema del ejercicio anterior, despues de gastar los reintentos. Y se "
   "puede acabar el <b>limite</b> que ustedes mismos pusieron."),

  ("habla",
   "Y para cada uno hay dos respuestas posibles, y son distintas: "
   "<b>reintentar</b>, o <b>rendirse bien.</b> Un cuatrocientos "
   "veintinueve se reintenta, con una espera. Una ruta mala no: reintentarla "
   "da el mismo error y les quema dos peticiones en vez de una. La regla: "
   "<b>reintenta lo que es temporal; rindete con lo que es permanente.</b> Y "
   "si se rinden, que sea devolviendo texto que el padre pueda leer."),

  ("habla",
   "Lo cual nos lleva a la decision que de verdad importa, y que no es de "
   "codigo: &iquest;una respuesta a medias sirve o no sirve? Si su MVP "
   "encontro el sintoma pero no la causa, &iquest;lo muestran con una nota, "
   "o dicen que no pudieron? Eso es una decision de producto, y va en el "
   "prompt del orquestador. <b>Si no se la dicen, se la inventa.</b>"),

  ("habla",
   "Mi consejo para el sabado: que su MVP prefiera <b>siempre</b> decir "
   "\"esto es lo que tengo, y esto me falta\" antes que fallar en silencio o "
   "inventar. Un jurado perdona un resultado incompleto que se anuncia. No "
   "perdona uno que se descubre en vivo."),

  ("trabajan",
   "6 min. Tarea 2: gather. Tareas 3 y 4: descomentan el raise, ven morir la "
   "corrida, y despues la protegen. Recuerdales que son las dos "
   "delegaciones."),

  ("pausa", ""),

  ("habla",
   "Y ya que hablamos del demo, les dejo la lista de los diez minutos antes "
   "de presentar. Cinco cosas. Apuntenlas."),

  ("habla",
   "Una: <b>corranlo completo, una vez, antes de subir.</b> No un pedazo: "
   "de punta a punta, como lo van a mostrar. La mitad de los demos que se "
   "caen es la primera vez que alguien corre el flujo entero."),

  ("habla",
   "Dos: <b>tengan una corrida buena guardada.</b> Guarden la salida de una "
   "corrida que funciono. Si en vivo les da un cuatrocientos veintinueve, "
   "ensenan esa y explican que es limite de tasa. Eso no es hacer trampa, es "
   "tener un respaldo."),

  ("habla",
   "Tres: <b>sepan cuanto tarda.</b> Cronometrenlo. Si su flujo tarda "
   "cuarenta segundos, tienen que saberlo para llenar esos cuarenta "
   "segundos hablando, en vez de quedarse callados mirando la terminal."),

  ("habla",
   "Cuatro: <b>revisen los limites.</b> Si los subieron para probar, "
   "bajenlos. Un bucle en vivo, delante del jurado, con el tope en cien, es "
   "una forma muy publica de quedarse sin cuota."),

  ("habla",
   "Y cinco: <b>que el MVP diga lo que no sabe.</b> Lo que acabamos de "
   "hablar. Si le falto una parte, que la anuncie. Es la diferencia entre "
   "\"tiene una limitacion conocida\" y \"esta mal y no se dieron cuenta\"."),

  ("pregunta",
   "Si un subagente falla y el orquestador sigue, &iquest;quien decide si la "
   "respuesta final todavia sirve?"),
  ("espera",
   "La respuesta es: tu, en el prompt del orquestador. Es una decision de "
   "producto, no de codigo. Si no se lo dices, se la inventa."),
 ]},

 # =========================================================================
 {"bloque": "Ejercicio 6  ·  el esqueleto de tu MVP",
  "reloj": "105:00 – 117:00", "partes": [

  ("habla",
   "Ejercicio seis. Este archivo es suyo y se lo llevan. Lo siguen el "
   "sabado."),

  ("habla",
   "Primero en papel. Cinco minutos, sin teclado. Y no copien el ejemplo de "
   "archivos de los ejercicios: pongan lo que su equipo va a construir de "
   "verdad."),

  ("habla",
   "Cuatro preguntas. Una: &iquest;que hace su MVP, en UNA frase? Si "
   "necesitan dos, todavia no esta claro. Dos: que subagentes necesita, y "
   "por cada uno, que herramientas SI tiene y que herramientas NO tiene. "
   "Tres: cual de las cuatro razones justifica separarlo. Cuatro: cual es su "
   "limite de peticiones."),

  ("habla",
   "De las cuatro, la que importa es <b>que herramientas NO tiene.</b> Si no "
   "pueden contestar eso de un subagente, todavia no saben que estan "
   "construyendo: saben que quieren uno, que no es lo mismo. Contestar esa "
   "pregunta les obliga a decidir el limite de responsabilidad, y de ahi "
   "sale el prompt casi solo."),

  ("habla",
   "Y aqui esta el filtro que les prometi al principio, cuando les dije que "
   "la mitad de la gente usa esto mal. Por cada subagente, marquen: "
   "&iquest;aisla contexto? &iquest;acota permisos? &iquest;reduce "
   "decisiones? &iquest;cambia de modelo?"),

  ("habla",
   "Si no marcaron ninguna, <b>ese subagente no deberia existir.</b> "
   "Haganlo una herramienta normal del orquestador y ya. Porque "
   "multi-agente no es gratis: cada salto son peticiones extra, latencia "
   "extra, y una traduccion mas donde se pierde informacion &mdash; la que "
   "vimos en la ultima tarea del ejercicio tres."),

  ("habla",
   "Y una cosa practica, de la que nadie se acuerda hasta que duele: pongan "
   "MIS-LIMITES antes de la primera corrida. Cuando lleven tres subagentes, "
   "el techo del padre es el unico que cuenta &mdash; si pasaron el ctx."),

  ("pausa", ""),

  ("habla",
   "Y hagamos la cuenta de la cuota, porque es la que decide si el sabado "
   "llegan al demo o no, y casi nadie la hace."),

  ("habla",
   "Tienen entre cinco y quince peticiones por minuto. Una corrida de su MVP, "
   "con un orquestador y dos subagentes, les va a costar facil <b>de seis a "
   "diez peticiones.</b> Hagan la division: eso es <b>una o dos corridas "
   "completas por minuto</b>, en el mejor caso. No veinte. Una o dos."),

  ("habla",
   "O sea que si se ponen a probar cambiando una palabra del prompt y "
   "corriendo otra vez, van a estar esperando mas de lo que van a estar "
   "programando. Y a las once de la noche, esperando sesenta segundos entre "
   "intento e intento, se toman malas decisiones."),

  ("habla",
   "Por eso insisto con MODO igual test, y no es un detalle del taller: es "
   "la estrategia. <b>Todo lo que se puede verificar sin el modelo real, "
   "verifiquenlo sin el modelo real.</b> Que las herramientas se llaman, que "
   "las delegaciones ocurren, que el esquema valida, que el try-except "
   "atrapa. Nada de eso necesita que el modelo piense. Guarden las "
   "peticiones de verdad para las preguntas que solo el modelo real puede "
   "contestar."),

  ("habla",
   "Y una ultima sobre el alcance, que es donde se pierden los hackathones. "
   "Su MVP tiene que hacer <b>una</b> cosa de punta a punta, no cinco a "
   "medias. El sabado nadie les va a dar puntos por la arquitectura: les van "
   "a pedir que lo corran. Si corre y resuelve una cosa, ganaron. Si tiene "
   "cinco features y dos se caen en el demo, perdieron con mas trabajo."),

  ("habla",
   "Asi que cuando contesten la primera pregunta &mdash; que hace en una "
   "frase &mdash; esa frase es su alcance. Todo lo que no quepa ahi es para "
   "despues del demo."),

  ("trabajan",
   "5 min. Circula. No revises codigo: pregunta \"que hace tu MVP en una "
   "frase\" y \"cuantos subagentes y por que\". Si no contestan en veinte "
   "segundos, ahi esta el trabajo, no en el teclado."),
 ]},

 # =========================================================================
 {"bloque": "Cierre", "reloj": "117:00 – 120:00", "partes": [

  ("habla",
   "Vamos a cerrar. Dos ideas. Si se les olvida todo lo demas &mdash; la "
   "sintaxis, los nombres de los parametros, todo &mdash; estas dos "
   "aguantan."),

  ("habla",
   "La primera: <b>un subagente es una herramienta</b>, y su descripcion es "
   "un prompt. Todo lo del ejercicio uno aplica igual al ejercicio tres. Y "
   "de ahi sale el diagnostico mas util que les puedo dar hoy: si el "
   "orquestador no esta usando a su subagente, casi siempre el problema no "
   "es el subagente. Es el docstring."),

  ("habla",
   "La segunda: <b>lo que garantiza algo es el codigo, no el prompt.</b> El "
   "explorador no escribe porque no tiene la herramienta. Ningun agente se "
   "sale del sandbox porque hay una funcion que rechaza la ruta. El padre "
   "no se cree al hijo porque hay un esquema y un if. Y la corrida no se "
   "muere porque hay un try-except."),

  ("habla",
   "Cuando le den herramientas de escritura a un agente &mdash; y el sabado "
   "se las van a dar &mdash; esa es la diferencia que mas les va a "
   "importar."),

  ("habla",
   "Y una tercera, de regalo: pongan los limites antes de la primera "
   "corrida. No despues del susto."),

  ("pausa", ""),

  ("habla",
   "Para el sabado, tres cosas concretas y me callo. Una: <b>empiecen en "
   "MODO igual test.</b> Armen la forma completa &mdash; los agentes, las "
   "herramientas, las delegaciones &mdash; sin gastar una sola peticion. "
   "Cuando corra de punta a punta, entonces cambien a gemini. Van a llegar al "
   "demo con cuota."),

  ("habla",
   "Dos: <b>el repo se lo llevan entero.</b> Taller, config punto py tiene "
   "el manejo de errores ya escrito: el cuatrocientos veintinueve, el modelo "
   "que no existe, la llave mala, el limite alcanzado, todo traducido a algo "
   "que se entiende. Copienlo. No lo escriban otra vez a las dos de la "
   "manana."),

  ("habla",
   "Y tres: <b>el ejercicio seis es su plan.</b> Si el sabado empiezan a "
   "programar sin haber contestado las cuatro preguntas, van a construir "
   "subagentes que no hacian falta. Contesten primero. Son cinco minutos y "
   "les ahorran dos horas."),

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
    # el texto hablado: grande y aireado, para leerlo de pie
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
    p = Paragraph("ELLOS TRABAJAN &mdash; tu te callas.  " + texto,
                  e["trabajan"])
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
    """Palabras que se dicen en voz alta. No cuenta las notas."""
    n = 0
    for b in LIBRETO:
        for tipo, texto in b["partes"]:
            if tipo in ("habla", "pregunta"):
                limpio = re.sub(r"<[^>]+>", " ", texto)
                limpio = re.sub(r"&[a-z]+;", " ", limpio)
                n += len(limpio.split())
    return n


def contar_trabajo():
    """Minutos declarados en las franjas de 'ellos trabajan'."""
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
    hablar = palabras / float(PALABRAS_POR_MINUTO)
    trabajo = contar_trabajo()
    resto = MINUTOS_TALLER - hablar - trabajo
    f = []

    f.append(Paragraph("Libreto del taller", e["titulo"]))
    f.append(Paragraph(
        "Sistemas Multi-Agente y Function Calling  ·  Hackathon FISC AI "
        "AGENTS  ·  UTP, salon 3-303  ·  dos horas", e["subtitulo"]))
    f.append(HRFlowable(width="100%", thickness=1.1, color=TINTA,
                        spaceBefore=0, spaceAfter=12))

    f.append(Paragraph("Como se lee esto", e["bloque"]))
    f.append(Spacer(1, 7))
    for linea in [
        "El <b>texto negro grande es literal</b>: es lo que dices en voz "
        "alta. Lo que esta en <b>negrita</b> dentro de una frase, "
        "acentualo.",
        "Lo <i>gris y en cursiva</i> NO se dice: es lo que haces, o la "
        "respuesta que estas buscando.",
        "Lo <font color=\"#0B5C8A\"><b>azul</b></font> son las preguntas que "
        "haces al salon. Despues de cada una, <b>callate</b> y espera.",
        "La <font color=\"#0B6B3A\"><b>franja verde</b></font> es cuando "
        "ellos trabajan y tu no hablas.",
        "La barrita gris corta es una pausa. Respira. No la llenes.",
    ]:
        f.append(Paragraph("&bull;&nbsp;&nbsp;" + linea, e["comoleer"]))

    f.append(Spacer(1, 9))
    f.append(Paragraph(
        "<b>De donde salen los %d minutos.</b> Hablando: %d palabras, unos "
        "<b>%.0f min</b> a %d palabras por minuto. Ellos trabajando: <b>%d "
        "min</b> en las franjas verdes. Queda <b>%.0f min</b>, y no son "
        "relleno: son las corridas, la espera del modelo, las preguntas "
        "sueltas y algun 429. Hablas el <b>%.0f%%</b> del taller."
        % (MINUTOS_TALLER, palabras, hablar, PALABRAS_POR_MINUTO, trabajo,
           resto, 100.0 * hablar / MINUTOS_TALLER), e["comoleer"]))
    f.append(Paragraph(
        "Los relojes de cada bloque son el plan; estas cifras son lo que "
        "de verdad hay escrito aqui. Si editas el texto, se recalculan.",
        e["comoleer"]))

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
    return SALIDA, palabras, hablar, trabajo


if __name__ == "__main__":
    ruta, palabras, hablar, trabajo = construir()
    print("PDF generado: %s" % ruta)
    print("%d palabras habladas  ->  %.0f min hablando (%.0f%% del taller)"
          % (palabras, hablar, 100.0 * hablar / MINUTOS_TALLER))
    print("%d min de teclado en franjas verdes" % trabajo)
    print("%.0f min de corridas, esperas y preguntas"
          % (MINUTOS_TALLER - hablar - trabajo))
