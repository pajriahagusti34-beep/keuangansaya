elif menu == "➕ Tambah Transaksi":

    st.title("💸 Tambah Transaksi")

    with st.container():

        col1, col2 = st.columns(2)

        with col1:

            tanggal = st.date_input(
                "📅 Tanggal",
                date.today()
            )

            jenis = st.selectbox(
                "🔄 Jenis Transaksi",
                [
                    "Pemasukan",
                    "Pengeluaran"
                ]
            )

            periode = st.selectbox(
                "📆 Periode",
                [
                    "Harian",
                    "Bulanan"
                ]
            )

        with col2:

            metode = st.selectbox(
                "💳 Metode Pembayaran",
                [
                    "Tunai",
                    "Transfer",
                    "E-Wallet",
                    "QRIS",
                    "Kartu Debit"
                ]
            )

            nominal = st.number_input(
                "💰 Nominal (Rp)",
                min_value=0,
                step=1000
            )

        if jenis == "Pemasukan":

            kategori = st.selectbox(
                "📈 Kategori Pemasukan",
                [
                    "💼 Gaji",
                    "🎁 Bonus",
                    "💻 Freelance",
                    "📈 Investasi",
                    "🏪 Usaha",
                    "📦 Lainnya"
                ]
            )

        else:

            kategori = st.selectbox(
                "📉 Kategori Pengeluaran",
                [
                    "🍔 Makan & Minum",
                    "🛒 Belanja",
                    "🚗 Transportasi",
                    "🏠 Tagihan Rumah",
                    "📱 Pulsa & Internet",
                    "🏥 Kesehatan",
                    "📚 Pendidikan",
                    "🎮 Hiburan",
                    "🎁 Hadiah",
                    "📦 Lainnya"
                ]
            )

        catatan = st.text_area(
            "📝 Catatan"
        )

        if st.button("💖 Simpan Transaksi"):

            data_baru = {
                "Tanggal": tanggal,
                "Jenis": jenis,
                "Periode": periode,
                "Kategori": kategori,
                "Metode": metode,
                "Nominal": nominal,
                "Catatan": catatan
            }

            df = pd.concat(
                [df, pd.DataFrame([data_baru])],
                ignore_index=True
            )

            df.to_csv(FILE, index=False)

            st.success(
                "✅ Transaksi berhasil disimpan"
            )

            st.rerun()
