import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Cálculo de peso neonatal", layout="wide")

st.title("🍼 Dashboard de Cálculo de Peso Neonatal")

st.markdown("""
Sube un archivo Excel con las columnas:
- **peso nacimiento**
- **peso 1ddv**
- **peso 2ddv**
- **peso 3ddv**

Opcional: columna **ID / nombre paciente**
""")

# ==============================
# 📂 CARGA DE ARCHIVO
# ==============================

uploaded = st.file_uploader("Sube tu archivo Excel", type=["xlsx"])

if uploaded is not None:
    df = pd.read_excel(uploaded)
else:
    example_path = "calculo de peso.xlsx"
    if os.path.exists(example_path):
        df = pd.read_excel(example_path)
        st.info("Usando archivo de ejemplo")
    else:
        st.info("Sube un archivo para comenzar")
        st.stop()

# ==============================
# ✅ VALIDACIÓN DE COLUMNAS
# ==============================

required_cols = ['peso nacimiento', 'peso 1ddv', 'peso 2ddv', 'peso 3ddv']
missing = [c for c in required_cols if c not in df.columns]

if missing:
    st.error(f"Faltan columnas: {missing}")
    st.write("Columnas detectadas:", list(df.columns))
    st.stop()

col_pn = "peso nacimiento"
col_d1 = "peso 1ddv"
col_d2 = "peso 2ddv"
col_d3 = "peso 3ddv"

# ==============================
# 🧮 CÁLCULOS
# ==============================

df["% perdida 1ddv"] = (df[col_pn] - df[col_d1]) / df[col_pn] * 100
df["% perdida 2ddv"] = (df[col_pn] - df[col_d2]) / df[col_pn] * 100
df["% perdida 3ddv"] = (df[col_pn] - df[col_d3]) / df[col_pn] * 100

# Clasificación clínica
def categoria_perdida(x):
    if x < 7:
        return "Normal"
    elif x <= 10:
        return "Alerta"
    else:
        return "Riesgo"

df["Estado 3ddv"] = df["% perdida 3ddv"].apply(categoria_perdida)

# ==============================
# 📊 TABLA PRINCIPAL
# ==============================

def highlight_loss(val):
    try:
        return 'color: red;' if float(val) > 10 else ''
    except:
        return ''

st.subheader("📊 Tabla con cálculos")

styled = df.style.applymap(
    highlight_loss,
    subset=["% perdida 1ddv", "% perdida 2ddv", "% perdida 3ddv"]
)

st.dataframe(styled)

# ==============================
# 📉 PROMEDIO
# ==============================

st.subheader("📉 Evolución del peso promedio")

df_mean = pd.DataFrame({
    "Nacimiento": [df[col_pn].mean()],
    "1ddv": [df[col_d1].mean()],
    "2ddv": [df[col_d2].mean()],
    "3ddv": [df[col_d3].mean()]
})

df_mean = df_mean.melt(var_name="Día", value_name="Peso")

fig = px.line(df_mean, x="Día", y="Peso", markers=True)
st.plotly_chart(fig, use_container_width=True)

# ==============================
# 📈 EVOLUCIÓN INDIVIDUAL
# ==============================

id_candidates = [c for c in df.columns if c.lower() in ['id','paciente','nombre','rut']]

if id_candidates:
    id_col = id_candidates[0]

    st.subheader("📈 Evolución por paciente")

    df_long = df.melt(
        id_vars=id_col,
        value_vars=[col_pn, col_d1, col_d2, col_d3],
        var_name="Día",
        value_name="Peso"
    )

    fig2 = px.line(df_long, x="Día", y="Peso", color=id_col, markers=True)
    st.plotly_chart(fig2, use_container_width=True)

# ==============================
# 🧾 SELECCIÓN E IMPRESIÓN
# ==============================

st.subheader("🧾 Seleccionar pacientes para impresión")

if id_candidates:
    seleccion = st.multiselect(
        "Selecciona pacientes",
        options=df[id_col].unique(),
        default=df[id_col].unique()
    )
    df_filtrado = df[df[id_col].isin(seleccion)]
else:
    st.info("No hay identificador, se imprimirá todo")
    df_filtrado = df.copy()

st.subheader("📋 Vista previa")
st.dataframe(df_filtrado)

# Estilo para impresión
def highlight_row(row):
    try:
        if row["% perdida 3ddv"] > 10:
            return ['background-color: #ffcccc'] * len(row)
    except:
        pass
    return [''] * len(row)

styled_print = df_filtrado.style.apply(highlight_row, axis=1)

# HTML imprimible
html = f"""
<html>
<head>
<meta charset="UTF-8">
<style>
body {{ font-family: Arial; }}
h2 {{ text-align: center; }}
table {{ border-collapse: collapse; width: 100%; }}
th, td {{ border: 1px solid #ccc; padding: 6px; text-align: center; }}
th {{ background-color: #f2f2f2; }}
</style>
</head>
<body>
<h2>Informe de Peso Neonatal</h2>
{styled_print.to_html(index=False)}
</body>
</html>
"""

st.download_button(
    "🖨️ Descargar para imprimir",
    data=html,
    file_name="informe_peso_neonatal.html",
    mime="text/html"
)

# ==============================
# 📥 DESCARGA CSV
# ==============================

st.subheader("📥 Descargar datos")

csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    "Descargar CSV",
    data=csv,
    file_name="resultado_peso.csv",
    mime="text/csv"
)
