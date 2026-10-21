"""Genera el informe del taller en PDF: reports/informe/Informe_Taller_Olist.pdf.

Antes de ejecutarlo, corra los notebooks en orden (00 → B → D) para que existan las figuras
en reports/figures/, y el diagrama con scripts/diagrama_relacional.py.

Uso:
    uv run python scripts/generar_informe.py

Las cifras del texto provienen de las salidas de los notebooks. Si se vuelven a ejecutar con
otros parámetros, revise que el texto siga coincidiendo.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (Image, KeepTogether, ListFlowable, ListItem, PageBreak,
                                Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle)

from olist.config import FIG_DIR, PROJECT_ROOT

# ---------------------------------------------------------------------------------
# Datos de portada (completar)
# ---------------------------------------------------------------------------------
INTEGRANTES = "[Nombres de los integrantes]"
FECHA = "Octubre de 2026"

SALIDA = PROJECT_ROOT / "reports" / "informe" / "Informe_Taller_Olist.pdf"
DIAGRAMA = PROJECT_ROOT / "reports" / "informe" / "modelo_relacional.png"

# ---------------------------------------------------------------------------------
# Estilos
# ---------------------------------------------------------------------------------
_FUENTES = Path(matplotlib.get_data_path()) / "fonts" / "ttf"
pdfmetrics.registerFont(TTFont("Texto", _FUENTES / "DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("Texto-Negrita", _FUENTES / "DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Texto-Cursiva", _FUENTES / "DejaVuSans-Oblique.ttf"))
pdfmetrics.registerFont(TTFont("Codigo", _FUENTES / "DejaVuSansMono.ttf"))
pdfmetrics.registerFontFamily("Texto", normal="Texto", bold="Texto-Negrita",
                              italic="Texto-Cursiva", boldItalic="Texto-Negrita")

AZUL = colors.HexColor("#1F4E79")
AZUL_CLARO = colors.HexColor("#E8F0F8")
GRIS = colors.HexColor("#555555")
ANCHO = letter[0] - 4 * cm

E = {
    "titulo": ParagraphStyle("titulo", fontName="Texto-Negrita", fontSize=18, leading=23,
                             textColor=AZUL, alignment=TA_CENTER, spaceAfter=4),
    "subtitulo": ParagraphStyle("subtitulo", fontName="Texto", fontSize=10, leading=14,
                                textColor=GRIS, alignment=TA_CENTER, spaceAfter=2),
    "h1": ParagraphStyle("h1", fontName="Texto-Negrita", fontSize=13.5, leading=17, textColor=AZUL,
                         spaceBefore=12, spaceAfter=5, keepWithNext=1),
    "h2": ParagraphStyle("h2", fontName="Texto-Negrita", fontSize=10.5, leading=14, spaceBefore=8,
                         spaceAfter=3, keepWithNext=1),
    "p": ParagraphStyle("p", fontName="Texto", fontSize=9.2, leading=13, alignment=TA_JUSTIFY,
                        spaceAfter=5),
    "item": ParagraphStyle("item", fontName="Texto", fontSize=9.2, leading=12.6, alignment=TA_JUSTIFY),
    "item_izq": ParagraphStyle("item_izq", fontName="Texto", fontSize=9.2, leading=12.6),
    "pie": ParagraphStyle("pie", fontName="Texto-Cursiva", fontSize=8, leading=10.5, textColor=GRIS,
                          alignment=TA_CENTER, spaceBefore=2, spaceAfter=8),
    "celda": ParagraphStyle("celda", fontName="Texto", fontSize=8, leading=10),
    "celda_n": ParagraphStyle("celda_n", fontName="Texto-Negrita", fontSize=8, leading=10,
                              textColor=colors.white),
}

_contador = {"figura": 0, "tabla": 0}


def c(texto: str) -> str:
    """Nombre de variable, tabla o archivo en fuente monoespaciada."""
    return f'<font name="Codigo" size="8.3">{texto}</font>'


def p(texto: str) -> Paragraph:
    return Paragraph(texto, E["p"])


def h1(texto: str) -> Paragraph:
    return Paragraph(texto, E["h1"])


def h2(texto: str) -> Paragraph:
    return Paragraph(texto, E["h2"])


def vinetas(textos: list[str]) -> ListFlowable:
    return ListFlowable([ListItem(Paragraph(t, E["item"]), leftIndent=10) for t in textos],
                        bulletType="bullet", start="•", leftIndent=12, bulletFontName="Texto",
                        spaceAfter=5)


def figura(ruta: Path, pie: str, ancho_cm: float = 16.5) -> KeepTogether:
    _contador["figura"] += 1
    ancho_px, alto_px = ImageReader(str(ruta)).getSize()
    ancho = min(ancho_cm * cm, ANCHO)
    imagen = Image(str(ruta), width=ancho, height=ancho * alto_px / ancho_px)
    return KeepTogether([imagen, Paragraph(f"<b>Figura {_contador['figura']}.</b> {pie}", E["pie"])])


def tabla(filas: list[list[str]], anchos_cm: list[float], pie: str, dividir: bool = False):
    _contador["tabla"] += 1
    datos = [[Paragraph(str(x), E["celda_n"]) for x in filas[0]]]
    datos += [[Paragraph(str(x), E["celda"]) for x in fila] for fila in filas[1:]]
    t = Table(datos, colWidths=[a * cm for a in anchos_cm], repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), AZUL),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, AZUL_CLARO]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 2.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
        ("LINEBELOW", (0, -1), (-1, -1), 0.5, colors.HexColor("#BBBBBB")),
    ]))
    titulo = Paragraph(f"<b>Tabla {_contador['tabla']}.</b> {pie}", E["pie"])
    titulo.keepWithNext = True
    if dividir:  # tablas largas: pueden continuar en la página siguiente
        return [titulo, t, Spacer(1, 8)]
    return KeepTogether([titulo, t, Spacer(1, 8)])


def pie_pagina(canvas, doc) -> None:
    canvas.saveState()
    canvas.setFont("Texto", 7.5)
    canvas.setFillColor(GRIS)
    canvas.drawString(2 * cm, 1.2 * cm, "Taller Olist · Aprendizaje Automático 2026-2")
    canvas.drawRightString(letter[0] - 2 * cm, 1.2 * cm, f"Página {doc.page}")
    canvas.restoreState()


F0 = FIG_DIR / "00_datos"
FB = FIG_DIR / "B_series"
FD = FIG_DIR / "D_integracion"

# ---------------------------------------------------------------------------------
# Contenido
# ---------------------------------------------------------------------------------
h: list = []

h += [
    Paragraph("Olist: demanda diaria, interpretabilidad e integración", E["titulo"]),
    Paragraph("Taller de Aprendizaje Automático · MCDA 2026-2 · Profesor Andrés Vásquez Restrepo", E["subtitulo"]),
    Paragraph(f"{INTEGRANTES} · {FECHA}", E["subtitulo"]),
    Spacer(1, 6),
]

# ------------------------------------------------------------------ 1
h += [
    h1("1. Resumen ejecutivo"),
    p("<b>Alcance.</b> El enunciado plantea un módulo común de datos y cuatro módulos de modelado. Este equipo "
      "desarrolló el <b>Módulo 0</b> (datos, calidad y EDA), el <b>Módulo B</b> (series de tiempo) y el "
      "<b>Módulo D</b> (interpretabilidad e integración). El Módulo D se adaptó: en lugar de explicar el "
      "clasificador del Módulo A, explica el modelo de pronóstico del Módulo B y lo integra con los datos del "
      "Módulo 0. Por eso este informe responde a la pregunta de <b>planeación</b>: ¿cuántas órdenes recibirá "
      "Olist cada día durante las próximas 4 semanas?"),
    p("<b>Respuesta.</b> En el período de prueba (27-jun a 21-ago-2018) Olist recibió en promedio 230 órdenes "
      "diarias, con un ciclo semanal marcado: los lunes son el día más alto y el sábado el más bajo. Los mejores "
      "pronósticos a 28 días se equivocaron en promedio en <b>37–39 órdenes por día</b> (sMAPE ≈ 18 %): el "
      "LightGBM recursivo (MAE 37,5) y el ingenuo estacional (MAE 38,9). Este último fue el modelo elegido en "
      "validación antes de ver la prueba, y quedó a 1,5 órdenes del mejor. Ningún modelo anticipó la caída de la "
      "demanda del 6 al 15 de julio de 2018 ni el repunte de agosto."),
]
h.append(tabla([
    ["Indicador", "Resultado"],
    ["Serie modelada", "594 días (2017-01-05 a 2018-08-21), 98.390 órdenes; media 2017: 125/día, 2018: 229/día"],
    ["Mejor MAE en prueba (2 ventanas de 28 días)", "37,5 órdenes/día (LightGBM recursivo); 38,9 el ingenuo estacional"],
    ["Cobertura de los intervalos del 90 %", "SARIMA 87,5 % (ancho medio 211); LightGBM conformal 94,6–100 %"],
    ["Qué mueve el pronóstico (SHAP)", "Nivel de las últimas 4 semanas y día de la semana; los rezagos diarios pesan 1 %"],
    ["Plan de despachos por estado (4 semanas)", "Error total +5,7 %; SP +12,6 %; estados pequeños hasta −35 %"],
], [6.3, 10.7], "Cifras clave."))
h += [
    p("<b>Recomendación.</b> Usar el ingenuo estacional o SARIMA como pronóstico base y re-pronosticar cada "
      "semana. Reservar la capacidad logística hasta el techo del intervalo del 90 %, porque los cambios bruscos "
      "de nivel no se anticipan. Repartir la capacidad por estado con los despachos por orden de las últimas 12 "
      "semanas, usando rangos para los estados pequeños."),
    PageBreak(),
]

# ------------------------------------------------------------------ 2
h += [
    h1("2. Datos, modelo relacional y calidad (Módulo 0)"),
    p(f"Toda la lectura se hace con SQL sobre {c('olist.duckdb')}, abierto en modo solo lectura. Las consultas "
      f"están en archivos {c('.sql')} dentro de {c('sql/')}, reciben las fechas de corte como parámetros "
      f"{c('?')} y se leen desde los notebooks. Pandas se usa solo a partir del resultado de cada consulta."),
    h2("2.1 Modelo relacional y granularidad"),
    figura(DIAGRAMA, "Modelo relacional. Filas por tabla, llaves y cardinalidades medidas con SQL.", 17.6),
    p(f"Las llaves {c('order_id')}, {c('customer_id')}, {c('product_id')} y {c('seller_id')} son únicas. "
      f"En {c('order_reviews')} ni {c('review_id')} (98.410 distintos en 99.224 filas) ni {c('order_id')} "
      f"(98.673) son únicos por separado, pero sí el par. {c('geolocation')} tiene 1.000.163 filas para solo "
      f"19.015 prefijos postales. Las tablas hijas de {c('orders')} multiplican filas al unirse: 9.803 órdenes "
      "tienen varios ítems (hasta 21), 2.961 varios pagos (hasta 29) y 547 varias reseñas (hasta 3). Por eso "
      "cada tabla hija se agrega a una fila por orden <b>antes</b> de unirla, y la geolocalización se resume a "
      "una coordenada por prefijo."),
    h2("2.2 Calidad de datos y decisiones"),
]
h.extend(tabla([
    ["Problema", "Casos", "Decisión"],
    ["Órdenes sin ítems", "775 (0,78 %)", "Se conservan en la serie de demanda; se excluyen de análisis de montos o productos."],
    ["Pagos ≠ precio + flete (> 0,01)", "380 de 98.665 (0,39 %)", "No se corrigen; los montos se toman de una sola tabla según la pregunta."],
    ["Fechas imposibles", "165 entregas al transportador antes de la compra; 23 al cliente antes que al transportador",
     "Se excluyen de los tiempos por etapa; no afectan la serie, que usa la fecha de compra."],
    ["Entregadas sin fecha de entrega", "8", "Se excluyen de los tiempos de entrega."],
    ["Productos sin categoría", "610 (1,85 %)", "Grupo «sin categoría» si se usa la categoría."],
    ["Categorías sin traducción", "2 categorías, 13 productos", "Se conserva el nombre en portugués."],
    ["Prefijos sin geolocalización", "157 de clientes, 7 de vendedores", "Se marcan como faltantes; no se imputan."],
    ["Reseñas sin comentario", "58,7 % sin mensaje", "Esperable (campo opcional); no afecta a B ni D."],
], [4.0, 4.6, 8.4], "Problemas de calidad detectados y decisión tomada. Ningún registro se borra de la base.",
    dividir=True))
h += [
    h2("2.3 Identidad del cliente"),
    p(f"{c('customer_id')} identifica al cliente <i>de una orden</i> (es 1:1 con {c('orders')}), mientras que "
      f"{c('customer_unique_id')} identifica a la <i>persona</i>: 99.441 registros corresponden a 96.096 "
      "personas. El 96,9 % de las personas compró una sola vez y solo 2.997 repitieron. Para medir recompra "
      "hay que agrupar por la persona. Para el Módulo B, esto implica que la demanda diaria depende de la llegada "
      "de clientes nuevos y no de la recompra."),
    h2("2.4 Período útil"),
    p("El período útil es <b>[2017-01-05, 2018-08-22)</b>. En 2016 hubo apenas 329 órdenes en cuatro meses, y "
      "del 1 al 4 de enero de 2017 no hubo ninguna. Al final, desde el 22 de agosto de 2018 las órdenes caen día "
      "a día (185 el 22, 96 el 24, 11 el 29) y desde el 30 solo quedan canceladas o en tránsito. Es la firma de "
      "un corte de extracción, no de una caída de la demanda. El período conserva 594 días y 98.390 órdenes "
      "(98,9 % del total), sin días en cero."),
    figura(F0 / "ordenes_diarias.png", "Órdenes diarias por fecha de compra (todos los estados) y período útil.", 15.5),
    h2("2.5 EDA orientado a los módulos"),
    vinetas([
        "<b>Tendencia.</b> La media semanal pasa de 415 órdenes (1.er trimestre de 2017) a 1.647 (1.er trimestre "
        "de 2018) y luego se aplana (1.533 y 1.493). La semana de Black Friday 2017 tuvo 3.008 órdenes.",
        "<b>Entregas.</b> La mediana de compra a entrega es de 10 días (p90: 23). Frente a la fecha estimada, la "
        "mediana llega 12 días antes; solo el 6,77 % llega tarde. Olist promete fechas holgadas.",
        "<b>Geografía.</b> São Paulo concentra el 41,9 % de los clientes y el 59,7 % de los vendedores; SP, PR y "
        "MG reúnen el 78,9 % de los vendedores. La serie nacional está dominada por SP.",
        "<b>Demanda incluida.</b> La serie cuenta <b>todas</b> las órdenes por fecha de compra, sin filtrar por "
        "estado: mide lo que Olist recibe; la cancelación es un desenlace posterior.",
    ]),
    figura(F0 / "geografia_estados.png", "Diez estados con más clientes únicos y con más vendedores.", 14.0),
]

# ------------------------------------------------------------------ 3
h += [
    h1("3. Módulo B: pronóstico de la demanda diaria"),
    h2("3.1 Formulación y validación"),
    p(f"La serie es el número de órdenes por día, construida en SQL ({c('sql/B_series/serie_diaria.sql')}) "
      "con un calendario que incluye los días sin órdenes. La <b>prueba</b> son las últimas 8 semanas del período "
      "útil (27-jun a 21-ago-2018) y se usa una sola vez. Antes de ella se definen 8 pliegues "
      "<b>walk-forward</b> de 28 días sin solaparse, con orígenes cada 28 días desde el 14-nov-2017: los 6 "
      "primeros sirven para elegir modelos e hiperparámetros, y los 2 últimos para calibrar los intervalos."),
    h2("3.2 Análisis de la serie"),
    p("Antes de la prueba, la media diaria por día de la semana va de 181 (lunes) y 179 (martes) a 134 (domingo) "
      "y 122 (sábado). La ACF es 0,77 en el rezago 1 y 0,64 en el 7. ADF rechaza la raíz unitaria (p = 0,017), "
      "pero KPSS rechaza la estacionariedad en nivel (p ≤ 0,01). Este resultado mixto, junto con la tendencia, "
      "justifica diferenciar en SARIMA y evaluar fuera de muestra. Los eventos atípicos se conservan: Black "
      "Friday (24-nov-2017, 1.176 órdenes frente a 173 diarias en las dos semanas previas) se modela con las "
      "variables de calendario conocidas de antemano. El paro de camioneros (21-may a 1-jun-2018: 142 órdenes "
      "diarias frente a 268 antes) se marca para interpretar errores, pero no se usa como variable porque no se "
      "conocía al emitir el pronóstico."),
    figura(FB / "stl.png", "Descomposición STL del tramo previo a la prueba: tendencia, componente semanal y residuo.", 13.5),
    h2("3.3 Modelos"),
    vinetas([
        "<b>Baselines:</b> ingenuo (último valor) e ingenuo estacional (mismo día de la semana anterior).",
        "<b>SARIMA(2,1,2)(0,1,1)[7]:</b> elegido por AIC entre 15 combinaciones ajustadas con el entrenamiento del "
        "primer pliegue, y confirmado por MAE en validación (57,9 frente a 58,1 del orden inicial).",
        "<b>LightGBM</b> con rezagos (1, 2, 3, 7, 14, 21 y 28 días), medias y desviaciones móviles (7, 14 y 28 "
        "días) calculadas solo con el pasado, y calendario (día de la semana, día del mes, mes, festivos de Brasil "
        "y distancia a Black Friday). Se compararon dos estrategias multi-paso: <b>recursiva</b> (cada "
        "predicción se usa como rezago de la siguiente) y <b>directa</b> (un modelo con el horizonte como "
        "variable, sin realimentar predicciones). De tres configuraciones de hiperparámetros, ganó en ambas la "
        "más compacta (250 árboles, 7 hojas).",
    ]),
]
h.append(tabla([
    ["Modelo", "MAE medio ± desv.", "RMSE medio", "sMAPE medio"],
    ["Ingenuo estacional", "<b>52,2 ± 35,7</b>", "76,6", "21,8 %"],
    ["SARIMA(2,1,2)(0,1,1)[7]", "57,9 ± 43,6", "81,6", "24,0 %"],
    ["Ingenuo", "60,7 ± 34,0", "86,1", "25,2 %"],
    ["LightGBM directo", "63,3 ± 53,8", "92,0", "27,0 %"],
    ["LightGBM recursivo", "74,3 ± 44,1", "100,4", "30,8 %"],
], [5.4, 4.0, 3.6, 4.0], "Validación walk-forward: media y desviación entre los 6 pliegues de selección (horizonte de 28 días)."))
h += [
    p("En validación ningún modelo superó en promedio al ingenuo estacional, que fue el elegido. La variabilidad "
      "entre pliegues es alta porque el primero contiene Black Friday: es el pico en el horizonte 10 de la "
      "Figura 5, donde todos los modelos fallan."),
    figura(FB / "mae_por_horizonte.png", "MAE por horizonte en validación. El pico en h = 10 es Black Friday 2017.", 14.0),
    h2("3.4 Evaluación en prueba"),
    p("La prueba se evalúa con el horizonte del problema: <b>dos ventanas de 28 días</b>. La segunda se emite con "
      "los datos reales observados hasta su origen y con los mismos hiperparámetros, sin volver a seleccionar "
      "nada."),
]
h.append(tabla([
    ["Modelo", "MAE", "RMSE", "sMAPE", "MAE ventana 1", "MAE ventana 2", "Cobertura 90 %", "Ancho medio"],
    ["LightGBM recursivo", "<b>37,5</b>", "48,7", "17,9 %", "49,5", "25,4", "100 %", "233"],
    ["Ingenuo estacional", "38,9", "48,9", "18,0 %", "44,4", "33,5", "—", "—"],
    ["SARIMA", "47,4", "60,2", "21,7 %", "51,6", "43,2", "87,5 %", "211"],
    ["LightGBM directo", "50,6", "61,6", "22,9 %", "43,7", "57,4", "94,6 %", "214"],
    ["Ingenuo", "54,9", "67,1", "25,0 %", "64,6", "45,1", "—", "—"],
], [3.6, 1.4, 1.4, 1.6, 2.1, 2.1, 2.3, 2.0],
    "Prueba (56 días en 2 ventanas de 28). Intervalos: SARIMA, del modelo; LightGBM, conformales calibrados en los pliegues reservados."))
h.append(tabla([
    ["Modelo", "Días 1–7", "Días 8–14", "Días 15–21", "Días 22–28"],
    ["Ingenuo estacional", "26,3 (32,5)", "62,5 (85,6)", "29,8 (53,1)", "37,1 (37,4)"],
    ["SARIMA", "31,3 (40,0)", "82,8 (93,8)", "53,5 (61,4)", "22,2 (36,2)"],
    ["LightGBM recursivo", "26,5 (47,6)", "48,6 (109,3)", "40,7 (87,0)", "34,1 (53,2)"],
    ["LightGBM directo", "27,3 (27,7)", "81,6 (106,1)", "46,4 (60,2)", "47,0 (59,1)"],
], [5.0, 3.0, 3.0, 3.0, 3.0], "MAE por semana de horizonte en prueba (entre paréntesis, en validación)."))
h += [
    p("El modelo elegido en validación quedó a solo 1,5 órdenes del mejor en prueba, así que la selección fue "
      "robusta. El cambio de ranking del LightGBM recursivo (último en validación, primero en prueba) indica que "
      "las diferencias entre modelos son pequeñas frente a la variabilidad de la demanda. El error <b>no crece "
      "de forma monótona</b> con el horizonte: en la primera semana todos rondan 26–31 órdenes, pero la semana 2 "
      "es la peor en ambos periodos porque los eventos (Black Friday en validación y la caída de julio en prueba) "
      "pesan más que la distancia al origen. La caída del 6 al 15 de julio de 2018 (91–168 órdenes diarias) "
      "coincide con el periodo entre la eliminación de Brasil del Mundial y la final; es una hipótesis que los "
      "datos no permiten confirmar."),
    figura(FB / "prueba_final.png", "Prueba: valores reales, el modelo elegido en validación, SARIMA y su intervalo del 90 %.", 16.0),
    p("<b>Incertidumbre.</b> El intervalo de SARIMA cubrió el 87,5 % de los días, cerca del 90 % nominal. El "
      "conformal del LightGBM directo cubrió el 94,6 % y el del recursivo el 100 %, más conservador. Los anchos "
      "(211–233 órdenes) equivalen casi a la demanda media diaria: sirven como techo de capacidad, no como "
      "pronóstico puntual preciso."),
]

# ------------------------------------------------------------------ 4
h += [
    h1("4. Módulo D: interpretabilidad e integración"),
    p("Se interpreta el <b>LightGBM directo</b>: el mejor LightGBM en validación, entrenado solo con datos "
      "hasta el 26-jun-2018. Para tener variedad de situaciones, el modelo fijo se aplica desde cada origen "
      "diario de la prueba con horizontes de 1 a 28 días. Son 1.190 pronósticos, cada uno con los datos "
      "disponibles en su origen (MAE 60,2: incluye los orígenes emitidos en plena caída de julio)."),
    h2("4.1 Importancia global y dependencia"),
    figura(FD / "shap_beeswarm.png", "SHAP sobre los 1.190 pronósticos de prueba. Valor base: 169 órdenes.", 13.0),
    p("El valor base (169) es el pronóstico medio sobre el entrenamiento, que incluye el 2017 de baja demanda. "
      f"{c('media_28')} suma entre +31 y +42 órdenes en todas las filas: corrige el nivel. {c('dia_semana')} "
      f"reproduce el ciclo semanal. {c('dias_a_black_friday')} resta entre −14 y −20 en todo julio y agosto. "
      "Agrupando por familias, el calendario aporta el 53 % del SHAP, las medias y desviaciones móviles el 46 % y "
      "los rezagos diarios apenas el 1 %, sin cambios entre la semana 1 y la 4 del horizonte. El modelo pronostica "
      "«nivel reciente × perfil semanal» y no usa el dato de ayer. Por eso su error casi no crece con el horizonte "
      "(57,7 en la semana 1 frente a 64,1 en la 4), pero tampoco reacciona rápido a cambios bruscos."),
    figura(FD / "shap_dependencia_top3.png", "Dependencia SHAP de las tres variables más relevantes.", 16.5),
    vinetas([
        f"<b>{c('media_28')}:</b> el efecto es positivo en todo el rango (180–270), pero no crece con la media y "
        "baja por encima de 240. Probablemente el modelo aprendió de diciembre de 2017, cuando una media inflada "
        "por Black Friday iba seguida de una caída.",
        f"<b>{c('dia_semana')}:</b> el efecto es escalonado y estable: lunes +25, martes +21, miércoles +17, "
        "jueves +6, viernes −9, sábado −33 y domingo −27. Es el patrón del Módulo 0.",
        f"<b>{c('dias_a_black_friday')}:</b> entre 94 y 150 días antes de Black Friday el efecto es siempre "
        "negativo y sin tendencia. En el entrenamiento esas distancias solo aparecen en julio y agosto de 2017, "
        "cuando la demanda era menor. Es una <b>relación espuria</b>: una estacionalidad anual aprendida de un "
        "solo año.",
    ]),
    h2("4.2 Explicaciones locales"),
    p("<b>Pronóstico acertado:</b> el emitido el 9-jul para el lunes 16-jul (horizonte 7) dio 245 órdenes, igual "
      "al valor real: base 169, nivel +40, efecto lunes +27 y penalización por Black Friday −18. <b>Mayor error</b> "
      "(el análogo del falso negativo): el emitido el 13-jul para el martes 7-ago (horizonte 25) dio 233 órdenes "
      "frente a 370 reales, el día más alto de la prueba. Se emitió en plena caída de julio, con "
      f"{c('media_28')} en 182, y el modelo arrastró ese nivel bajo 25 días hacia adelante. En operación ese "
      "error equivale a quedarse corto de capacidad en un pico, el error más costoso."),
    figura(FD / "shap_local_mayor_error.png", "Explicación local del pronóstico con mayor error (real 370, pronóstico 233).", 14.5),
]
h.append(KeepTogether([h2("4.3 Contraste con la importancia por permutación"), tabla([
    ["Variable", "SHAP medio |valor|", "Rango SHAP", "Aumento del MAE al permutar", "Rango permutación"],
    ["media_28", "37,5", "1", "0,00", "10"],
    ["dia_semana", "19,9", "2", "7,01", "1"],
    ["dias_a_black_friday", "17,2", "3", "0,01", "9"],
    ["dia_mes", "5,5", "4", "−0,51", "22"],
    ["desv_28", "5,3", "5", "0,24", "3"],
    ["media_14", "2,8", "8", "0,31", "2"],
], [4.2, 3.2, 2.3, 4.4, 2.9], "SHAP frente a permutación en las mismas 1.190 filas (correlación de Spearman entre rankings: 0,26).")]))
h += [
    p(f"Los dos métodos coinciden poco, y la razón es instructiva. {c('dia_semana')} es importante en ambos: es la "
      f"variable que explica la variación entre días. {c('media_28')} y {c('dias_a_black_friday')} encabezan SHAP "
      "pero tienen permutación casi nula, porque en la prueba su efecto es casi constante (+35 y −18): desordenarlas "
      "no cambia el error. SHAP mide cuánto mueve cada variable el pronóstico frente a la base del entrenamiento "
      "(aquí, sobre todo, una corrección de nivel); la permutación mide qué explica el error dentro del período. "
      "Que «la demanda depende del nivel reciente y del día de la semana» está respaldado por ambos métodos; el peso "
      f"de {c('dias_a_black_friday')} es un artefacto del poco historial."),
    h2("4.4 Integración: plan de despachos por estado de origen"),
    p("Se conecta el pronóstico de B con los datos del Módulo 0. (1) El modelo pronostica las órdenes de los 28 "
      "días posteriores al 26-jun-2018. (2) En SQL se mide cuántos despachos genera cada estado de origen de los "
      "vendedores por cada orden nacional en las 12 semanas previas; un despacho es un par (orden, vendedor), así "
      "que no se multiplican filas por ítem. En total son 1,017 despachos por orden, y SP genera 0,739. (3) El "
      "plan es el producto de ambos. (4) Se valida contra los despachos reales de esas semanas."),
]
h.append(tabla([
    ["Estado", "Plan 4 semanas", "Real", "Error del plan", "Error si B acertara"],
    ["SP", "4.184", "3.716", "+12,6 %", "+6,8 %"],
    ["PR", "400", "441", "−9,4 %", "−14,0 %"],
    ["MG", "399", "395", "+1,0 %", "−4,2 %"],
    ["RJ", "289", "267", "+8,1 %", "+2,6 %"],
    ["SC", "174", "209", "−17,0 %", "−21,2 %"],
    ["RS", "110", "169", "−35,2 %", "−38,5 %"],
    ["Total (todos los estados)", "5.753", "5.442", "+5,7 %", "+0,3 %"],
], [4.6, 2.8, 2.4, 3.3, 3.9], "Plan de despachos frente a lo real. «Si B acertara» usa las órdenes reales para aislar el error de participación."))
h += [
    p("Por semanas, el pronóstico de órdenes fue casi plano (1.371–1.441) frente a 1.328, 1.067, 1.185 y 1.790 "
      "reales: errores de +3 %, +35 %, +22 % y −22 % que se compensan en el total (+5 %). La suma de los techos "
      "diarios del 90 % (2.119–2.189 por semana) nunca fue superada. A nivel nacional, el error del plan viene del "
      "pronóstico de órdenes: si B hubiera acertado, el error total sería del 0,3 %. Por estado el panorama cambia: "
      "SP queda sobreplanificado y los estados pequeños quedan cortos (SC −17 %, RS −35 %), porque su participación "
      "varió y con 27–44 despachos semanales cualquier cambio pesa mucho."),
    figura(FD / "plan_vs_real_estados.png", "Despachos en 4 semanas por estado de origen: plan frente a real (escala logarítmica).", 14.0),
    h2("4.5 Caso de uso"),
    vinetas([
        "Cada lunes, con datos hasta el domingo, se emite el pronóstico de 28 días y su techo del 90 %.",
        "Con SQL se calculan los despachos por orden de cada estado en las últimas 12 semanas y se publica el plan "
        "semanal: en esta prueba, unos 1.000–1.070 despachos desde SP, unos 100 desde PR y MG y unos 70 desde RJ.",
        "Las transportadoras reservan capacidad base según el plan y capacidad contingente hasta el techo del 90 %.",
        "Si una semana se desvía más de un 20 % (como las semanas 2 y 4 de la prueba), se re-pronostica sin esperar "
        "al lunes siguiente.",
    ]),
]

# ------------------------------------------------------------------ 5
h += [
    h1("5. Limitaciones, conclusiones y trabajo futuro"),
    h2("Limitaciones"),
    vinetas([
        "<b>Deriva temporal.</b> Los modelos se apoyan en el nivel reciente y no anticipan caídas ni repuntes; el "
        "peor error fue un pico no previsto (370 reales frente a 233).",
        "<b>Poco historial.</b> Con un año y medio de datos, la estacionalidad anual se aprende de un solo año "
        f"({c('dias_a_black_friday')} es espuria).",
        "<b>Cobertura del dataset.</b> El período útil termina el 21-ago-2018 por el corte de extracción. Los "
        "despachos se cuentan por fecha de compra y no por fecha real de envío, y las 775 órdenes sin ítems no "
        "generan despacho.",
        "<b>Sesgo geográfico.</b> SP concentra el 73 % de los despachos. El plan es fiable a nivel nacional y para "
        "SP, pero no para los estados pequeños.",
        "<b>Interpretación.</b> SHAP explica el modelo, no causas. El modelo interpretado (el LightGBM directo) "
        "se eligió antes de la prueba y no es el mejor en ella; la integración no depende del modelo.",
    ]),
    h2("Conclusiones"),
    p("La demanda diaria de Olist se explica sobre todo por su nivel reciente y el ciclo semanal. Un modelo tan "
      "simple como el ingenuo estacional es difícil de superar con 18 meses de historia, y la validación "
      "walk-forward lo eligió correctamente. El valor del aprendizaje automático aquí no está en reducir mucho el "
      "error puntual, sino en <b>cuantificar la incertidumbre</b> (intervalos con la cobertura verificada), "
      "<b>entender qué mueve el pronóstico</b> (SHAP y permutación, que además detectan una variable espuria) y "
      "<b>convertirlo en decisiones</b>: un plan de capacidad por estado validado contra lo que ocurrió."),
    h2("Trabajo futuro"),
    vinetas([
        "Combinar modelos (ingenuo estacional, SARIMA y LightGBM) y reentrenar cada semana.",
        "Agregar variables de eventos conocidos de antemano (campañas, festivos regionales, partidos).",
        f"Limitar {c('dias_a_black_friday')} a las semanas cercanas al evento hasta tener más años de historia.",
        "Pronosticar por separado SP y los estados pequeños, con intervalos propios para cada uno.",
    ]),
]

# ------------------------------------------------------------------ Anexo
h += [
    h1("Anexo. Reproducibilidad"),
    p(f"El repositorio fija las versiones con {c('pyproject.toml')}, {c('uv.lock')} y {c('requirements.txt')}, "
      f"usa rutas relativas y la semilla {c('RANDOM_STATE = 42')}. Para reproducir los resultados:"),
    ListFlowable([ListItem(Paragraph(x, E["item_izq"]), leftIndent=10) for x in [
        f"Instalar el entorno: {c('uv sync')}",
        f"Construir la base con el script del curso: "
        f"{c('uv run python scripts/build_olist_duckdb.py --out data/olist.duckdb')}",
        f"Ejecutar en orden {c('notebooks/00_datos.ipynb')}, {c('B_series.ipynb')} y "
        f"{c('D_integracion.ipynb')} (B guarda el modelo que usa D).",
        f"Opcional: {c('uv run python scripts/diagrama_relacional.py')} y "
        f"{c('uv run python scripts/generar_informe.py')}",
    ]], bulletType="1", leftIndent=14, bulletFontName="Texto", bulletFontSize=9, spaceAfter=5),
    p(f"Las consultas principales están en {c('sql/00_datos/')}, {c('sql/B_series/')} y {c('sql/D_integracion/')}."),
]


def main() -> None:
    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    faltantes = [str(r) for r in [DIAGRAMA, F0 / "ordenes_diarias.png", FB / "prueba_final.png",
                                  FD / "shap_beeswarm.png"] if not r.exists()]
    if faltantes:
        raise SystemExit("Faltan figuras; ejecute primero los notebooks y el diagrama:\n" + "\n".join(faltantes))
    doc = SimpleDocTemplate(str(SALIDA), pagesize=letter, leftMargin=2 * cm, rightMargin=2 * cm,
                            topMargin=1.7 * cm, bottomMargin=1.8 * cm,
                            title="Olist: demanda diaria, interpretabilidad e integración",
                            author=INTEGRANTES, subject="Taller de Aprendizaje Automático 2026-2")
    doc.build(h, onFirstPage=pie_pagina, onLaterPages=pie_pagina)
    print("Informe generado:", SALIDA.relative_to(PROJECT_ROOT))


if __name__ == "__main__":
    main()
