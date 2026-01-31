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
        # Konfigurasi Lokasi (Denpasar)
        self.location = LocationInfo("Denpasar", "Indonesia", "Asia/Makassar", -8.6705, 115.2126)
        self.tz = pytz.timezone("Asia/Makassar")
        
        # ANCHOR POINT: 19 Juli 2020 (Redite Paing Sinta)
        # Ini adalah titik nol perhitungan matematis sistem ini.
        self.anchor_date = datetime.date(2020, 7, 19)

    def get_dina_status(self, check_time):
        # Normalisasi Zona Waktu
        if check_time.tzinfo is None: 
            check_time = self.tz.localize(check_time)
        else: 
            check_time = check_time.astimezone(self.tz)
        
        current_date = check_time.date()
        
        # Hitung Rahina Counter (Total hari berlalu sejak Anchor)
        # Variabel ini adalah kunci utama untuk semua modul lain.
        days_passed = (current_date - self.anchor_date).days
        
        # Hitung Siklus Global (untuk Fase Bulan)
        dina_global = (days_passed // 3) + 1
        dina_display = ((dina_global - 1) % 14) + 1
        
        # Hitung Posisi Matahari (Deklinasi)
        day_of_year = current_date.timetuple().tm_yday
        declination = 23.45 * math.sin(math.radians(360/365 * (284 + day_of_year)))
        posisi_ls = f"{abs(round(declination, 2))}° {'LU' if declination > 0 else 'LS'}"

        # Hitung Rentang Tri-Dina (Pasaran 3 Hari)
        urutan_tri_dina = (days_passed % 3) + 1 
        start_date = current_date - datetime.timedelta(days=(urutan_tri_dina - 1))
        range_str = f"{start_date.strftime('%d %b')} - {(start_date + datetime.timedelta(days=2)).strftime('%d %b %Y')}"

        return {
            "dina_id_global": dina_global, 
            "dina_id_display": dina_display,
            "rahina_counter": days_passed, 
            "posisi_ls": posisi_ls,
            "range_masehi": range_str, 
            "current_date": current_date
        }
# ==========================================
# 2. MODUL KALKULATOR (WUKU)
# ==========================================
class KaTikaCalendar:
    def __init__(self):
        self.sapta = ["Redite", "Soma", "Anggara", "Buda", "Wraspati", "Sukra", "Saniscara"]
        self.panca = ["Umanis", "Paing", "Pon", "Wage", "Kliwon"]
        self.wuku_list = ["Sinta", "Landep", "Ukir", "Kulantir", "Tolu", "Gumbreg", "Wariga", "Warigadean", "Julungwangi", "Sungsang", "Dungulan", "Kuningan", "Langkir", "Medangsia", "Pujut", "Pahang", "Krulut", "Merakih", "Tambir", "Medangkungan", "Matal", "Uye", "Menail", "Prangbakat", "Bala", "Ugu", "Wayang", "Klawu", "Dukut", "Watugunung"]

    def get_calendar(self, rahina_cnt):
        # Hitung Wuku (Siklus 210 hari / 30 wuku)
        idx_wuku = (rahina_cnt // 7) % 30
        return {
            "sapta": self.sapta[rahina_cnt % 7],
            "panca": self.panca[(1 + rahina_cnt) % 5],
            "wuku": self.wuku_list[idx_wuku],
            "wuku_index": idx_wuku
        }

# ==========================================
# 3. MODUL WEWARAN LENGKAP (LOGIKA RESET)
# ==========================================
class KaTikaWewaran:
    def __init__(self):
        # Database Nama Wewaran
        self.eka_wara = ["Luang", "Tungle"]
        self.dwi_wara = ["Menga", "Pepet"]
        self.tri_wara = ["Pasah", "Beteng", "Kajeng"]
        self.catur_wara = ["Sri", "Laba", "Jaya", "Menala"]
        self.panca_wara = ["Umanis", "Paing", "Pon", "Wage", "Kliwon"]
        self.sad_wara = ["Tungleh", "Aryang", "Urukung", "Paniron", "Was", "Maulu"]
        self.sapta_wara = ["Redite", "Soma", "Anggara", "Buda", "Wraspati", "Sukra", "Saniscara"]
        self.asta_wara = ["Sri", "Indra", "Guru", "Yama", "Ludra", "Brahma", "Kala", "Uma"]
        self.sanga_wara = ["Dangu", "Jangur", "Gigis", "Nohan", "Ogan", "Erangan", "Urungan", "Tulus", "Dadi"]
        self.dasa_wara = ["Pandita", "Pati", "Suka", "Duka", "Sri", "Manuh", "Manusa", "Raja", "Dewa", "Raksasa"]

        # Database Urip (Nilai Angka)
        self.urip_sapta = [5, 4, 3, 7, 8, 6, 9] 
        self.urip_panca = [5, 9, 7, 4, 8]
        
        # Database Narasi Watak
        self.watak_sapta = ["Redite: Pemimpin, Berwibawa", "Soma: Lembut, Tekun", "Anggara: Pemberani, Panas", "Buda: Sabar, Subur", "Wraspati: Bijaksana, Cerdas", "Sukra: Romantis, Seni", "Saniscara: Teguh, Pekerja Keras"]
        self.watak_panca = ["Umanis: Penyayang, Banyak Bicara", "Paing: Rajin, Keras Hati", "Pon: Bijaksana, Suka Pamer", "Wage: Setia, Kaku", "Kliwon: Spiritual, Pandai Bicara"]
        
        # Database Lintang (Sampel)
        self.lintang_map = {(0,0): ("Kala Sungsang", "Rejeki Lancar"), (5,4): ("Udang", "Ulet & Hemat")}

    def get_wewaran_lengkap(self, rahina_cnt):
        # LOGIKA RESET OTOMATIS (MODULO)
        idx_tri = rahina_cnt % 3
        idx_catur = rahina_cnt % 4
        idx_panca = (1 + rahina_cnt) % 5
        idx_sad = rahina_cnt % 6
        idx_sapta = rahina_cnt % 7
        idx_asta = rahina_cnt % 8
        idx_sanga = rahina_cnt % 9
        
        # Hitungan Urip & Eka/Dwi/Dasa
        total_urip = self.urip_sapta[idx_sapta] + self.urip_panca[idx_panca]
        idx_eka = 0 if (total_urip % 2) != 0 else 1
        idx_dwi = 1 if idx_eka == 0 else 0
        idx_dasa = (total_urip + 1) % 10 
        idx_dasa_final = 9 if idx_dasa == 0 else (idx_dasa - 1)

        lintang = self.lintang_map.get((idx_sapta, idx_panca), ("Lumbung", "Hidup Sederhana"))
        
        return {
            "tri": self.tri_wara[idx_tri], "catur": self.catur_wara[idx_catur],
            "panca": self.panca_wara[idx_panca], "sad": self.sad_wara[idx_sad],
            "sapta": self.sapta_wara[idx_sapta], "asta": self.asta_wara[idx_asta],
            "sanga": self.sanga_wara[idx_sanga], "dasa": self.dasa_wara[idx_dasa_final],
            "sapta_idx": idx_sapta, "panca_idx": idx_panca, "total_urip": total_urip,
            "watak_sapta": self.watak_sapta[idx_sapta], "watak_panca": self.watak_panca[idx_panca],
            "lintang_nama": lintang[0], "lintang_watak": lintang[1]
        }
# ==========================================
# 4. MODUL SASIH (SIKLUS 420 HARI)
# ==========================================
class KaTikaSasih:
    def __init__(self):
        # 12 Sasih (Siklus Wuku berulang 2x dalam setahun)
        self.nama_sasih = [
            "Kasa", "Karo", "Katiga", "Kapat", "Kalima", "Kanem",      
            "Kapitu", "Kaulu", "Kasanga", "Kadasa", "Jiyestha", "Sada" 
        ]

    def get_sasih_info(self, rahina_counter, dina_global, wuku_idx):
        # 1. Nama Sasih: Berdasarkan posisi hari dalam siklus 420 hari
        posisi_tahun = rahina_counter % 420
        sasih_idx = posisi_tahun // 35 # Setiap sasih 35 hari
        
        # 2. Fase Bulan: Berdasarkan dina_global astronomi
        local_pos = ((dina_global - 1) % 14) + 1
        status = "PURNAMA" if 6 <= local_pos <= 10 else "TILEM" if local_pos <= 5 else "PANGLONG"
        
        # 3. Status Wariga: Berdasarkan Wuku
        status_wariga = "TUNGGAK (Utama)" if (wuku_idx % 3) != 2 else "NAMPIH (Transisi)"
        
        return {
            "sasih_label": self.nama_sasih[sasih_idx],
            "status": status,
            "dina_lokal": local_pos,
            "status_wariga": status_wariga
        }

class KaTikaRainan:
    def get_rainan(self, wuku_idx, sapta_idx, panca_idx, tri_nama):
        res = []
        if wuku_idx == 10 and sapta_idx == 3 and panca_idx == 4: res.append("🌟 GALUNGAN")
        if wuku_idx == 11 and sapta_idx == 6 and panca_idx == 4: res.append("🌟 KUNINGAN")
        if wuku_idx == 15 and sapta_idx == 3 and panca_idx == 4: res.append("🔒 PEGATWAKAN")
        if wuku_idx == 29 and sapta_idx == 6 and panca_idx == 0: res.append("📚 SARASWATI")
        if wuku_idx == 0 and sapta_idx == 3 and panca_idx == 4: res.append("🌟 PAGERWESI")
        if sapta_idx == 6 and panca_idx == 4: res.append("🔔 TUMPEK")
        if tri_nama == "Kajeng" and panca_idx == 4: res.append("👻 KAJENG KLIWON")
        return res
# ==========================================
# 5. MODUL PADEWASAN (5 KATEGORI LENGKAP)
# ==========================================
class KaTikaPadewasan:
    def __init__(self, cal, wew, astro):
        self.cal = cal; self.wew = wew; self.astro = astro
        self.hari_indo = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
        self.bulan_indo = ["", "Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]

    # Filter Pembatal
    def is_uncal_balung(self, wuku_idx, sapta_idx):
        if wuku_idx < 10 or wuku_idx > 15: return False
        if wuku_idx == 10 and sapta_idx < 3: return False 
        if wuku_idx == 15 and sapta_idx > 3: return False 
        return True

    def is_kala_gotongan(self, wuku_idx, sapta_idx):
        return wuku_idx in [6, 7] and sapta_idx in [1, 4]

    def get_usaha_match(self, jenis_usaha, sapta_idx):
        map_usaha = {
            "Emas, Perhiasan": [0], "Sayur, Minuman": [1], "Besi, Elektronik": [2],
            "Sembako, Umum": [3], "Pakaian, Buku": [4], "Kosmetik, Seni": [5], "Properti, Bangunan": [6]
        }
        for k, v in map_usaha.items():
            if k.split(",")[0] in jenis_usaha: return sapta_idx in v
        return False

    def find_dewasa_yearly(self, category, start_date, sub_category=None):
        results = []
        # Scan 1 Tahun (365 Hari)
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
                    if score >= 2: is_good = True; label = "✅ BAIK"; alasan = "Energi menyatukan"
            # 2. BANGUN
            elif category == "bangun":
                if not self.is_uncal_balung(wuku_idx, w['sapta_idx']) and not self.is_kala_gotongan(wuku_idx, w['sapta_idx']):
                    if idx_ingkel not in [0, 4]:
                        if w['tri'] == "Beteng": is_good = True; label = "🏗️ UTAMA"; alasan = "Pondasi Kuat"
                        elif w['sapta_idx'] == 6: is_good = True; label = "✅ BAIK"; alasan = "Elemen Benda Mati"
            # 3. USAHA
            elif category == "usaha":
                if self.get_usaha_match(sub_category, w['sapta_idx']):
                    if w['tri'] != "Kajeng": is_good=True; label="✅ COCOK"; alasan=f"Elemen {c['sapta']} selaras"
            # 4. TANI
            elif category == "tani":
                if idx_ingkel not in [4, 5]: 
                    if w['sapta_idx'] == 1: is_good=True; label="✅ BAIK (UMBI)"; alasan="Soma (Bulan)"
                    elif w['sapta_idx'] == 6: is_good=True; label="✅ BAIK (GANTUNG)"; alasan="Saniscara"
            # 5. LAUT
            elif category == "laut":
                if idx_ingkel != 2: 
                    if w['tri'] == "Pasah": is_good=True; label="🌟 UTAMA"; alasan="Pasah (Arus Lancar)"

            if is_good:
                tgl_str = f"{self.hari_indo[target_date.weekday()]}, {target_date.day} {self.bulan_indo[target_date.month]} {target_date.year}"
                results.append({"Tanggal Masehi": tgl_str, "Wuku": c['wuku'], "Wewaran": f"{c['sapta']} {c['panca']}", "Status": label, "Keterangan": alasan})
        return results
# ==========================================
# 6. MODUL WRAPPER (PENCARIAN & OTONAN)
# ==========================================
class KaTikaPencarian:
    def __init__(self, astro, cal, wew, sas):
        self.astro = astro; self.cal = cal; self.wew = wew; self.sas = sas
    def analisis_tanggal(self, target_date):
        delta = (target_date - self.astro.anchor_date).days
        c = self.cal.get_calendar(delta); w = self.wew.get_wewaran_lengkap(delta)
        # Update: Mengirim 'delta' (rahina counter) ke Sasih
        s = self.sas.get_sasih_info(delta, (delta // 3) + 1, c['wuku_index'])
        return {
            "tanggal_masehi": target_date.strftime("%d %B %Y"),
            "sapta": c['sapta'], "panca": c['panca'], "wuku": c['wuku'], 
            "sasih": s['sasih_label'], "urip": w['total_urip'], "tri": w['tri'], 
            "fase_bulan": s['status']
        }

class KaTikaOtonan:
    def __init__(self, astro, cal, wew, sas):
        self.astro = astro; self.cal = cal; self.wew = wew; self.sas = sas
    def hitung(self, tgl):
        delta = (tgl - self.astro.anchor_date).days
        c = self.cal.get_calendar(delta); w = self.wew.get_wewaran_lengkap(delta)
        # Update: Mengirim 'delta' (rahina counter) ke Sasih
        s = self.sas.get_sasih_info(delta, (delta // 3) + 1, c['wuku_index'])
        
        hari_ini = datetime.date.today(); sisa = 210 - ((hari_ini - tgl).days % 210)
        return {
            "weton_text": f"{c['sapta']} {c['panca']} {c['wuku']}", 
            "urip": w['total_urip'], "lintang": w['lintang_nama'], 
            "watak_hari": w['watak_sapta'], "watak_pasar": w['watak_panca'],
            "sasih": s['sasih_label'], "next_otonan": hari_ini + datetime.timedelta(days=sisa)
        }
# ==========================================
# 7. MAIN EXECUTION & DATA FETCH
# ==========================================
# Init All Engines
astro = KaTikaAstronomy()
cal = KaTikaCalendar()
wew = KaTikaWewaran()
sas = KaTikaSasih()
rai = KaTikaRainan()
dew = KaTikaPadewasan(cal, wew, astro)
oto = KaTikaOtonan(astro, cal, wew, sas)
search_engine = KaTikaPencarian(astro, cal, wew, sas)

# Fetch Realtime Data (Hari Ini)
t_now = datetime.datetime.now(astro.tz)
dina = astro.get_dina_status(t_now) # Data Dina Utama

c_d = cal.get_calendar(dina['rahina_counter'])
w_d = wew.get_wewaran_lengkap(dina['rahina_counter'])

# Kalkulasi Sasih (Menggunakan 'rahina_counter' dari Dina)
s_d = sas.get_sasih_info(dina['rahina_counter'], dina['dina_id_global'], c_d['wuku_index'])

# Cek Rainan
rains = rai.get_rainan(c_d['wuku_index'], w_d['sapta_idx'], w_d['panca_idx'], w_d['tri'])
# ==========================================
# 8. RENDER UI (MOBILE DARK MODE OPTIMIZED)
# ==========================================
st.set_page_config(page_title="Ka-Tika Wangsa Agra", page_icon="🔆", layout="centered")

# CSS Injection
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Inter:wght@300;400;600&display=swap');
    .stApp { background-color: #0e1117; }
    .header-box { text-align: center; font-family: 'Cinzel', serif; padding: 15px 0; }
    .header-mid { font-size: 32px; font-weight: 700; color: #e0e0e0; margin: 5px 0; }
    .header-sub { font-size: 12px; letter-spacing: 4px; color: #8b7355; }
    .sapta-wara { font-size: 58px; font-weight: 800; text-align: center; color: #fff; line-height: 1; font-family: 'Inter'; text-shadow: 0 4px 10px rgba(0,0,0,0.5); }
    .tri-panca { font-size: 16px; text-align: center; color: #9e9e9e; letter-spacing: 2px; text-transform: uppercase; }
    .widget-container { display: flex; gap: 10px; margin-top: 20px; justify-content: center; }
    .widget-box { background: #1c1f26; border: 1px solid #333; border-radius: 12px; padding: 10px; text-align: center; flex: 1; }
    .widget-val { font-size: 13px; font-weight: 600; color: #e0e0e0; }
    .rainan-notif { background: rgba(30, 81, 40, 0.9); color: #a5d6a7; padding: 10px; border-radius: 8px; text-align: center; font-weight: 600; margin: 15px 0; }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown(f'<div class="header-box"><div class="header-mid">KA-TIKA</div><div class="header-sub">WANGSA AGRA</div></div>', unsafe_allow_html=True)
if rains: st.markdown(f'<div class="rainan-notif">🔔 {" • ".join(rains)}</div>', unsafe_allow_html=True)

# Hero Section
st.markdown(f'<div class="tri-panca">{w_d["tri"]} — {c_d["panca"]}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="sapta-wara">{c_d["sapta"].upper()}</div>', unsafe_allow_html=True)
st.markdown(f'<div style="text-align:center; color:#bfa15f; font-size:12px; font-style:italic;">{dina["range_masehi"]}</div>', unsafe_allow_html=True)

# Widgets
st.markdown(f"""
<div class="widget-container">
    <div class="widget-box"><div style="font-size:24px">🌙</div><div class="widget-val">{s_d["status"]}</div></div>
    <div class="widget-box"><div style="font-size:24px">☀️</div><div class="widget-val">{dina["posisi_ls"]}</div></div>
    <div class="widget-box"><div style="font-size:24px">📅</div><div class="widget-val">{s_d["sasih_label"]}</div></div>
</div>
""", unsafe_allow_html=True)

# Tabs
st.markdown("<br>", unsafe_allow_html=True)
tab_h, tab_s, tab_w, tab_d, tab_r = st.tabs(["🏠 Info", "🔍 Cari", "👶 Weton", "🌺 Dewasa", "📅 Rainan"])

# Tab 1: Info Home
with tab_h:
    st.markdown("---")
    c1, c2, c3 = st.columns(3)
    c1.metric("Wuku", c_d['wuku']); c2.metric("Urip", w_d['total_urip']); c3.metric("Dina", f"Ke-{s_d['dina_lokal']}")
    st.info(f"**Posisi Sasih:** {s_d['status_wariga']}")

# Tab 2: Pencarian
with tab_s:
    ts_in = st.date_input("Tanggal Target", datetime.date.today())
    if st.button("Analisis", type="primary", use_container_width=True):
        res_s = search_engine.analisis_tanggal(ts_in)
        st.success(f"{res_s['sapta']} {res_s['panca']} {res_s['wuku']} | Sasih {res_s['sasih']}")
        st.caption(f"Fase: {res_s['fase_bulan']}")

# Tab 3: Weton
with tab_w:
    t_l = st.date_input("Tanggal Lahir", datetime.date(1995, 1, 1))
    if st.button("Cek Weton", type="primary", use_container_width=True):
        res = oto.hitung(t_l)
        st.markdown(f"<h3 style='text-align:center; color:#e91e63'>{res['weton_text']}</h3>", unsafe_allow_html=True)
        st.caption(f"Urip: {res['urip']} | Lintang: {res['lintang']}")
        st.warning(f"**Watak:** {res['watak_hari']}")

# Tab 4: Dewasa Ayu
with tab_d:
    # Dropdown 5 Kategori
    kp = st.selectbox("Keperluan", ["💍 Pernikahan (Wiwaha)", "🏗️ Membangun (Wewangunan)", "💰 Memulai Usaha (Dagang)", "🌾 Pertanian (Nandur)", "🎣 Melaut (Nelayan)"], label_visibility="collapsed")
    sub_cat = None
    if "Usaha" in kp: sub_cat = st.selectbox("Dagangan", ["Emas, Perhiasan", "Sayur, Minuman", "Besi, Elektronik", "Sembako, Umum", "Pakaian, Buku", "Kosmetik, Seni", "Properti, Bangunan"])
    
    if st.button("Scan Hari Baik (1 Thn)", type="primary", use_container_width=True):
        code = "nikah"
        if "Membangun" in kp: code = "bangun"
        elif "Pertanian" in kp: code = "tani"
        elif "Melaut" in kp: code = "laut"
        elif "Usaha" in kp: code = "usaha"
        
        h = dew.find_dewasa_yearly(code, datetime.date.today(), sub_cat)
        if h: st.dataframe(h, use_container_width=True, hide_index=True)
        else: st.error("Belum ada hari baik UTAMA terdekat.")

# Tab 5: Rainan
with tab_r:
    if rains: 
        for r in rains: st.success(f"• {r}")
    else: st.caption("Tidak ada rainan besar hari ini.")
