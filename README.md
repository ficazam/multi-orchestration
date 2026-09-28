# Taller: Sistemas Multi-Agente y Function Calling

Hackathon FISC AI AGENTS · UTP · Salón 3-303

Construimos sobre lo que ya viste en los talleres anteriores: Pydantic AI,
agentes, memoria y tools. Aquí vamos a lo que sigue — **orquestador con
subagentes** — y sales con el esqueleto del MVP que vas a presentar.

---

## Antes del taller (5 minutos)

```bash
git clone <url> taller-agentes
cd taller-agentes
pip install -r requirements.txt
python verificar.py
```

Si dice `Todo lo critico esta OK`, estás listo.

**Consigue tu llave de Gemini** en [aistudio.google.com](https://aistudio.google.com) →
*Get API key*. Es gratis, no pide tarjeta, toma dos minutos.

Copia el archivo de ejemplo y pon tu llave ahí:

```bash
cp .env.ejemplo .env
```

```
MODO=gemini
GEMINI_API_KEY=tu_llave
```

El `.env` está en `.gitignore`: tu llave no se sube. Si prefieres variables
de entorno, también funcionan y le ganan al archivo:

```bash
export MODO=gemini
export GEMINI_API_KEY=tu_llave
```

PowerShell:

```powershell
$env:MODO="gemini"
$env:GEMINI_API_KEY="tu_llave"
```

> **Cada quien necesita SU PROPIA llave.** La capa gratuita permite unas
> 5–15 peticiones por minuto. Una llave compartida entre 30 personas se
> muere en el primer ejercicio.

---

## Los dos modos

| `MODO` | Necesita | Para qué |
|---|---|---|
| `test` | nada | Verificar que tu código corre. Sin red, sin llave, sin gastar cuota. |
| `gemini` | `GEMINI_API_KEY` | Respuestas reales. |

`MODO=test` usa `TestModel` de Pydantic AI: llama a todas tus herramientas
con datos de relleno y no razona. Sirve para comprobar que la estructura
funciona **antes** de gastar peticiones. Arma en `test`, prueba en `gemini`.

---

## Si te sale un 429

Es el límite de tasa de Google, no tu código. Espera un minuto, o cambia a
`MODO=test` y sigue. El repo te lo dice con todas sus letras cuando pasa.

---

## Los ejercicios

| # | Archivo | Min | Qué construyes |
|---|---|---|---|
| 1 | `01_herramientas.py` | 20 | Una herramienta desde cero. El docstring **es** el prompt. |
| 2 | `02_bajo_el_capo.py` | 10 | Qué hace `run_sync` por dentro. Por qué el costo crece. |
| 3 | `03_delegacion.py` | 25 | **Orquestador + 2 subagentes.** El ejercicio central. |
| 4 | `04_mi_mvp.py` | 15 | El esqueleto de tu propio MVP. |

Cada archivo trae sus tareas en el docstring de arriba. **Corre primero, lee
después.**

```bash
python ejercicios/01_herramientas.py
```

`soluciones/` tiene la versión terminada de cada uno. Si te trabas, cópiala y
sigue con el grupo — no pierdas veinte minutos en un typo.

---

## Lo que hay aquí

```
taller/
  config.py        modelo, límites de uso, manejo de errores
  herramientas.py  las funciones que los agentes ejecutan
ejercicios/        lo que tú modificas
soluciones/        la versión terminada (1 y 3)
sandbox/           archivos de juguete con un bug plantado
verificar.py
```

---

## Dos cosas que vale la pena mirar en el código

**`taller/config.py` → `LIMITES`.** Son `UsageLimits` de Pydantic AI:
`request_limit` y `tool_calls_limit`. Con la cuota gratuita esto no es
higiene, es supervivencia — un bucle suelto se come tu día en una corrida.

**`taller/herramientas.py` → `_ruta_segura()`.** Ningún agente puede tocar
nada fuera de `sandbox/`. Eso no está en el prompt, está en el código. Un
prompt que dice "no borres nada" es una recomendación; una función que
rechaza la ruta es una garantía. Es la diferencia que más importa cuando le
das herramientas de escritura a un agente.
