import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="PILAR-JKN | Employer Risk Intelligence",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- Theme ----------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');
    html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
    .stApp { background: #f4f7fb; }
    section[data-testid="stSidebar"] { background: #101d36; }
    section[data-testid="stSidebar"] * { color: #e8eefb !important; }
    .hero {
        background: linear-gradient(115deg, #102447 0%, #173d68 58%, #176b78 100%);
        border-radius: 22px; padding: 28px 30px; color: white; margin-bottom: 18px;
        box-shadow: 0 12px 28px rgba(18,42,76,.14);
    }
    .eyebrow { color:#9de5dc; font-size:11px; font-weight:800; letter-spacing:2px; text-transform:uppercase; }
    .hero h1 { font-family:'Manrope',sans-serif; font-size:30px; margin:8px 0 8px 0; color:white; font-weight:800; }
    .hero p { color:#d5e2f4; margin:0; font-size:14px; max-width:850px; }
    .hero-pill { display:inline-block; margin-top:16px; padding:6px 10px; border-radius:99px; background:rgba(255,255,255,.12); border:1px solid rgba(255,255,255,.17); font-size:11px; color:#e9f5ff; }
    .metric {
        background:white; border:1px solid #e3eaf3; border-radius:16px; padding:17px 18px;
        box-shadow: 0 4px 14px rgba(23,47,77,.035); min-height:122px;
    }
    .metric-label { color:#687891; font-size:11px; text-transform:uppercase; letter-spacing:1px; font-weight:800; }
    .metric-value { font-family:'Manrope',sans-serif; font-size:27px; font-weight:800; color:#172b4d; margin-top:8px; }
    .metric-foot { color:#73829a; font-size:11px; margin-top:5px; }
    .section-title { font-family:'Manrope',sans-serif; font-size:19px; font-weight:800; color:#152847; margin: 8px 0 2px; }
    .section-sub { color:#73829a; font-size:12px; margin-bottom:14px; }
    .panel { background:white; border:1px solid #e3eaf3; border-radius:16px; padding:18px 18px 12px 18px; }
    .mini-label { font-size:11px; color:#73829a; text-transform:uppercase; font-weight:800; letter-spacing:1px; }
    .big-number { font-size:22px; font-family:'Manrope',sans-serif; font-weight:800; color:#172b4d; }
    .tag { padding:4px 8px; border-radius:7px; font-size:10px; font-weight:800; display:inline-block; }
    .tag-high { background:#ffe8e7; color:#b42318; }
    .tag-med { background:#fff2d6; color:#925f00; }
    .tag-low { background:#e1f7ef; color:#087653; }
    .footnote { color:#8290a4; font-size:10px; line-height:1.5; }
    div[data-testid="stPlotlyChart"] { border-radius:12px; }
    .stTabs [data-baseweb="tab-list"] { gap:8px; }
    .stTabs [data-baseweb="tab"] { background:#e9eff7; border-radius:9px 9px 0 0; padding:8px 15px; }
    .stTabs [aria-selected="true"] { background:white !important; }
</style>
""", unsafe_allow_html=True)

# ---------- Synthetic data ----------
companies = pd.DataFrame([
    ["BU-1042","PT Aruna Logistik","Logistik",420,372,48,63,28.4,88, "Tinggi"],
    ["BU-1088","PT Sinar Pangan","Manufaktur",310,286,24,41,16.2,76, "Tinggi"],
    ["BU-1103","CV Mitra Niaga","Perdagangan",165,158,7,12,4.8,43, "Sedang"],
    ["BU-1121","PT Karya Digital","Teknologi",205,202,3,8,1.1,22, "Rendah"],
    ["BU-1134","PT Bumi Sejahtera","Konstruksi",580,521,59,74,36.7,91, "Tinggi"],
    ["BU-1150","PT Lintas Mandiri","Logistik",275,258,17,29,9.6,67, "Sedang"],
    ["BU-1172","CV Cipta Usaha","Perdagangan",98,96,2,5,0.7,18, "Rendah"],
    ["BU-1195","PT Sentosa Prima","Manufaktur",360,329,31,52,21.3,82, "Tinggi"],
    ["BU-1210","PT Nusa Kreatif","Jasa",145,139,6,16,3.2,48, "Sedang"],
    ["BU-1228","PT Andalan Teknik","Konstruksi",240,225,15,34,11.8,72, "Sedang"],
    ["BU-1241","PT Cakra Retail","Perdagangan",190,184,6,9,2.0,31, "Rendah"],
    ["BU-1266","PT Roda Utama","Logistik",335,301,34,58,24.6,86, "Tinggi"],
], columns=["ID Badan Usaha","Nama Badan Usaha","Sektor","Pekerja Referensi","Peserta JKN PPU","Gap Pekerja","Median Delay (hari)","Estimasi Exposure (Rp jt)","Skor Prioritas","Level Risiko"])

competitors = pd.DataFrame([
    ["Pemadanan data manual","Pencocokan data","Terbatas","Tidak terstandar","Rendah","Daftar mismatch"],
    ["Dashboard pelaporan umum","Monitoring KPI","Sedang","Ringkasan deskriptif","Rendah","Grafik agregat"],
    ["Rule-based mismatch alert","Deteksi selisih","Sedang","Aturan statis","Sedang","Alert per aturan"],
    ["PILAR-JKN (proposed)","Prioritas pemeriksaan","Lintas indikator","Pola berulang + confidence bukti","Tinggi*","Ranking + ringkasan bukti"],
], columns=["Pendekatan","Fokus","Lintas sumber","Prioritisasi","Explainability","Output utama"])

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown("## 🛡️ PILAR-JKN")
    st.caption("Employer Risk Intelligence")
    st.markdown("---")
    st.markdown("### Tampilan dashboard")
    page = st.radio("Pilih halaman", ["Ringkasan Risiko", "Perbandingan Pendekatan", "Detail Kasus"], index=0)
    st.markdown("---")
    st.markdown("### Filter data demo")
    sectors = ["Semua sektor"] + sorted(companies["Sektor"].unique().tolist())
    sector_filter = st.selectbox("Sektor usaha", sectors)
    risk_filter = st.multiselect("Level risiko", ["Tinggi", "Sedang", "Rendah"], default=["Tinggi", "Sedang", "Rendah"])
    st.markdown("---")
    st.caption("DEMO DATA • BUKAN DATA BPJS RIIL")
    st.caption("Seluruh angka, nama badan usaha, dan exposure pada dashboard ini adalah data sintetis untuk demonstrasi UI.")

filtered = companies.copy()
if sector_filter != "Semua sektor":
    filtered = filtered[filtered["Sektor"] == sector_filter]
if risk_filter:
    filtered = filtered[filtered["Level Risiko"].isin(risk_filter)]
else:
    filtered = filtered.iloc[0:0]

# ---------- Header ----------
st.markdown("""
<div class="hero">
  <div class="eyebrow">Healthkathon 2026 • Efisiensi Risiko Pemberi Kerja</div>
  <h1>From Data Discrepancies to Actionable Compliance Insights.</h1>
  <p>PILAR-JKN membantu petugas menyaring ketidaksesuaian data pekerja menjadi daftar kasus yang layak ditelaah terlebih dahulu — bukan menetapkan perusahaan bersalah secara otomatis.</p>
  <span class="hero-pill">● DEMO MODE — Synthetic data</span>
  <span class="hero-pill">Human-in-the-loop</span>
  <span class="hero-pill">Explainable prioritization</span>
</div>
""", unsafe_allow_html=True)

if page == "Ringkasan Risiko":
    st.markdown('<div class="section-title">Portfolio risk overview</div><div class="section-sub">Gambaran risiko badan usaha berdasarkan data demo yang dapat difilter.</div>', unsafe_allow_html=True)
    n_comp = len(filtered)
    workers_ref = int(filtered["Pekerja Referensi"].sum()) if n_comp else 0
    gap = int(filtered["Gap Pekerja"].sum()) if n_comp else 0
    exposure = float(filtered["Estimasi Exposure (Rp jt)"].sum()) if n_comp else 0
    high = int((filtered["Level Risiko"] == "Tinggi").sum()) if n_comp else 0

    cols = st.columns(4)
    metrics = [
        ("BADAN USAHA", f"{n_comp:,}", "Dalam filter saat ini"),
        ("GAP PEKERJA", f"{gap:,}", "Indikasi untuk diverifikasi"),
        ("POTENSI EXPOSURE", f"Rp {exposure:,.1f} jt", "Estimasi sintetis, bukan tagihan"),
        ("PRIORITAS TINGGI", f"{high:,}", "Bukan keputusan pelanggaran"),
    ]
    for c, (label, value, foot) in zip(cols, metrics):
        c.markdown(f'<div class="metric"><div class="metric-label">{label}</div><div class="metric-value">{value}</div><div class="metric-foot">{foot}</div></div>', unsafe_allow_html=True)

    st.markdown("")
    left, right = st.columns([1.05, 1])
    with left:
        st.markdown('<div class="panel"><div class="section-title">Komposisi level risiko</div><div class="section-sub">Pilih jenis visualisasi untuk mengeksplorasi data yang sama.</div>', unsafe_allow_html=True)
        chart_type = st.selectbox("Visualisasi", ["Donut chart", "Bar chart", "Tabel ringkasan"], key="risk_chart")
        risk_counts = filtered["Level Risiko"].value_counts().reindex(["Tinggi","Sedang","Rendah"], fill_value=0).rename_axis("Level Risiko").reset_index(name="Jumlah")
        if chart_type == "Donut chart":
            if len(risk_counts) and risk_counts["Jumlah"].sum():
                fig = px.pie(risk_counts, names="Level Risiko", values="Jumlah", hole=.63,
                             color="Level Risiko", color_discrete_map={"Tinggi":"#e05d5d","Sedang":"#f3b84b","Rendah":"#29a887"})
                fig.update_traces(textposition="inside", textinfo="label+value", hovertemplate="%{label}: %{value}<extra></extra>")
                fig.update_layout(showlegend=True, legend_title_text="", margin=dict(l=5,r=5,t=10,b=5), height=280,
                                  font=dict(family="DM Sans", color="#34445d"), paper_bgcolor="rgba(0,0,0,0)")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Tidak ada data untuk filter ini.")
        elif chart_type == "Bar chart":
            fig = px.bar(risk_counts, x="Level Risiko", y="Jumlah", color="Level Risiko",
                         color_discrete_map={"Tinggi":"#e05d5d","Sedang":"#f3b84b","Rendah":"#29a887"}, text="Jumlah")
            fig.update_layout(showlegend=False, margin=dict(l=5,r=5,t=10,b=5), height=280,
                              xaxis_title="", yaxis_title="Badan usaha", paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.dataframe(risk_counts, hide_index=True, use_container_width=True, height=280)
        st.markdown('</div>', unsafe_allow_html=True)

    with right:
        st.markdown('<div class="panel"><div class="section-title">Indikasi gap pekerja per badan usaha</div><div class="section-sub">Selisih pekerja referensi terhadap peserta JKN PPU pada data demo.</div>', unsafe_allow_html=True)
        bar_df = filtered.sort_values("Gap Pekerja", ascending=True).tail(8)
        if not bar_df.empty:
            fig2 = px.bar(bar_df, x="Gap Pekerja", y="Nama Badan Usaha", orientation="h", text="Gap Pekerja",
                          color="Level Risiko", color_discrete_map={"Tinggi":"#e05d5d","Sedang":"#f3b84b","Rendah":"#29a887"})
            fig2.update_layout(showlegend=True, legend_title_text="", margin=dict(l=5,r=5,t=10,b=5), height=280,
                               xaxis_title="Indikasi gap pekerja", yaxis_title="", paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("Tidak ada data untuk filter ini.")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-title">Priority queue</div><div class="section-sub">Daftar awal untuk membantu petugas memilih kasus yang perlu ditelaah lebih dulu.</div>', unsafe_allow_html=True)
    display = filtered.sort_values(["Skor Prioritas","Estimasi Exposure (Rp jt)"], ascending=False).copy()
    display = display.rename(columns={"Gap Pekerja":"Gap", "Median Delay (hari)":"Median delay (hari)", "Estimasi Exposure (Rp jt)":"Exposure (Rp jt)", "Skor Prioritas":"Skor demo"})
    st.dataframe(display[["ID Badan Usaha","Nama Badan Usaha","Sektor","Pekerja Referensi","Peserta JKN PPU","Gap","Median delay (hari)","Exposure (Rp jt)","Skor demo","Level Risiko"]],
                 use_container_width=True, hide_index=True, height=360,
                 column_config={
                     "Exposure (Rp jt)": st.column_config.NumberColumn(format="Rp %.1f jt"),
                     "Skor demo": st.column_config.ProgressColumn(min_value=0,max_value=100,format="%d"),
                 })
    st.markdown('<div class="footnote">Catatan: skor prioritas dan estimasi exposure di atas adalah data demo yang dibuat untuk memperagakan antarmuka. Ini bukan hasil model terlatih, bukan formula resmi BPJS, dan bukan kesimpulan kepatuhan.</div>', unsafe_allow_html=True)

elif page == "Perbandingan Pendekatan":
    st.markdown('<div class="section-title">Competitive landscape</div><div class="section-sub">Bandingkan jenis pendekatan yang mungkin ditemui dalam proses pemeriksaan. Ini adalah kerangka pembanding konseptual, bukan klaim bahwa semua sistem berikut digunakan oleh BPJS.</div>', unsafe_allow_html=True)
    st.info("Gunakan slide ini sebagai perbandingan pendekatan, bukan menuduh produk/instansi tertentu tidak memiliki fitur. Validasi dengan riset kompetitor sebelum pitch final.")
    view = st.radio("Mode tampilan", ["Tabel komparasi", "Visual matriks"], horizontal=True)
    if view == "Tabel komparasi":
        st.dataframe(competitors, use_container_width=True, hide_index=True, height=280)
    else:
        matrix = pd.DataFrame({
            "Pendekatan": ["Pemadanan manual","Dashboard umum","Rule-based alert","PILAR-JKN (proposed)"],
            "Lintas sumber": [1,2,2,3],
            "Prioritisasi": [1,1,2,3],
            "Pola berulang": [1,1,1,3],
            "Ringkasan bukti": [1,2,2,3],
        })
        melt = matrix.melt(id_vars="Pendekatan", var_name="Kapabilitas", value_name="Skor ilustratif")
        fig = px.imshow(
            matrix.set_index("Pendekatan").T,
            aspect="auto", color_continuous_scale=["#e8eef6","#77c9bf","#174b75"],
            labels=dict(x="Pendekatan", y="Kapabilitas", color="Skor")
        )
        fig.update_layout(height=360, margin=dict(l=10,r=10,t=10,b=10), paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)
        st.caption("Skala ilustratif: 1 = terbatas, 2 = sebagian, 3 = dirancang sebagai fokus. Bukan hasil benchmark empiris.")
    st.markdown("#### Diferensiasi yang ingin dibuktikan")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div class="metric"><div class="metric-label">BUKAN HANYA</div><div class="metric-value">Mismatch list</div><div class="metric-foot">Daftar selisih antar sumber data.</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="metric"><div class="metric-label">TAMBAHAN NILAI</div><div class="metric-value">Evidence + pattern</div><div class="metric-foot">Membedakan indikasi berulang dari kemungkinan noise administratif.</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="metric"><div class="metric-label">OUTPUT</div><div class="metric-value">Priority queue</div><div class="metric-foot">Urutan telaah dengan alasan yang dapat diperiksa manusia.</div></div>', unsafe_allow_html=True)
    st.markdown('<div class="footnote">*“Tinggi” pada explainability untuk PILAR-JKN berarti fitur tersebut dirancang untuk menyediakan alasan yang transparan. Implementasi aktual perlu dibuktikan melalui pengujian prototype.</div>', unsafe_allow_html=True)

else:
    st.markdown('<div class="section-title">Case review workspace</div><div class="section-sub">Pilih satu badan usaha untuk melihat bagaimana ringkasan kasus dapat ditampilkan kepada petugas.</div>', unsafe_allow_html=True)
    if not filtered.empty:
        chosen = st.selectbox("Badan usaha", filtered["Nama Badan Usaha"].tolist(), index=0)
        row = filtered[filtered["Nama Badan Usaha"] == chosen].iloc[0]
        a,b,c,d = st.columns(4)
        for col, lab, val in [
            (a,"ID BADAN USAHA",row["ID Badan Usaha"]),
            (b,"LEVEL DEMO",row["Level Risiko"]),
            (c,"SKOR PRIORITAS DEMO",f'{row["Skor Prioritas"]}/100'),
            (d,"EXPOSURE SINTETIS",f'Rp {row["Estimasi Exposure (Rp jt)"]:.1f} jt'),
        ]:
            col.markdown(f'<div class="metric"><div class="metric-label">{lab}</div><div class="metric-value" style="font-size:22px">{val}</div><div class="metric-foot">Bukan keputusan kepatuhan</div></div>', unsafe_allow_html=True)
        st.markdown("")
        left,right = st.columns([1,1])
        with left:
            st.markdown("#### Indikator kasus (contoh)")
            evidence = pd.DataFrame([
                ["Indikasi gap pekerja", int(row["Gap Pekerja"]), "Perlu pencocokan dan verifikasi"],
                ["Median delay registrasi", int(row["Median Delay (hari)"]), "Periksa tanggal efektif dan grace period"],
                ["Sumber data tersedia", 3, "Nilai contoh; cek kelengkapan aktual"],
            ], columns=["Indikator","Nilai demo","Tindak lanjut"])
            st.dataframe(evidence, hide_index=True, use_container_width=True)
        with right:
            st.markdown("#### Ringkasan untuk petugas")
            st.markdown(f"""
            <div class="panel">
              <div class="mini-label">Alasan masuk antrean telaah</div>
              <p style="color:#263b58;font-size:14px;line-height:1.7">
              • Terdapat indikasi selisih sekitar <b>{int(row["Gap Pekerja"])} pekerja</b> antara data referensi dan peserta JKN PPU.<br>
              • Median jeda registrasi pada simulasi adalah <b>{int(row["Median Delay (hari)"])} hari</b>.<br>
              • Estimasi exposure sintetis sebesar <b>Rp {row["Estimasi Exposure (Rp jt)"]:.1f} juta</b> perlu diverifikasi dengan formula dan data yang sah.
              </p>
              <div style="background:#fff2d6;color:#925f00;border-radius:8px;padding:10px;font-size:12px;font-weight:700">
              Rekomendasi: telaah dokumen pendukung. Jangan menyimpulkan pelanggaran hanya dari mismatch.
              </div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("#### Checklist verifikasi manusia")
        checks = st.columns(3)
        checks[0].checkbox("Pastikan identitas pekerja cocok", key="check1")
        checks[1].checkbox("Periksa periode sinkronisasi data", key="check2")
        checks[2].checkbox("Cocokkan bukti payroll/administrasi", key="check3")
    else:
        st.warning("Tidak ada badan usaha yang sesuai dengan filter sidebar.")

st.markdown("---")
st.markdown('<div class="footnote">PILAR-JKN • Prototype UI untuk diskusi dan demo Healthkathon 2026. Semua nama, skor, jumlah pekerja, jeda registrasi, dan estimasi exposure merupakan data sintetis. Dashboard ini tidak mengakses API atau model AI apa pun.</div>', unsafe_allow_html=True)
