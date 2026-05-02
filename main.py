import streamlit as st
import pandas as pd
import random
from datetime import datetime

# 1. Veri Seti: Değerler ve Görev Havuzu
gorev_havuzu = {
    "Yardımlaşma": [
        "Bugün sofrayı kurma/kaldırma görevini tek başına üstlen.",
        "Aile üyelerinden birine 'Senin için ne yapabilirim?' diye sor.",
        "Evdeki bitkileri sula veya evcil hayvanın bakımını yap."
    ],
    "Saygı & Vefa": [
        "Bir aile büyüğüne çocukluk anısını sor ve dikkatle dinle.",
        "Akşam yemeği boyunca telefonunu başka bir odada bırak.",
        "Bugün aile üyelerine 'Teşekkür ederim' ve 'Lütfen' demeye özen göster."
    ],
    "Empati": [
        "Bugün evdeki birinin yerine kendini koy ve onun en yorucu işini düşün.",
        "Bir aile üyesinin sevdiği bir müziği onunla birlikte dinle.",
        "Karşındakinin cümlesini kesmeden sonuna kadar dinleme alıştırması yap."
    ]
}

# 2. Sayfa Yapılandırması
st.set_page_config(page_title="Değerli Günlük", layout="wide")
st.title("🛡️ Dijital Köprüden Gönül Köprüsüne")
st.subheader("Değer Kartları ve Görev Kutusu")

# 3. Oturum Yönetimi (Verilerin Kaybolmaması İçin)
if 'tamamlanan_gorevler' not in st.session_state:
    st.session_state.tamamlanan_gorevler = []

# --- SOL PANEL: Değer Seçimi ---
with st.sidebar:
    st.header("⚙️ Ayarlar")
    secilen_deger = st.selectbox("Bu Haftanın Değeri:", list(gorev_havuzu.keys()))
    aile_uyesi = st.text_input("Adınız:", placeholder="Örn: Tuğçe")
    
    if st.button("🎰 Günün Görevini Çek"):
        st.session_state.gunun_gorevi = random.choice(gorev_havuzu[secilen_deger])

# --- ANA PANEL: Görev Ekranı ---
col1, col2 = st.columns([2, 1])

with col1:
    st.info(f"**Mevcut Odak:** {secilen_deger}")
    
    if 'gunun_gorevi' in st.session_state:
        st.success(f"### 🎯 Görevin:\n {st.session_state.gunun_gorevi}")
        
        if st.button("✅ Görevi Tamamladım!"):
            yeni_kayit = {
                "Tarih": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "Üye": aile_uyesi if aile_uyesi else "Anonim",
                "Değer": secilen_deger,
                "Görev": st.session_state.gunun_gorevi
            }
            st.session_state.tamamlanan_gorevler.append(yeni_kayit)
            st.balloons()
            st.write("Harikasın! Puanın hanene yazıldı.")
    else:
        st.warning("Henüz görev çekilmedi. Sol menüden görevini belirle!")

# --- İSTATİSTİK PANELİ: Digital Twin Altyapısı ---
with col2:
    st.write("📊 **Haftalık Gelişim**")
    if st.session_state.tamamlanan_gorevler:
        df = pd.DataFrame(st.session_state.tamamlanan_gorevler)
        # Değerlere göre görev sayılarını sayalım
        skorlar = df['Değer'].value_counts()
        st.bar_chart(skorlar)
    else:
        st.write("Henüz veri girişi yok.")

# --- ALT PANEL: Geçmiş Kayıtlar ---
st.divider()
st.write("📜 **Gönül Günlüğü (Tamamlanan Etkinlikler)**")
st.table(pd.DataFrame(st.session_state.tamamlanan_gorevler))