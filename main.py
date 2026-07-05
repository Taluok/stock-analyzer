# ============================================
# STOCK ANALYZER - Proyecto 1
# AI FinTech Engineer Portfolio - Tania
# ============================================

#Conceptos financieros que aparecen acá:

#Retorno diario → cuánto subió o bajó el precio cada día en %
#MA20 / MA50 → promedios móviles para ver tendencia
#Volatilidad → desviación estándar = medida de riesgo
#Candlestick → gráfico de velas japonesa

import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ============================================
# SECCIÓN 1: INPUT DEL USUARIO
# ============================================
# Acá le preguntamos al usuario qué acción quiere analizar
# y por cuánto tiempo. Todo mediante la consola (terminal).
 
print("=" * 45)
# print() → muestra texto en la consola.
# "=" * 45 → en Python podés multiplicar un string por un número
# y repite ese caracter N veces. Resultado: "============...=" (45 veces).
# Es solo para que se vea prolijo en la terminal.
 
print("   ANALIZADOR DE ACCIONES - AI FinTech")
print("=" * 45)
# Estas dos líneas simplemente muestran el título del programa.
 
TICKER = input("\nIngresá el ticker (ej: AAPL, TSLA, BTC-USD): ").upper().strip()
# input() → pausa el programa, muestra el mensaje, y espera que el usuario
#            escriba algo y presione Enter. Lo que escribe se guarda en TICKER.
# .upper() → convierte todo a mayúsculas. Si el usuario escribe "aapl" → "AAPL".
# .strip()  → elimina espacios en blanco al principio y al final.
#             Evita errores si el usuario escribe " AAPL " con espacios.
# TICKER es una variable que guarda el símbolo de la acción (ej: "AAPL").
# En Python las variables en MAYÚSCULAS son convención para constantes
# (valores que no van a cambiar durante la ejecución del programa).
 
print("\nPERÍODOS DISPONIBLES:")
print("  1 → 1 mes")
print("  2 → 3 meses")
print("  3 → 6 meses")
print("  4 → 1 año")
print("  5 → 2 años")
# Mostramos el menú de opciones al usuario.
# El "\n" dentro del string es un salto de línea (como presionar Enter).
 
opcion = input("\nElegí una opción (1-5): ").strip()
# Guardamos la opción que elige el usuario (un string: "1", "2", etc.)
 
periodos = {"1": "1mo", "2": "3mo", "3": "6mo", "4": "1y", "5": "2y"}
# Esto es un DICCIONARIO — la estructura de datos más útil de Python.
# Es como un mapa de clave → valor. Similar a HashMap en Java.
# Relaciona la opción del usuario ("1", "2"...) con el código que
# entiende yfinance ("1mo", "3mo"...).
# Sintaxis: {clave: valor, clave: valor, ...}
 
PERIODO = periodos.get(opcion, "1y")
# .get(clave, valor_por_defecto) → busca la clave en el diccionario.
# Si el usuario escribió "4", devuelve "1y".
# Si escribió algo inválido (ej: "9"), devuelve "1y" como valor por defecto.
# Así el programa no se rompe si el usuario se equivoca.


# ============================================
# SECCIÓN 2: DESCARGAR DATOS DE YAHOO FINANCE
# ============================================

print(f"\nDescargando datos de {TICKER}...")
# Las f-strings (f"...") permiten insertar variables dentro de un string.
# {TICKER} se reemplaza por el valor real de la variable. Ej: "Descargando datos de AAPL..."
# Es equivalente a concatenar strings, pero más legible.

try:
    # TRY/EXCEPT → manejo de errores. Igual que try/catch en Java.
    # El código dentro del "try" se intenta ejecutar.
    # Si algo falla (error de internet, ticker inválido, etc.),
    # en vez de que el programa explote, salta al "except" y manejamos el error.

    stock = yf.Ticker(TICKER)
    # yf.Ticker() crea un objeto que representa esa acción en Yahoo Finance.
    # stock es ahora un objeto con toda la info de la empresa:
    # precios, dividendos, información financiera, etc.

    df = stock.history(period=PERIODO)
    # .history() descarga el historial de precios del período que pedimos.
    # Devuelve un DataFrame (df) — una tabla donde:
    #   - Cada FILA es un día de trading
    #   - Las COLUMNAS son: Open, High, Low, Close, Volume, Dividends, Stock Splits
    #
    # Open  → precio de apertura (al inicio del día)
    # High  → precio más alto del día
    # Low   → precio más bajo del día
    # Close → precio de cierre (al final del día) — el más importante
    # Volume → cantidad de acciones que se compraron/vendieron ese día

    if df.empty:
        # df.empty → propiedad que devuelve True si el DataFrame no tiene datos.
        # Esto pasa si el ticker no existe o no tiene datos históricos.
        print("No se encontraron datos. Verificá el ticker e intentá de nuevo.")
        exit()
        # exit() → termina el programa inmediatamente.

    print(f"Datos descargados: {len(df)} días de trading\n")
    # len(df) → devuelve la cantidad de filas del DataFrame.
    # Para 1 año son aproximadamente 252 días (días hábiles, sin fines de semana).

except Exception as e:
    # Exception → captura cualquier tipo de error que haya ocurrido en el try.
    # "as e" guarda el mensaje de error en la variable e.
    print(f"Error al descargar datos: {e}")
    exit()


# ============================================
# SECCIÓN 3: CALCULAR INDICADORES FINANCIEROS
# ============================================
# Acá agregamos nuevas columnas al DataFrame con cálculos financieros.
# df["NombreColumna"] = cálculo → crea una columna nueva o sobreescribe una existente.

df["Retorno"] = df["Close"].pct_change() * 100
# df["Close"] → la columna de precios de cierre. Es una Serie (lista de números).
# .pct_change() → calcula el cambio porcentual entre cada fila y la anterior.
#   Fórmula: (precio_hoy - precio_ayer) / precio_ayer
#   Si ayer cerró en $100 y hoy en $103 → retorno = 0.03
# * 100 → lo convertimos a porcentaje: 0.03 → 3%
# Resultado: cada día tiene su retorno diario en %.
# El primer día es NaN (Not a Number) porque no hay día anterior para comparar.

df["MA20"] = df["Close"].rolling(window=20).mean()
# .rolling(window=20) → crea una "ventana deslizante" de 20 días.
# .mean() → calcula el promedio de esos 20 días.
# Juntos calculan el PROMEDIO MÓVIL DE 20 DÍAS:
#   Para cada día, promedia los últimos 20 precios de cierre.
# ¿Para qué sirve? Para suavizar el ruido del precio y ver la tendencia.
# Si el precio actual está POR ENCIMA de MA20 → señal alcista (sube).
# Si está POR DEBAJO → señal bajista (baja).
# Los primeros 19 días son NaN porque no hay 20 días anteriores todavía.

df["MA50"] = df["Close"].rolling(window=50).mean()
# Igual que MA20 pero con 50 días → tendencia más larga.
# MA20 reacciona rápido a cambios. MA50 es más lenta y estable.
# Cuando MA20 cruza por ENCIMA de MA50 → "Golden Cross" (señal de compra).
# Cuando MA20 cruza por DEBAJO de MA50 → "Death Cross" (señal de venta).

df["Volatilidad"] = df["Retorno"].rolling(window=20).std()
# .std() → desviación estándar. Mide qué tan dispersos están los retornos.
# Si los retornos son muy variables (un día +5%, otro -4%) → alta volatilidad.
# Si son estables (siempre entre +0.5% y -0.5%) → baja volatilidad.
# En finanzas, volatilidad = riesgo. Más volatilidad = más riesgo.


# ============================================
# SECCIÓN 4: MOSTRAR ESTADÍSTICAS EN CONSOLA
# ============================================

retorno_total = ((df["Close"].iloc[-1] / df["Close"].iloc[0]) - 1) * 100
# df["Close"].iloc[-1] → .iloc[] accede a filas por posición numérica.
#   iloc[-1] = la ÚLTIMA fila (el día más reciente). Precio actual.
#   iloc[0]  = la PRIMERA fila (el día más antiguo del período). Precio inicial.
# Fórmula del retorno total: (precio_final / precio_inicial - 1) * 100
# Ej: compré a $100, hoy vale $120 → (120/100 - 1) * 100 = 20%

emoji = "📈" if retorno_total >= 0 else "📉"
# Esto es un IF en una sola línea — se llama "operador ternario".
# Sintaxis: valor_si_true IF condicion ELSE valor_si_false
# Si el retorno es positivo o cero → emoji alcista. Si no → bajista.
# En Java sería: String emoji = retornoTotal >= 0 ? "📈" : "📉";

print("=" * 45)
print(f"  RESUMEN: {TICKER} {emoji}")
print("=" * 45)
print(f"  Precio actual:       ${df['Close'].iloc[-1]:.2f}")
# :.2f → formato de número flotante con 2 decimales. Ej: 182.3456 → 182.35
print(f"  Precio inicial:      ${df['Close'].iloc[0]:.2f}")
print(f"  Retorno total:       {retorno_total:.2f}%")
print(f"  Retorno diario prom: {df['Retorno'].mean():.3f}%")
# .mean() → promedio de todos los retornos diarios del período.
# :.3f → 3 decimales. Los retornos diarios son pequeños, necesitamos precisión.
print(f"  Volatilidad prom:    {df['Volatilidad'].mean():.2f}%")
print(f"  Mejor día:           +{df['Retorno'].max():.2f}%")
# .max() → el valor más alto de toda la columna. El mejor día del período.
print(f"  Peor día:            {df['Retorno'].min():.2f}%")
# .min() → el valor más bajo. El peor día.
print("=" * 45)


# ============================================
# SECCIÓN 5: CREAR EL GRÁFICO INTERACTIVO
# ============================================

fig = make_subplots(
    rows=2, cols=1,
    # rows=2 → dos filas de gráficos (arriba y abajo)
    # cols=1 → una sola columna (apilados verticalmente)

    shared_xaxes=True,
    # Comparten el eje X (las fechas). Si hacés zoom en uno,
    # el otro se mueve al mismo tiempo. Muy útil para comparar.

    row_heights=[0.7, 0.3],
    # El gráfico de arriba ocupa 70% del espacio, el de abajo 30%.

    subplot_titles=(f"{TICKER} — Precio y Medias Móviles", "Retorno Diario %")
    # Títulos de cada subgráfico.
)
# fig es el objeto figura — el "lienzo" donde dibujamos todos los gráficos.

fig.add_trace(go.Candlestick(
    # add_trace() → agrega una "capa" de datos al gráfico.
    # go.Candlestick() → gráfico de velas japonesas. Cada vela representa un día:
    #   - Cuerpo verde: el precio subió (close > open)
    #   - Cuerpo rojo: el precio bajó (close < open)
    #   - Mecha superior: hasta dónde llegó el precio más alto (High)
    #   - Mecha inferior: hasta dónde bajó el precio más bajo (Low)
    x=df.index,
    # df.index → el índice del DataFrame son las fechas. Va en el eje X.
    open=df["Open"],
    high=df["High"],
    low=df["Low"],
    close=df["Close"],
    name="Precio"
), row=1, col=1)
# row=1, col=1 → este trace va en el gráfico de arriba.

fig.add_trace(go.Scatter(
    # go.Scatter() → gráfico de línea.
    x=df.index, y=df["MA20"],
    name="MA20", line=dict(color="orange", width=1.5)
    # dict() → crea un diccionario en Python. Acá define el color y grosor de la línea.
), row=1, col=1)
# Agregamos la MA20 encima del gráfico de velas.

fig.add_trace(go.Scatter(
    x=df.index, y=df["MA50"],
    name="MA50", line=dict(color="#4a90e2", width=1.5)
    # "#4a90e2" → color en formato hexadecimal (igual que en CSS).
), row=1, col=1)
# Agregamos la MA50 encima del gráfico de velas.

fig.add_trace(go.Bar(
    # go.Bar() → gráfico de barras. Cada barra = retorno de un día.
    x=df.index,
    y=df["Retorno"],
    name="Retorno %",
    marker_color=df["Retorno"].apply(lambda x: "#00c896" if x >= 0 else "#ff5757")
    # .apply() → aplica una función a cada elemento de la columna.
    # lambda x: → función anónima (sin nombre). Como una arrow function en JS: x => ...
    # Para cada retorno: si es positivo → verde (#00c896), si es negativo → rojo (#ff5757).
), row=2, col=1)
# row=2 → este gráfico va abajo.

fig.update_layout(
    # update_layout() → configura el aspecto general de la figura.
    title=f"Análisis de {TICKER}",
    xaxis_rangeslider_visible=False,
    # Oculta el slider de rango que plotly agrega por defecto a los candlestick.
    template="plotly_dark",
    # Tema oscuro. Otras opciones: "plotly", "plotly_white", "seaborn", "ggplot2".
    height=700
    # Altura total de la figura en píxeles.
)

fig.show()
# Abre el gráfico en el browser predeterminado como archivo HTML interactivo.
# Podés hacer zoom, pasar el mouse, ocultar/mostrar series, etc.

print("\nGráfico generado. ¡Listo!")
