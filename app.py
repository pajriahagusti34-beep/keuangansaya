import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime

# ==========================
# KONFIGURASI
# ==========================

st.set_page_config(
    page_title="Blue Finance Tracker",
    page_icon="💰",
    layout="wide"
)

# ==========================
# CSS BIRU MODERN
# ==========================

st.markdown("""
<style>

.stApp{
    background: linear-gradient(135deg,#eaf4ff,#f5f9ff);
}

section[data-testid="stSidebar"]{
    background: linear-gradient(180deg,#1565C0,#42A5F5);
}

h1,h2,h3{
    color:#1565C0;
}

[data-testid="stMetric"]{
    background:white;
    padding:15px;
    border-radius:15px;
    box-shadow:0px 3px 10px rgba(0,0,0,0.1);
}

</style>
""", unsafe_allow_html=True)

# ==========================
# DATABASE CSV
# ==========================

FILE = "keuangan.csv"

if not os.path.exists(FILE):
    pd.DataFrame(columns=[
        "Tanggal",
        "Jenis",
        "Periode",
        "Kategori",
        "Nominal",
        "Catatan"
    ]).to_csv(FILE,index=False)

df = pd.read_csv(FILE)

# ==========================
# SIDEBAR
# ==========================

st.sidebar.title("💰 Blue Finance")

menu = st.sidebar.radio(
    "Menu",
    [
        "🏠 Dashboard",
        "➕ Tambah Transaksi",
        "📋 Riwayat",
        "📊 Laporan Bulanan",
        "📈 Analisis",
        "🎯 Target Tabungan"
    ]
)

# ==========================
# PERHITUNGAN
# ==========================

if len(df) > 0:

    pemasukan = df[df["Jenis"]=="Pemasukan"]["Nominal"].sum()

    pengeluaran = df[df["Jenis"]=="Pengeluaran"]["Nominal"].sum()

else:

    pemasukan = 0
    pengeluaran = 0

sisa_uang = pemasukan - pengeluaran

# ==========================
# DASHBOARD
# ==========================

if menu == "🏠 Dashboard":

    st.title("💰 Dashboard Keuangan")

    c1,c2,c3 = st.columns(3)

    with c1:
        st.metric(
            "💵 Total Pemasukan",
            f"Rp {pemasukan:,.0f}"
        )

    with c2:
        st.metric(
            "💸 Total Pengeluaran",
            f"Rp {pengeluaran:,.0f}"
        )

    with c3:
        st.metric(
            "💙 Sisa Uang",
            f"Rp {sisa_uang:,.0f}"
        )

    st.markdown("---")

    if len(df) > 0:

        chart = pd.DataFrame({
            "Jenis":["Pemasukan","Pengeluaran"],
            "Jumlah":[pemasukan,pengeluaran]
        })

        fig = px.bar(
            chart,
            x="Jenis",
            y="Jumlah",
            text_auto=True,
            color="Jenis"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

# ==========================
# TAMBAH TRANSAKSI
# ==========================

elif menu == "➕ Tambah Transaksi":

    st.title("➕ Tambah Transaksi")

    jenis = st.selectbox(
        "Jenis Transaksi",
        [
            "Pemasukan",
            "Pengeluaran"
        ]
    )

    periode = st.selectbox(
        "Periode",
        [
            "Harian",
            "Bulanan"
        ]
    )

    if jenis == "Pemasukan":

        kategori = st.selectbox(
            "Kategori",
            [
                "Gaji",
                "Bonus",
                "Freelance",
                "Investasi",
                "Uang Saku",
                "Lainnya"
            ]
        )

    else:

        kategori = st.selectbox(
            "Kategori",
            [
                "Makan",
                "Minum",
                "Belanja",
                "Transportasi",
                "Tagihan",
                "Internet",
                "Kesehatan",
                "Pendidikan",
                "Hiburan",
                "Rumah Tangga",
                "Lainnya"
            ]
        )

    nominal = st.number_input(
        "Nominal (Rp)",
        min_value=0,
        step=1000
    )

    catatan = st.text_area(
        "Catatan"
    )

    if st.button("💾 Simpan"):

        tanggal_otomatis = datetime.now().strftime(
            "%d-%m-%Y %H:%M:%S"
        )

        data_baru = {
            "Tanggal": tanggal_otomatis,
            "Jenis": jenis,
            "Periode": periode,
            "Kategori": kategori,
            "Nominal": nominal,
            "Catatan": catatan
        }

        df = pd.concat(
            [df,pd.DataFrame([data_baru])],
            ignore_index=True
        )

        df.to_csv(FILE,index=False)

        st.success(
            "Transaksi berhasil disimpan"
        )

# ==========================
# RIWAYAT
# ==========================

elif menu == "📋 Riwayat":

    st.title("📋 Riwayat Transaksi")

    if len(df) == 0:

        st.warning(
            "Belum ada transaksi"
        )

    else:

        st.dataframe(
            df,
            use_container_width=True
        )

# ==========================
# LAPORAN BULANAN
# ==========================

elif menu == "📊 Laporan Bulanan":

    st.title("📊 Laporan Bulanan")

    st.metric(
        "Total Pemasukan",
        f"Rp {pemasukan:,.0f}"
    )

    st.metric(
        "Total Pengeluaran",
        f"Rp {pengeluaran:,.0f}"
    )

    st.metric(
        "Sisa Uang",
        f"Rp {sisa_uang:,.0f}"
    )

# ==========================
# ANALISIS
# ==========================

elif menu == "📈 Analisis":

    st.title("📈 Analisis Pengeluaran")

    data_pengeluaran = df[
        df["Jenis"]=="Pengeluaran"
    ]

    if len(data_pengeluaran) > 0:

        fig = px.pie(
            data_pengeluaran,
            names="Kategori",
            values="Nominal",
            hole=0.4
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:

        st.warning(
            "Belum ada data pengeluaran"
        )

# ==========================
# TARGET TABUNGAN
# ==========================

elif menu == "🎯 Target Tabungan":

    st.title("🎯 Target Tabungan")

    target = st.number_input(
        "Masukkan Target",
        min_value=1,
        step=100000
    )

    progress = min(
        sisa_uang / target,
        1.0
    )

    st.progress(progress)

    st.success(
        f"Progress : {progress*100:.1f}%"
    )
