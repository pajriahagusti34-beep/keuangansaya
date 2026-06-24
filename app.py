import streamlit as st

st.set_page_config(page_title="Keuangan Pribadi")

st.title("💰 Aplikasi Keuangan Pribadi")

if "saldo" not in st.session_state:
    st.session_state.saldo = 0

if "riwayat" not in st.session_state:
    st.session_state.riwayat = []

menu = st.selectbox(
    "Pilih Transaksi",
    ["Pemasukan", "Pengeluaran"]
)

keterangan = st.text_input("Keterangan")
jumlah = st.number_input("Jumlah", min_value=0)

if st.button("Simpan"):
    if menu == "Pemasukan":
        st.session_state.saldo += jumlah
        st.session_state.riwayat.append(
            f"Pemasukan - {keterangan} : Rp {jumlah:,.0f}"
        )
    else:
        st.session_state.saldo -= jumlah
        st.session_state.riwayat.append(
            f"Pengeluaran - {keterangan} : Rp {jumlah:,.0f}"
        )

    st.success("Data berhasil disimpan")

st.subheader("Saldo Saat Ini")
st.write(f"Rp {st.session_state.saldo:,.0f}")

st.subheader("Riwayat Transaksi")

for item in st.session_state.riwayat:
    st.write(item)