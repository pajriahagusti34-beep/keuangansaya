import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import date

# =====================
# CONFIG
# =====================
st.set_page_config(
    page_title="Smart Finance Manager",
    page_icon="💰",
    layout="wide"
)

# =====================
# CSS PREMIUM
# =====================
st.markdown("""
<style>
.stApp{
    background: linear-gradient(to right,#0f172a,#1e293b);
}

.card{
    background:white;
    padding:20px;
    border-radius:15px;
    box-shadow:0 4px 15px rgba(0,0,0,0.2);
}

h1,h2,h3{
    color:white;
}
</style>
""", unsafe_allow_html=True)

# =====================
# FILE DATA
# =====================
FILE = "data.csv"

if not os.path.exists(FILE):
    pd.DataFrame(columns=[
        "Tanggal",
        "Jenis",
        "Kategori",
        "Nominal",
        "Keterangan"
    ]).to_csv(FILE,index=False)

df = pd.read_csv(FILE)

# =====================
# SIDEBAR
# =====================
st.sidebar.title("💰 Smart Finance")

menu = st.sidebar.radio(
    "Menu",
    [
        "🏠 Dashboard",
        "➕ Tambah Transaksi",
        "📋 Riwayat",
        "📊 Analisis",
        "🎯 Target Tabungan"
    ]
)

# =====================
# DASHBOARD
# =====================
if menu == "🏠 Dashboard":

    st.title("💰 Dashboard Keuangan")

    pemasukan = df[df["Jenis"]=="Pemasukan"]["Nominal"].sum()
    pengeluaran = df[df["Jenis"]=="Pengeluaran"]["Nominal"].sum()

    saldo_awal = 1000000
    saldo_akhir = saldo_awal + pemasukan - pengeluaran

    c1,c2,c3,c4 = st.columns(4)

    c1.metric("💵 Saldo Awal",f"Rp {saldo_awal:,.0f}")
    c2.metric("📈 Pemasukan",f"Rp {pemasukan:,.0f}")
    c3.metric("📉 Pengeluaran",f"Rp {pengeluaran:,.0f}")
    c4.metric("💰 Saldo Akhir",f"Rp {saldo_akhir:,.0f}")

    st.subheader("📌 Ringkasan")

    st.info(f"""
Saldo awal Anda Rp {saldo_awal:,.0f}

Total pemasukan Rp {pemasukan:,.0f}

Total pengeluaran Rp {pengeluaran:,.0f}

Saldo akhir Rp {saldo_akhir:,.0f}
""")

# =====================
# TAMBAH TRANSAKSI
# =====================
elif menu == "➕ Tambah Transaksi":

    st.title("➕ Tambah Transaksi")

    with st.form("transaksi"):

        tanggal = st.date_input("Tanggal",date.today())

        jenis = st.selectbox(
            "Jenis",
            ["Pemasukan","Pengeluaran"]
        )

        kategori = st.selectbox(
            "Kategori",
            [
                "Gaji",
                "Makan",
                "Transportasi",
                "Belanja",
                "Hiburan",
                "Pendidikan",
                "Kesehatan",
                "Tagihan"
            ]
        )

        nominal = st.number_input(
            "Nominal",
            min_value=0
        )

        ket = st.text_input("Keterangan")

        simpan = st.form_submit_button("💾 Simpan")

        if simpan:

            baru = {
                "Tanggal":tanggal,
                "Jenis":jenis,
                "Kategori":kategori,
                "Nominal":nominal,
                "Keterangan":ket
            }

            df = pd.concat(
                [df,pd.DataFrame([baru])],
                ignore_index=True
            )

            df.to_csv(FILE,index=False)

            st.success("Data berhasil disimpan")

# =====================
# RIWAYAT
# =====================
elif menu == "📋 Riwayat":

    st.title("📋 Riwayat Transaksi")

    cari = st.text_input("🔍 Cari transaksi")

    tampil = df.copy()

    if cari:
        tampil = tampil[
            tampil["Keterangan"]
            .astype(str)
            .str.contains(cari,case=False)
        ]

    st.dataframe(
        tampil,
        use_container_width=True
    )

# =====================
# ANALISIS
# =====================
elif menu == "📊 Analisis":

    st.title("📊 Analisis Keuangan")

    pemasukan = df[df["Jenis"]=="Pemasukan"]["Nominal"].sum()
    pengeluaran = df[df["Jenis"]=="Pengeluaran"]["Nominal"].sum()

    grafik1 = pd.DataFrame({
        "Jenis":["Pemasukan","Pengeluaran"],
        "Jumlah":[pemasukan,pengeluaran]
    })

    fig = px.bar(
        grafik1,
        x="Jenis",
        y="Jumlah",
        title="Perbandingan Keuangan"
    )

    st.plotly_chart(fig,use_container_width=True)

    pengeluaran_df = df[df["Jenis"]=="Pengeluaran"]

    if not pengeluaran_df.empty:

        pie = px.pie(
            pengeluaran_df,
            names="Kategori",
            values="Nominal",
            title="Kategori Pengeluaran"
        )

        st.plotly_chart(
            pie,
            use_container_width=True
        )

# =====================
# TARGET TABUNGAN
# =====================
elif menu == "🎯 Target Tabungan":

    st.title("🎯 Target Tabungan")

    pemasukan = df[df["Jenis"]=="Pemasukan"]["Nominal"].sum()
    pengeluaran = df[df["Jenis"]=="Pengeluaran"]["Nominal"].sum()

    saldo = pemasukan - pengeluaran

    target = st.number_input(
        "Masukkan Target",
        min_value=1
    )

    progress = min(saldo/target,1.0)

    st.progress(progress)

    st.success(
        f"Progress : {progress*100:.1f}%"
    )

    st.write(
        f"Saldo Saat Ini : Rp {saldo:,.0f}"
    )
