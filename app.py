import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date
import os

st.set_page_config(
    page_title="Finance Tracker Pro",
    page_icon="💰",
    layout="wide"
)

# ================= CSS =================

st.markdown("""
<style>

.main{
    background-color:#f5f7fa;
}

.block-container{
    padding-top:1rem;
}

.card{
    background:white;
    padding:20px;
    border-radius:15px;
    box-shadow:0 4px 12px rgba(0,0,0,0.1);
    text-align:center;
}

.card-title{
    color:gray;
    font-size:16px;
}

.card-value{
    font-size:28px;
    font-weight:bold;
    color:#0f766e;
}

.title{
    text-align:center;
    font-size:42px;
    font-weight:bold;
}

.subtitle{
    text-align:center;
    color:gray;
    margin-bottom:25px;
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
        "Keterangan"
    ]).to_csv(FILE,index=False)

df = pd.read_csv(FILE)

# ================= SIDEBAR =================

st.sidebar.image(
    "https://cdn-icons-png.flaticon.com/512/3135/3135706.png",
    width=100
)

st.sidebar.title("💰 Finance Tracker")

menu = st.sidebar.radio(
    "Navigasi",
    [
        "Dashboard",
        "Tambah Transaksi",
        "Riwayat",
        "Analisis",
        "Target Keuangan",
        "Laporan"
    ]
)

# ================= DASHBOARD =================

if menu == "Dashboard":

    pemasukan = df[df["Jenis"]=="Pemasukan"]["Nominal"].sum()
    pengeluaran = df[df["Jenis"]=="Pengeluaran"]["Nominal"].sum()

    saldo_awal = 1000000

    saldo_akhir = saldo_awal + pemasukan - pengeluaran

    st.markdown(
        "<div class='title'>💰 Finance Tracker Pro</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div class='subtitle'>Kelola Keuangan Pribadi Dengan Mudah</div>",
        unsafe_allow_html=True
    )

    c1,c2,c3,c4 = st.columns(4)

    with c1:
        st.markdown(f"""
        <div class='card'>
        <div class='card-title'>💵 Saldo Awal</div>
        <div class='card-value'>Rp {saldo_awal:,.0f}</div>
        </div>
        """,unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class='card'>
        <div class='card-title'>📈 Pemasukan</div>
        <div class='card-value'>Rp {pemasukan:,.0f}</div>
        </div>
        """,unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class='card'>
        <div class='card-title'>📉 Pengeluaran</div>
        <div class='card-value'>Rp {pengeluaran:,.0f}</div>
        </div>
        """,unsafe_allow_html=True)

    with c4:
        st.markdown(f"""
        <div class='card'>
        <div class='card-title'>💰 Saldo Akhir</div>
        <div class='card-value'>Rp {saldo_akhir:,.0f}</div>
        </div>
        """,unsafe_allow_html=True)

    st.markdown("---")

    col1,col2 = st.columns(2)

    with col1:

        grafik = pd.DataFrame({
            "Jenis":["Pemasukan","Pengeluaran"],
            "Jumlah":[pemasukan,pengeluaran]
        })

        fig = px.bar(
            grafik,
            x="Jenis",
            y="Jumlah",
            title="Perbandingan Pemasukan dan Pengeluaran"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        pengeluaran_df = df[
            df["Jenis"]=="Pengeluaran"
        ]

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

    st.markdown("### 💡 Insight Keuangan")

    if pengeluaran > pemasukan:
        st.error(
            "⚠ Pengeluaran lebih besar dari pemasukan."
        )
    else:
        st.success(
            "✅ Kondisi keuangan masih sehat."
        )

# ================= TAMBAH =================

elif menu == "Tambah Transaksi":

    st.title("➕ Tambah Transaksi")

    with st.form("form"):

        tanggal = st.date_input(
            "Tanggal",
            date.today()
        )

        jenis = st.selectbox(
            "Jenis Transaksi",
            [
                "Pemasukan",
                "Pengeluaran"
            ]
        )

        kategori = st.selectbox(
            "Kategori",
            [
                "Gaji",
                "Bonus",
                "Makan",
                "Transportasi",
                "Belanja",
                "Tagihan",
                "Hiburan",
                "Pendidikan",
                "Kesehatan",
                "Lainnya"
            ]
        )

        nominal = st.number_input(
            "Nominal",
            min_value=0
        )

        ket = st.text_area(
            "Keterangan"
        )

        submit = st.form_submit_button(
            "💾 Simpan"
        )

        if submit:

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

            df.to_csv(
                FILE,
                index=False
            )

            st.success(
                "Transaksi berhasil ditambahkan"
            )

# ================= RIWAYAT =================

elif menu == "Riwayat":

    st.title("📋 Riwayat Transaksi")

    cari = st.text_input(
        "Cari Transaksi"
    )

    tampil = df.copy()

    if cari:
        tampil = tampil[
            tampil["Keterangan"]
            .astype(str)
            .str.contains(
                cari,
                case=False
            )
        ]

    st.dataframe(
        tampil,
        use_container_width=True
    )

# ================= ANALISIS =================

elif menu == "Analisis":

    st.title("📊 Analisis Keuangan")

    if not df.empty:

        df["Tanggal"] = pd.to_datetime(
            df["Tanggal"]
        )

        df["Bulan"] = (
            df["Tanggal"]
            .dt.strftime("%Y-%m")
        )

        bulanan = (
            df.groupby("Bulan")["Nominal"]
            .sum()
            .reset_index()
        )

        fig = px.line(
            bulanan,
            x="Bulan",
            y="Nominal",
            markers=True,
            title="Tren Keuangan"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

# ================= TARGET =================

elif menu == "Target Keuangan":

    st.title("🎯 Target Tabungan")

    pemasukan = df[
        df["Jenis"]=="Pemasukan"
    ]["Nominal"].sum()

    pengeluaran = df[
        df["Jenis"]=="Pengeluaran"
    ]["Nominal"].sum()

    saldo = pemasukan - pengeluaran

    target = st.number_input(
        "Target Tabungan",
        min_value=1
    )

    progress = min(
        saldo/target,
        1.0
    )

    st.progress(progress)

    st.write(
        f"Progress : {progress*100:.1f}%"
    )

    st.write(
        f"Saldo Saat Ini : Rp {saldo:,.0f}"
    )

# ================= LAPORAN =================

elif menu == "Laporan":

    st.title("📄 Laporan Keuangan")

    pemasukan = df[
        df["Jenis"]=="Pemasukan"
    ]["Nominal"].sum()

    pengeluaran = df[
        df["Jenis"]=="Pengeluaran"
    ]["Nominal"].sum()

    saldo = pemasukan - pengeluaran

    st.write(
        f"Total Pemasukan : Rp {pemasukan:,.0f}"
    )

    st.write(
        f"Total Pengeluaran : Rp {pengeluaran:,.0f}"
    )

    st.write(
        f"Saldo Akhir : Rp {saldo:,.0f}"
    )

    st.download_button(
        label="⬇ Download CSV",
        data=df.to_csv(index=False),
        file_name="laporan_keuangan.csv",
        mime="text/csv"
    )
