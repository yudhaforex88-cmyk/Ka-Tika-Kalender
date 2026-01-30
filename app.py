import streamlit as st
import datetime
import pytz
import calendar
import math
from astral import LocationInfo
from astral.sun import sun

# ==========================================
# 1. MODUL JANTUNG (ASTRONOMI & WAKTU)
# ==========================================
class KaTikaAstronomy:
    def __init__(self):
        # Koordinat Denpasar
        self.location = LocationInfo("Denpasar", "Indonesia", "Asia/Makassar", -8.6705, 115.2126)
        self.tz = pytz.timezone("Asia/Makassar")
        # ANCHOR: 19 Juli 2020 (Redite Paing Sinta)
        self.anchor_date = datetime.date(2020, 7, 19)

    def get_dina_status(self, check_time):
        if check_time.tzinfo is None: check_time = self.tz.localize(check_time)
        else: check_time = check_time.astimezone(self.tz)
        current_date = check_time.date()
        
        # Hitung Hari Fisik Berlalu (rahina_counter)
        days_passed = (current_date - self.anchor_date).days
        dina_global = (days_passed // 3) + 1
        dina_display = ((dina_global - 1) % 14) + 1
        
        # Hitung Posisi Lintang Matahari (LU/LS)
        day_of_year = current_date.timetuple().tm_yday
        declination = 23.45 * math.sin(math.radians(360/365 * (284 + day_of_year)))
        posisi_ls = f"{abs(round(declination, 2))}° {'LU' if declination > 0 else 'LS'}"

        # Rentang Tri-Dina
        urutan_tri_dina = (days_passed % 3) + 1 
        start_date = current_date - datetime.timedelta(days=(urutan_tri_dina - 1))
        range_str = f"{start_date.strftime('%d %b')} - {(start_date + datetime.timedelta(days=2)).strftime('%d %b %Y')}"

        return {
            "dina_id_global": dina_global, "dina_id_display": dina_display,
            "rahina_counter": days_passed, "posisi_ls": posisi_ls,
            "range_masehi": range_str, "current_date": current_date
        }

# ==========================================
# 2. MODUL KALKULATOR (WUKU & WEWARAN)
# ==========================================
class KaTikaCalendar:
    def __init__(self):
        self.sapta = ["Redite", "Soma", "Anggara", "Buda", "Wraspati", "Sukra", "Saniscara"]
        self.panca = ["Umanis", "Paing", "Pon", "Wage", "Kliwon"]
        self.wuku_list = ["Sinta", "Landep", "Ukir", "Kulantir", "Tolu", "Gumbreg", "Wariga", "Warigadean", "Julungwangi", "Sungsang", "Dungulan", "Kuningan", "Langkir", "Medangsia", "Pujut", "Pahang", "Krulut", "Merakih", "Tambir", "Medangkungan", "Matal", "Uye", "Menail", "Prangbakat", "Bala", "Ugu", "Wayang", "Klawu", "Dukut", "Watugunung"]

    def get_calendar(self, rahina_cnt):
        idx_wuku = (rahina_cnt // 7) % 30
        return {
            "sapta": self.sapta[rahina_cnt % 7],
            "panca": self.panca[(1 + rahina_cnt) % 5],
            "wuku": self.wuku_list[idx_wuku],
            "wuku_index": idx_wuku
        }

class KaTikaWewaran:
    def __init__(self):
        self.tri_wara = ["Kajeng", "Pasah", "Beteng", "Pasah"]
        self.urip_sapta = [5, 4, 3, 7, 8, 6, 9] 
        self.urip_panca = [5, 9, 7, 4, 8]
        self.dasa_wara = ["Pandita", "Pati", "Suka", "Duka", "Sri", "Manuh", "Manusa", "Raja", "Dewa", "Raksasa"]
        
        # Database Watak
        self.watak_sapta = [
            "Redite (Matahari): Berwibawa, Pemimpin, Keras Kemauan.",
            "Soma (Bulan): Lembut, Tekun, Mudah Berubah.",
            "Anggara (Api): Pemberani, Panas Hati, Suka Tantangan.",
            "Buda (Bumi): Sabar, Tenang, Subur Rejekinya.",
            "Wraspati (Langit): Cerdas, Bijaksana, Berita-cita Tinggi.",
            "Sukra (Bintang): Romantis, Menyenangkan, Suka Seni.",
            "Saniscara (Angin): Teguh Pendirian, Pekerja Keras, Penyendiri."
        ]
        self.watak_panca = [
            "Umanis: Penyayang, Banyak Bicara, Mudah Tersinggung.",
            "Paing: Rajin, Keras Hati, Tidak Mau Kalah.",
            "Pon: Bijaksana, Suka Pamer, Tutur Kata Halus.",
            "Wage: Setia, Berpikir Panjang, Kaku.",
            "Kliwon: Spiritual, Pandai Merangkai Kata, Pemikir."
        ]
        # Database Lintang (Sampel)
        self.lintang_map = {
            (0,0): ("Kala Sungsang", "Pemberani & Rejeki Lancar"), 
            (1,4): ("Pedati", "Pekerja Keras & Hemat"), 
            (5,4): ("Udang", "Ulet & Hemat"),
            (0,4): ("Gajah Mina", "Kuat Agama & Pikiran Suci"),
            (3,1): ("Gajah", "Setia & Penolong")
        }

    def get_wewaran_lengkap(self, rahina_cnt):
        idx_s = rahina_cnt % 7; idx_p = (1 + rahina_cnt) % 5
        total_urip = self.urip_sapta[idx_s] + self.urip_panca[idx_p]
        lintang = self.lintang_map.get((idx_s, idx_p), ("Lumbung", "Hidup Makmur & Sederhana"))
        return {
            "tri": self.tri_wara[rahina_cnt % 4], "total_urip": total_urip,
            "dasa": self.dasa_wara[(total_urip - 1) % 10], "sapta_idx": idx_s, "panca_idx": idx_p,
            "watak_sapta": self.watak_sapta[idx_s], "watak_panca": self.watak_panca[idx_p],
            "lintang_nama": lintang[0], "lintang_watak": lintang[1]
        }
# ==========================================
# 3. MODUL SASIH & RAINAN (PARIPURNA)
# ==========================================
class KaTikaSasih:
    def __init__(self):
        self.nama_sasih = ["Kasa", "Karo", "Katiga", "Kapat", "Kalima", "Kanem", "Kapitu", "Kaulu", "Kasanga", "Kadasa"]

    def get_sasih_info(self, dina_global, wuku_idx):
        sasih_idx = min(wuku_idx // 3, 9); label = self.nama_sasih[sasih_idx]
        local_pos = ((dina_global - 1) % 14) + 1
        
        status = "PURNAMA" if 6 <= local_pos <= 10 else "TILEM" if local_pos <= 5 else "PANGLONG"
        status_wariga = "TUNGGAK (Utama)" if (wuku_idx % 3) != 2 else "NAMPIH (Transisi)"
        
        return {"sasih_label": label, "status": status, "dina_lokal": local_pos, "status_wariga": status_wariga}

class KaTikaRainan:
    def get_rainan(self, wuku_idx, sapta_idx, panca_idx, tri_nama):
        res = []
        # Siklus Galungan
        if wuku_idx == 9: # Sungsang
            if sapta_idx == 4 and panca_idx == 3: res.append("🙏 SUGIHAN JAWA")
            if sapta_idx == 5 and panca_idx == 4: res.append("🙏 SUGIHAN BALI")
        if wuku_idx == 10: # Dungulan
            if sapta_idx == 0: res.append("PENYEKEBAN")
            if sapta_idx == 1: res.append("PENYAJAAN")
            if sapta_idx == 2: res.append("PENAMPAHAN")
            if sapta_idx == 3 and panca_idx == 4: res.append("🌟 GALUNGAN")
            if sapta_idx == 4: res.append("MANIS GALUNGAN")
        if wuku_idx == 11 and sapta_idx == 6 and panca_idx == 4: res.append("🌟 KUNINGAN")
        if wuku_idx == 15 and sapta_idx == 3 and panca_idx == 4: res.append("🔒 PEGATWAKAN")
        
        # Saraswati & Pagerwesi
        if wuku_idx == 29 and sapta_idx == 6 and panca_idx == 0: res.append("📚 SARASWATI")
        if wuku_idx == 0 and sapta_idx == 3 and panca_idx == 4: res.append("🌟 PAGERWESI")
        
        # Rainan Rutin
        if sapta_idx == 6 and panca_idx == 4: res.append("🔔 TUMPEK")
        if tri_nama == "Kajeng" and panca_idx == 4: res.append("👻 KAJENG KLIWON")
        if sapta_idx == 2 and panca_idx == 4: res.append("❤️ ANGGARA KASIH")
        if sapta_idx == 3 and panca_idx == 4 and wuku_idx not in [10, 15, 0]: res.append("🙏 BUDA KLIWON")
        
        return res

# ==========================================
# 4. MODUL KHUSUS: PENCARIAN TANGGAL (TERPISAH)
# ==========================================
class KaTikaPencarian:
    def __init__(self, astro, cal, wew, sas):
        self.astro = astro; self.cal = cal; self.wew = wew; self.sas = sas

    def analisis_tanggal(self, target_date):
        delta_hari = (target_date - self.astro.anchor_date).days
        c_data = self.cal.get_calendar(delta_hari)
        w_data = self.wew.get_wewaran_lengkap(delta_hari)
        s_data = self.sas.get_sasih_info((delta_hari // 3) + 1, c_data['wuku_index'])
        
        day_of_year = target_date.timetuple().tm_yday
        declination = 23.45 * math.sin(math.radians(360/365 * (284 + day_of_year)))
        posisi_ls = f"{abs(round(declination, 2))}° {'LU' if declination > 0 else 'LS'}"
        
        urutan_tri_dina = (delta_hari % 3) + 1 
        start_date = target_date - datetime.timedelta(days=(urutan_tri_dina - 1))
        range_str = f"{start_date.strftime('%d %b')} - {(start_date + datetime.timedelta(days=2)).strftime('%d %b %Y')}"

        return {
            "tanggal_masehi": target_date.strftime("%d %B %Y"),
            "range_tri_dina": range_str,
            "sapta": c_data['sapta'], "panca": c_data['panca'], "tri_wara": w_data['tri'],
            "wuku": c_data['wuku'], "urip": w_data['total_urip'],
            "sasih": s_data['sasih_label'], "sasih_status": s_data['status_wariga'], "fase_bulan": s_data['status'],
            "posisi_matahari": posisi_ls
        }
# ==========================================
# 5. MODUL ANALISIS (DEWASA AYU & OTONAN)
# ==========================================
class KaTikaPadewasan:
    def __init__(self, cal, wew, astro):
        self.cal = cal; self.wew = wew; self.astro = astro
        self.hari_indo = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
        self.bulan_indo = ["", "Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]

    def is_uncal_balung(self, wuku_idx, sapta_idx):
        # Range Wuku Dungulan (10) s.d. Pahang (15)
        if wuku_idx < 10 or wuku_idx > 15: return False
        if wuku_idx == 10 and sapta_idx < 3: return False 
        if wuku_idx == 15 and sapta_idx > 3: return False 
        return True

    def get_usaha_match(self, jenis_usaha, sapta_idx):
        map_usaha = {
            "Emas, Perhiasan, Logam Mulia": [0], # Redite
            "Sayur, Minuman, Barang Cair": [1],  # Soma
            "Besi, Alat Masak, Elektronik": [2], # Anggara
            "Sembako, Kelontong, Umum": [3],     # Buda
            "Pakaian, Tekstil, Buku": [4],       # Wraspati
            "Kosmetik, Seni, Hiburan": [5],      # Sukra
            "Properti, Tanah, Ternak, Bangunan": [6] # Saniscara
        }
        return sapta_idx in map_usaha.get(jenis_usaha, [])

    def find_dewasa_yearly(self, category, start_date, sub_category=None):
        results = []
        # Scan 1 Tahun (365 Hari) - FILTER KETAT (GOOD DAYS ONLY)
        for i in range(1, 366):
            target_date = start_date + datetime.timedelta(days=i)
            cnt = (target_date - self.astro.anchor_date).days
            c = self.cal.get_calendar(cnt); w = self.wew.get_wewaran_lengkap(cnt)
            wuku_idx = c['wuku_index']; idx_ingkel = wuku_idx % 6
            
            is_good = False; label = ""; alasan = ""
            
            # 1. NIKAH
            if category == "nikah":
                if not self.is_uncal_balung(wuku_idx, w['sapta_idx']) and idx_ingkel != 0:
                    score = 0
                    if w['tri'] == "Beteng": score += 1
                    if w['panca_idx'] == 4: score += 1
                    if score >= 2: is_good = True; label = "✅ BAIK"; alasan = "Energi menyatukan & Bebas Uncal"
            
            # 2. TANI
            elif category == "tani":
                if idx_ingkel not in [4, 5]: 
                    if w['sapta_idx'] == 1: is_good=True; label="✅ BAIK (UMBI)"; alasan="Soma (Bulan)"
                    elif w['sapta_idx'] == 6: is_good=True; label="✅ BAIK (GANTUNG)"; alasan="Saniscara"
            
            # 3. LAUT
            elif category == "laut":
                if idx_ingkel != 2: 
                    if w['tri'] == "Pasah": is_good=True; label="🌟 UTAMA"; alasan="Pasah (Arus Lancar)"
            
            # 4. USAHA
            elif category == "usaha":
                if self.get_usaha_match(sub_category, w['sapta_idx']):
                    if w['tri'] != "Kajeng": is_good=True; label="✅ COCOK"; alasan=f"Elemen {c['sapta']} selaras"

            if is_good:
                tgl_str = f"{self.hari_indo[target_date.weekday()]}, {target_date.day} {self.bulan_indo[target_date.month]} {target_date.year}"
                results.append({"Tanggal Masehi": tgl_str, "Wuku": c['wuku'], "Wewaran": f"{c['sapta']} {c['panca']}", "Status": label, "Keterangan": alasan})
        return results

class KaTikaOtonan:
    def __init__(self, astro, cal, wew, sasih):
        self.astro = astro; self.cal = cal; self.wew = wew; self.sasih = sasih

    def hitung(self, tgl):
        cnt = (tgl - self.astro.anchor_date).days
        c = self.cal.get_calendar(cnt)
        w = self.wew.get_wewaran_lengkap(cnt)
        s = self.sasih.get_sasih_info((cnt // 3) + 1, c['wuku_index'])
        
        hari_ini = datetime.date.today()
        sisa = 210 - ((hari_ini - tgl).days % 210)
        
        return {
            "weton_text": f"{c['sapta']} {c['panca']} {c['wuku']}", 
            "urip": w['total_urip'],
            "tri_wara": w['tri'], "dasa_wara": w['dasa'], 
            "lintang": w['lintang_nama'], "lintang_desc": w['lintang_watak'],
            "sasih": s['sasih_label'], "sasih_status": s['status_wariga'],
            "watak_hari": w['watak_sapta'], "watak_pasar": w['watak_panca'], 
            "next_otonan": hari_ini + datetime.timedelta(days=sisa)
        }
# ==========================================
# 6. DASHBOARD UI (MOBILE & DARK MODE)
# ==========================================
st.set_page_config(page_title="Ka-Tika Wangsa Agra", page_icon="🔆", layout="centered")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Inter:wght@300;400;600&display=swap');
    
    .stApp { background-color: #0e1117; } /* Dark BG */
    
    /* HEADER */
    .header-box { text-align: center; font-family: 'Cinzel', serif; padding: 15px 0; margin-bottom: 10px; }
    .header-small { font-size: 10px; letter-spacing: 3px; color: #bfa15f; text-transform: uppercase; }
    .header-mid { font-size: 32px; font-weight: 700; color: #e0e0e0; margin: 5px 0; line-height: 1.2; }
    .header-sub { font-size: 12px; letter-spacing: 4px; color: #8b7355; margin-top: -5px; }
    
    /* HERO SECTION */
    .hero-container { text-align: center; padding: 20px 0; }
    .tri-panca { font-size: 16px; text-align: center; color: #9e9e9e; letter-spacing: 2px; font-family: 'Inter', sans-serif; text-transform: uppercase; margin-bottom: 5px; }
    .sapta-wara { font-size: 58px; font-weight: 800; text-align: center; color: #ffffff; line-height: 1; margin: 0; font-family: 'Inter', sans-serif; text-shadow: 0 4px 10px rgba(0,0,0,0.5); }
    .dina-date { text-align: center; color: #bfa15f; font-size: 12px; font-style: italic; margin-top: 10px; }
    
    /* WIDGETS FLEXBOX */
    .widget-container { display: flex; gap: 10px; margin-top: 20px; justify-content: center; }
    .widget-box { background: #1c1f26; border: 1px solid #333; border-radius: 12px; padding: 15px 10px; text-align: center; flex: 1; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
    .widget-icon { font-size: 24px; margin-bottom: 5px; }
    .widget-label { font-size: 9px; color: #8b7355; text-transform: uppercase; letter-spacing: 1px; }
    .widget-val { font-size: 13px; font-weight: 600; color: #e0e0e0; margin-top: 2px; }
    
    /* NOTIF */
    .rainan-notif { background: rgba(30, 81, 40, 0.9); color: #a5d6a7; padding: 10px; border-radius: 8px; text-align: center; font-weight: 600; font-size: 14px; border: 1px solid #2e7d32; margin: 15px 0; }
    
    /* TABS */
    .stTabs [data-baseweb="tab-list"] { gap: 2px; }
    .stTabs [data-baseweb="tab"] { height: 40px; background-color: #0e1117; color: #9e9e9e; font-size: 12px; padding: 0 10px; }
    .stTabs [aria-selected="true"] { background-color: #1c1f26; color: #bfa15f; border-bottom: 2px solid #bfa15f; }
</style>
""", unsafe_allow_html=True)

# INIT ENGINES
astro = KaTikaAstronomy(); cal = KaTikaCalendar(); wew = KaTikaWewaran()
sas = KaTikaSasih(); rai = KaTikaRainan()
dew = KaTikaPadewasan(cal, wew, astro); oto = KaTikaOtonan(astro, cal, wew, sas)
search_engine = KaTikaPencarian(astro, cal, wew, sas)

# REALTIME DATA
t_now = datetime.datetime.now(astro.tz)
dina = astro.get_dina_status(t_now)
c_d = cal.get_calendar(dina['rahina_counter']); w_d = wew.get_wewaran_lengkap(dina['rahina_counter'])
s_d = sas.get_sasih_info(dina['dina_id_global'], c_d['wuku_index'])
rains = rai.get_rainan(c_d['wuku_index'], w_d['sapta_idx'], w_d['panca_idx'], w_d['tri'])

# HEADER
st.markdown(f'''
<div class="header-box">
    <div class="header-small">KALENDER</div>
    <div class="header-mid">KA-TIKA</div>
    <div class="header-sub">WANGSA AGRA</div>
</div>
''', unsafe_allow_html=True)

if rains: st.markdown(f'<div class="rainan-notif">🔔 {" • ".join(rains)}</div>', unsafe_allow_html=True)

# HERO SECTION
st.markdown(f'''
<div class="hero-container">
    <div class="tri-panca">{w_d["tri"]} — {c_d["panca"]}</div>
    <div class="sapta-wara">{c_d["sapta"].upper()}</div>
    <div class="dina-date">{dina["range_masehi"]}</div>
</div>
''', unsafe_allow_html=True)

# WIDGETS
st.markdown(f"""
<div class="widget-container">
    <div class="widget-box"><div class="widget-icon">🌙</div><div class="widget-label">Fase Bulan</div><div class="widget-val">{s_d["status"]}</div></div>
    <div class="widget-box"><div class="widget-icon">☀️</div><div class="widget-label">Lintang</div><div class="widget-val">{dina["posisi_ls"]}</div></div>
    <div class="widget-box"><div class="widget-icon">📅</div><div class="widget-label">Sasih</div><div class="widget-val">{s_d["sasih_label"]}</div></div>
</div>
""", unsafe_allow_html=True)

# TABS
st.markdown("<br>", unsafe_allow_html=True)
tab_h, tab_s, tab_w, tab_d, tab_r = st.tabs(["🏠 Info", "🔍 Cari", "👶 Weton", "🌺 Dewasa", "📅 Rainan"])

with tab_h:
    st.markdown("---")
    c1, c2, c3 = st.columns(3)
    c1.metric("Wuku", c_d['wuku']); c2.metric("Urip", w_d['total_urip']); c3.metric("Dina", f"Ke-{s_d['dina_lokal']}")
    st.info(f"**Posisi Sasih:** {s_d['status_wariga']}")

with tab_s:
    st.caption("Pilih tanggal target:")
    ts_in = st.date_input("Target", datetime.date.today(), label_visibility="collapsed")
    if st.button("Analisis", type="primary", use_container_width=True):
        res_s = search_engine.analisis_tanggal(ts_in)
        st.markdown(f"""
        <div style="background:#1c1f26; border:1px solid #333; border-radius:10px; padding:15px; text-align:center; margin-top:10px;">
            <div style="color:#bfa15f; font-size:10px;">{res_s['tanggal_masehi']}</div>
            <h2 style="color:#fff; margin:5px 0;">{res_s['sapta'].upper()}</h2>
            <div style="color:#ccc;">{res_s['tri_wara']} - {res_s['panca']}</div>
            <hr style="border-color:#444;">
            <div style="color:#fff;">{res_s['wuku']} | Sasih {res_s['sasih']}</div>
        </div>
        """, unsafe_allow_html=True)

with tab_w:
    st.caption("Tanggal Lahir:")
    t_l = st.date_input("Lahir", datetime.date(1995, 1, 1), label_visibility="collapsed")
    if st.button("Cek Weton", type="primary", use_container_width=True):
        res = oto.hitung(t_l)
        st.markdown(f"""
        <div style="background:#261c21; border:1px solid #5a2e45; border-radius:10px; padding:15px; text-align:center; margin-bottom:10px;">
            <h3 style="color:#e91e63; margin:0;">{res['weton_text']}</h3>
            <small style="color:#ccc;">Urip: {res['urip']} | {res['lintang']}</small>
        </div>
        """, unsafe_allow_html=True)
        st.warning(f"**Watak Hari:** {res['watak_hari']}")
        st.warning(f"**Watak Pasaran:** {res['watak_pasar']}")

with tab_d:
    st.caption("Cari hari baik (1 Tahun):")
    kp = st.selectbox("Keperluan", ["💍 Pernikahan", "💰 Memulai Usaha", "🌾 Pertanian", "🎣 Melaut"], label_visibility="collapsed")
    sub_cat = None
    if "Usaha" in kp:
        sub_cat = st.selectbox("Dagangan", ["Emas, Perhiasan, Logam Mulia", "Sayur, Minuman, Barang Cair", "Besi, Alat Masak, Elektronik", "Sembako, Kelontong, Umum", "Pakaian, Tekstil, Buku", "Kosmetik, Seni, Hiburan", "Properti, Tanah, Ternak, Bangunan"])
    if st.button("Scan Hari Baik", type="primary", use_container_width=True):
        code = "nikah"
        if "Pertanian" in kp: code = "tani"
        elif "Melaut" in kp: code = "laut"
        elif "Usaha" in kp: code = "usaha"
        h = dew.find_dewasa_yearly(code, datetime.date.today(), sub_cat)
        if h: st.dataframe(h, use_container_width=True, hide_index=True)
        else: st.error("Belum ada hari baik UTAMA terdekat.")

with tab_r:
    if rains: 
        for r in rains: st.success(f"• {r}")
    else: st.caption("Tidak ada hari raya besar hari ini.")

