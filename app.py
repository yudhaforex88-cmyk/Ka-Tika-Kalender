import streamlit as st
import pytz
import pandas as pd
from datetime import datetime, date, time, timedelta
from astral import LocationInfo
from astral.sun import sun

# ==========================================
# 1. MODUL JANTUNG (PULSE)
# ==========================================
class KaTikaPulse:
    def __init__(self):
        self.timezone = pytz.timezone('Asia/Makassar')
        # Lokasi: Denpasar, Bali
        self.location = LocationInfo("Denpasar", "Bali", "Asia/Makassar", -8.6705, 115.2126)
        # Anchor Date: 19 Juli 2020 (Titik Nol)
        self.anchor_date = date(2020, 7, 19)

    def get_heartbeat(self, check_time: datetime) -> dict:
        # Normalisasi Timezone
        if check_time.tzinfo is None:
            check_time = self.timezone.localize(check_time)
        else:
            check_time = check_time.astimezone(self.timezone)

        # Hitung Data Matahari
        s_data = sun(self.location.observer, date=check_time.date(), tzinfo=self.timezone)
        sunrise, sunset = s_data['sunrise'], s_data['sunset']
        
        # Hitung Signal Dasar
        delta = check_time.date() - self.anchor_date
        base_signal = delta.days
        
        # Logika Pergantian Dina (CRITICAL)
        if check_time < sunrise:
            final_signal = base_signal - 1
            phase = "WENGI (Sebelum Fajar)"
        else:
            final_signal = base_signal
            phase = "RAHINA" if check_time < sunset else "WENGI"
            
        return {
            "signal": final_signal,
            "sunrise": sunrise,
            "sunset": sunset,
            "phase": phase
        }

# ==========================================
# 2. MODUL WEWARAN (CUSTOM + WATAK)
# ==========================================
class KaTikaWewaran:
    def __init__(self):
        # Tri Wara (Custom 4 Siklus: Ada 2 Pasah)
        self.TRI_WARA = ['Kajeng', 'Pasah', 'Beteng', 'Pasah']
        
        self.CATUR_WARA = ['Sri', 'Laba', 'Jaya', 'Menala']
        
        # Panca Wara (Start Paing)
        self.PANCA_WARA = ['Paing', 'Pon', 'Wage', 'Kliwon', 'Umanis']
        self.URIP_PANCA = [9, 7, 4, 8, 5]
        
        self.SAD_WARA = ['Tungleh', 'Aryang', 'Urukung', 'Paniron', 'Was', 'Maulu']
        
        self.SAPTA_WARA = ['Redite', 'Soma', 'Anggara', 'Buda', 'Wraspati', 'Sukra', 'Saniscara']
        self.URIP_SAPTA = [5, 4, 3, 7, 8, 6, 9]
        
        self.ASTA_WARA = ['Sri', 'Indra', 'Guru', 'Yama', 'Ludra', 'Brahma', 'Kala', 'Uma']
        self.SANGA_WARA = ['Dangu', 'Jangur', 'Gigis', 'Nohan', 'Ogan', 'Erangan', 'Urungan', 'Tulus', 'Dadi']
        self.DASA_WARA = ['Pandita', 'Pati', 'Suka', 'Duka', 'Sri', 'Manuh', 'Manusa', 'Raja', 'Dewa', 'Raksasa']

        # Database Lintang / Watak (Sample)
        self.DATA_LINTANG = {
            (0, 0): {"nama": "Kukus", "sifat": "Keras hati, cemburu, penyayang."},
            (0, 4): {"nama": "Kala Sungsang", "sifat": "Pemberani, suka bicara, mudah tersinggung."},
            (1, 1): {"nama": "Lembu", "sifat": "Pendiam, cerdas, setia."},
            # ... (Tambahkan sisa kombinasi 35 weton di sini)
        }
        self.DEFAULT_WATAK = {"nama": "Belum Terdata", "sifat": "Data pustaka sedang dilengkapi."}

    def get_wewaran_lengkap(self, signal: int) -> dict:
        tri = self.TRI_WARA[signal % 4]
        catur = self.CATUR_WARA[signal % 4]
        
        panca_idx = signal % 5
        panca = self.PANCA_WARA[panca_idx]
        urip_panca = self.URIP_PANCA[panca_idx]
        
        sad = self.SAD_WARA[signal % 6]
        
        sapta_idx = signal % 7
        sapta = self.SAPTA_WARA[sapta_idx]
        urip_sapta = self.URIP_SAPTA[sapta_idx]
        
        asta = self.ASTA_WARA[signal % 8]
        sanga = self.SANGA_WARA[signal % 9]
        
        total_urip = urip_sapta + urip_panca
        dasa = self.DASA_WARA[(total_urip + 1) % 10]
        
        # Ambil Watak
        watak = self.DATA_LINTANG.get((sapta_idx, panca_idx), self.DEFAULT_WATAK)
        
        return {
            "tri": tri, "catur": catur, "panca": panca, "sad": sad,
            "sapta": sapta, "asta": asta, "sanga": sanga, "dasa": dasa,
            "total_urip": total_urip,
            "lintang_nama": watak['nama'],
            "lintang_sifat": watak['sifat']
        }

# ==========================================
# 3. MODUL KALENDER (SSOT)
# ==========================================
class KaTikaCalendar:
    def __init__(self):
        self.WUKU = ["Sinta", "Landep", "Ukir", "Kulantir", "Tolu", "Gumbreg",
                     "Wariga", "Warigadean", "Julungwangi", "Sungsang", "Dungulan", "Kuningan",
                     "Langkir", "Medangsia", "Pujut", "Pahang", "Krulut", "Merakih",
                     "Tambir", "Medangkungan", "Matal", "Uye", "Menail", "Prangbakat",
                     "Bala", "Ugu", "Wayang", "Klawu", "Dukut", "Watugunung"]
        self.INGKEL = ["Wong", "Sato", "Mina", "Manuk", "Taru", "Buku"]

    def get_calendar(self, signal: int, wew_data: dict) -> dict:
        wuku_idx = (signal // 7) % 30
        return {
            "wuku_name": self.WUKU[wuku_idx],
            "wuku_index": wuku_idx,
            "ingkel_name": self.INGKEL[wuku_idx % 6],
            "full_label": f"{wew_data['sapta']} {wew_data['panca']} {self.WUKU[wuku_idx]}"
        }

# ==========================================
# 4. MODUL SASIH (420 HARI)
# ==========================================
class KaTikaSasih:
    def __init__(self):
        self.SASIH = ["Kasa", "Karo", "Katiga", "Kapat", "Kalima", "Kanem",
                      "Kapitu", "Kaulu", "Kasanga", "Kadasa", "Jyestha", "Sada"]
    
    def get_sasih_info(self, signal: int) -> dict:
        cycle_pos = signal % 420
        sasih_idx = cycle_pos // 35
        day_sasih = (cycle_pos % 35) + 1
        
        status = "PANGALANTAKA"
        is_purnama, is_tilem = False, False
        
        # Logika Custom Gelap/Terang
        if sasih_idx % 2 == 0: # Index Genap (Kasa, Katiga...) -> Pola Gelap
            if day_sasih == 18: status, is_purnama = "PURNAMA", True
            elif day_sasih in [1, 35]: status, is_tilem = "TILEM", True
            elif 1 < day_sasih < 18: status = "PENANGGAL"
            else: status = "PANGLONG"
        else: # Index Ganjil (Karo, Kapat...) -> Pola Terang
            if day_sasih in [1, 35]: status, is_purnama = "PURNAMA", True
            elif day_sasih == 18: status, is_tilem = "TILEM", True
            elif 1 < day_sasih < 18: status = "PANGLONG"
            else: status = "PENANGGAL"
            
        return {
            "sasih_name": self.SASIH[sasih_idx], 
            "status_bulan": status, 
            "is_purnama": is_purnama, 
            "is_tilem": is_tilem
        }

# ==========================================
# 5. MODUL PADEWASAN (8 KATEGORI + RULE WARIGA)
# ==========================================
class KaTikaPadewasan:
    def __init__(self, cal, wew, sas, astro):
        self.cal, self.wew, self.sas, self.astro = cal, wew, sas, astro
        self.CATEGORIES = [
            "Pernikahan (Wiwaha)", "Membangun (Wisma)", "Pertanian (Tanam Tuwuh)", 
            "Peternakan (Wewalungan)", "Perabotan (Pande/Alat)", 
            "Ekonomi (Dagang)", "Melaut (Mina)", "Upacara (Yadnya)"
        ]

    def _is_uncal_balung(self, wuku_idx): return 10 <= wuku_idx <= 15
    def _is_rangda_tiga(self, wuku_idx): return wuku_idx in [6, 7, 14, 15, 22, 23]
    def _is_kala_gotongan(self, sapta, panca): return sapta == "Saniscara" and panca == "Paing"

    def _format_date_ranges(self, date_list):
        if not date_list: return ""
        sorted_dates = sorted(list(set(date_list)))
        ranges = []
        if not sorted_dates: return ""
        start, end = sorted_dates[0], sorted_dates[0]
        bln = ["", "Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Ags", "Sep", "Okt", "Nov", "Des"]
        for i in range(1, len(sorted_dates)):
            curr = sorted_dates[i]
            if (curr - end).days == 1: end = curr
            else:
                ranges.append(self._str(start, end, bln))
                start, end = curr, curr
        ranges.append(self._str(start, end, bln))
        return ", ".join(ranges)

    def _str(self, start, end, bln):
        if start == end: return f"{start.day} {bln[start.month]} {start.year}"
        elif start.month == end.month: return f"{start.day}-{end.day} {bln[start.month]} {start.year}"
        else: return f"{start.day} {bln[start.month]} - {end.day} {bln[end.month]} {end.year}"

    def cari_dewasa_ayu(self) -> list:
        start_date = datetime.now(self.astro.timezone) + timedelta(days=1)
        start_date = start_date.replace(hour=12, minute=0, second=0, microsecond=0)
        raw_results = {cat: [] for cat in self.CATEGORIES}

        # Scanner 365 Hari
        for i in range(365):
            curr_date = start_date + timedelta(days=i)
            pulse = self.astro.get_heartbeat(curr_date)
            wew = self.wew.get_wewaran_lengkap(pulse['signal'])
            cal = self.cal.get_calendar(pulse['signal'], wew)
            sas = self.sas.get_sasih_info(pulse['signal'])

            # Variables
            sapta, panca, tri = wew['sapta'], wew['panca'], wew['tri']
            wuku_idx, ingkel = cal['wuku_index'], cal['ingkel_name']
            
            # Filter Negatif
            is_uncal = self._is_uncal_balung(wuku_idx)
            is_rangda = self._is_rangda_tiga(wuku_idx)
            is_kala = self._is_kala_gotongan(sapta, panca)

            # --- RULE ENGINE WARIGA ---
            
            # 1. Pernikahan (No Uncal, No Rangda Tiga, No Ingkel Wong)
            if not is_uncal and not is_rangda and not is_kala and ingkel != 'Wong':
                if sapta in ['Wraspati', 'Sukra'] and panca in ['Umanis', 'Kliwon']:
                    raw_results["Pernikahan (Wiwaha)"].append(curr_date.date())

            # 2. Membangun (No Kala Gotongan, No Ingkel Taru)
            if not is_kala and ingkel != 'Taru':
                if sapta == 'Saniscara' or (sapta == 'Wraspati' and panca == 'Pon'):
                    raw_results["Membangun (Wisma)"].append(curr_date.date())

            # 3. Pertanian (Tanam Tuwuh)
            if not is_kala and ingkel not in ['Taru', 'Buku'] and sapta in ['Soma', 'Wraspati', 'Sukra']:
                raw_results["Pertanian (Tanam Tuwuh)"].append(curr_date.date())

            # 4. Peternakan (No Ingkel Sato/Mina)
            if not is_kala and ingkel not in ['Sato', 'Mina']:
                if sapta in ['Wraspati', 'Saniscara'] or cal['wuku_name'] == 'Uye':
                    raw_results["Peternakan (Wewalungan)"].append(curr_date.date())
            
            # 5. Perabotan (Anggara/Pasah, No Ingkel Buku)
            if not is_kala and ingkel != 'Buku' and (sapta == 'Anggara' or tri == 'Pasah'):
                raw_results["Perabotan (Pande/Alat)"].append(curr_date.date())

            # 6. Ekonomi (Pasah, Soma Pon/Buda Wage)
            if not is_kala and tri == 'Pasah':
                if (sapta == 'Soma' and panca == 'Pon') or (sapta == 'Buda' and panca == 'Wage') or tri == 'Pasah':
                    raw_results["Ekonomi (Dagang)"].append(curr_date.date())

            # 7. Melaut (Mina)
            if not is_kala and ingkel != 'Mina' and (tri == 'Pasah' or sapta == 'Soma'):
                raw_results["Melaut (Mina)"].append(curr_date.date())

            # 8. Upacara (Yadnya)
            if not is_uncal and not is_kala:
                is_kajeng_kliwon = (tri == 'Kajeng' and panca == 'Kliwon')
                if sas['is_purnama'] or sas['is_tilem'] or is_kajeng_kliwon:
                    raw_results["Upacara (Yadnya)"].append(curr_date.date())

        return [{"kategori": k, "Tanggal masehi": self._format_date_ranges(v), "jumlah_hari": len(v)} for k, v in raw_results.items() if v]

# ==========================================
# 6. MODUL ODALAN (DB LENGKAP)
# ==========================================
class KaTikaOdalan:
    def __init__(self):
        # Database Pawukon (Sad Kahyangan & Jajar Kemiri)
        self.DB_PAWUKON = {
            ('Anggara', 'Kliwon', 'Medangsia'): ["Pura Luhur Uluwatu", "Pura Taman Ayun"],
            ('Buda', 'Wage', 'Langkir'): ["Pura Tanah Lot (Buda Cemeng)"],
            ('Wraspati', 'Umanis', 'Dungulan'): ["Pura Luhur Batukaru"],
            ('Saniscara', 'Kliwon', 'Dungulan'): ["Pura Lempuyang Luhur (Kuningan)"],
            ('Saniscara', 'Kliwon', 'Wayang'): ["Pura Dasar Buana Gelgel"],
            # Jajar Kemiri Tabanan
            ('Saniscara', 'Kliwon', 'Wariga'): ["Pura Luhur Besikalung"],
            ('Saniscara', 'Kliwon', 'Krulut'): ["Pura Luhur Muncak Sari"],
            ('Buda', 'Umanis', 'Prangbakat'): ["Pura Luhur Tambawaras"],
            ('Buda', 'Kliwon', 'Ugu'): ["Pura Luhur Petali"],
        }
        # Database Sasih
        self.DB_SASIH = {
            ('Kadasa', 'PURNAMA'): ["Pura Besakih", "Pura Ulun Danu Batur", "Pura Tuluk Biyu"],
            ('Kapat', 'PURNAMA'): ["Pura Jati Batur", "Pura Pulaki"]
        }
    
    def scan_year(self, wew_mod, cal_mod, sas_mod, astro_mod):
        results = []
        start_date = datetime.now(astro_mod.timezone) + timedelta(days=1)
        start_date = start_date.replace(hour=12)
        
        # Scan 365 hari
        for i in range(365):
            curr = start_date + timedelta(days=i)
            pulse = astro_mod.get_heartbeat(curr)
            wew = wew_mod.get_wewaran_lengkap(pulse['signal'])
            cal = cal_mod.get_calendar(pulse['signal'], wew)
            sas = sas_mod.get_sasih_info(pulse['signal'])
            
            key_pawukon = (wew['sapta'], wew['panca'], cal['wuku_name'])
            key_sasih = (sas['sasih_name'], sas['status_bulan'])
            
            found = []
            if key_pawukon in self.DB_PAWUKON: found.extend(self.DB_PAWUKON[key_pawukon])
            if key_sasih in self.DB_SASIH: found.extend(self.DB_SASIH[key_sasih])
            
            if found:
                t_pagi, t_sore = pulse['sunrise'], pulse['sunset'] - timedelta(hours=1)
                rentang = f"{t_pagi.strftime('%H:%M')} - {t_sore.strftime('%H:%M')}"
                for p in found:
                    results.append({
                        "Tanggal": curr.strftime("%d %B %Y"),
                        "Pura": p,
                        "Waktu": rentang
                    })
        return results

# ==========================================
# 7. MODUL OTONAN (WRAPPER)
# ==========================================
class KaTikaOtonan:
    def __init__(self, astro, cal, wew, sas):
        self.astro, self.cal, self.wew, self.sas = astro, cal, wew, sas
    
    def hitung(self, tgl_lahir):
        if isinstance(tgl_lahir, datetime): tgl_lahir_date = tgl_lahir.date()
        else: tgl_lahir_date = tgl_lahir
        
        # Normalisasi ke Jam 12 Siang
        birth_noon = datetime.combine(tgl_lahir_date, time(12, 0, 0))
        birth_noon = self.astro.timezone.localize(birth_noon)

        pulse = self.astro.get_heartbeat(birth_noon)
        wew = self.wew.get_wewaran_lengkap(pulse['signal'])
        cal = self.cal.get_calendar(pulse['signal'], wew)
        
        # Next Otonan
        now = datetime.now(self.astro.timezone).date()
        delta = (now - tgl_lahir_date).days
        days_until = 210 - (delta % 210)
        if days_until == 210: days_until = 0
        
        return {
            "weton_text": f"{wew['sapta']} {wew['panca']} {cal['wuku_name']}",
            "urip_total": wew['total_urip'],
            "hasil_analisa": {"bintang": wew['lintang_nama'], "watak": wew['lintang_sifat']},
            "next_otonan_date": now + timedelta(days=days_until),
            "sisa_hari": days_until
        }

# ==========================================
# 8. UI DASHBOARD (STREAMLIT)
# ==========================================

# Init Modules
pulse_mod = KaTikaPulse()
wew_mod = KaTikaWewaran()
cal_mod = KaTikaCalendar()
sas_mod = KaTikaSasih()
padewasan_mod = KaTikaPadewasan(cal_mod, wew_mod, sas_mod, pulse_mod)
odalan_mod = KaTikaOdalan()
otonan_mod = KaTikaOtonan(pulse_mod, cal_mod, wew_mod, sas_mod)

st.set_page_config(page_title="Ka-Tika Dashboard", layout="wide", page_icon="🌞")

# CSS Styling
def inject_css(theme):
    bg = "#0e1117" if theme == "Dark" else "#f0f2f6"
    txt = "#ffffff" if theme == "Dark" else "#31333F"
    card = "rgba(255, 255, 255, 0.05)" if theme == "Dark" else "rgba(255, 255, 255, 0.6)"
    
    st.markdown(f"""
    <style>
        .stApp {{ background-color: {bg}; color: {txt}; }}
        .glass {{
            background: {card}; backdrop-filter: blur(10px);
            border-radius: 15px; border: 1px solid rgba(255,255,255,0.18);
            padding: 20px; margin-bottom: 20px;
        }}
        .big {{ font-size: 2.5rem; font-weight: bold; line-height: 1.2; }}
        .med {{ font-size: 1.5rem; opacity: 0.9; }}
    </style>
    """, unsafe_allow_html=True)

# Sidebar
st.sidebar.title("🌸 Ka-Tika")
theme = st.sidebar.radio("Mode", ["Dark", "Light"], horizontal=True)
inject_css(theme)
menu = st.sidebar.selectbox("Navigasi", ["Home", "Cek Weton", "Dewasa Ayu", "Odalan"])

now = datetime.now(pulse_mod.timezone)

if menu == "Home":
    st.title(f"Rahina {now.strftime('%A, %d %B %Y')}")
    pulse = pulse_mod.get_heartbeat(now)
    wew = wew_mod.get_wewaran_lengkap(pulse['signal'])
    cal = cal_mod.get_calendar(pulse['signal'], wew)
    sas = sas_mod.get_sasih_info(pulse['signal'])
    
    c1, c2 = st.columns([2, 1])
    with c1:
        st.markdown(f"""
        <div class="glass">
            <div>Dina Ini</div>
            <div class="big">{wew['sapta']} {wew['panca']}</div>
            <div class="med">{wew['tri']} - {cal['wuku_name']}</div>
            <hr>
            <div>Ingkel: {cal['ingkel_name']} | Sasih: {sas['sasih_name']}</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        # Surya Progress
        curr_sec = (now - pulse['sunrise']).total_seconds()
        tot_sec = (pulse['sunset'] - pulse['sunrise']).total_seconds()
        pct = max(0, min(100, (curr_sec / tot_sec) * 100))
        st.markdown(f"""<div class="glass" style="text-align:center"><div>☀️ Surya ({pulse['phase']})</div></div>""", unsafe_allow_html=True)
        st.progress(int(pct))
    
    colA, colB, colC = st.columns(3)
    with colA: st.markdown(f"""<div class="glass"><h4>🌙 Bulan</h4><h2>{sas['status_bulan']}</h2></div>""", unsafe_allow_html=True)
    with colB: st.markdown(f"""<div class="glass"><h4>👹 Dasa Wara</h4><h2>{wew['dasa']}</h2></div>""", unsafe_allow_html=True)
    with colC: st.markdown(f"""<div class="glass"><h4>🗓️ Masehi</h4><h2>{now.day}</h2></div>""", unsafe_allow_html=True)

elif menu == "Cek Weton":
    st.title("🎂 Cek Weton & Watak")
    with st.container():
        st.markdown('<div class="glass">', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        tgl = c1.date_input("Tanggal Lahir", value=date(2000, 1, 1))
        jam = c2.time_input("Jam Lahir", value=time(12, 0))
        
        if st.button("Analisa"):
            res = otonan_mod.hitung(datetime.combine(tgl, jam))
            st.success(f"Weton: {res['weton_text']}")
            st.info(f"Watak: {res['hasil_analisa']['bintang']} - {res['hasil_analisa']['watak']}")
            st.warning(f"Otonan Berikutnya: {res['next_otonan_date'].strftime('%d %B %Y')} ({res['sisa_hari']} hari lagi)")
        st.markdown('</div>', unsafe_allow_html=True)

elif menu == "Dewasa Ayu":
    st.title("✅ Pencarian Dewasa Ayu")
    cat = st.selectbox("Kategori", padewasan_mod.CATEGORIES)
    if st.button("Cari Hari Baik"):
        with st.spinner("Scanning 365 hari (Logika Wariga)..."):
            res = padewasan_mod.cari_dewasa_ayu()
            filtered = [r for r in res if r['kategori'] == cat]
            if filtered:
                st.success(f"Ditemukan {filtered[0]['jumlah_hari']} hari baik.")
                st.write(filtered[0]['Tanggal masehi'])
            else:
                st.error("Tidak ditemukan hari baik yang memenuhi syarat dalam 1 tahun ke depan.")

elif menu == "Odalan":
    st.title("🙏 Jadwal Odalan Pura")
    if st.button("Scan Odalan (1 Tahun)"):
        with st.spinner("Mencocokkan Database Sad Kahyangan & Jajar Kemiri..."):
            data = odalan_mod.scan_year(wew_mod, cal_mod, sas_mod, pulse_mod)
        if data:
            st.dataframe(pd.DataFrame(data), use_container_width=True)
        else:
            st.info("Tidak ada odalan dalam database untuk rentang ini.")
