"""
listar_modelos.py  --  que modelos puede llamar TU llave, y si la llave sirve.

    python listar_modelos.py

Sirve para dos cosas:

  1. Confirmar el ID exacto del modelo. Google los renombra y los retira,
     y un ID viejo da 404. Revisa esto la manana del taller, no la semana
     anterior.

  2. Probar la llave por separado. Si aqui la llave funciona y el ejercicio
     falla, el problema no es la llave. Y al contrario.

No imprime la llave, solo su largo y sus primeros caracteres.
No necesita instalar nada: usa la libreria estandar.
"""

import json
import os
import pathlib
import sys
import urllib.error
import urllib.request

RAIZ = pathlib.Path(__file__).resolve().parent
ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models?key=%s"


def cargar_env():
    """Mismo .env que taller/config.py, con la misma regla: el entorno gana.

    Devuelve (existe, ruta, nombres_leidos, impostores).
    """
    archivo = RAIZ / ".env"
    # Nombres reales de la carpeta: en Windows (RAIZ / ".ENV").exists() es
    # True si existe ".env", y eso daria un aviso falso.
    reales = {p.name for p in RAIZ.iterdir() if p.is_file()}
    impostores = [n for n in (".env.txt", "env", "env.txt") if n in reales]

    if ".env" not in reales:
        return False, archivo, [], impostores

    nombres = []
    for linea in archivo.read_text(encoding="utf-8").splitlines():
        linea = linea.strip()
        if not linea or linea.startswith("#") or "=" not in linea:
            continue
        clave, _, valor = linea.partition("=")
        clave = clave.strip()
        if clave.startswith("export "):
            clave = clave[len("export "):].strip()
        if clave.startswith("$env:"):
            clave = clave[len("$env:"):].strip()
        nombres.append(clave)
        os.environ.setdefault(clave, valor.strip().strip("\"'"))
    return True, archivo, nombres, impostores


def tapada(v):
    return "%d caracteres, empieza con %r" % (len(v), v[:6])


def main():
    print("\n=== Modelos disponibles para tu llave ===\n")

    existe, ruta, nombres, impostores = cargar_env()
    print("[ .env ] busco en: %s" % ruta)
    if existe:
        print("[ .env ] leido. Variables que encontre: %s"
              % (", ".join(nombres) if nombres else "NINGUNA (archivo vacio "
                                                    "o mal formateado)"))
        esperadas = {"GEMINI_API_KEY", "GOOGLE_API_KEY"}
        if not esperadas & set(nombres):
            print("\n  El .env existe pero no trae GEMINI_API_KEY.")
            print("  La linea tiene que ser exactamente:")
            print("      GEMINI_API_KEY=AIza...")
            print("  Sin 'export', sin comillas, sin espacios antes del =.")
    else:
        print("[ .env ] NO EXISTE en esa ruta.")
        print("  Crealo desde la terminal, en la raiz del repo:")
        print("      printf 'MODO=gemini\\nGEMINI_API_KEY=tu_llave\\n' > .env")
    if impostores:
        print("\n  OJO: existe %s. El archivo tiene que llamarse '.env' "
              "exacto." % " y ".join(impostores))
        print("  Windows esconde las extensiones: si lo creaste con el "
              "Explorador, probablemente es .env.txt.")

    # OJO: este es el mismo orden de precedencia que usa Pydantic AI.
    # GOOGLE_API_KEY le gana a GEMINI_API_KEY. Es la trampa numero uno:
    # una GOOGLE_API_KEY vieja de otro proyecto tapa la llave nueva.
    google = os.environ.get("GOOGLE_API_KEY")
    gemini = os.environ.get("GEMINI_API_KEY")

    print("[ GOOGLE_API_KEY ] %s" % (tapada(google) if google else "no definida"))
    print("[ GEMINI_API_KEY ] %s" % (tapada(gemini) if gemini else "no definida"))

    if google and gemini and google != gemini:
        print("\n  AVISO: tienes las dos definidas y son DISTINTAS.")
        print("  Pydantic AI usa GOOGLE_API_KEY y descarta GEMINI_API_KEY.")
        print("  Si la buena es la de GEMINI, borra GOOGLE_API_KEY:")
        print("      PowerShell:  Remove-Item Env:GOOGLE_API_KEY")
        print("      bash:        unset GOOGLE_API_KEY")

    llave = google or gemini
    if not llave:
        print("\nNo hay llave. Ponla en .env:")
        print("    GEMINI_API_KEY=tu_llave")
        print("O sacala gratis en https://aistudio.google.com")
        return 1

    usada = "GOOGLE_API_KEY" if google else "GEMINI_API_KEY"
    print("\nUsando %s (la misma que va a usar Pydantic AI)." % usada)

    if llave != llave.strip():
        print("\n  AVISO: la llave tiene espacios o salto de linea al borde.")
        print("  Eso da 'API key not valid'. Quitalos del .env.")

    try:
        with urllib.request.urlopen(ENDPOINT % llave, timeout=30) as r:
            datos = json.load(r)
    except urllib.error.HTTPError as e:
        cuerpo = e.read().decode("utf-8", "replace")
        print("\n--- GOOGLE RECHAZO LA LLAVE  (HTTP %s) ---" % e.code)
        print(cuerpo[:900])
        if e.code in (400, 401, 403):
            print("\nCausas tipicas, en orden:")
            print("  1. La llave esta mal copiada (sobra un espacio o falta")
            print("     un caracter). Vuelve a copiarla de AI Studio.")
            print("  2. Tienes GOOGLE_API_KEY vieja tapando la nueva (arriba")
            print("     te digo cual se esta usando).")
            print("  3. La llave tiene restricciones de API o de IP en la")
            print("     consola de Google Cloud.")
        return 1
    except Exception as e:
        print("\n--- NO SE PUDO CONSULTAR  (%s) ---" % type(e).__name__)
        print("%s" % e)
        print("\nRevisa la conexion, el proxy o el firewall.")
        return 1

    modelos = []
    for m in datos.get("models", []):
        if "generateContent" in m.get("supportedGenerationMethods", []):
            modelos.append(m["name"].replace("models/", ""))

    if not modelos:
        print("\nLa llave sirve pero no hay modelos con generateContent.")
        return 1

    print("\nLa llave SIRVE. Modelos que puedes usar (%d):\n" % len(modelos))
    for n in sorted(modelos):
        marca = "  <-- flash: el bueno para cuota gratis" if (
            "flash" in n and "lite" not in n and n.count("-") <= 2) else ""
        print("    %s%s" % (n, marca))

    actual = os.environ.get("MODELO_GEMINI", "google:gemini-2.5-flash")
    sin_prefijo = actual.split(":", 1)[-1]
    print("\nTu MODELO_GEMINI actual: %s" % actual)
    if sin_prefijo in modelos:
        print("Ese ID esta en la lista: OK.")
    else:
        print("Ese ID NO esta en la lista: te va a dar 404.")
        sugerencia = next((n for n in sorted(modelos) if "flash" in n), modelos[0])
        print("Prueba con:")
        print("    MODELO_GEMINI=google:%s" % sugerencia)
        print("(o ponlo en el .env; acuerdate del prefijo google:)")

    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
