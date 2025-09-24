import streamlit as st
import pandas as pd
import plotly.express as px

st.title("📊 Cálculo de peso neonatal")

# Inicializar dataset en la sesión
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=[
        "Sala", "Peso nacimiento", "Peso 1ddv", "Peso 2ddv", "Peso 3ddv",
        "% pérdida 1ddv", "% pérdida 2ddv", "% pérdida 3ddv"
    ])

st.header("➕ Ingresar datos del recién nacido")

with st.form("form_rn"):
    sala = st.text_input("Sala / ID")
    peso_nac = st.number_input("Peso nacimiento (g)", min_value=0, step=1, format="%d")

    peso_1 = st.number_input("Peso 1ddv (g)", min_value=0, step=1)
    peso_2 = st.number_input("Peso 2ddv (g)", min_value=0, step=1)
    peso_3 = st.number_input("Peso 3ddv (g)", min_value=0, step=1)
    submit = st.form_submit_button("Calcular y guardar")

if submit:
    if peso_nac > 0:
        perdida_1 = ((peso_nac - peso_1) / peso_nac) * 100 if peso_1 > 0 else None
        perdida_2 = ((peso_nac - peso_2) / peso_nac) * 100 if peso_2 > 0 else None
        perdida_3 = ((peso_nac - peso_3) / peso_nac) * 100 if peso_3 > 0 else None

        # Agregar fila
        new_row = {
            "Sala": sala,
            "Peso nacimiento": peso_nac,
            "Peso 1ddv": peso_1,
            "Peso 2ddv": peso_2,
            "Peso 3ddv": peso_3,
            "% pérdida 1ddv": perdida_1,
            "% pérdida 2ddv": perdida_2,
            "% pérdida 3ddv": perdida_3,
        }
        st.session_state.data = pd.concat(
            [st.session_state.data, pd.DataFrame([new_row])],
            ignore_index=True
        )
        st.success("Datos guardados ✅")

# Mostrar tabla
if not st.session_state.data.empty:
    st.subheader("📋 Tabla de registros")
    st.dataframe(st.session_state.data.style.applymap(
        lambda x: "color: red" if isinstance(x, float) and x > 10 else None
    ))

    # Gráfico de evolución promedio
    pesos_cols = ["Peso nacimiento", "Peso 1ddv", "Peso 2ddv", "Peso 3ddv"]
    df_mean = st.session_state.data[pesos_cols].mean().reset_index()
    df_mean.columns = ["Día", "Peso promedio"]

    fig = px.line(df_mean, x="Día", y="Peso promedio", markers=True, title="Evolución promedio de peso")
    st.plotly_chart(fig)

    # Descargar CSV
    csv = st.session_state.data.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Descargar registros en CSV", csv, "peso_neonatal.csv", "text/csv")
