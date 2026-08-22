import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


# =========================
# KONFIGURASI HALAMAN
# =========================

st.set_page_config(
    page_title="Bike Sharing Dashboard",
    page_icon="🚲",
    layout="wide"
)


# =========================
# LOAD DATA
# =========================

df = pd.read_csv("data/day.csv")

df["dteday"] = pd.to_datetime(df["dteday"])


# =========================
# JUDUL DASHBOARD
# =========================

st.title("🚲 Bike Sharing Dashboard")

st.markdown(
    """
    Dashboard ini menyajikan hasil analisis data penyewaan sepeda
    berdasarkan waktu dan kondisi cuaca selama periode 2011-2012.
    """
)


# =========================
# SIDEBAR FILTER
# =========================

st.sidebar.header("Filter Data")

tahun = st.sidebar.selectbox(
    "Pilih Tahun",
    ["Semua Tahun", 2011, 2012]
)


# =========================
# FILTER DATA
# =========================

if tahun == "Semua Tahun":
    filtered_df = df.copy()
else:
    filtered_df = df[df["dteday"].dt.year == tahun]


# =========================
# METRICS
# =========================

total_rental = filtered_df["cnt"].sum()
rata_rental = filtered_df["cnt"].mean()
total_registered = filtered_df["registered"].sum()
total_casual = filtered_df["casual"].sum()


col1, col2, col3, col4 = st.columns(4)


with col1:
    st.metric(
        "Total Rental",
        f"{total_rental:,.0f}"
    )

with col2:
    st.metric(
        "Rata-rata Rental",
        f"{rata_rental:,.0f}"
    )

with col3:
    st.metric(
        "Registered User",
        f"{total_registered:,.0f}"
    )

with col4:
    st.metric(
        "Casual User",
        f"{total_casual:,.0f}"
    )


# =========================
# TREN PENYEWAAN
# =========================

st.subheader("📈 Tren Penyewaan Sepeda")

daily_rental = (
    filtered_df
    .groupby("dteday")["cnt"]
    .sum()
)


fig, ax = plt.subplots(figsize=(12, 5))

ax.plot(
    daily_rental.index,
    daily_rental.values
)

ax.set_xlabel("Tanggal")
ax.set_ylabel("Jumlah Rental")
ax.set_title("Tren Penyewaan Sepeda")

plt.xticks(rotation=45)

st.pyplot(fig)


# =========================
# RENTAL BERDASARKAN BULAN
# =========================

st.subheader("📅 Rata-rata Penyewaan Berdasarkan Bulan")

monthly_rental = (
    filtered_df
    .groupby(filtered_df["dteday"].dt.month)["cnt"]
    .mean()
)


fig, ax = plt.subplots(figsize=(10, 5))

ax.bar(
    monthly_rental.index,
    monthly_rental.values
)

ax.set_xlabel("Bulan")
ax.set_ylabel("Rata-rata Rental")
ax.set_title("Rata-rata Penyewaan Berdasarkan Bulan")

st.pyplot(fig)


# =========================
# PENGARUH CUACA
# =========================

st.subheader("🌤️ Penyewaan Berdasarkan Kondisi Cuaca")

weather_rental = (
    filtered_df
    .groupby("weathersit")["cnt"]
    .mean()
)


fig, ax = plt.subplots(figsize=(8, 5))

ax.bar(
    weather_rental.index.astype(str),
    weather_rental.values
)

ax.set_xlabel("Kondisi Cuaca")
ax.set_ylabel("Rata-rata Rental")
ax.set_title("Rata-rata Rental Berdasarkan Kondisi Cuaca")

st.pyplot(fig)

# =========================
# ANALISIS CASUAL VS REGISTERED
# =========================

st.subheader("👥 Casual vs Registered User")

user_type = (
    filtered_df[["casual", "registered"]]
    .mean()
)

fig, ax = plt.subplots(figsize=(8, 5))

ax.bar(
    user_type.index,
    user_type.values
)

ax.set_xlabel("Tipe Pengguna")
ax.set_ylabel("Rata-rata Jumlah Pengguna")
ax.set_title("Perbandingan Rata-rata Casual dan Registered User")

st.pyplot(fig)

# =========================
# DATA TABLE
# =========================

st.subheader("📋 Data")

st.dataframe(
    filtered_df,
    use_container_width=True
)
