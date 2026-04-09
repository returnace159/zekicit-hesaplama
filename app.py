import streamlit as st

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Çit Metraj Paneli", layout="centered")

# --- CSS: BEYAZ BARLARI VE BOŞLUKLARI KÖKTEN SİLME ---
st.markdown("""
    <style>
    /* Ana konteyner boşluklarını sıfırla */
    .block-container { padding-top: 1rem !important; padding-bottom: 0rem !important; }
    
    /* Başlık ve kutu arasına sızan beyazlıkları kapat */
    .ana-baslik { font-size:38px !important; font-weight: bold; color: #E74C3C; text-align: center; margin-bottom: -10px; }
    
    /* Kutuların arasındaki boşlukları (gap) öldür */
    [data-testid="stVerticalBlock"] > div { gap: 0.1rem !important; }
    
    /* Elemanların alt boşluklarını daralt */
    div[data-baseweb="input"], .stSelectbox { margin-bottom: -10px; }
    
    .kutu { background-color: #f8f9fa; padding: 15px 25px; border-radius: 15px; border: 2px solid #dee2e6; margin-bottom: 5px; }
    .buyuk-yazi { font-size:22px !important; font-weight: bold; color: #2C3E50; margin-bottom: 5px; }
    .fiyat-yazi { font-size:50px !important; color: #27AE60; font-weight: bold; margin: 5px 0px; }
    
    /* Header ve gereksiz Streamlit öğelerini gizle */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="ana-baslik">🚧 ZEKİ ÇİT HESAPLAMA</p>', unsafe_allow_html=True)

# --- 1. GİRDİ ALANI ---
with st.container():
    st.markdown('<div class="kutu">', unsafe_allow_html=True)
    st.markdown('<p class="buyuk-yazi">📏 Bahçe ve Fiyat Bilgileri</p>', unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        uzun_kenar = st.number_input("Uzun Kenar (m)", value=30.0, step=1.0)
        h_yukseklik = st.number_input("Tel Yüksekliği (m)", value=1.5, step=0.1)
    with c2:
        kisa_kenar = st.number_input("Kısa Kenar (m)", value=12.0, step=1.0)
        birim_fiyat = st.number_input("m² Birim Fiyat (TL)", value=50.0, step=1.0)
    
    c3, c4 = st.columns(2)
    with c3:
        gergi_sirasi = st.number_input("Gergi Teli Sırası", value=3, step=1)
    with c4:
        kar_orani = st.number_input("Kâr Oranı (%)", value=30, step=1)
    st.markdown('</div>', unsafe_allow_html=True)

# --- 2. HESAPLAMA MOTORU ---
# Çevre hesabı
cevre = (uzun_kenar + kisa_kenar) * 2

# Rulo Hesabı (1 Top = 20 Metre)
rulo_lazim = -(-cevre // 20) 

# Alan ve Gergi Hesabı
toplam_m2 = cevre * h_yukseklik
toplam_gergi = cevre * gergi_sirasi

# Maliyet ve Satış
maliyet = toplam_m2 * birim_fiyat
satis = maliyet * (1 + kar_orani/100)

# --- 3. SONUÇ EKRANI ---
st.markdown('<div class="kutu">', unsafe_allow_html=True)
st.markdown('<p class="buyuk-yazi">📋 İş Listesi ve Malzeme</p>', unsafe_allow_html=True)

col_sol, col_sag = st.columns(2)
with col_sol:
    st.success(f"📏 Metraj: **{cevre}m**")
    st.success(f"📦 Rulo: **{int(rulo_lazim)} Top**")
with col_sag:
    st.info(f"📐 Alan: **{toplam_m2:.1f} m²**")
    st.info(f"⛓️ Gergi: **{toplam_gergi}m**")
st.markdown('</div>', unsafe_allow_html=True)

# --- 4. FİYAT KUTUSU ---
st.markdown(f'''
    <div class="kutu" style="text-align:center; border: 3px solid #27AE60; background-color: #f0fff4;">
        <p style="margin:0; font-weight:bold; color:#2C3E50;">💰 MÜŞTERİYE VERİLECEK TEKLİF</p>
        <p class="fiyat-yazi">{satis:,.2f} TL</p>
        <p style="margin:0; color:#555;">Maliyet: {maliyet:,.2f} TL | Net Kâr: {satis-maliyet:,.2f} TL</p>
    </div>
    ''', unsafe_allow_html=True)

st.caption("Not: Rulo hesabı 20 metrelik toplar üzerinden otomatik yukarı yuvarlanmıştır.")
