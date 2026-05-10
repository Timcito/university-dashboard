import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ── Configuración de página ────────────────────────────────────────────────────
st.set_page_config(
    page_title="University Student Dashboard",
    page_icon="🎓",
    layout="wide",
)

# ── Carga de datos ─────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("university_student_data.csv")
    df.columns = df.columns.str.strip()
    return df

df = load_data()

DEPT_COLS = {
    "Engineering": "Engineering Enrolled",
    "Business":    "Business Enrolled",
    "Arts":        "Arts Enrolled",
    "Science":     "Science Enrolled",
}

# ── Sidebar / Filtros ──────────────────────────────────────────────────────────
st.sidebar.title("🔎 Filtros")

years = sorted(df["Year"].unique())
sel_years = st.sidebar.multiselect("Año académico", years, default=years)

terms = df["Term"].unique().tolist()
sel_terms = st.sidebar.multiselect("Semestre", terms, default=terms)

departments = list(DEPT_COLS.keys())
sel_depts = st.sidebar.multiselect("Departamento", departments, default=departments)

st.sidebar.markdown("---")
st.sidebar.markdown("**Equipo:**")
st.sidebar.markdown("Martin Torres\n- William Angulo")

# ── Filtrado ───────────────────────────────────────────────────────────────────
filtered = df[df["Year"].isin(sel_years) & df["Term"].isin(sel_terms)].copy()

# ── Título ─────────────────────────────────────────────────────────────────────
st.title("🎓 University Student Analytics Dashboard")
st.markdown("Análisis de admisiones, matrícula, retención y satisfacción estudiantil.")

# ══════════════════════════════════════════════════════════════════════════════
# SECCIÓN 1 — KPI Cards
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("---")
st.subheader("📊 Indicadores Clave (KPIs)")

if filtered.empty:
    st.warning("No hay datos para los filtros seleccionados.")
else:
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📋 Total Aplicaciones",   f"{int(filtered['Applications'].sum()):,}")
    col2.metric("✅ Total Admitidos",       f"{int(filtered['Admitted'].sum()):,}")
    col3.metric("🎓 Total Matriculados",    f"{int(filtered['Enrolled'].sum()):,}")
    col4.metric("⭐ Satisfacción Promedio", f"{filtered['Student Satisfaction (%)'].mean():.1f}%")

    col5, col6 = st.columns(2)
    col5.metric("📈 Retención Promedio",    f"{filtered['Retention Rate (%)'].mean():.1f}%")
    admit_rate = filtered['Admitted'].sum() / filtered['Applications'].sum() * 100
    col6.metric("🔢 Tasa de Admisión",      f"{admit_rate:.1f}%")

# ══════════════════════════════════════════════════════════════════════════════
# SECCIÓN 2 — Tendencia de retención a lo largo del tiempo (Line Chart)
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("---")
st.subheader("📈 Tendencia de Tasa de Retención por Año")

if not filtered.empty:
    ret_trend = (
        filtered.groupby(["Year", "Term"])["Retention Rate (%)"]
        .mean()
        .reset_index()
    )
    fig1, ax1 = plt.subplots(figsize=(10, 4))
    for term, grp in ret_trend.groupby("Term"):
        ax1.plot(grp["Year"], grp["Retention Rate (%)"], marker="o", label=term, linewidth=2)
    ax1.set_xlabel("Año")
    ax1.set_ylabel("Tasa de Retención (%)")
    ax1.set_title("Retención a lo largo del tiempo por Semestre")
    ax1.legend()
    ax1.grid(True, linestyle="--", alpha=0.5)
    st.pyplot(fig1)
    plt.close(fig1)

# ══════════════════════════════════════════════════════════════════════════════
# SECCIÓN 3 — Satisfacción estudiantil por año (Bar Chart)
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("---")
st.subheader("😊 Satisfacción Estudiantil por Año")

if not filtered.empty:
    sat_year = (
        filtered.groupby("Year")["Student Satisfaction (%)"]
        .mean()
        .reset_index()
    )
    fig2, ax2 = plt.subplots(figsize=(10, 4))
    bars = ax2.bar(
        sat_year["Year"],
        sat_year["Student Satisfaction (%)"],
        color=sns.color_palette("Blues_d", len(sat_year)),
        edgecolor="white",
    )
    ax2.bar_label(bars, fmt="%.1f%%", padding=3, fontsize=9)
    ax2.set_xlabel("Año")
    ax2.set_ylabel("Satisfacción (%)")
    ax2.set_title("Promedio de Satisfacción Estudiantil por Año")
    ax2.set_ylim(70, 100)
    ax2.grid(axis="y", linestyle="--", alpha=0.5)
    st.pyplot(fig2)
    plt.close(fig2)

# ══════════════════════════════════════════════════════════════════════════════
# SECCIÓN 4 — Comparación Spring vs Fall (Grouped Bar Chart)
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("---")
st.subheader("🔄 Comparación Spring vs Fall")

if not filtered.empty:
    compare = (
        filtered.groupby("Term")[["Applications", "Admitted", "Enrolled"]]
        .sum()
        .reset_index()
    )
    fig3, ax3 = plt.subplots(figsize=(8, 4))
    x = range(len(compare["Term"]))
    width = 0.25
    ax3.bar([i - width for i in x], compare["Applications"], width, label="Aplicaciones", color="#4C72B0")
    ax3.bar([i          for i in x], compare["Admitted"],    width, label="Admitidos",    color="#55A868")
    ax3.bar([i + width for i in x], compare["Enrolled"],     width, label="Matriculados", color="#C44E52")
    ax3.set_xticks(list(x))
    ax3.set_xticklabels(compare["Term"])
    ax3.set_ylabel("Cantidad de Estudiantes")
    ax3.set_title("Aplicaciones, Admitidos y Matriculados: Spring vs Fall")
    ax3.legend()
    ax3.grid(axis="y", linestyle="--", alpha=0.5)
    st.pyplot(fig3)
    plt.close(fig3)

# ══════════════════════════════════════════════════════════════════════════════
# SECCIÓN 5 — Distribución por Departamento (Pie / Donut)
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("---")
st.subheader("🏫 Distribución de Matriculados por Departamento")

if not filtered.empty and sel_depts:
    dept_totals = {d: filtered[DEPT_COLS[d]].sum() for d in sel_depts if d in DEPT_COLS}
    fig4, ax4 = plt.subplots(figsize=(6, 6))
    wedges, texts, autotexts = ax4.pie(
        dept_totals.values(),
        labels=dept_totals.keys(),
        autopct="%1.1f%%",
        pctdistance=0.75,
        startangle=140,
        wedgeprops=dict(width=0.5),
        colors=sns.color_palette("Set2", len(dept_totals)),
    )
    ax4.set_title("Proporción de Matriculados por Departamento")
    st.pyplot(fig4)
    plt.close(fig4)
else:
    st.info("Selecciona al menos un departamento para ver este gráfico.")

# ══════════════════════════════════════════════════════════════════════════════
# SECCIÓN 6 — Matrícula por Departamento a lo largo del tiempo (Line Chart)
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("---")
st.subheader("📉 Evolución de Matrícula por Departamento")

if not filtered.empty and sel_depts:
    dept_time = filtered.groupby("Year")[[DEPT_COLS[d] for d in sel_depts]].sum().reset_index()
    fig5, ax5 = plt.subplots(figsize=(10, 4))
    for dept in sel_depts:
        ax5.plot(dept_time["Year"], dept_time[DEPT_COLS[dept]], marker="o", label=dept, linewidth=2)
    ax5.set_xlabel("Año")
    ax5.set_ylabel("Estudiantes Matriculados")
    ax5.set_title("Evolución de Matrícula por Departamento")
    ax5.legend()
    ax5.grid(True, linestyle="--", alpha=0.5)
    st.pyplot(fig5)
    plt.close(fig5)

st.markdown("---")
st.caption("Dashboard desarrollado para la asignatura Data Mining — Universidad de la Costa (CUC)")
