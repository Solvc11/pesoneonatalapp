# ==============================
# 🧾 IMPRESIÓN SIMPLE (SIN ROMPER APP)
# ==============================

st.subheader("🖨️ Imprimir tabla")

# Detectar columna ID si existe
id_candidates = [c for c in df.columns if c.lower() in ['id','paciente','nombre','rut','id paciente']]

if id_candidates:
    id_col = id_candidates[0]

    seleccion = st.multiselect(
        "Selecciona pacientes para imprimir",
        options=df[id_col].unique(),
        default=df[id_col].unique()
    )

    df_print = df[df[id_col].isin(seleccion)]
else:
    df_print = df.copy()

# Generar HTML simple (sin estilos raros)
html = df_print.to_html(index=False)

st.download_button(
    "Descargar tabla para imprimir",
    data=html,
    file_name="tabla_peso.html",
    mime="text/html"
)
