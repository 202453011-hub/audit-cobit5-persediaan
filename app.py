
import streamlit as st
import pandas as pd
from datetime import datetime
from io import BytesIO

# ==========================================
# 1. KONFIGURASI HALAMAN
# ==========================================

st.set_page_config(
    page_title="Audit Sistem Informasi Persediaan",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Aplikasi Audit Sistem Informasi Persediaan Barang")
st.subheader("CV Sumber Makmur")
st.write("Audit menggunakan Framework COBIT 5")

st.info(
    "Aplikasi ini digunakan untuk membantu proses audit "
    "Sistem Informasi Persediaan Barang berdasarkan lima domain COBIT 5."
)

# ==========================================
# 2. DAFTAR PERTANYAAN AUDIT COBIT 5
# ==========================================

pertanyaan_audit = {
    "EDM": [
        "Apakah pimpinan melakukan pengawasan terhadap penggunaan sistem informasi persediaan?",
        "Apakah keputusan terkait sistem informasi sudah sesuai dengan kebutuhan perusahaan?",
        "Apakah perusahaan melakukan pemantauan terhadap risiko penggunaan sistem?",
        "Apakah manfaat penggunaan sistem informasi persediaan dievaluasi oleh pimpinan?",
        "Apakah manajemen memberikan arahan terkait pengelolaan sistem informasi?",
        "Apakah kinerja sistem informasi persediaan dievaluasi secara berkala?"
    ],

    "APO": [
        "Apakah perusahaan memiliki prosedur pengelolaan persediaan barang?",
        "Apakah perencanaan sistem informasi sudah sesuai dengan kebutuhan perusahaan?",
        "Apakah pembagian tugas dan tanggung jawab pengelolaan sistem sudah jelas?",
        "Apakah hak akses pengguna sistem telah diatur sesuai tugas masing-masing?",
        "Apakah perusahaan mengidentifikasi risiko dalam pengelolaan sistem?",
        "Apakah pengguna mendapatkan pelatihan dalam menggunakan sistem informasi?"
    ],

    "BAI": [
        "Apakah sistem informasi yang digunakan telah sesuai dengan kebutuhan perusahaan?",
        "Apakah pengujian dilakukan sebelum perubahan sistem diterapkan?",
        "Apakah dokumentasi sistem diperbarui ketika terjadi perubahan?",
        "Apakah data persediaan barang dijaga agar tetap konsisten?",
        "Apakah pemeriksaan dilakukan ketika terjadi pemindahan atau perubahan data?",
        "Apakah sistem memiliki penanganan ketika terjadi kesalahan?"
    ],

    "DSS": [
        "Apakah sistem digunakan untuk mencatat barang masuk dan barang keluar?",
        "Apakah perusahaan membandingkan stok fisik dengan stok yang tercatat di sistem?",
        "Apakah akses sistem dibatasi berdasarkan hak akses pengguna?",
        "Apakah perusahaan melakukan pencadangan (backup) data persediaan?",
        "Apakah terdapat prosedur penanganan ketika terjadi gangguan sistem?",
        "Apakah aktivitas pengguna dalam sistem dicatat dan dapat diperiksa?"
    ],

    "MEA": [
        "Apakah perusahaan memeriksa keakuratan data persediaan barang?",
        "Apakah laporan persediaan diperiksa secara berkala?",
        "Apakah perusahaan menindaklanjuti perbedaan antara stok fisik dan sistem?",
        "Apakah penggunaan sistem telah sesuai dengan prosedur perusahaan?",
        "Apakah hasil pemeriksaan atau audit didokumentasikan?",
        "Apakah tindak lanjut hasil evaluasi sistem dipantau?"
    ]
}

# ==========================================
# 3. FORMULIR IDENTITAS DAN AUDIT
# ==========================================

st.header("1. Identitas Auditor")

with st.form("form_audit"):

    nama_auditor = st.text_input("Nama Auditor")
    nim = st.text_input("NIM")
    perusahaan = st.text_input(
        "Nama Perusahaan",
        value="CV Sumber Makmur"
    )
    sistem = st.text_input(
        "Sistem yang Diaudit",
        value="Sistem Informasi Persediaan Barang"
    )

    st.divider()

    st.header("2. Kuesioner Audit COBIT 5")
    st.write(
        "Pilih jawaban sesuai kondisi yang ditemukan "
        "pada sistem informasi persediaan barang."
    )

    jawaban = {}

    for domain, daftar_pertanyaan in pertanyaan_audit.items():

        st.subheader(f"Domain {domain}")

        for nomor, pertanyaan in enumerate(
            daftar_pertanyaan, start=1
        ):

            kode = f"{domain}_{nomor}"

            jawaban[kode] = st.selectbox(
                f"{nomor}. {pertanyaan}",
                options=["Pilih jawaban", "Ya", "Tidak", "N/A"],
                key=kode
            )

    st.divider()

    tombol_submit = st.form_submit_button(
        "Proses Hasil Audit",
        use_container_width=True
    )

# ==========================================
# 4. PENGOLAHAN HASIL AUDIT
# ==========================================

if tombol_submit:

    if not nama_auditor.strip():
        st.error("Nama auditor harus diisi.")

    elif not nim.strip():
        st.error("NIM harus diisi.")

    elif not perusahaan.strip() or not sistem.strip():
        st.error("Nama perusahaan dan sistem yang diaudit harus diisi.")

    elif any(
        nilai == "Pilih jawaban"
        for nilai in jawaban.values()
    ):
        st.error("Semua pertanyaan harus diberikan jawaban.")

    else:

        data_audit = []

        for domain, daftar_pertanyaan in pertanyaan_audit.items():

            for nomor, pertanyaan in enumerate(
                daftar_pertanyaan, start=1
            ):

                kode = f"{domain}_{nomor}"

                data_audit.append({
                    "Domain": domain,
                    "Nomor": nomor,
                    "Pertanyaan": pertanyaan,
                    "Jawaban": jawaban[kode]
                })

        df_audit = pd.DataFrame(data_audit)

        # Menghitung jawaban yang valid
        jumlah_ya = (
            df_audit["Jawaban"] == "Ya"
        ).sum()

        jumlah_tidak = (
            df_audit["Jawaban"] == "Tidak"
        ).sum()

        jumlah_na = (
            df_audit["Jawaban"] == "N/A"
        ).sum()

        jumlah_valid = jumlah_ya + jumlah_tidak

        if jumlah_valid > 0:
            persentase_ya = (
                jumlah_ya / jumlah_valid
            ) * 100

            persentase_tidak = (
                jumlah_tidak / jumlah_valid
            ) * 100
        else:
            persentase_ya = 0
            persentase_tidak = 0

        # ==========================================
        # 5. PERHITUNGAN HASIL SETIAP DOMAIN
        # ==========================================

        hasil_domain = []

        for domain in pertanyaan_audit:

            df_domain = df_audit[
                df_audit["Domain"] == domain
            ]

            ya = (
                df_domain["Jawaban"] == "Ya"
            ).sum()

            tidak = (
                df_domain["Jawaban"] == "Tidak"
            ).sum()

            na = (
                df_domain["Jawaban"] == "N/A"
            ).sum()

            valid = ya + tidak

            if valid > 0:
                persentase = (ya / valid) * 100
            else:
                persentase = 0

            hasil_domain.append({
                "Domain": domain,
                "Jumlah Ya": ya,
                "Jumlah Tidak": tidak,
                "Jumlah N/A": na,
                "Persentase Ya (%)": round(
                    persentase, 2
                )
            })

        df_hasil_domain = pd.DataFrame(
            hasil_domain
        )

        # ==========================================
        # 6. MEMBUAT REKOMENDASI AUDIT
        # ==========================================

        rekomendasi = []

        for _, baris in df_hasil_domain.iterrows():

            domain = baris["Domain"]
            persentase = baris["Persentase Ya (%)"]

            if persentase >= 80:
                kondisi = "Baik"
                saran = (
                    "Pertahankan penerapan pengelolaan sistem "
                    "dan lakukan evaluasi secara berkala."
                )

            elif persentase >= 60:
                kondisi = "Cukup"
                saran = (
                    "Tingkatkan penerapan prosedur dan lakukan "
                    "perbaikan pada aspek yang belum terpenuhi."
                )

            else:
                kondisi = "Perlu Perbaikan"
                saran = (
                    "Perusahaan perlu melakukan evaluasi dan "
                    "perbaikan terhadap pengelolaan sistem "
                    "pada domain ini."
                )

            rekomendasi.append({
                "Domain": domain,
                "Persentase Ya (%)": persentase,
                "Kondisi": kondisi,
                "Rekomendasi": saran
            })

        df_rekomendasi = pd.DataFrame(
            rekomendasi
        )

        # ==========================================
        # 7. MENAMPILKAN HASIL AUDIT
        # ==========================================

        st.success("Hasil audit berhasil diproses!")

        st.header("3. Hasil Audit")

        st.write(f"**Nama Auditor:** {nama_auditor}")
        st.write(f"**NIM:** {nim}")
        st.write(f"**Perusahaan:** {perusahaan}")
        st.write(f"**Sistem:** {sistem}")
        st.write(
            f"**Tanggal Audit:** "
            f"{datetime.now().strftime('%d-%m-%Y %H:%M')}"
        )

        st.subheader("Ringkasan Hasil Audit")

        kolom1, kolom2, kolom3, kolom4 = st.columns(4)

        kolom1.metric("Jawaban Ya", jumlah_ya)
        kolom2.metric("Jawaban Tidak", jumlah_tidak)
        kolom3.metric("Jawaban N/A", jumlah_na)
        kolom4.metric(
            "Persentase Ya",
            f"{persentase_ya:.2f}%"
        )

        st.write(
            f"Persentase jawaban Ya: "
            f"{persentase_ya:.2f}%"
        )

        st.write(
            f"Persentase jawaban Tidak: "
            f"{persentase_tidak:.2f}%"
        )

        # ==========================================
        # 8. GRAFIK HASIL AUDIT
        # ==========================================

        st.header("4. Grafik Hasil Audit")

        grafik = df_hasil_domain.set_index(
            "Domain"
        )[["Persentase Ya (%)"]]

        st.bar_chart(grafik)

        # ==========================================
        # 9. MENAMPILKAN REKOMENDASI
        # ==========================================

        st.header("5. Rekomendasi Perbaikan")

        st.dataframe(
            df_rekomendasi,
            use_container_width=True,
            hide_index=True
        )

        # ==========================================
        # 10. DETAIL HASIL KUESIONER
        # ==========================================

        st.header("6. Detail Jawaban Audit")

        st.dataframe(
            df_audit,
            use_container_width=True,
            hide_index=True
        )

        # ==========================================
        # 11. EKSPOR HASIL AUDIT KE EXCEL
        # ==========================================

        output = BytesIO()

        with pd.ExcelWriter(
            output,
            engine="openpyxl"
        ) as writer:

            df_audit.to_excel(
                writer,
                sheet_name="Data Kuesioner",
                index=False
            )

            df_hasil_domain.to_excel(
                writer,
                sheet_name="Hasil Per Domain",
                index=False
            )

            df_rekomendasi.to_excel(
                writer,
                sheet_name="Rekomendasi",
                index=False
            )

            df_ringkasan = pd.DataFrame({
                "Keterangan": [
                    "Nama Auditor",
                    "NIM",
                    "Perusahaan",
                    "Sistem yang Diaudit",
                    "Jumlah Jawaban Ya",
                    "Jumlah Jawaban Tidak",
                    "Jumlah Jawaban N/A",
                    "Persentase Ya",
                    "Persentase Tidak"
                ],
                "Hasil": [
                    nama_auditor,
                    nim,
                    perusahaan,
                    sistem,
                    jumlah_ya,
                    jumlah_tidak,
                    jumlah_na,
                    f"{persentase_ya:.2f}%",
                    f"{persentase_tidak:.2f}%"
                ]
            })

            df_ringkasan.to_excel(
                writer,
                sheet_name="Ringkasan",
                index=False
            )

        output.seek(0)

        st.download_button(
            label="📥 Download Hasil Audit Excel",
            data=output.getvalue(),
            file_name="Hasil_Audit_COBIT5_CV_Sumber_Makmur.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        st.caption(
            "Catatan: Persentase pada aplikasi ini merupakan "
            "hasil perhitungan jawaban kuesioner, bukan nilai "
            "resmi capability level atau maturity level COBIT 5. "
            "Hasil audit tetap perlu didukung bukti pemeriksaan."
        )
