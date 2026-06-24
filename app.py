import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date
import os

st.set_page_config(
    page_title="Keuangan Pribadi",
    page_icon="💰",
    layout="wide"
)

DATA_FILE = "data.csv"

# Membuat file CSV jika belum ada
if not os.path.exists(DATA_FILE):
    df_awal = pd.DataFrame(
        columns=[
            "Tanggal",
            "Jenis",
            "Kategori",
            "Nominal",
            "Keterangan"
        ]
    )
    df_awal.to_csv(DATA_FILE, index=False)

# Membaca data
df = pd.read_csv(DATA_FILE)

# Sidebar
menu = st.sidebar.radio(
    "📌 Menu",
    [
        "Dashboard",
        "Tambah Transaksi",
        "Riwayat",
        "Analisis",
        "Target Tabungan"
    ]
)

# ================= DASHBOARD =================

if menu == "Dashboard":

    st.title("💰 Dashboard Keuangan Pribadi")

    pemasukan = df[df["Jenis"] == "Pemasukan"]["Nominal"].sum()
    pengeluaran = df[df["Jenis"] == "Pengeluaran"]["Nominal"].sum()
    saldo = pemasukan - pengeluaran

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "💵 Total Pemasukan",
        f"Rp {pemasukan:,.0f}"
    )

    col2.metric(
        "📉 Total Pengeluaran",
        f"Rp {pengeluaran:,.0f}"
    )

    col3.metric(
        "💰 Saldo Saat Ini",
        f"Rp {saldo:,.0f}"
    )

    st.subheader("📋 Transaksi Terbaru")
    st.dataframe(df.tail(10), use_container_width=True)

# ================= TAMBAH TRANSAKSI =================

elif menu == "Tambah Transaksi":

    st.title("➕ Tambah Transaksi")

    with st.form("form_transaksi"):

        tanggal = st.date_input(
            "Tanggal",
            date.today()
        )

        jenis = st.selectbox(
            "Jenis",
            ["Pemasukan", "Pengeluaran"]
        )

        kategori = st.selectbox(
            "Kategori",
            [
                "Gaji",
                "Makan & Minum",
                "Transportasi",
                "Belanja",
                "Hiburan",
                "Pendidikan",
                "Tagihan",
                "Lainnya"
            ]
        )

        nominal = st.number_input(
            "Nominal",
            min_value=0
        )

        keterangan = st.text_input(
            "Keterangan"
        )

        simpan = st.form_submit_button(
            "💾 Simpan"
        )

        if simpan:

            data_baru = {
                "Tanggal": tanggal,
                "Jenis": jenis,
                "Kategori": kategori,
                "Nominal": nominal,
                "Keterangan": keterangan
            }

            df = pd.concat(
                [df, pd.DataFrame([data_baru])],
                ignore_index=True
            )

            df.to_csv(DATA_FILE, index=False)

            st.success(
                "Transaksi berhasil disimpan!"
            )

# ================= RIWAYAT =================

elif menu == "Riwayat":

    st.title("📋 Riwayat Transaksi")

    cari = st.text_input(
        "Cari Keterangan"
    )

    tampil = df.copy()

    if cari:
        tampil = tampil[
            tampil["Keterangan"]
            .astype(str)
            .str.contains(cari, case=False)
        ]

    st.dataframe(
        tampil,
        use_container_width=True
    )

# ================= ANALISIS =================

elif menu == "Analisis":

    st.title("📊 Analisis Keuangan")

    pemasukan = df[df["Jenis"] == "Pemasukan"]["Nominal"].sum()
    pengeluaran = df[df["Jenis"] == "Pengeluaran"]["Nominal"].sum()

    grafik1 = pd.DataFrame({
        "Jenis": ["Pemasukan", "Pengeluaran"],
        "Jumlah": [pemasukan, pengeluaran]
    })

    fig1 = px.bar(
        grafik1,
        x="Jenis",
        y="Jumlah",
        title="Perbandingan Pemasukan dan Pengeluaran"
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

    pengeluaran_df = df[
        df["Jenis"] == "Pengeluaran"
    ]

    if not pengeluaran_df.empty:

        fig2 = px.pie(
            pengeluaran_df,
            names="Kategori",
            values="Nominal",
            title="Kategori Pengeluaran"
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

# ================= TARGET =================

elif menu == "Target Tabungan":

    st.title("🎯 Target Tabungan")

    pemasukan = df[df["Jenis"] == "Pemasukan"]["Nominal"].sum()
    pengeluaran = df[df["Jenis"] == "Pengeluaran"]["Nominal"].sum()

    saldo = pemasukan - pengeluaran

    target = st.number_input(
        "Masukkan Target Tabungan",
        min_value=1
    )

    progress = min(
        saldo / target,
        1.0
    )

    st.progress(progress)

    st.write(
        f"Progress Tabungan: {progress*100:.1f}%"
    )

    st.write(
        f"Saldo Saat Ini: Rp {saldo:,.0f}"
    )
