import streamlit as st

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Çit Metraj Paneli", layout="centered")

# --- DEV PUNTOLAR VE SADE ARAYÜZ STİLİ ---
st.markdown("""
    <style>
    .ana-baslik { font-size:40px !important; font-weight: bold; color: #E74C3C; text-align: center; }
    .kutu { background-color: #f8f9fa; padding: 25px; border-radius: 15px; border: 3px solid #dee2e6; margin-bottom: 20px; }
    .buyuk-yazi { font-size:24px !important; font-weight: bold; color: #2C3E50; }
    .fiyat-yazi { font-size:50px !important; color: #27AE60; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="ana-baslik">🚧 ZEKİ ÇİT HESAPLAMA</p>', unsafe_allow_html=True)

# --- 1. VERİ MERKEZİ (İLERİDE BURASI GENİŞLEYECEK) ---
tel_tipleri = {
    "1.5 Metre Yükseklik": {"h": 1.5, "gergi": 3, "fiyat": 50},  # Fiyatlar örnek, değiştirebilirsin
    "1.7 Metre Yükseklik": {"h": 1.7, "gergi": 3, "fiyat": 65},
    "2.0 Metre Yükseklik": {"h": 2.0, "gergi": 4, "fiyat": 80}
}

# --- 2. GİRDİ ALANI (İLKOKUL SEVİYESİNDE BASİT) ---
with st.container():
    st.markdown('<div class="kutu">', unsafe_allow_html=True)
    st.markdown('<p class="buyuk-yazi">📏 Bahçe Ölçülerini Gir</p>', unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        uzun_kenar = st.number_input("Uzun Kenar (Metre)", value=30.0, step=1.0)
    with c2:
        kisa_kenar = st.number_input("Kısa Kenar (Metre)", value=12.0, step=1.0)
    
    secim = st.selectbox("Tel Boyu Seçiniz", list(tel_tipleri.keys()))
    kar_orani = st.slider("Kâr Oranın (%)", 0, 100, 30)
    st.markdown('</div>', unsafe_allow_html=True)

# --- 3. HESAPLAMA MOTORU ---
# Çevre hesabı
cevre = (uzun_kenar + kisa_kenar) * 2

# Tel Özellikleri
h = tel_tipleri[secim]["h"]
gergi_sirasi = tel_tipleri[secim]["gergi"]
birim_fiyat = tel_tipleri[secim]["fiyat"]

# Rulo Hesabı (1 Top = 20 Metre)
rulo_lazim = -(-cevre // 20) 

# Alan ve Gergi Hesabı
toplam_m2 = cevre * h
toplam_gergi = cevre * gergi_sirasi

# Maliyet ve Satış
maliyet = toplam_m2 * birim_fiyat
satis = maliyet * (1 + kar_orani/100)

# --- 4. GELECEK MODÜLLER İÇİN YERLER (ŞİMDİLİK BOŞ) ---
# profil_maliyeti = 0  # SONRA EKLENECEK
# beton_maliyeti = 0   # SONRA EKLENECEK

# --- 5. SONUÇ EKRANI ---
st.markdown('<p class="buyuk-yazi">📋 İŞ LİSTESİ VE MALZEME</p>', unsafe_allow_html=True)

col_sol, col_sag = st.columns(2)
with col_sol:
    st.success(f"📏 Toplam Metraj: **{cevre} Metre**")
    st.success(f"📦 Alınacak Rulo: **{int(rulo_lazim)} Top**")

with col_sag:
    st.info(f"📐 Toplam Alan: **{toplam_m2:.2f} m²**")
    st.info(f"⛓️ Gergi Teli: **{toplam_gergi} Metre**")

st.markdown('<div class="kutu" style="text-align:center;">', unsafe_allow_html=True)
st.write("💰 **MÜŞTERİYE SÖYLENECEK TOPLAM FİYAT:**")
st.markdown(f'<p class="fiyat-yazi">{satis:,.2f} TL</p>', unsafe_allow_html=True)
st.write(f"Maliyet: {maliyet:,.2f} TL | Net Kârın: {satis-maliyet:,.2f} TL")
st.markdown('</div>', unsafe_allow_html=True)

st.caption("Not: Rulo hesabı 20 metrelik toplar üzerinden otomatik yukarı yuvarlanmıştır.")
