# Türkçe NER (Named Entity Recognition) Maskeleme Sistemi

Bu proje, Türkçe metinlerdeki kişi adları, soyadları ve kullanıcı adlarını tespit edip maskeleyen güçlü bir sistemdir. Türkçe dilinin ekler, çekim ekleri ve birleşik kelimeler gibi karmaşık yapılarını ele alır.

## 🌟 Özellikler

- Kişi adları, soyadları ve kullanıcı adlarını tespit edip maskeleme
- Türkçe dil eklerini ve çekim eklerini işleme
- Bağlam-duyarlı tespit için BERT-tabanlı NER modeli kullanımı
- E-posta adreslerini koruma
- Modüler ve sürdürülebilir kod yapısı
- Kapsamlı test senaryoları

## 🛠️ Kurulum

1. Projeyi klonlayın:
```bash
git clone <repository-url>
cd turkish-ner-masker
```

2. Sanal ortam oluşturun ve aktifleştirin:
```bash
python -m venv venv
# Windows için:
venv\Scripts\activate
# Linux/Mac için:
source venv/bin/activate
```

3. Bağımlılıkları yükleyin:
```bash
pip install -r requirements.txt
```

4. Veritabanı kimlik bilgileri için `.env` dosyası oluşturun:
```env
DB_NAME=veritabani_adi
DB_USER=kullanici_adi
DB_PASSWORD=sifre
DB_HOST=sunucu_adresi
DB_PORT=5432

TRAINING_DB_NAME=egitim_veritabani_adi
TRAINING_DB_USER=egitim_kullanici_adi
TRAINING_DB_PASSWORD=egitim_sifresi
TRAINING_DB_HOST=egitim_sunucu_adresi
TRAINING_DB_PORT=5432
```

## 📚 Proje Yapısı

```
turkish-ner-masker/
├── src/
│   ├── __init__.py
│   ├── database.py      # Veritabanı bağlantı işlemleri
│   ├── masking.py       # Ana maskeleme fonksiyonları
│   ├── ner_model.py     # NER model entegrasyonu
│   └── text_processor.py # Metin işleme araçları
├── tests/              # Test dosyaları
│   └── tester.py       # Test senaryoları
├── main.py              # Ana giriş noktası
├── requirements.txt     # Proje bağımlılıkları
├── .env                # Ortam değişkenleri (git'te yok)
├── .gitignore         # Git yoksayma kuralları
└── README.md          # Proje dokümantasyonu
```

## 🚀 Kullanım

### 1. Programı Çalıştırma
```bash
# Ana programı çalıştır
python main.py

```

### 2. Kod Örneği
```python
from src.database import get_training_data, get_people_data
from src.masking import NameMasker

# Veritabanından verileri al
training_data = get_training_data()
people_data = get_people_data()

# Maskeleme nesnesini oluştur
name_list = people_data['name'].tolist()
surname_list = people_data['surname'].tolist()
username_list = people_data['username'].tolist()

masker = NameMasker(name_list, surname_list, username_list)

# Metni maskele
text = "Ahmet Yılmaz'a geçen hafta atanan arızaların listesi nedir?"
masked_text, original_text, masked_words = masker.mask_named_entities(text)

print(f"Orijinal: {original_text}")
print(f"Maskelenmiş: {masked_text}")
print("Maskelenen Kelimeler:", masked_words)
```

## 🧪 Test Etme

Projenin test senaryolarını çalıştırmak için:

```bash
# Test dosyasını çalıştır
python tests/tester.py
```

Test dosyası isim maskeleme, e-posta koruma ve kullanıcı adı maskeleme işlemlerinin doğru çalışıp çalışmadığını kontrol eder.

## 🧠 Nasıl Çalışır

# Türkçe NER Maskeleme Kodunun Akış Mantığı

## 🎯 Genel Amaç
Bu kod, Türkçe metinlerdeki **kişi adları**, **soyadları** ve **kullanıcı adlarını** otomatik olarak tespit edip `{name}`, `{surname}`, `{kullanici_adi}` şeklinde maskeleyen bir sistemdir. Özellikle Türkçe dil yapısının karmaşıklığını (ekler, çekim vs.) dikkate alarak çalışır.

---

## 📊 Ana Fonksiyon: `mask_named_entities_name_surname()`

### 🔄 **ADIM 1: Giriş Kontrolü ve Hazırlık**
```python
# Metin boş mu kontrol et
if not text or not isinstance(text, str):
    return [text, text, {}]

# Sonuç sözlüğünü hazırla
masked_words_dict = {
    'kullanici_adi': [],
    'name': [],
    'surname': []
}
```

### 🔄 **ADIM 2: Veri Listelerini Hazırla**
DataFrame'den üç liste çıkarır:
- `name_list`: İsimler listesi
- `surname_list`: Soyadlar listesi  
- `username_list`: Kullanıcı adları listesi

### 🔄 **ADIM 3: E-posta Koruma Sistemi**
```python
# E-postaları geçici placeholder'larla değiştir
# Örnek: "ali@gmail.com" → "{EMAIL0}"
```
**Neden?** E-postalar maskeleme sırasında bozulmasın diye koruma altına alınır.

### 🔄 **ADIM 4: Kullanıcı Adı Maskeleme**
`mask_usernames()` fonksiyonu çağrılır:
- Regex ile tam kelime eşleşmesi arar
- Bulunanları `{kullanici_adi}` ile değiştirir
- E-posta koruması devam eder

### 🔄 **ADIM 5: Gelişmiş İsim/Soyad Maskeleme**
`enhanced_fallback_name_mask()` fonksiyonu - **EN KARMAŞIK KISIM**

### 🔄 **ADIM 6: NER Model Desteği**
`analyze_with_ner()` fonksiyonu:
- BERT tabanlı Türkçe NER modeli kullanır
- Kalan isimleri yakalar
- Bağlamsal analiz yapar

### 🔄 **ADIM 7: Son Temizlik**
- E-postaları geri yerleştirir
- Çift boşlukları temizler
- Duplicate maskelenen kelimeleri kaldırır

---

## 🧠 Gelişmiş İsim/Soyad Maskeleme Detayı

### `enhanced_fallback_name_mask()` Fonksiyonu

#### **Döngü Yapısı:**
```python
words = text.split()
i = 0
while i < len(words):
    # Her kelimeyi kontrol et
```

#### **Her Kelime İçin Yapılan İşler:**

1. **Zaten Maskelenmiş mi?**
   ```python
   if words[i].startswith('{') and words[i].endswith('}'):
       continue  # Atla
   ```

2. **En İyi Kombinasyonu Bul**
   ```python
   found_combination = find_best_name_surname_combination(words, i, name_list, surname_list)
   ```

3. **Fiil Kontrolü**
   ```python
   if is_verb_or_common_word(first_word, name_list + surname_list):
       continue  # Fiilse atla
   ```

4. **Maskeleme Yap**
   ```python
   mask_parts = []
   if name_part:
       mask_parts.append("{name}")
   if surname_part:
       mask_parts.append("{surname}")
   ```

---

## 🔍 En İyi Kombinasyon Bulma Algoritması

### `find_best_name_surname_combination()` Fonksiyonu

#### **Çalışma Mantığı:**
```python
# Maksimum 6 kelimeye kadar dene
for end_idx in range(start_idx, start_idx + max_words):
    phrase = ' '.join(words[start_idx:end_idx + 1])
    
    # Ekleri temizle
    clean_last_word, suffix = strip_turkish_suffixes(last_word)
    
    # Kombinasyonları dene
    combination = try_name_surname_combinations(clean_phrase, name_list, surname_list)
```

#### **Skorlama Sistemi:**
- **Tam eşleşme**: 100 puan
- **İsim+Soyad**: 50 + kelime sayısı × 5
- **Sadece isim/soyad**: 20 + kelime sayısı × 3
- **Kısmi eşleşme**: 10-15 puan

### 📊 Skorlama Sistemi Örneği

Sistemin nasıl çalıştığını somut bir örnek üzerinden inceleyelim:

Örnek metin: `"Mehmet Ali Yılmaz'a mesaj at"`

**1. Tek Tek Kelime Kontrolü:**
```
"Mehmet"
- İsim listesinde: EVET ✓
- Puan: 23 puan

"Ali"
- İsim listesinde: EVET ✓
- Puan: 23 puan

"Yılmaz"
- Soyad listesinde: EVET ✓
- Puan: 23 puan
```

**2. İkili Kombinasyon Kontrolü:**
```
"Mehmet Ali"
- İsim listesinde birlikte var mı? EVET ✓
- TAM EŞLEŞME: 100 puan ⭐ (En yüksek puan)

"Ali Yılmaz"
- İsim + Soyad: 60 puan
```

**3. Üçlü Kombinasyon Kontrolü:**
```
"Mehmet Ali Yılmaz"
- Puan: 50 + (3 kelime × 5) = 65 puan
```

**4. Karar ve Sonuç:**
```
En yüksek puan: "Mehmet Ali" (100 puan, çünkü tam eşleşme)

Sistem şöyle maskeler:
"Mehmet Ali Yılmaz'a mesaj at"
      ↓
"{name} {surname}'a mesaj at"

Burada:
- "Mehmet Ali" -> {name} olarak maskelenir (birlikte)
- "Yılmaz" -> {surname} olarak maskelenir
```

**Neden Böyle Çalışır?**
- Birleşik isimler ("Mehmet Ali" gibi) tam eşleşme durumunda en yüksek puanı alır (100)
- İsim + Soyad kombinasyonları ikinci en yüksek puanı alır (50 + kelime sayısı × 5)
- Tek kelimelik isimler en düşük puanı alır (20 + kelime sayısı × 3)
- Sistem her zaman en yüksek puanlı kombinasyonu seçer
- Bu sayede birleşik isimler ve soyadlar doğru şekilde tespit edilir

---

## 🎯 Kombinasyon Deneme Stratejileri

### `try_name_surname_combinations()` Fonksiyonu

#### **1. Tek Kelime Durumu:**
```python
if len(words) == 1:
    name_match = any(word.lower() == n.lower() for n in name_list)
    surname_match = any(word.lower() == s.lower() for s in surname_list)
    
    if name_match and surname_match:
        return (word, None, 10)  # Name öncelikli
```

#### **2. Çok Kelimeli Durumlar:**

**A) Tam Eşleşme (En Yüksek Öncelik)**
```python
full_phrase = ' '.join(words)
if full_phrase in name_list:
    return (full_phrase, None, 100)
```

**B) Parçalı Kombinasyonlar**
```python
for split_point in range(1, len(words)):
    name_candidate = ' '.join(words[:split_point])
    surname_candidate = ' '.join(words[split_point:])
    
    # İkisi de eşleşirse
    if name_match and surname_match:
        score = 50 + len(words) * 5
```

**C) Kısmi Eşleşme**
```python
# En az bir kelimenin listede olması
name_words = [w for w in words if w in name_list]
surname_words = [w for w in words if w in surname_list]
```

---

## 🛠️ Yardımcı Fonksiyonlar

### 1. `strip_turkish_suffixes()`
**Amaç:** Türkçe ekleri temizler
```python
# "Ahmet'e" → ("Ahmet", "'e")
# "kitabından" → ("kitab", "ından")
```

**Çalışma Mantığı:**
- 40+ Türkçe ek listesi
- En uzun eşleşen eki bulur
- Kelimeyi ek+kök olarak ayırır

### 2. `is_verb_or_common_word()`
**Amaç:** Fiil köklerini tespit eder
```python
# "ulaştı" → True (fiil)
# "Ulaş" → False (isim listesindeyse)
```

**Mantık:**
- 70+ fiil kökü listesi
- Kelimenin fiil köküyle başlayıp başlamadığını kontrol eder
- İsim listesinde varsa isim öncelikli

### 3. `is_name_in_context()`
**Amaç:** BERT ile bağlamsal analiz
- Kelime etrafından 100 karakter bağlam alır
- NER modeline gönderir
- PER (Person) entity'si mi kontrol eder

---

## 🤖 NER Model Entegrasyonu

### `analyze_with_ner()` Fonksiyonu

#### **Çalışma Adımları:**

1. **Model Yükleme**
   ```python
   model = load_ner_model()  # Global değişken
   ```

2. **Entity Tespit**
   ```python
   entities = model(text)
   person_entities = [e for e in entities if e['entity_group'] == 'PER']
   ```

3. **Uzunluk Sıralama**
   ```python
   # Uzun entity'leri önce işle (çakışmayı önlemek için)
   person_entities.sort(key=lambda x: x['end'] - x['start'], reverse=True)
   ```

4. **Entity Analizi**
   ```python
   for entity in person_entities:
       entity_text = text[start:end].strip()
       
       # Çok kelimeli mi?
       if len(parts) > 1:
           # İsim+soyad kombinasyonu dene
       else:
           # Tek kelime - ek kontrolü yap
   ```

---

## 📈 Akış Şeması Özeti

```
TEXT GİRİŞİ
    ↓
E-POSTA KORUMA
    ↓
KULLANICI ADI MASKELEME
    ↓
GELİŞMİŞ İSİM/SOYAD MASKELEME
├── Her kelime için kombinasyon ara
├── Türkçe ek temizleme
├── Fiil kontrolü
├── Skorlama sistemi
└── En iyi eşleşmeyi seç
    ↓
NER MODEL DESTEĞİ
├── BERT tabanlı analiz
├── PER entity tespiti
└── Kaçan isimleri yakala
    ↓
SON TEMİZLİK
├── E-posta geri yerleştirme
├── Boşluk düzenleme
└── Duplicate temizleme
    ↓
SONUÇ: [ORİJİNAL, MASKELENMİŞ, SÖZLÜK]
```

---

## 🎯 Sistemin Güçlü Yanları

1. **Türkçe Ek Desteği**: "'e", "'den", "'nın" gibi ekleri handle eder
2. **Çok Katmanlı Yaklaşım**: Regex + Rule-based + NER model
3. **Skorlama Sistemi**: En iyi eşleşmeyi akıllıca seçer
4. **Fiil Kontrolü**: "ulaştı" gibi fiilleri isim sanmaz
5. **Bağlam Koruma**: E-postalar ve diğer veriler korunur
6. **Kombinasyon Desteği**: "Ahmet Can Yılmaz" gibi karmaşık isimleri handle eder

## ⚠️ Sistemin Zayıf Yanları

1. **Performans**: Her kelime için çoklu algoritma çalışır
2. **Dil Bağımlılığı**: Sadece Türkçe için optimize edilmiş
3. **Model Bağımlılığı**: NER model yüklenemezse kısmi çalışır
4. **Karmaşıklık**: Çok fazla nested fonksiyon ve mantık

## 🔍 Test Senaryoları

Proje, çeşitli senaryoları kapsayan kapsamlı test durumları içerir:

1. Basit isim maskeleme:
   - Girdi: "ahmete geçen hafta atanan arızaların listesi nedir?"
   - Çıktı: "{name}'e geçen hafta atanan arızaların listesi nedir?"

2. Birleşik isimler:
   - Girdi: "Merve Melisa Ezgi Erdoğan Yılmaz'a geçen hafta atanan arızaların listesi nedir?"
   - Çıktı: "{name} {surname}'a geçen hafta atanan arızaların listesi nedir?"

3. E-posta koruma:
   - Girdi: "zeynep'in email adresi 'zeynep.uzun@example.com' olan kişinin çözdüğü arızalar nelerdir?"
   - Çıktı: "{name}'in email adresi 'zeynep.uzun@example.com' olan kişinin çözdüğü arızalar nelerdir?"

4. Kullanıcı adı maskeleme:
   - Girdi: 'kullanıcı adı "ali.kaya" olan kişinin çözümlediği arızalar nelerdir?'
   - Çıktı: 'kullanıcı adı "{kullanici_adi}" olan kişinin çözümlediği arızalar nelerdir?'

## 📝 Lisans

Bu proje MIT Lisansı altında lisanslanmıştır - detaylar için LICENSE dosyasına bakınız.

## 🙏 Teşekkürler

- BERT Türkçe NER modeli için [akdeniz27](https://huggingface.co/akdeniz27/bert-base-turkish-cased-ner)'ye
