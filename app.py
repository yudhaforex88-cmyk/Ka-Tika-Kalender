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
        self.location = LocationInfo("Denpasar", "Indonesia", "Asia/Makassar", -8.6705, 115.2126)
        self.tz = pytz.timezone("Asia/Makassar")
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
            "range_masehi": range_str, "current_date": current_date,
            "fase": "LIVE" if current_date == datetime.date.today() else "SEARCH"
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
        self.watak_sapta = ["Matahari: Berwibawa, Keras Kemauan", "Bulan: Lembut, Tekun", "Api: Pemberani, Panas Hati", "Bumi: Sabar, Tenang", "Langit: Cerdas, Bijaksana", "Bintang: Romantis, Menyenangkan", "Angin: Teguh, Pekerja Keras"]
        self.watak_panca = ["Umanis: Penyayang", "Paing: Rajin & Keras", "Pon: Bijaksana", "Wage: Setia & Kaku", "Kliwon: Spiritual"]
        self.lintang_map = {(0,0): ("Kala Sungsang", "Pemberani & Rejeki"), (1,4): ("Pedati", "Pekerja Keras"), (5,4): ("Udang", "Ulet")}

    def get_wewaran_lengkap(self, rahina_cnt):
        idx_s = rahina_cnt % 7; idx_p = (1 + rahina_cnt) % 5
        total_urip = self.urip_sapta[idx_s] + self.urip_panca[idx_p]
        lintang = self.lintang_map.get((idx_s, idx_p), ("Lumbung", "Hidup Makmur & Hemat"))
        return {
            "tri": self.tri_wara[rahina_cnt % 4], "total_urip": total_urip,
            "dasa": self.dasa_wara[(total_urip - 1) % 10], "sapta_idx": idx_s, "panca_idx": idx_p,
            "watak_sapta": self.watak_sapta[idx_s], "watak_panca": self.watak_panca[idx_p],
            "lintang_nama": lintang[0], "lintang_watak": lintang[1]
        }

# ==========================================
# 3. MODUL SASIH & RAINAN
# ==========================================
class KaTikaSasih:
    def __init__(self):
        self.nama_sasih = ["Kasa", "Karo", "Katiga", "Kapat", "Kalima", "Kanem", "Kapitu", "Kaulu", "Kasanga", "Kadasa"]

    def get_sasih_info(self, dina_global, wuku_idx):
        sasih_idx = min(wuku_idx // 3, 9); label = self.nama_sasih[sasih_idx]
        local_pos = ((dina_global - 1) % 14) + 1
        status = "PURNAMA" if 6 <= local_pos <= 10 else "TILEM" if local_pos <= 5 else "PANGLONG"
        return {"sasih_label": label, "status": status, "dina_lokal": local_pos, "status_wariga": "TUNGGAK" if (wuku_idx % 3) != 2 else "NAMPIH"}

class KaTikaRainan:
    def get_rainan(self, wuku_idx, sapta_idx, panca_idx, tri_nama):
        res = []
        if wuku_idx == 10 and sapta_idx == 3 and panca_idx == 4: res.append("🌟 GALUNGAN")
        if wuku_idx == 11 and sapta_idx == 6 and panca_idx == 4: res.append("🌟 KUNINGAN")
        if sapta_idx == 6 and panca_idx == 4: res.append("🔔 TUMPEK")
        if tri_nama == "Kajeng" and panca_idx == 4: res.append("👻 KAJENG KLIWON")
        return res

# ==========================================
# 4. MODUL ANALISIS (DEWASA & OTONAN)
# ==========================================
class KaTikaPadewasan:
    def __init__(self, cal, wew, astro):
        self.cal = cal; self.wew = wew; self.astro = astro

    def find_monthly(self, cat, month, year):
        res_list = []
        num_days = calendar.monthrange(year, month)[1]
        for d in range(1, num_days + 1):
            t = datetime.date(year, month, d)
            cnt = (t - self.astro.anchor_date).days
            c = self.cal.get_calendar(cnt); w = self.wew.get_wewaran_lengkap(cnt)
            if c['wuku_index'] < 10 or c['wuku_index'] > 15: # Filter sederhana Uncal Balung
                res_list.append({"Tanggal": f"{d}-{month}-{year}", "Wewaran": f"{c['sapta']} {c['panca']}", "Wuku": c['wuku']})
        return res_list

class KaTikaOtonan:
    def __init__(self, astro, cal, wew, sasih):
        self.astro = astro; self.cal = cal; self.wew = wew; self.sasih = sasih

    def hitung(self, tgl):
        cnt = (tgl - self.astro.anchor_date).days
        c = self.cal.get_calendar(cnt); w = self.wew.get_wewaran_lengkap(cnt)
        s = self.sasih.get_sasih_info((cnt // 3) + 1, c['wuku_index'])
        return {
            "weton": f"{c['sapta']} {c['panca']} {c['wuku']}", 
            "sasih": s['sasih_label'], "lintang": w['lintang_nama'], 
            "watak": f"{w['watak_sapta']}. {w['watak_panca']}",
            "urip": w['total_urip']
        }

# ==========================================
# 5. DASHBOARD UI (BALI MODERN)
# ==========================================
st.set_page_config(page_title="Ka-Tika Wangsa Agra", page_icon="🔆", layout="centered")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Inter:wght@300;400;600&display=swap');
    .header-box { text-align: center; font-family: 'Cinzel', serif; padding: 20px 0; }
    .header-mid { font-size: 42px; font-weight: 700; color: #1a1a1a; margin: 0; }
    .header-sub { font-size: 16px; letter-spacing: 6px; color: #c5a059; margin-top: -5px; }
    .sapta-wara { font-size: 80px; font-weight: 800; text-align: center; color: #2d2d2d; line-height: 1; margin: 10px 0;}
    .tri-panca { font-size: 22px; text-align: center; color: #5e5e5e; letter-spacing: 3px; }
    .widget-box { background: white; border: 1px solid #eee; border-radius: 12px; padding: 15px; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.02);}
</style>
""", unsafe_allow_html=True)

# Initialize
astro = KaTikaAstronomy(); cal = KaTikaCalendar(); wew = KaTikaWewaran()
sas = KaTikaSasih(); rai = KaTikaRainan()
dew = KaTikaPadewasan(cal, wew, astro); oto = KaTikaOtonan(astro, cal, wew, sas)

# Sidebar
with st.sidebar:
    st.title("🎛️ Navigasi")
    mode = st.radio("Mode Operasi", ["⏱️ Realtime", "📅 Cari Tanggal"])
    if mode == "⏱️ Realtime":
        t_ref = datetime.datetime.now(astro.tz)
    else:
        t_ref = astro.tz.localize(datetime.datetime.combine(st.date_input("Pilih Tanggal"), datetime.time(12, 0)))
    dina = astro.get_dina_status(t_ref)

# Perform Calculations
c_d = cal.get_calendar(dina['rahina_counter'])
w_d = wew.get_wewaran_lengkap(dina['rahina_counter'])
s_d = sas.get_sasih_info(dina['dina_id_global'], c_d['wuku_index'])
rains = rai.get_rainan(c_d['wuku_index'], w_d['sapta_idx'], w_d['panca_idx'], w_d['tri'])

# HEADER
st.markdown(f'''
<div class="header-box">
    <div style="font-size:12px; letter-spacing:4px; color:#8b7355">KALENDER</div>
    <div class="header-mid">KA-TIKA</div>
    <div class="header-sub">WANGSA AGRA</div>
</div>
''', unsafe_allow_html=True)

if rains: st.success(f"✨ {' • '.join(rains)} ✨")

# HERO SECTION
st.markdown(f'<div class="tri-panca">{w_d["tri"].upper()} — {c_d["panca"].upper()}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="sapta-wara">{c_d["sapta"].upper()}</div>', unsafe_allow_html=True)
st.markdown(f'<div style="text-align:center; color:#9a9a9a; font-size:14px; margin-bottom:20px;">Dina: {dina["range_masehi"]}</div>', unsafe_allow_html=True)

# WIDGETS
cw1, cw2 = st.columns(2)
with cw1: st.markdown(f'<div class="widget-box"><div style="font-size:30px">🌙</div><div style="font-size:11px; color:#8b7355">SITUASI BULAN</div><div style="font-size:15px; font-weight:600">{s_d["status"]}</div></div>', unsafe_allow_html=True)
with cw2: st.markdown(f'<div class="widget-box"><div style="font-size:30px">☀️</div><div style="font-size:11px; color:#8b7355">POSISI LINTANG</div><div style="font-size:15px; font-weight:600">{dina["posisi_ls"]}</div></div>', unsafe_allow_html=True)

# NAV TABS
tab_h, tab_w, tab_d, tab_r = st.tabs(["🏠 HOME", "👶 WETON", "🌺 DEWASA AYU", "📅 RAINAN"])

with tab_h:
    st.markdown("---")
    m1, m2, m3 = st.columns(3)
    m1.metric("Wuku", c_d['wuku'])
    m2.metric("Sasih", s_d['sasih_label'])
    m3.metric("Urip", w_d['total_urip'])
    st.info(f"Keterangan Sasih: Posisi **{s_d['status_wariga']}** (Dina ke-{s_d['dina_lokal']})")

with tab_w:
    t_l = st.date_input("Input Tanggal Lahir", datetime.date(1995, 1, 1))
    if st.button("Proses Weton & Watak"):
        res = oto.hitung(t_l)
        st.markdown(f"""
        <div style="background-color:#f3e5f5; padding:20px; border-radius:15px; border:2px solid #ce93d8; text-align:center;">
            <h2 style="color:#4a148c;">{res['weton']}</h2>
            <p>Sasih: {res['sasih']} | Urip: {res['urip']} | Lintang: {res['lintang']}</p>
            <hr>
            <p><i>{res['watak']}</i></p>
        </div>
        """, unsafe_allow_html=True)

with tab_d:
    cat = st.selectbox("Pilih Kategori", ["nikah", "bangun", "tani"])
    cb1, cb2 = st.columns(2)
    b_s = cb1.selectbox("Bulan", list(range(1, 13)))
    t_s = cb2.number_input("Tahun", 2026, 2030)
    if st.button("Cari Hari Baik"):
        st.table(dew.find_monthly(cat, b_s, t_s))

with tab_r:
    st.write("Daftar Hari Raya Terdeteksi:")
    if rains:
        for r in rains: st.write(f"• {r}")
    else:
        st.write("Tidak ada hari raya besar pada tanggal pilihan.")