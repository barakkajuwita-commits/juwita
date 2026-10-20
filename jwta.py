import os
import pandas as pd
import plotly.express as px
import streamlit as st

# LOAD DATA
st.set_page_config(page_title="Dashboard Fiskal Daerah", layout="wide")


@st.cache_data
def load_data():
  # Membuat path file relatif agar aman dibaca di GitHub / Streamlit Cloud
  current_dir = os.path.dirname(os.path.abspath(__file__))
  file_path = os.path.join(current_dir, "dataset_fiskal_97_hipoFull.csv")
  df = pd.read_csv(file_path)
  return df


df = load_data()


# SIDEBAR
st.sidebar.title("Filter Dashboard")

kota_list = sorted(df["Kota"].unique())

kota = st.sidebar.selectbox("Pilih Kota", kota_list)

tahun = st.sidebar.multiselect(
    "Pilih Tahun", sorted(df["Tahun"].unique()), default=sorted(df["Tahun"].unique())
)

df_filter = df[(df["Kota"] == kota) & (df["Tahun"].isin(tahun))]

# ==================================
# HEADER
# ==================================
st.title("📊 Dashboard Fiskal Daerah")
st.write(f"Analisis untuk: **{kota}**")

# ==================================
# KPI
# ==================================
data_terbaru = df_filter.sort_values("Tahun").iloc[-1]

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("PAD", round(data_terbaru["PAD"], 2))

col2.metric("IPM", round(data_terbaru["IPM"], 2))

col3.metric("Kemiskinan", round(data_terbaru["KEMISKINAN"], 2))

col4.metric("Pengangguran", round(data_terbaru["PENGANGGURAN"], 2))

col5.metric("Pertumbuhan Ekonomi", round(data_terbaru["PE"], 2))

# ==================================
# TREND INDIKATOR
# ==================================
st.subheader("Tren Indikator")

indikator = st.selectbox(
    "Pilih Variabel", ["PAD", "ICT", "IPM", "KEMISKINAN", "PENGANGGURAN", "PE"]
)

fig = px.line(
    df_filter, x="Tahun", y=indikator, markers=True, title=f"Tren {indikator}"
)

st.plotly_chart(fig, use_container_width=True)

# ==================================
# PERBANDINGAN KOTA
# ==================================
st.subheader("Perbandingan Antar Kota")

tahun_pilih = st.selectbox("Tahun Perbandingan", sorted(df["Tahun"].unique()))

indikator2 = st.selectbox(
    "Indikator Perbandingan", ["PAD", "IPM", "KEMISKINAN", "PENGANGGURAN", "PE"]
)

df_compare = df[df["Tahun"] == tahun_pilih]

fig2 = px.bar(
    df_compare.sort_values(indikator2, ascending=False),
    x="Kota",
    y=indikator2,
    color=indikator2,
    title=f"{indikator2} Tahun {tahun_pilih}",
)

st.plotly_chart(fig2, use_container_width=True)

# ==================================
# KORELASI
# ==================================
st.subheader("Korelasi Variabel")

numeric_cols = [
    "PAD",
    "ICT",
    "IPM",
    "KEMISKINAN",
    "PENGANGGURAN",
    "PE",
    "DAK_Fisik",
    "DAK_Nonfisik",
    "DAU_Grant",
    "DAU_Earmark",
]

corr = df[numeric_cols].corr()

fig3 = px.imshow(
    corr,
    text_auto=True,
    color_continuous_scale="RdBu_r",
    title="Correlation Matrix",
)

st.plotly_chart(fig3, use_container_width=True)


# DATA TABLE
st.subheader("Data Lengkap")

st.dataframe(df_filter, use_container_width=True)
