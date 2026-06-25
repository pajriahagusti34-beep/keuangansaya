# ================= HITUNG DATA =================

if len(df) == 0:
    pemasukan = 0
    pengeluaran = 0
else:
    pemasukan = df[df["Jenis"]=="Pemasukan"]["Nominal"].sum()
    pengeluaran = df[df["Jenis"]=="Pengeluaran"]["Nominal"].sum()

sisa_uang = pemasukan - pengeluaran

# kategori khusus
makan = df[df["Kategori"].astype(str).str.contains("Makan", na=False)]["Nominal"].sum()

minum = df[df["Kategori"].astype(str).str.contains("Minum", na=False)]["Nominal"].sum()

belanja = df[df["Kategori"].astype(str).str.contains("Belanja", na=False)]["Nominal"].sum()

transportasi = df[df["Kategori"].astype(str).str.contains("Transportasi", na=False)]["Nominal"].sum()
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
        elif menu == "➕ Tambah Transaksi":

    st.title("➕ Tambah Transaksi")

    tanggal = st.date_input("Tanggal")

    periode = st.selectbox(
        "Periode",
        ["Harian","Bulanan"]
    )

    jenis = st.selectbox(
        "Jenis",
        ["Pemasukan","Pengeluaran"]
    )

    if jenis == "Pemasukan":

        kategori = st.selectbox(
            "Kategori",
            [
                "Gaji",
                "Bonus",
                "Freelance",
                "Investasi",
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
                "Lainnya"
            ]
        )

    nominal = st.number_input(
        "Nominal (Rp)",
        min_value=0,
        step=1000
    )

    catatan = st.text_area("Catatan")

    if st.button("💾 Simpan"):

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

        st.success("Data berhasil disimpan")
