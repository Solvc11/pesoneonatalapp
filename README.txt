
App para cálculo de pérdida de peso neonatal (generada automáticamente)

Archivos incluidoss:
- app.py               : código principal (Streamlit)
- requirements.txt     : dependencias
- calculo de peso.xlsx : archivo de ejemplo (tu archivo subido)

Cómo probar localmente:
1) Instala dependencias: pip install -r requirements.txt
2) Ejecuta: streamlit run app.py
3) Abre el navegador en la URL que Streamlit muestre (por defecto http://localhost:8501)

Cómo desplegar en Streamlit Cloud:
1) Crea un repositorio en GitHub y sube los archivos (app.py, requirements.txt, calculo de peso.xlsx)
2) Ve a https://streamlit.io/cloud, inicia sesión con GitHub y crea una "New app"
3) Selecciona el repo, branch y archivo app.py y haz Deploy.

Notas:
- La app intentará usar el archivo subido; si no subes nada, carga el ejemplo incluido.
- Si los nombres de columna de tu Excel son distintos, la app intenta detectarlos; si no los encuentra, te avisará y mostrará las columnas detectadas.
- Si quieres personalizaciones (umbral distinto a 10%, gráficos adicionales, export a Excel en vez de CSV), pídemelo y lo modifico.
