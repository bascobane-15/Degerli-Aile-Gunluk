import streamlit as st
import pandas as pd
import random
from datetime import datetime
from streamlit_gsheets import GSheetsConnection # Bunu 5. satıra ekle

# --- GOOGLE SHEETS BAĞLANTISI  ---
conn = st.connection("gsheets", type=GSheetsConnection)
def veriyi_tabloya_yaz(yeni_veri):
    try:
        # Mevcut veriyi oku
        existing_data = conn.read(spreadsheet=st.secrets["connections"]["gsheets"]["spreadsheet"], worksheet="Sayfa1")
        # Yeni veriyi ekle
        updated_df = pd.concat([existing_data, pd.DataFrame([yeni_veri])], ignore_index=True)
        # Tabloyu güncelle
        conn.update(spreadsheet=st.secrets["connections"]["gsheets"]["spreadsheet"], worksheet="Sayfa1", data=updated_df)
    except Exception as e:
        st.error(f"Veri kaydedilirken bir hata oluştu: {e}")
# 1. Veri Seti: Değerler ve Görev Havuzu
gorev_havuzu = {
    "Yardımlaşma": [
        "Bugün evde senin sorumluluğunda olmayan bir işi (sofra kurmak, çiçek sulamak vb.) 'görünmez kahraman' olarak tamamla.",
        "Aile üyelerinden birine 'Bugün senin için ne yapabilirim?' diye sor ve bir isteğini yerine getir.",
        "Evdeki ortak kullanım alanlarından birini (kitaplık, ayakkabılık vb.) kimse söylemeden düzenle."
    ],
    "Saygı & Vefa": [
        "Bir aile büyüğüne (dede, anneanne vb.) telefon aç veya yanına git; ona en sevdiği çocukluk oyuncağını sor.",
        "Akşam yemeği saati boyunca telefonunu tamamen başka bir odada bırakarak aileyle vakit geçir.",
        "Bugün aile üyelerine karşı 'Teşekkür ederim' ve 'Rica ederim' kelimelerini her fırsatta kullanmaya özen göster."
    ],
    "Empati": [
        "Bugün evdeki birinin yerine kendini koy ve onun gün içinde en çok yorulduğu anı fark edip ona teşekkür et.",
        "Bir aile üyesinin sevdiği bir müziği veya hikayeyi, yargılamadan onunla birlikte dinle.",
        "Karşındaki bir şey anlatırken sözünü kesmeden, sadece dinleyerek onun duygusunu anlamaya çalış."
    ],
    "Dürüstlük": [
        "Bugün yaptığın küçük bir hatayı (bir şeyi unutmak, geç kalmak vb.) saklamadan dürüstçe paylaş.",
        "Bir aile üyesine, onun dürüst davranmasının sana ne kadar güven verdiğini söyle.",
        "Verdiğin bir sözü (küçük de olsa) bugün tam vaktinde ve eksiksiz yerine getir."
    ],
    "Sorumluluk": [
        "Bugün kendi odanı ve çalışma masanı hiç hatırlatılmadan, en düzenli haline getir.",
        "Evde tasarruf etmek için (gereksiz ışıkları söndürmek, suyu dikkatli kullanmak vb.) bir 'enerji nöbetçisi' ol.",
        "Bugün okul veya iş çantanı/eşyalarını bir sonraki gün için akşamdan eksiksiz hazırla."
    ],
    "Sabır": [
        "Bugün evde seni bekleten veya biraz sinirlendiren bir duruma karşı derin bir nefes alıp gülümseyerek karşılık ver.",
        "Sıra beklediğin veya bir şeyin olmasını istediğin bir anda içinden 10'a kadar sayarak sakin kalma alıştırması yap.",
        "Bugün bir teknolojik cihazın (oyun, sosyal medya vb.) başında geçirdiğin süreyi sabrederek 15 dakika azalt."
    ],
    "Adalet & Paylaşma": [
        "Evdeki bir imkanı (televizyon kumandası, atıştırmalık paylaşımı vb.) kendi isteğinden önce başkasının hakkını gözeterek kullan.",
        "Bugün sevdiğin bir eşyanı veya bir yiyeceğini aile üyelerinden biriyle isteyerek paylaş.",
        "Aile içinde bir karar alınırken herkesin fikrini söyleyebilmesi için ortam oluştur veya kardeşinin hakkını savun."
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
    st.header("🔑 Giriş Bilgileri")
    aile_kodu = st.text_input("Aile Kodunuz (Örn: AILE01):") # Bunu yeni ekliyoruz
    aile_uyesi = st.text_input("Adınız:", placeholder="Örn: Tuğçe")
    secilen_deger = st.selectbox("Bu Haftanın Değeri:", list(gorev_havuzu.keys()))
        
    if st.button("🎰 Günün Görevini Çek"):
        st.session_state.gunun_gorevi = random.choice(gorev_havuzu[secilen_deger])

# --- ANA PANEL: Görev Ekranı ---
col1, col2 = st.columns([2, 1])

with col1:
    st.info(f"**Mevcut Odak:** {secilen_deger}")
 
    if 'gunun_gorevi' in st.session_state:
        st.success(f"### 🎯 Görevin:\n {st.session_state.gunun_gorevi}")
        
        if st.button("✅ Görevi Tamamladım!"):
           if aile_kodu and aile_uyesi: # Kod ve isim boş değilse
                yeni_kayit = {
                     "Tarih": datetime.now().strftime("%Y-%m-%d %H:%M"),
                     "Aile_Kodu": aile_kodu,
                     "Üye": aile_uyesi,
                     "Değer": secilen_deger,
                     "Görev": st.session_state.gunun_gorevi
                 }
            
                veriyi_tabloya_yaz(yeni_kayit) 
                st.success("Tebrikler! Göreviniz başarıyla kaydedildi.")
                st.balloons()
                
            else:
                st.error("Lütfen önce Aile Kodunuzu ve Adınızı giriniz!")

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
