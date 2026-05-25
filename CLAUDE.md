# CLAUDE.md — Guía del proyecto Trading Predictor

> Este archivo lo lee Claude Code automáticamente al abrir el proyecto.
> Sirve para que, cada vez que Juan encienda Claude, sepa **qué es el proyecto, cómo ayudar y por dónde se quedó**.

---

## 🎯 Cómo debe ayudar Claude aquí (MODO INSTRUCTOR — leer siempre)

Juan está **aprendiendo**. El objetivo NO es que el proyecto se termine rápido, sino que él
entienda cada pieza. Por eso, en este repo:

- ❌ **NO escribas el código por él** salvo que lo pida explícitamente ("escríbeme esto").
- ✅ **Explica conceptos** antes de cada paso: qué es, por qué se usa, qué alternativas hay.
- ✅ **Da pistas y pseudocódigo**, no la solución completa. Deja que él escriba el código.
- ✅ Cuando él te enseñe código, **revísalo**: di qué está bien, qué falla y por qué.
- ✅ Propón **un solo paso a la vez**. Pregunta antes de avanzar al siguiente.
- ✅ Usa analogías sencillas. Juan no asume conocimiento previo profundo de ML.
- ✅ Responde en **español**.
- ✅ Si algo es una mala práctica (p. ej. data leakage, lookahead bias), **avísalo siempre**,
  aunque él no lo pregunte. En trading esto es crítico.

Al final de cada sesión: **actualiza la sección "Estado actual / Dónde lo dejamos"** de este archivo.

---

## 📌 Qué estamos construyendo

Un **predictor de señales de trading** para criptomonedas usando **TensorFlow**.

- **Salida:** una señal **al día** que diga si el precio va a **subir o bajar** en la próxima hora
  (o el horizonte que definamos). Es un problema de **clasificación binaria** (sube / baja).
- **Activos objetivo:** Bitcoin (BTC), **Ethereum (ETH)** y **Litecoin (LTC)**.
  - 📝 Cambio de plan (2026-05-25): se descartaron SOL y SHIB en favor de ETH y LTC.
    Motivo: ambas tienen mucha más historia y profundidad de mercado en Coinbase, lo que da
    series más limpias y modelos más comparables entre sí (SHIB es una memecoin con dinámica
    de precio muy ruidosa que complicaba el aprendizaje).
- **Marco temporal:** velas de 1 hora; se genera **1 señal diaria**.

### Aviso importante (decir a Juan cuando toque)
Predecir mercados es **muy difícil**; ningún modelo es una bola de cristal. El valor real de
este proyecto es **aprender ML aplicado a series temporales**. Nunca tratar las señales como
consejo financiero ni operar dinero real basándose solo en esto.

---

## 🗺️ Hoja de ruta (fases). Marca con [x] lo completado.

### Fase 0 — Entorno
- [ ] Activar el venv y `pip install -r requirements.txt`
- [ ] Arreglar typo en `requirements.txt`: `matplolib` → `matplotlib`
- [ ] Decidir si `selenium` se queda (¿se va a hacer scraping?) o se quita y se usan APIs
- [ ] Crear estructura de carpetas (ver abajo) y un `.gitignore` (ignorar `venv/`, `.env`, datos)

### Fase 1 — Datos ✅ COMPLETA
- [x] Elegir fuente de datos de precios → **Coinbase** API pública
- [x] Descargar histórico de velas de 1h para BTC, ETH, LTC (OHLCV: open, high, low, close, volume)
- [x] Guardar los datos (CSV en `data/`)
- [x] Explorar los datos — sin NaN, sin precios raros, solo 2 huecos sistémicos de 5h cada uno
      (2025-10-25 16:00→20:00 y 2026-05-08 02:00→06:00) en las 3 monedas (caídas de Coinbase).
      Decidido: NO se interpolan, son irrelevantes (10h / 17.690 = 0,056%).

### Fase 2 — Features e indicadores (CASI COMPLETA)
- [x] Crear features con la librería `ta` (SMA, EMA, RSI, MACD + macd_signal + macd_diff)
- [x] Definir la **etiqueta (target)**: `1` si `close(t+24h) > close(t)`, `0` en caso contrario
- [x] ⚠️ Lookahead bias: features no miran al futuro; target sí (es lo que se predice)
- [ ] Normalizar/escalar features (scikit-learn `StandardScaler` / `MinMaxScaler`)
      ⚠️ Hacerlo DESPUÉS del split temporal: `fit` solo sobre train, luego `transform` en val/test.
      Si se escala antes del split → lookahead bias.

### Fase 3 — Preparar para el modelo
- [ ] Crear ventanas temporales (secuencias) para alimentar la red
- [ ] **Split temporal** train/validation/test (NO aleatorio — es serie temporal)
- [ ] Revisar balance de clases (¿hay tantos "sube" como "baja"?)

### Fase 4 — Modelo (TensorFlow / Keras)
- [ ] Empezar simple: un modelo denso o una **LSTM** pequeña
- [ ] Compilar (loss = `binary_crossentropy`, métrica = accuracy y otras)
- [ ] Entrenar y mirar las curvas de train vs validation (¿overfitting?)
- [ ] Evaluar en test: accuracy, precision, recall, matriz de confusión

### Fase 5 — Señal diaria, actualización de datos y entrega por UI web
- [ ] Refactor de `download_history(pair)` para aceptar `days=N` y **mergear** con el CSV existente
      sin duplicar filas (función `update_recent(pair, days=7)`). Idea de Juan (2026-05-25): que
      cada **domingo** se descarguen los últimos 7 días de velas y se actualicen los CSVs.
- [ ] Función que toma datos recientes y devuelve la señal (sube/baja + confianza)
- [ ] Programar con `APScheduler`: **semanal** (descarga de datos nuevos, domingos) +
      **diaria** (cálculo de la señal). Vive dentro del contenedor Docker en Fase 7.
- [ ] Guardar la última señal (archivo JSON o base de datos)
- [ ] Decidir framework web: **Flask** (mínimo, fácil) vs **FastAPI** (moderno). Añadir a requirements.
- [ ] Montar una **UI web simple** que lea y muestre la última señal en un puerto del servidor
- [ ] (Opcional) Backtest sencillo: ¿la señal habría acertado en el pasado?

### Fase 6 — Mejora
- [ ] Probar más features, otras arquitecturas, ajustar hiperparámetros
- [ ] Comparar contra una **baseline tonta** (p. ej. "siempre sube") para saber si el modelo aporta

### Fase 7 — Despliegue en Docker (servidor de casa de Juan)
> Objetivo de Juan: que el proyecto corra en un **servidor que tiene en casa**, dentro de **Docker**.
> ⚠️ Esto es lo ÚLTIMO. Primero el modelo tiene que funcionar en local; luego se "empaqueta".
- [ ] Escribir un `Dockerfile` (imagen base `python:3.11-slim`, instalar requirements, copiar `src/`)
- [ ] (Opcional) `docker-compose.yml` si hay varios servicios (p. ej. base de datos)
- [ ] Configurar el scheduler (APScheduler) para que la señal diaria se genere dentro del contenedor
- [ ] Persistir datos y modelos con un **volumen** de Docker (que no se pierdan al reiniciar)
- [ ] Pasar secretos/config con variables de entorno (`.env`), no hardcodear
- [ ] Probar la build en local y luego desplegar en el servidor de casa

---

## 📁 Estructura de carpetas propuesta (crear cuando toque la Fase 0)

```
trading-predictor/
├── data/            # datos descargados (ignorar en git)
├── src/
│   ├── data.py      # descarga y carga de datos
│   ├── features.py  # indicadores y etiquetas
│   ├── model.py     # definición y entrenamiento del modelo
│   └── predict.py   # genera la señal diaria
├── notebooks/       # exploración (opcional)
├── models/          # modelos entrenados guardados (.keras)
├── requirements.txt
└── CLAUDE.md
```

---

## 🛠️ Decisiones técnicas tomadas
- **Lenguaje:** Python 3.11.14 (venv en `./venv`)
- **Framework ML:** TensorFlow 2.15.0 / Keras
- **Tipo de problema:** clasificación binaria (sube/baja)
- **Fuente de datos:** **Coinbase** API pública (`api.exchange.coinbase.com`, velas vía `requests`,
  sin API key). ⚠️ Binance se descartó: bloquea a usuarios de EE.UU. (Juan está en Washington State).
  Endpoint: `/products/{PAR}/candles?granularity=3600` (3600s = 1h). Pares: BTC-USD, ETH-USD, LTC-USD.
  ⚠️ Formato de cada vela en Coinbase: `[time, low, high, open, close, volume]` (¡OJO, NO es orden OHLC!).
  Devuelve máx. 300 velas por petición, orden descendente; para histórico largo hay que paginar con `start`/`end`.
- **Horizonte de predicción:** ¿sube o baja en las **próximas 24h**? (1 señal al día)
- **Arquitectura de modelos:** **un modelo por cripto** (BTC, SOL, SHIB por separado)
- **Selenium:** ❌ eliminado de `requirements.txt` (no se hace scraping; los precios vienen de API)
- **Entrega de la señal:** **UI web simple** servida en un puerto del servidor de casa
  (pequeña app web; framework por decidir: Flask o FastAPI). El contenedor expondrá ese puerto.
- **Despliegue:** Docker en el servidor de casa de Juan (Fase 7, al final)
- **Ritmo del proyecto:** largo plazo, **poco a poco**. Sin prisa; prioridad = que Juan entienda.

## ❓ Decisiones pendientes (preguntar a Juan)
- **Histórico a descargar: 2 años** de velas de 1h (~17.500 velas, ~59 peticiones paginadas). ✅ decidido
- **Horizonte de predicción: 24h** (confirmado 2026-05-25). ✅ decidido
- **Umbral de "sube": cualquier subida > 0%** (confirmado 2026-05-25). Etiqueta binaria:
  `1` si `close(t+24h) > close(t)`, `0` en caso contrario. ✅ decidido
- ¿A qué hora exacta del día se emite la señal diaria? (relevante para Fase 5, no para Fase 2)

---

## 📍 Estado actual / Dónde lo dejamos
**Última sesión:** 2026-05-25

- ✅ Typo `matplolib`→`matplotlib` corregido en `requirements.txt`.
- ✅ Dependencias instaladas en el venv (`pip install -r requirements.txt` OK).
- 🆕 Nuevo objetivo de Juan: **desplegar en Docker** en su servidor de casa (ver Fase 7).
- ✅ Decisiones de diseño tomadas: Binance API, horizonte 24h, un modelo por cripto, selenium fuera.
- ✅ `requirements.txt` limpiado (selenium y webdriver-manager eliminados).
- ✅ Estructura de carpetas creada (`src/`, `data/`, `models/`, `notebooks/`).
- ✅ Decidido: la señal se entregará por **UI web en un puerto del servidor** (framework por elegir).
- ✅ `.gitignore` creado y funcionando. **Fase 0 COMPLETA.**
- ✅ Fuente de datos confirmada: **Coinbase** (Binance bloquea EE.UU.). Probado BTC/ETH/LTC OK.
- ✅ `data.py` (en la raíz, de momento) hace una petición a Coinbase y devuelve las velas en crudo.
  Juan ya entiende: import, requests.get, .json(), print, slicing `[:2]` y la importancia de que
  los nombres de variable coincidan exacto.
- ✅ `data.py` ya: crea DataFrame con columnas nombradas, convierte `time` (unix s) a fecha con
  `pd.to_datetime(unit="s")` y ordena ascendente con `sort_values + reset_index(drop=True)`.
  Juan aprendió: dict `{}` vs `()`, booleanos `True`/`False` con mayúscula, argumentos con nombre `unit=`.
- ✅ Guarda el DataFrame en `data/BTC-USD_1h.csv` con `df.to_csv(index=False)`. Confirmado en disco.
- ✅ **PAGINACIÓN HECHA Y FUNCIONANDO.** Juan escribió la función `get_candles(start, end)` y un bucle
  `while` que retrocede 300 horas por iteración hasta cubrir 2 años. Descargadas **17.690 velas de
  BTC-USD** (2024-05-17 → 2026-05-25), ordenadas ascendentemente y guardadas en `data/BTC-USD_1h.csv`.
- 📚 Errores que pasó Juan en el proceso y le sirvieron para aprender:
  - Orden de declaración: hay que definir `def` antes de llamarlo.
  - `pd.concat` con lista vacía si lo pones antes del `while` (todavía no se ha llenado).
  - Colisión de nombres entre `from datetime import time` y `import time` (el módulo `time.sleep`).
  - `sort_values` es **método del DataFrame** (`df.sort_values`), no función suelta.
  - El clásico `df = df.sort_values(..., inplace=True)` que asigna `None` a `df` (no mezclar nunca
    `inplace=True` con reasignación).
- ✅ **DRY aplicado.** `get_candles(pair, start, end)` y `download_history(pair)` parametrizadas;
  bucle `for par in pares:` recorre la lista. Conceptos que entendió Juan: parámetros de función,
  f-strings dentro de URLs y nombres de archivo, bucle `for` sobre listas, indentación de funciones,
  separación de responsabilidades (`get_candles` baja UNA ventana, `download_history` orquesta todo).
- ✅ **Tres CSVs descargados** (~17.690 filas cada uno, 2024-05-18 → 2026-05-25, ascendente):
  `data/BTC-USD_1h.csv`, `data/ETH-USD_1h.csv`, `data/LTC-USD_1h.csv`.
- 🔄 **Cambio de plan (2026-05-25):** las cripto pasan de SOL/SHIB → ETH/LTC. CLAUDE.md actualizado
  arriba para reflejarlo.
- ✅ **`data.py` movido a `src/data.py`** (estructura final del proyecto).
- ✅ **`src/explore.py` creado** con función `explore(pair)` que ejecuta `read_csv` (con
  `parse_dates=["time"]`), `df.info()`, `df.describe()`, `df["time"].diff().value_counts()` y
  detección de huecos con filtrado booleano `df[diferencias > pd.Timedelta(hours=1)]`. Bucle
  `for par in pares:` lo aplica a BTC, ETH y LTC. Conceptos nuevos: `pd.read_csv` con
  `parse_dates`, dtypes (`object` vs `datetime64[ns]`), filtrado booleano, indentación = scope.
- 🔎 **Hallazgo importante:** los 2 huecos están en las mismas fechas/horas en las 3 monedas
  (2025-10-25 21:00 y 2026-05-08 07:00). Conclusión: caídas sistémicas de Coinbase, NO bug del
  pipeline. Se dejan los datos tal cual.
- **FASE 1 OFICIALMENTE CERRADA.**
- ✅ **`src/features.py` creado** con función `build_features(pair)`. Crea target (`label` con
  `shift(-24)`), 6 features (`sma_24`, `rsi_14`, `ema_24`, `macd`, `macd_signal`, `macd_diff`),
  hace `dropna()` para limpiar NaN de calentamiento (~34) Y de cierre (24), y guarda en
  `data/{pair}_features.csv`. Bucle `for` aplica a BTC, ETH, LTC. 17.633 filas por moneda.
- ✅ **Balance de label sano** en las 3 monedas: BTC 51,3/48,7, ETH 50,5/49,5, LTC 50,8/49,2.
  No hace falta tratamiento especial de clases.
- 📚 Conceptos nuevos que aprendió Juan en Fase 2: `shift(-N)` para mirar futuro vs `shift(+N)`
  pasado, lookahead bias en target vs features, `astype(int)` para bool→0/1, NaN al final del
  dataset por shift y al principio por calentamiento de indicadores, `rolling(N).mean()`,
  patrón "instanciar clase + llamar método" de `ta`, `dropna()` con y sin `subset`, importancia
  de guardar el dataset enriquecido para no recalcular en cada entrenamiento.
- **Siguiente paso:** Fase 3 — preparar para el modelo. **Split temporal** (NO aleatorio:
  train = más antiguo, test = más reciente), luego normalización con `StandardScaler` ajustado
  solo en train. Después de eso, crear ventanas temporales si vamos a usar LSTM.

> 👉 Claude: cuando Juan vuelva, lee esta sección, salúdalo, recuérdale en qué punto está
> y propón **el siguiente paso pequeño** (no varios a la vez).
