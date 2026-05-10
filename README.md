# 🎓 University Student Analytics Dashboard

**Asignatura:** Data Mining  
**Institución:** Universidad de la Costa (CUC)  
**Profesor:** José Escorcia-Gutierrez, Ph.D.

---

## 📋 Descripción

Dashboard interactivo desarrollado en **Streamlit** para analizar datos estudiantiles universitarios: admisiones, matrícula, retención y satisfacción, segmentados por año, semestre y departamento.

## 👥 Integrantes del equipo

- Martin Torres
- William Angulo

## 📊 Visualizaciones incluidas

| # | Tipo | Descripción |
|---|------|-------------|
| 1 | KPI Cards | Totales de aplicaciones, admitidos, matriculados, satisfacción y retención |
| 2 | Line Chart | Tendencia de tasa de retención por año y semestre |
| 3 | Bar Chart | Satisfacción estudiantil promedio por año |
| 4 | Grouped Bar | Comparación Spring vs Fall (aplicaciones, admitidos, matriculados) |
| 5 | Donut Chart | Distribución de matriculados por departamento |
| 6 | Line Chart | Evolución de matrícula por departamento a lo largo del tiempo |

## 🔎 Filtros interactivos

- **Año académico** (2015–2024)
- **Semestre** (Spring / Fall)
- **Departamento** (Engineering, Business, Arts, Science)

Todos los gráficos e indicadores se actualizan dinámicamente al cambiar los filtros.

## 🚀 Cómo ejecutar localmente

```bash
# 1. Clonar el repositorio
git clone https://github.com/TU_USUARIO/TU_REPOSITORIO.git
cd TU_REPOSITORIO

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Ejecutar la app
streamlit run app.py
```

> Asegúrate de que el archivo `university_student_data.csv` esté en la misma carpeta que `app.py`.

## ☁️ Deploy en Streamlit Cloud

La app está desplegada en:  
🔗 **[https://TU-APP.streamlit.app](https://TU-APP.streamlit.app)**

## 📁 Estructura del repositorio

```
📦 repositorio/
 ┣ 📄 app.py                      # Dashboard Streamlit
 ┣ 📄 requirements.txt            # Dependencias Python
 ┣ 📄 university_student_data.csv # Dataset
 ┗ 📄 README.md                   # Este archivo
```
