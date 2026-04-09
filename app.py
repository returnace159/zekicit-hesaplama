import streamlit as st
import plotly.graph_objects as go

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Çit Metraj Paneli", layout="centered")

# --- CSS: BEYAZ BARLARI KALDIRMA VE GÖRSEL SADAKAT ---
st.markdown("""
    <style>
    .ana-baslik { font-size:40px !important; font-weight: bold; color: #E74C3C; text-align: center; margin-bottom: 0px; }
    .kutu { background-color: #f8f9fa; padding: 20px; border-radius: 15px; border: 3px solid #dee2e6; margin-top: 10px; }
    .buyuk-yazi { font-size:24px !important; font-weight: bold; color: #2C3E50; margin-bottom: 5px; }
    .fiyat-yazi { font-size:50px !important; color: #27AE60; font-weight: bold; }
    /* Gereksiz boşlukları ve beyaz barları temizleyen kod */
    .stNumberInput, .stSelectbox, .stSlider { margin-bottom: -15px; }
    hr { margin-top: 5px; margin-bottom: 5px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="ana-baslik">🚧 ZEKİ ÇİT HESAPLAMA</p>', unsafe_allow_html=True)

# --- 1. VERİ MERKEZİ ---
tel_tipleri = {
    "1.5 Metre Yükseklik": {"h": 1.5, "gergi": 3, "fiyat": 50},
    "1.7 Metre Yükseklik": {"h": 1.7, "gergi": 3, "fiyat": 65},
    "2.0 Metre Yükseklik": {"h": 2.0, "gergi": 4, "fiyat": 80}
}

# --- 2. GİRDİ ALANI ---
with st.container():
    st.markdown('<div class="kutu">', unsafe_allow_html=True)
    st.markdown('<p class="buyuk-yazi">📏 Bahçe Ölçülerini Gir</p>', unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        uzun_kenar = st.number_input("Uzun Kenar (Metre)", value=30.0, step=1.0)
    with c2:
        kisa_kenar = st.number_input("Kısa Kenar (Metre)", value=12.0, step=1.0)
    
    secim = st.selectbox("Tel Boyu Seçiniz", list(tel_tipleri.keys()))
    # KAR ORANI: Artık elle girilebilir (%173 kâr hayırlı olsun kanka)
    kar_orani = st.number_input("Kâr Oranı (%)", value=30, step=1)
    st.markdown('</div>', unsafe_allow_html=True)

# --- 3. İZOMETRİK GÖRSELLEŞTİRME (PLOTLY) ---
def bahce_ciz(u, k):
    fig = go.Figure()
    # İzometrik kutu hatları
    fig.add_trace(go.Scatter3d(
        x=[0, u, u, 0, 0], y=[0, 0, k, k, 0], z=[0, 0, 0, 0, 0],
        mode='lines', line=dict(color='#E74C3C', width=10), name="Çit Hattı"
    ))
    # Köşe direkleri temsili
    fig.add_trace(go.Scatter3d(
        x=[0, u, u, 0], y=[0, 0, k, k], z=[0, 0, 0, 0],
        mode='markers', marker=dict(size=5, color='#2C3E50'), name="Direkler"
    ))
    fig.update_layout(
        scene=dict(
            xaxis=dict(visible=False), yaxis=dict(visible=False), zaxis=dict(visible=False),
            aspectmode='manual', aspectratio=dict(x=1, y=k/u if u>0 else 1, z=0.3)
        ),
        margin=dict(l=0, r=0, b=0, t=0), height=300, showlegend=False
    )
    return fig

st.plotly_chart(bahce_ciz(uzun_kenar, kisa_kenar), use_container_width=True)

# --- 4. HESAPLAMA MOTORU ---
cevre = (uzun_kenar + kisa_kenar) * 2
h = tel_tipleri[secim]["h"]
gergi_sirasi = tel_tipleri[secim]["gergi"]
birim_fiyat = tel_tipleri[secim]["fiyat"]
rulo_lazim = -(-cevre // 20) 
toplam_m2 = cevre * h
toplam_gergi = cevre * gergi_sirasi
maliyet = toplam_m2 * birim_fiyat
satis = maliyet * (1 + kar_orani/100)

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
