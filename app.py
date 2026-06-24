import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import date

st.set_page_config(
    page_title="Pink Finance Tracker",
    page_icon="🌸",
    layout="wide"
)

# ================= CSS =================

st.markdown("""
<style>

.stApp{
background: linear-gradient(135deg,#FFE4EC,#FFF0F5);
}

section[data-testid="stSidebar"]{
background:#FFB6C1;
}

.card{
background:white;
padding:20px;
border-radius:20px;
box-shadow:0px 5px 15px rgba(0,0,0,0.1);
text-align:center;
}

.bigtitle{
text-align:center;
font-size:45px;
font-weight:bold;
color:#d63384;
}

.subtitle{
text-align:center;
color:#666;
font-size:18px;
margin-bottom:20px;
}

</style>
""", unsafe_allow_html=True)

# ================= FILE =================

FILE = "keuangan.csv"

if not os.path.exists(FILE):
    pd.DataFrame(columns=[
        "Tanggal",
        "Jenis",
        "Kategori",
        "Nominal",
        "Catatan"
    ]).to_csv(FILE,index=False)

df = pd.read_csv(FILE)

# ================= SIDEBAR =================

st.sidebar.title("🌸 Pink Finance")

menu = st.sidebar.radio(
    "Menu",
    [
        "🏠 Dashboard",
        "💸 Tambah Transaksi",
        "📋 Riwayat",
        "📊 Laporan Bulanan",
        "🥧 Analisis",
        "🎯 Target Tabungan",
        "💡 Insight"
    ]
)

# ================= HITUNG =================

saldo_awal = 1000000

pemasukan = df[df["Jenis"]=="Pemasukan"]["Nominal"].sum()

pengeluaran = df[df["Jenis"]=="Pengeluaran"]["Nominal"].sum()

saldo_akhir = saldo_awal + pemasukan - pengeluaran

# ================= DASHBOARD =================

if menu == "🏠 Dashboard":

    st.markdown(
    "<div class='bigtitle'>🌸 Pink Finance Tracker</div>",
    unsafe_allow_html=True
    )

    st.markdown(
    "<div class='subtitle'>Kelola Keuangan Harian dan Bulanan</div>",
    unsafe_allow_html=True
    )

    c1,c2,c3,c4 = st.columns(4)

    with c1:
        st.markdown(f"""
        <div class='card'>
        <h4>💰 Saldo Awal</h4>
        <h2>Rp {saldo_awal:,.0f}</h2>
        </div>
        """,unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class='card'>
        <h4>📈 Pemasukan</h4>
        <h2>Rp {pemasukan:,.0f}</h2>
        </div>
        """,unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class='card'>
        <h4>📉 Pengeluaran</h4>
        <h2>Rp {pengeluaran:,.0f}</h2>
        </div>
        """,unsafe_allow_html=True)

    with c4:
        st.markdown(f"""
        <div class='card'>
        <h4>💖 Saldo Akhir</h4>
        <h2>Rp {saldo_akhir:,.0f}</h2>
        </div>
        """,unsafe_allow_html=True)

    st.markdown("---")

    st.subheader("📊 Ringkasan Keuangan")

    chart = pd.DataFrame({
        "Jenis":["Pemasukan","Pengeluaran"],
        "Jumlah":[pemasukan,pengeluaran]
    })

    fig = px.bar(
        chart,
        x="Jenis",
        y="Jumlah",
        text_auto=True
    )

    st.plotly_chart(fig,use_container_width=True)

# ================= TRANSAKSI =================

elif menu == "💸 Tambah Transaksi":

    st.title("💸 Tambah Transaksi")

    with st.form("form_keuangan"):

        tanggal = st.date_input(
            "Tanggal",
            date.today()
        )

        jenis = st.radio(
            "Jenis",
            ["Pemasukan","Pengeluaran"]
        )

        kategori = st.selectbox(
            "Kategori",
            [
                "💼 Gaji",
                "🍔 Makan",
                "🛍 Belanja",
                "🚌 Transportasi",
                "🎮 Hiburan",
                "📚 Pendidikan",
                "💡 Tagihan",
                "🏥 Kesehatan"
            ]
        )

        nominal = st.number_input(
            "Nominal",
            min_value=0
        )

        catatan = st.text_area(
            "Catatan"
        )

        simpan = st.form_submit_button(
            "💖 Simpan Transaksi"
        )

        if simpan:

            data_baru = {
                "Tanggal":tanggal,
                "Jenis":jenis,
                "Kategori":kategori,
                "Nominal":nominal,
                "Catatan":catatan
            }

            df = pd.concat(
                [df,pd.DataFrame([data_baru])],
                ignore_index=True
            )

            df.to_csv(FILE,index=False)

            st.success("Data berhasil disimpan 🌸")

# ================= RIWAYAT =================

elif menu == "📋 Riwayat":

    st.title("📋 Riwayat Transaksi")

    st.dataframe(
        df,
        use_container_width=True
    )

# ================= LAPORAN =================

elif menu == "📊 Laporan Bulanan":

    st.title("📊 Laporan Bulanan")

    st.info(f"""
    Total Pemasukan Bulan Ini : Rp {pemasukan:,.0f}

    Total Pengeluaran Bulan Ini : Rp {pengeluaran:,.0f}

    Sisa Uang Bulan Ini : Rp {saldo_akhir:,.0f}
    """)

# ================= ANALISIS =================

elif menu == "🥧 Analisis":

    st.title("🥧 Analisis Pengeluaran")

    data_pengeluaran = df[
        df["Jenis"]=="Pengeluaran"
    ]

    if not data_pengeluaran.empty:

        pie = px.pie(
            data_pengeluaran,
            names="Kategori",
            values="Nominal",
            hole=0.4
        )

        st.plotly_chart(
            pie,
            use_container_width=True
        )

    else:
        st.warning(
            "Belum ada data pengeluaran"
        )

# ================= TARGET =================

elif menu == "🎯 Target Tabungan":

    st.title("🎯 Target Tabungan")

    target = st.number_input(
        "Masukkan Target Tabungan",
        min_value=1
    )

    progress = min(
        saldo_akhir/target,
        1.0
    )

    st.progress(progress)

    st.success(
        f"Progress {progress*100:.1f}%"
    )

# ================= INSIGHT =================

elif menu == "💡 Insight":

    st.title("💡 Insight Keuangan")

    if pengeluaran > pemasukan:

        st.error(
        "⚠ Pengeluaran lebih besar daripada pemasukan."
        )

    else:

        st.success(
        "✅ Kondisi keuangan sehat."
        )

    st.info(
    f"💖 Saldo saat ini Rp {saldo_akhir:,.0f}"
    )
