import streamlit as st
import datetime
import pytz
import calendar
import math
from astral import LocationInfo
from astral.sun import sun

# ==========================================
# 1. MODUL JANTUNG (ASTRONOMIS - SUNRISE TRIGGER)
# ==========================================
class KaTikaAstronomy:
    def __init__(self):
        # Konfigurasi Lokasi (Denpasar)
        self.location = LocationInfo("Denpasar", "Indonesia", "Asia/Makassar", -8.6705, 115.2126)
        self.tz = pytz.timezone("Asia/Makassar")
        
        # ANCHOR: 19 Juli 2020
        # Dianggap dimulai saat Matahari Terbit pada tanggal tersebut.
        self.anchor_date = datetime.date(2020, 7, 19)

    def get_heartbeat(self, check_time):
        """
        Menghitung Sinyal berdasarkan posisi Matahari.
        - Sebelum Sunrise = Hari Kemarin (Signal - 1)
        - Setelah Sunrise = Hari Ini (Signal Normal)
        """
        # 1. Normalisasi Waktu
        if check_time.tzinfo is None: check_time = self.tz.localize(check_time)
        else: check_time = check_time.astimezone(self.tz)
        
        target_date = check_time.date()
        
        # 2. HITUNG DATA MATAHARI (ASTRONOMIS)
        # Menggunakan library 'astral' untuk menghitung waktu presisi di Denpasar
        try:
            s_data = sun(self.location.observer, date=target_date, tzinfo=self.tz)
            sunrise = s_data['sunrise']
            sunset = s_data['sunset']
        except:
            # Fallback jika library astral error (jarang terjadi)
            sunrise = check_time.replace(hour=6, minute=0, second=0)
            sunset = check_time.replace(hour=18, minute=30, second=0)
        
        # 3. TENTUKAN SINYAL (HEARTBEAT)
        # Sinyal dasar (selisih hari kalender Masehi)
        base_signal = (target_date - self.anchor_date).days
        
        # Koreksi Sinyal berdasarkan Matahari Terbit (Dau)
        # Dalam Wariga, hari baru dimulai saat Terbit Fajar.
        if check_time < sunrise:
            # Jika belum terbit, ikut hitungan hari kemarin
            final_signal = base_signal - 1
            status_waktu = "WENGI (Sebelum Fajar)"
        elif check_time >= sunrise and check_time < sunset:
            # Jika sudah terbit dan belum terbenam
            final_signal = base_signal
            status_waktu = "RAHINA (Siang)"
        else:
            # Jika sudah terbenam (Malam hari tapi masih tanggal yang sama)
            final_signal = base_signal
            status_waktu = "WENGI (Malam)"

        # 4. TENTUKAN SIKLUS (Ganjil/Genap)
        cycle_type = "GENAP" if final_signal % 2 == 0 else "GANJIL"

        return {
            "signal": final_signal,         # Integer Sinyal (Kunci Modul Lain)
            "cycle_type": cycle_type,       # Info Ganjil/Genap
            "sunrise": sunrise,             # Waktu Terbit
            "sunset": sunset,               # Waktu Terbenam
            "phase": status_waktu,          # Info Visual (Pagi/Siang/Malam)
            "tgl_obj": target_date          # Tanggal Masehi
        }

# ==========================================
# 2. MODUL KALENDER (WUKU)
# ==========================================
class KaTikaCalendar:
    def __init__(self):
        self.sapta = ["Redite", "Soma", "Anggara", "Buda", "Wraspati", "Sukra", "Saniscara"]
        self.panca = ["Umanis", "Paing", "Pon", "Wage", "Kliwon"]
        self.wuku_list = ["Sinta", "Landep", "Ukir", "Kulantir", "Tolu", "Gumbreg", "Wariga", "Warigadean", "Julungwangi", "Sungsang", "Dungulan", "Kuningan", "Langkir", "Medangsia", "Pujut", "Pahang", "Krulut", "Merakih", "Tambir", "Medangkungan", "Matal", "Uye", "Menail", "Prangbakat", "Bala", "Ugu", "Wayang", "Klawu", "Dukut", "Watugunung"]

    def get_calendar(self, signal):
        # Menerima Sinyal -> Terjemahkan ke Wuku
        # Modulo 30 wuku
        idx_wuku = (signal // 7) % 30
        return {
            "sapta": self.sapta[signal % 7],
            "panca": self.panca[(1 + signal) % 5],
            "wuku": self.wuku_list[idx_wuku],
            "wuku_index": idx_wuku
        }

# ==========================================
# 3. MODUL WEWARAN (RESET OTOMATIS)
# ==========================================
class KaTikaWewaran:
    def __init__(self):
        # Database Wewaran
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

        self.urip_sapta = [5, 4, 3, 7, 8, 6, 9] 
        self.urip_panca = [5, 9, 7, 4, 8]
        
        self.watak_sapta = ["Redite: Pemimpin", "Soma: Lembut", "Anggara: Pemberani", "Buda: Sabar", "Wraspati: Bijaksana", "Sukra: Romantis", "Saniscara: Teguh"]
        self.watak_panca = ["Umanis: Penyayang", "Paing: Rajin", "Pon: Bijaksana", "Wage: Setia", "Kliwon: Spiritual"]
        self.lintang_map = {(0,0): ("Kala Sungsang", "Rejeki"), (5,4): ("Udang", "Ulet")}

    def get_wewaran_lengkap(self, signal):
        # Menerima Sinyal Integer -> Hitung Modulo
        idx_tri = signal % 3
        idx_catur = signal % 4
        idx_panca = (1 + signal) % 5
        idx_sad = signal % 6
        idx_sapta = signal % 7
        idx_asta = signal % 8
        idx_sanga = signal % 9
        
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
# 4. MODUL SASIH (TERHUBUNG KE DINA JANTUNG)
# ==========================================
class KaTikaSasih:
    def __init__(self):
        # Siklus 420 Hari (12 Sasih x 35 Hari)
        self.nama_sasih = [
            "Kasa", "Karo", "Katiga", "Kapat", "Kalima", "Kanem",      
            "Kapitu", "Kaulu", "Kasanga", "Kadasa", "Jiyestha", "Sada" 
        ]

    def get_sasih_info(self, signal, wuku_idx):
        """
        signal: Data mentah dari Modul Jantung (KaTikaAstronomy).
        wuku_idx: Data dari Modul Kalender.
        """
        
        # 1. HITUNG NAMA SASIH (Siklus 420 Hari)
        # Sinyal dari Jantung menentukan kita ada di hari keberapa dalam tahun Saka
        posisi_tahun = signal % 420
        sasih_idx = posisi_tahun // 35
        
        # 2. HITUNG DINA & FASE BULAN (Dari Dina Jantung)
        # Di sini Sasih menerjemahkan 'Sinyal Jantung' menjadi 'Dina Global' (Siklus 3 harian)
        dina_global = (signal // 3) + 1 
        
        local_pos = ((dina_global - 1) % 14) + 1
        status = "PURNAMA" if 6 <= local_pos <= 10 else "TILEM" if local_pos <= 5 else "PANGLONG"
        
        # 3. STATUS WARIGA
        status_wariga = "TUNGGAK (Utama)" if (wuku_idx % 3) != 2 else "NAMPIH"
        
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
# 5. MODUL PADEWASAN (5 KATEGORI)
# ==========================================
class KaTikaPadewasan:
    def __init__(self, cal, wew, astro):
        self.cal = cal; self.wew = wew; self.astro = astro
        self.hari_indo = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
        self.bulan_indo = ["", "Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]

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
        # Gunakan Sinyal Dasar (Hari Kalender Masehi) untuk scan ke depan
        start_signal = (start_date - self.astro.anchor_date).days
        
        for i in range(1, 366):
            target_signal = start_signal + i
            target_date = start_date + datetime.timedelta(days=i)
            
            c = self.cal.get_calendar(target_signal)
            w = self.wew.get_wewaran_lengkap(target_signal)
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
# 6. MODUL WRAPPER (SINKRONISASI SIGNAL)
# ==========================================
class KaTikaPencarian:
    def __init__(self, astro, cal, wew, sas):
        self.astro = astro; self.cal = cal; self.wew = wew; self.sas = sas
    
    def analisis_tanggal(self, target_date):
        # 1. Generate Sinyal Dasar (Asumsi jam 12 siang/Rahina)
        signal = (target_date - self.astro.anchor_date).days
        
        # 2. Distribusi Sinyal
        c = self.cal.get_calendar(signal)
        w = self.wew.get_wewaran_lengkap(signal)
        s = self.sas.get_sasih_info(signal, c['wuku_index'])
        
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
        signal = (tgl - self.astro.anchor_date).days
        
        c = self.cal.get_calendar(signal)
        w = self.wew.get_wewaran_lengkap(signal)
        s = self.sas.get_sasih_info(signal, c['wuku_index'])
        
        hari_ini = datetime.date.today(); sisa = 210 - ((hari_ini - tgl).days % 210)
        return {
            "weton_text": f"{c['sapta']} {c['panca']} {c['wuku']}", 
            "urip": w['total_urip'], "lintang": w['lintang_nama'], 
            "watak_hari": w['watak_sapta'], "watak_pasar": w['watak_panca'],
            "sasih": s['sasih_label'], "next_otonan": hari_ini + datetime.timedelta(days=sisa)
        }

# ==========================================
# 8. RENDER UI (MOBILE OPTIMIZED)
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

# Header & Notif
st.markdown(f'<div class="header-box"><div class="header-mid">KA-TIKA</div><div class="header-sub">WANGSA AGRA</div></div>', unsafe_allow_html=True)
if rains: st.markdown(f'<div class="rainan-notif">🔔 {" • ".join(rains)}</div>', unsafe_allow_html=True)

# Hero Section
st.markdown(f'<div class="tri-panca">{w_d["tri"]} — {c_d["panca"]}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="sapta-wara">{c_d["sapta"].upper()}</div>', unsafe_allow_html=True)
st.markdown(f'<div style="text-align:center; color:#bfa15f; font-size:12px; font-style:italic;">{range_text}</div>', unsafe_allow_html=True)

# Widgets (Update: Menampilkan Data Astronomis)
st.markdown(f"""
<div class="widget-container">
    <div class="widget-box">
        <div style="font-size:20px">🌅</div>
        <div class="widget-val">Terbit</div>
        <div style="font-size:11px; color:#bfa15f;">{heart['sunrise'].strftime('%H:%M')}</div>
    </div>
    <div class="widget-box">
        <div style="font-size:24px; color:#fff; font-weight:bold;">{heart['cycle_type']}</div>
        <div style="font-size:10px; color:#888;">{heart['phase']}</div>
    </div>
    <div class="widget-box">
        <div style="font-size:20px">🌇</div>
        <div class="widget-val">Terbenam</div>
        <div style="font-size:11px; color:#bfa15f;">{heart['sunset'].strftime('%H:%M')}</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Tabs
st.markdown("<br>", unsafe_allow_html=True)
tab_h, tab_s, tab_w, tab_d, tab_r = st.tabs(["🏠 Info", "🔍 Cari", "👶 Weton", "🌺 Dewasa", "📅 Rainan"])

# Tab 1: Info
with tab_h:
    st.markdown("---")
    c1, c2, c3 = st.columns(3)
    c1.metric("Wuku", c_d['wuku']); c2.metric("Urip", w_d['total_urip']); c3.metric("Dina", f"Ke-{s_d['dina_lokal']}")
    st.info(f"**Posisi Sasih:** {s_d['status_wariga']} | {s_d['sasih_label']}")

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
