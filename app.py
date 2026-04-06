import streamlit as st
import pandas as pd

st.set_page_config(page_title="Control Peso Neonatal", layout="wide")

st.title("Control de Peso Neonatal")

# Inicializar datos en sesión
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=[
        "Sala", "Peso Nacimiento", "Peso Día 1", "Peso Día 2",
        "% Pérdida Día 1", "% Pérdida Día 2"
    ])

# Función para calcular pérdidas
def calcular_perdidas(df):
    df["% Pérdida Día 1"] = ((df["Peso Nacimiento"] - df["Peso Día 1"]) / df["Peso Nacimiento"]) * 100
    df["% Pérdida Día 2"] = ((df["Peso Nacimiento"] - df["Peso Día 2"]) / df["Peso Nacimiento"]) * 100
    return df

# Formulario de ingreso
with st.form("formulario"):
    sala = st.text_input("Sala")
    pn = st.number_input("Peso Nacimiento (g)", min_value=0.0)
    p1 = st.number_input("Peso Día 1 (g)", min_value=0.0)
    p2 = st.number_input("Peso Día 2 (g)", min_value=0.0)

    submit = st.form_submit_button("Agregar")

    if submit:
        nueva_fila = pd.DataFrame([[sala, pn, p1, p2, 0, 0]], columns=st.session_state.data.columns)
        st.session_state.data = pd.concat([st.session_state.data, nueva_fila], ignore_index=True)
        st.session_state.data = calcular_perdidas(st.session_state.data)

# Estilo condicional

def highlight(row):
    color = [''] * len(row)
    if row["% Pérdida Día 1"] > 5:
        color = ['background-color: red'] * len(row)
    if row["% Pérdida Día 2"] > 10:
        color = ['background-color: red'] * len(row)
    return color

# Mostrar tabla
if not st.session_state.data.empty:
    st.subheader("Datos registrados")
    styled_df = st.session_state.data.style.apply(highlight, axis=1)
    st.dataframe(styled_df, use_container_width=True)

# Selección para imprimir
st.subheader("Seleccionar datos para imprimir")

if not st.session_state.data.empty:
    seleccion = st.multiselect("Selecciona filas", st.session_state.data.index)

    if seleccion:
        df_print = st.session_state.data.loc[seleccion]
        st.write(df_print)

        csv = df_print.to_csv(index=False).encode('utf-8')
        st.download_button("Descargar selección", csv, "datos_neonatales.csv", "text/csv")

# Botón limpiar
if st.button("Limpiar datos"):
    st.session_state.data = pd.DataFrame(columns=st.session_state.data.columns)
