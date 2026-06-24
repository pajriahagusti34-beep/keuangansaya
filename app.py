import streamlit as st
import pandas as pd

st.set_page_config(page_title="Keuangan Pribadi", page_icon="💰")

st.title("💰 Aplikasi Keuangan Pribadi")

if "data" not in st.session_state:
    st.session_state.data = []

with st.form("form_keuangan"):
    jenis = st.selectbox(
        "Jenis Transaksi",
        ["Pemasukan", "Pengeluaran"]
    )

    keterangan = st.text_input("Keterangan")

    nominal = st.number_input(
        "Nominal",
        min_value=0
    )

    submit = st.form_submit_button("Simpan")

    if submit:
        st.session_state.data.append({
            "Jenis": jenis,
            "Keterangan": keterangan,
            "Nominal": nominal
        })

df = pd.DataFrame(st.session_state.data)

if not df.empty:

    total_pemasukan = df[df["Jenis"]=="Pemasukan"]["Nominal"].sum()

    total_pengeluaran = df[df["Jenis"]=="Pengeluaran"]["Nominal"].sum()

    saldo = total_pemasukan - total_pengeluaran

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Total Pemasukan",
            f"Rp {total_pemasukan:,.0f}"
        )

    with col2:
        st.metric(
            "Total Pengeluaran",
            f"Rp {total_pengeluaran:,.0f}"
        )

    with col3:
        st.metric(
            "Saldo Saat Ini",
            f"Rp {saldo:,.0f}"
        )

    st.subheader("📋 Riwayat Transaksi")
    st.dataframe(df, use_container_width=True)

    st.subheader("📊 Grafik Keuangan")

    grafik = pd.DataFrame({
        "Jumlah": [
            total_pemasukan,
            total_pengeluaran
        ]
    },
    index=[
        "Pemasukan",
        "Pengeluaran"
    ])

    st.bar_chart(grafik)

else:
    st.info("Belum ada transaksi.")
