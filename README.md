# PILAR-JKN Streamlit Mockup

## Jalankan di VS Code
1. Install Python 3.10+ dan VS Code.
2. Extract ZIP ini, lalu buka folder `pilar_jkn_streamlit_mockup` di VS Code.
3. Buka terminal VS Code: **Terminal → New Terminal**.
4. Buat virtual environment (opsional tapi disarankan):
   - Windows: `py -m venv .venv` lalu `.venv\\Scripts\\activate`
   - macOS/Linux: `python3 -m venv .venv` lalu `source .venv/bin/activate`
5. Install dependensi:
   `pip install -r requirements.txt`
6. Jalankan:
   `streamlit run app.py`
7. Browser akan terbuka otomatis. Jika tidak, buka alamat lokal yang muncul di terminal, biasanya `http://localhost:8501`.

## Yang bisa dicoba
- Sidebar: pindah antara Ringkasan Risiko, Perbandingan Pendekatan, dan Detail Kasus.
- Filter sektor dan level risiko.
- Pada Ringkasan Risiko, ganti visualisasi komposisi risiko dari donut ke bar chart atau tabel.
- Pada Perbandingan Pendekatan, ganti tabel ke visual matriks.
- Pada Detail Kasus, pilih badan usaha dan checklist langkah verifikasi.

## Catatan penting
Semua nama badan usaha, angka, skor, dan exposure adalah data sintetis/fiktif untuk mockup UI. Tidak ada model AI yang dipanggil. Skor bukan formula resmi BPJS dan bukan hasil eksperimen empiris. Gunakan data resmi/riset tervalidasi sebelum membuat klaim kompetitor di pitch deck.
