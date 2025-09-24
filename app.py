import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Cálculo de peso neonatal", layout="wide")

st.title("🍼 Dashboard de Cálculo de Peso Neonatal")

st.markdown("Sube un archivo Excel con las columnas: **sala**, **peso 1ddv**, **peso 2ddv**, **peso 3ddv**. Si tu archivo tiene una columna identificadora (ID o Nombre), la app graficará por paciente.")

# Cargar archivo: preferencia a upload; si no, intenta cargar el ejemplo incluido
uploaded = st.file_uploader("Sube tu archivo Excel (o usa el ejemplo incluido)", type=["xlsx"])
if uploaded is not None:
    df = pd.read_excel(uploaded)
else:
    example_path = "calculo de peso.xlsx"
    if os.path.exists(example_path):
        df = pd.read_excel(example_path)
        st.info("Usando el archivo de ejemplo incluido en la app.")
    else:
        st.info("Sube un archivo Excel para comenzar.")
        st.stop()

# Asegurar que las columnas importantes existan
required_cols = ['peso nacimiento', 'peso 1ddv', 'peso 2ddv', 'peso 3ddv']
missing = [c for c in required_cols if c not in df.columns]
if missing:
    st.error(f"No se encontraron las columnas esperadas en el Excel: {missing}. Revisa los nombres de columna y prueba subir el archivo de nuevo.")
    st.write("Columnas detectadas en tu archivo:", list(df.columns))
    st.stop()

# Normalizar columnas (el código asume nombres exactos detectados)
col_pn = "peso nacimiento"
col_d1 = "peso 1ddv"
col_d2 = "peso 2ddv"
col_d3 = "peso 3ddv"

# Calcular % pérdida (si no existen o para sobreescribir)
df["% perdida 1ddv"] = (df[col_pn] - df[col_d1]) / df[col_pn] * 100
df["% perdida 2ddv"] = (df[col_pn] - df[col_d2]) / df[col_pn] * 100
df["% perdida 3ddv"] = (df[col_pn] - df[col_d3]) / df[col_pn] * 100

# Mostrar tabla con formato: resaltar >10%
def highlight_loss(val):
    try:
        v = float(val)
    except:
        return ''
    color = 'color: red;' if v > 10 else ''
    return color

st.subheader("📊 Tabla con cálculos")
styled = df.style.applymap(highlight_loss, subset=["% perdida 1ddv", "% perdida 2ddv", "% perdida 3ddv"])
st.dataframe(styled)

# Gráfico de evolución promedio
st.subheader("📉 Evolución del peso promedio (por día)")
df_mean = pd.DataFrame({
    "Nacimiento": [df[col_pn].mean()],
    "1ddv": [df[col_d1].mean()],
    "2ddv": [df[col_d2].mean()],
    "3ddv": [df[col_d3].mean()]
})
df_mean = df_mean.melt(var_name="Día", value_name="Peso promedio")
fig = px.line(df_mean, x="Día", y="Peso promedio", markers=True, title="Evolución del peso promedio")
st.plotly_chart(fig, use_container_width=True)

# Evolución por paciente (si existe columna ID o similar)
id_candidates = [c for c in df.columns if c.lower() in ['id','paciente','nombre','rut','id paciente','identificador']]
if id_candidates:
    id_col = id_candidates[0]
    st.subheader("📈 Evolución individual de peso")
    df_long = df.melt(id_vars=id_col, value_vars=[col_pn, col_d1, col_d2, col_d3],
                      var_name="Día", value_name="Peso")
    fig2 = px.line(df_long, x="Día", y="Peso", color=id_col, markers=True, title="Evolución de peso por paciente")
    st.plotly_chart(fig2, use_container_width=True)

# Descarga de resultados
st.subheader("📥 Descargar resultados")
csv = df.to_csv(index=False).encode("utf-8")
st.download_button("Descargar CSV con % perdida", data=csv, file_name="resultado_peso.csv", mime="text/csv")
