import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import date

st.set_page_config(
    page_title="Finance Monthly Tracker",
    page_icon="💰",
    layout="wide"
)

# ================= CSS =================

st.markdown("""
<style>

.stApp{
background: linear-gradient(135deg,#ffd6e7,#ffeef5,#ffffff);
}

section[data-testid="stSidebar"]{
background:#ff8fb1;
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

# ================= DATABASE =================

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

# ================= PERHITUNGAN =================

pemasukan = df[df["Jenis"]=="Pemasukan"]["Nominal"].sum()

pengeluaran = df[df["Jenis"]=="Pengeluaran"]["Nominal"].sum()

sisa_uang = pemasukan - pengeluaran

if pemasukan > 0:
    persen_tabungan = (sisa_uang / pemasukan) * 100
else:
    persen_tabungan = 0

# ================= SIDEBAR =================

st.sidebar.title("🌸 Finance Tracker")

menu = st.sidebar.radio(
    "Menu",
    [
        "🏠 Dashboard",
        "➕ Tambah Transaksi",
        "📋 Riwayat",
        "📊 Laporan Bulanan",
        "🥧 Analisis",
        "🎯 Target Tabungan",
        "💡 Insight"
    ]
)

# ================= DASHBOARD =================

if menu == "🏠 Dashboard":

    st.title("🌸 Dashboard Keuangan Bulanan")

    c1,c2,c3,c4 = st.columns(4)

    c1.metric(
        "💰 Pemasukan",
        f"Rp {pemasukan:,.0f}"
    )

    c2.metric(
        "💸 Pengeluaran",
        f"Rp {pengeluaran:,.0f}"
    )

    c3.metric(
        "💖 Sisa Uang",
        f"Rp {sisa_uang:,.0f}"
    )

    c4.metric(
        "🎯 Tabungan",
        f"{persen_tabungan:.1f}%"
    )

    st.markdown("---")

    chart = pd.DataFrame({
        "Jenis":["Pemasukan","Pengeluaran"],
        "Jumlah":[pemasukan,pengeluaran]
    })

    fig = px.bar(
        chart,
        x="Jenis",
        y="Jumlah",
        color="Jenis",
        text_auto=True
    )

    st.plotly_chart(fig,use_container_width=True)

# ================= TRANSAKSI =================

elif menu == "➕ Tambah Transaksi":

    st.header("➕ Tambah Transaksi")

    with st.form("transaksi"):

        tanggal = st.date_input(
            "Tanggal",
            date.today()
        )

        jenis = st.selectbox(
            "Jenis",
            ["Pemasukan","Pengeluaran"]
        )

        if jenis == "Pemasukan":
            kategori = st.selectbox(
                "Kategori",
                [
                    "💼 Gaji",
                    "🎁 Bonus",
                    "💻 Freelance",
                    "📈 Investasi",
                    "📦 Lainnya"
                ]
            )

        else:
            kategori = st.selectbox(
                "Kategori",
                [
                    "🍔 Makan",
                    "🛒 Belanja",
                    "🚗 Transportasi",
                    "🏠 Tagihan",
                    "🏥 Kesehatan",
                    "🎮 Hiburan",
                    "📚 Pendidikan",
                    "📱 Internet"
                ]
            )

        nominal = st.number_input(
            "Nominal",
            min_value=0
        )

        catatan = st.text_area(
            "Catatan"
        )

        submit = st.form_submit_button(
            "Simpan"
        )

        if submit:

            data = {
                "Tanggal":tanggal,
                "Jenis":jenis,
                "Kategori":kategori,
                "Nominal":nominal,
                "Catatan":catatan
            }

            df = pd.concat(
                [df,pd.DataFrame([data])],
                ignore_index=True
            )

            df.to_csv(FILE,index=False)

            st.success("Transaksi berhasil disimpan")

# ================= RIWAYAT =================

elif menu == "📋 Riwayat":

    st.header("📋 Riwayat Transaksi")

    st.dataframe(
        df,
        use_container_width=True
    )

# ================= LAPORAN =================

elif menu == "📊 Laporan Bulanan":

    st.header("📊 Laporan Bulanan")

    st.success(f"""
💰 Total Pemasukan : Rp {pemasukan:,.0f}

💸 Total Pengeluaran : Rp {pengeluaran:,.0f}

💖 Sisa Uang : Rp {sisa_uang:,.0f}
""")

# ================= ANALISIS =================

elif menu == "🥧 Analisis":

    st.header("🥧 Analisis Pengeluaran")

    data_pengeluaran = df[
        df["Jenis"]=="Pengeluaran"
    ]

    if not data_pengeluaran.empty:

        fig = px.pie(
            data_pengeluaran,
            names="Kategori",
            values="Nominal",
            hole=0.5
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:
        st.warning(
            "Belum ada data pengeluaran"
        )

# ================= TARGET TABUNGAN =================

elif menu == "🎯 Target Tabungan":

    st.header("🎯 Target Tabungan")

    target = st.number_input(
        "Masukkan Target",
        min_value=1
    )

    progress = min(
        sisa_uang/target,
        1.0
    )

    st.progress(progress)

    st.success(
        f"{progress*100:.1f}% tercapai"
    )

# ================= INSIGHT =================

elif menu == "💡 Insight":

    st.header("💡 Insight Keuangan")

    if pemasukan == 0:
        st.warning(
            "Belum ada data pemasukan"
        )

    elif pengeluaran > pemasukan:

        st.error(
            "⚠ Pengeluaran lebih besar dari pemasukan"
        )

    else:

        st.success(
            "✅ Kondisi keuangan sehat"
        )

    st.info(
        f"Sisa uang saat ini Rp {sisa_uang:,.0f}"
    )
