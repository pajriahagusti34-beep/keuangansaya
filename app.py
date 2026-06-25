import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import date

# =========================
# CONFIG
# =========================

st.set_page_config(
    page_title="My Finance Tracker",
    page_icon="💖",
    layout="wide"
)

# =========================
# CSS
# =========================

st.markdown("""
<style>

.stApp{
background: linear-gradient(135deg,#ffe5ec,#fff5f8,#ffffff);
}

section[data-testid="stSidebar"]{
background: linear-gradient(180deg,#ff8fb1,#ffb6c1);
}

h1,h2,h3{
color:#d63384;
}

.card{
background:white;
padding:20px;
border-radius:20px;
box-shadow:0 4px 15px rgba(0,0,0,0.1);
text-align:center;
}

</style>
""", unsafe_allow_html=True)

# =========================
# FILE DATABASE
# =========================

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

# =========================
# PERHITUNGAN
# =========================

if len(df) == 0:
    pemasukan = 0
    pengeluaran = 0
else:
    pemasukan = df[df["Jenis"]=="Pemasukan"]["Nominal"].sum()
    pengeluaran = df[df["Jenis"]=="Pengeluaran"]["Nominal"].sum()

sisa_uang = pemasukan - pengeluaran

makan = df[df["Kategori"].astype(str).str.contains("Makan",na=False)]["Nominal"].sum()
minum = df[df["Kategori"].astype(str).str.contains("Minum",na=False)]["Nominal"].sum()
belanja = df[df["Kategori"].astype(str).str.contains("Belanja",na=False)]["Nominal"].sum()
transportasi = df[df["Kategori"].astype(str).str.contains("Transportasi",na=False)]["Nominal"].sum()

# =========================
# SIDEBAR
# =========================

st.sidebar.title("💖 Finance Tracker")

menu = st.sidebar.radio(
    "Menu",
    [
        "🏠 Dashboard",
        "➕ Tambah Transaksi",
        "📋 Riwayat",
        "📊 Laporan Bulanan",
        "📈 Analisis",
        "🎯 Target Menabung"
    ]
)

# =========================
# DASHBOARD
# =========================

if menu == "🏠 Dashboard":

    st.title("💖 Dashboard Keuangan")

    c1,c2,c3 = st.columns(3)

    with c1:
        st.metric(
            "💰 Total Pemasukan",
            f"Rp {pemasukan:,.0f}"
        )

    with c2:
        st.metric(
            "💸 Total Pengeluaran",
            f"Rp {pengeluaran:,.0f}"
        )

    with c3:
        st.metric(
            "💖 Sisa Uang",
            f"Rp {sisa_uang:,.0f}"
        )

    st.markdown("---")

    a,b,c,d = st.columns(4)

    with a:
        st.info(f"🍔 Makan\n\nRp {makan:,.0f}")

    with b:
        st.info(f"🥤 Minum\n\nRp {minum:,.0f}")

    with c:
        st.info(f"🛍 Belanja\n\nRp {belanja:,.0f}")

    with d:
        st.info(f"🚗 Transportasi\n\nRp {transportasi:,.0f}")

    st.markdown("---")

    grafik = pd.DataFrame({
        "Jenis":["Pemasukan","Pengeluaran"],
        "Jumlah":[pemasukan,pengeluaran]
    })

    fig = px.bar(
        grafik,
        x="Jenis",
        y="Jumlah",
        color="Jenis",
        text_auto=True,
        title="Perbandingan Pemasukan & Pengeluaran"
    )

    st.plotly_chart(fig, use_container_width=True)

# =========================
# TAMBAH TRANSAKSI
# =========================

elif menu == "➕ Tambah Transaksi":

    st.title("➕ Tambah Transaksi")

    tanggal = st.date_input(
        "📅 Tanggal",
        date.today()
    )

    periode = st.selectbox(
        "📆 Periode",
        [
            "Harian",
            "Bulanan"
        ]
    )

    jenis = st.radio(
        "Jenis Transaksi",
        [
            "Pemasukan",
            "Pengeluaran"
        ]
    )

    if jenis == "Pemasukan":

        kategori = st.selectbox(
            "Kategori Pemasukan",
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
            "Kategori Pengeluaran",
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
        "💰 Nominal (Rp)",
        min_value=0,
        step=1000
    )

    catatan = st.text_area(
        "📝 Catatan"
    )

    if st.button("💾 Simpan Transaksi"):

        data_baru = {
            "Tanggal":tanggal,
            "Jenis":jenis,
            "Periode":periode,
            "Kategori":kategori,
            "Nominal":nominal,
            "Catatan":catatan
        }

        df = pd.concat(
            [df,pd.DataFrame([data_baru])],
            ignore_index=True
        )

        df.to_csv(FILE,index=False)

        st.success("✅ Data berhasil disimpan")

# =========================
# RIWAYAT
# =========================

elif menu == "📋 Riwayat":

    st.title("📋 Riwayat Transaksi")

    if len(df) == 0:
        st.warning("Belum ada transaksi")
    else:
        st.dataframe(
            df,
            use_container_width=True
        )

# =========================
# LAPORAN
# =========================

elif menu == "📊 Laporan Bulanan":

    st.title("📊 Laporan Keuangan")

    st.success(f"""
💰 Total Pemasukan : Rp {pemasukan:,.0f}

💸 Total Pengeluaran : Rp {pengeluaran:,.0f}

💖 Sisa Uang : Rp {sisa_uang:,.0f}
""")

# =========================
# ANALISIS
# =========================

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

# =========================
# TARGET TABUNGAN
# =========================

elif menu == "🎯 Target Menabung":

    st.title("🎯 Target Menabung")

    target = st.number_input(
        "Masukkan Target Tabungan",
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

    st.info(
        f"Sisa Uang Saat Ini : Rp {sisa_uang:,.0f}"
    )
