# Türkçe NER (Named Entity Recognition) Maskeleme Sistemi

## 📌 Genel Amaç
Bu kod, Türkçe metinlerdeki **kişi adları**, **soyadları** ve **kullanıcı adlarını** otomatik olarak tespit edip `{name}`, `{surname}`, `{kullanici_adi}` şeklinde maskeleyen bir sistemdir. Özellikle Türkçe dil yapısının karmaşıklığını (ekler, çekim vs.) dikkate alarak çalışır.

## 🌟 Özellikler
- Kişi adları, soyadları ve kullanıcı adlarını tespit edip maskeleme
- Türkçe dil eklerini ve çekim eklerini işleme
- Bağlam-duyarlı tespit için BERT-tabanlı NER modeli kullanımı
- E-posta adreslerini koruma
- Modüler ve sürdürülebilir kod yapısı
- Kapsamlı test senaryoları

## 🚀 Hızlı Başlangıç

### 1. Kurulum
```bash
# Projeyi klonla
git clone <repository-url>
cd turkish-ner-masker

# Sanal ortam oluştur ve aktifleştir
python -m venv venv
# Windows için:
venv\Scripts\activate
# Linux/Mac için:
source venv/bin/activate

# Bağımlılıkları yükle
pip install -r requirements.txt
```

### 2. Veritabanı Yapılandırması
Projenin kök dizininde `.env` dosyası oluşturun ve aşağıdaki bilgileri ekleyin:

#### Veritabanı Bilgileri
```env
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
```

### 3. Basit Kullanım
```python
from src.masking import NameMasker

# Maskeleme nesnesini oluştur
masker = NameMasker(name_list, surname_list, username_list)

# Metni maskele
text = "Ahmet Yılmaz'a geçen hafta atanan arızaların listesi nedir?"
masked_text, original_text, masked_words = masker.mask_named_entities(text)

print(f"Orijinal: {original_text}")
print(f"Maskelenmiş: {masked_text}")
print(f"Algılanan: {masked_words}")
```

### 4. Programı Çalıştırma
```bash
# Veritabanından isim, soyisim, kullanıcı adı ve metin verilerini çekerek maskeleme yapar.
python main.py
```

### 5. Hızlı Test
```bash
python tests/tester.py
```

## 🏗️ Sistem Mimarisi

### 1. Proje Yapısı
```
turkish-ner-masking/
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

### 2. Hibrit Yapı
Sistem, üç farklı yaklaşımı birleştirir:

#### a) Kural Tabanlı Bileşenler (%60):
- İsim ve soyisim listelerinde arama
- Türkçe ek (suffix) işleme
- Fiil kökleri kontrolü
- Zaman ifadeleri kontrolü
- Skor tabanlı karar verme

#### b) BERT Tabanlı NER (%30):
- Bağlamsal analiz
- Liste dışı isimleri tespit
- Semantik analiz

#### c) Pattern Matching (%10):
- Regex ile kelime eşleştirme
- String manipülasyonları

### 3. Akış Şeması
```
TEXT GİRİŞİ
    ↓
E-POSTA KORUMA
    ↓
KULLANICI ADI MASKELEME
    ↓
GELİŞMİŞ İSİM/SOYAD MASKELEME
    ↓
NER MODEL DESTEĞİ
    ↓
SON TEMİZLİK
    ↓
SONUÇ
```

## 📚 Detaylı Kullanım

### 1. Maskeleme Süreci
Sistem bir metni işlerken şu adımları takip eder:

#### a) E-posta Koruma
- E-posta adreslerini geçici olarak maskeler
- İşlem sonunda orijinal e-postaları geri yerleştirir

#### b) Kullanıcı Adı Maskeleme
- Veritabanındaki kullanıcı adlarını kontrol eder
- Eşleşenleri `{kullanici_adi}` ile maskeler

#### c) Kural Tabanlı İsim/Soyisim Tespiti
- İsim ve soyisim listelerinde arama yapar
- Türkçe ekleri analiz eder
- Bağlam kontrolü yapar

#### d) BERT NER Analizi
- Kural tabanlı sistemin bulamadığı isimleri arar
- Her kelime için 50 karakter öncesi ve sonrasını analiz eder
- Bağlamdan kişi isimlerini tespit eder

### 2. Bağlam Analizi
Sistem üç farklı seviyede bağlam analizi yapar:

#### a) Kural Tabanlı Bağlam Analizi:
- Zaman ifadelerini kontrol eder
- Fiil köklerini kontrol eder
- Edatları kontrol eder
- Noktalama işaretlerini analiz eder

#### b) BERT Bağlam Analizi:
- Kelimenin öncesi ve sonrasını inceler
- Semantik analiz yapar
- Entity tiplerini belirler

#### c) Skor Tabanlı Analiz:
- İsim-soyisim kombinasyonlarını puanlar
- Kelime uzunluklarını değerlendirir
- Bağlam ipuçlarına göre skor ayarlar

### 3. Metin İşleme ve Benzerlik Analizi
Sistem, metin işleme ve benzerlik analizi için Jellyfish kütüphanesini kullanmaktadır:

#### a) Jaro-Winkler Benzerlik Algoritması
- İsim ve soyisimlerin benzerlik oranını hesaplar
- Yazım hatalarına karşı toleranslıdır
- 0.95 eşik değeri ile çalışır
- Türkçe karakterleri destekler

#### b) Benzerlik Analizi Özellikleri
- Küçük yazım hatalarını tolere eder
- Türkçe karakterlerdeki farklılıkları analiz eder
- Yüksek doğruluk oranı ile çalışır
- Hızlı ve verimli işlem yapar

### 4. Skorlama Sistemi
- **Tam eşleşme**: 100 puan
- **İsim+Soyad**: 50 + kelime sayısı × 5
- **Sadece isim/soyad**: 20 + kelime sayısı × 3
- **Kısmi eşleşme**: 10-15 puan

#### 📊 Skorlama Sistemi Örneği

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

## 🔧 Teknik Detaylar

### 1. Ana Fonksiyonlar

#### `mask_named_entities()`
```python
def mask_named_entities(self, text: str) -> Tuple[str, str, Dict[str, List[str]]]:
    """Main function to mask named entities in text"""
    # ... fonksiyon detayları ...
```

#### `enhanced_fallback_name_mask()`
```python
def enhanced_fallback_name_mask(self, text: str) -> Tuple[str, Dict[str, List[str]]]:
    """Enhanced name/surname masking"""
    # ... fonksiyon detayları ...
```

### 2. Yardımcı Fonksiyonlar

#### `strip_turkish_suffixes()`
```python
def strip_turkish_suffixes(word: str) -> Tuple[str, str]:
    """Remove Turkish suffixes from a word"""
    # ... fonksiyon detayları ...
```

#### `is_verb_or_common_word()`
```python
def is_verb_or_common_word(word: str) -> bool:
    """Check if word is a verb root or common word"""
    # ... fonksiyon detayları ...
```

## 🚀 Performans ve Optimizasyon

### 1. Bellek Kullanımı
- Singleton pattern ile NER model yönetimi
- Verimli veri yapıları kullanımı
- Gereksiz kopya oluşturmaktan kaçınma

### 2. İşlem Süresi Optimizasyonu
- Önce basit kontroller
- Ağır işlemler (BERT) son çare
- Paralel işleme potansiyeli

### 3. Cache Stratejileri
- Sık kullanılan isimler için önbellek
- Model çıktılarının cachelenmesi
- Tekrarlı işlemlerin optimizasyonu

## 🔍 Test Senaryoları

Proje, çeşitli senaryoları kapsayan kapsamlı test durumları içerir:

### Test Örnekleri ve Maskeleme Sözlüğü

1. Basit isim maskeleme:
   - Girdi: "ahmete geçen hafta atanan arızaların listesi nedir?"
   - Çıktı: "{name}'e geçen hafta atanan arızaların listesi nedir?"
   - Sözlük:
     ```python
     {
         'name': ['ahmet'],      # İsim
         'surname': [],          # Soyisim yok
         'kullanici_adi': []     # Kullanıcı adı yok
     }
     ```

2. Birleşik isimler:
   - Girdi: "Merve Melisa Ezgi Erdoğan Yılmaz'a geçen hafta atanan arızaların listesi nedir?"
   - Çıktı: "{name} {surname}'a geçen hafta atanan arızaların listesi nedir?"
   - Sözlük:
     ```python
     {
         'name': ['merve melisa ezgi'],     # Birleşik isim
         'surname': ['erdoğan yılmaz'],     # Birleşik soyisim
         'kullanici_adi': []                # Kullanıcı adı yok
     }
     ```

3. E-posta koruma:
   - Girdi: "zeynep'in email adresi 'zeynep.uzun@example.com' olan kişinin çözdüğü arızalar nelerdir?"
   - Çıktı: "{name}'in email adresi 'zeynep.uzun@example.com' olan kişinin çözdüğü arızalar nelerdir?"
   - Sözlük:
     ```python
     {
         'name': ['zeynep'],     # İsim
         'surname': [],          # Soyisim yok
         'kullanici_adi': []     # Kullanıcı adı yok
     }
     ```

4. Kullanıcı adı maskeleme:
   - Girdi: 'kullanıcı adı "ali.kaya" olan kişinin çözümlediği arızalar nelerdir?'
   - Çıktı: 'kullanıcı adı "{kullanici_adi}" olan kişinin çözümlediği arızalar nelerdir?'
   - Sözlük:
     ```python
     {
         'name': [],                # İsim yok
         'surname': [],             # Soyisim yok
         'kullanici_adi': ['ali.kaya']  # Kullanıcı adı
     }
     ```

5. Karışık senaryo:
   - Girdi: "ali.demir kullanıcısı ve Ahmet Yılmaz'ın ortak çözdüğü arızalar nelerdir?"
   - Çıktı: "{kullanici_adi} kullanıcısı ve {name} {surname}'ın ortak çözdüğü arızalar nelerdir?"
   - Sözlük:
     ```python
     {
         'name': ['ahmet'],         # İsim
         'surname': ['yılmaz'],     # Soyisim
         'kullanici_adi': ['ali.demir']  # Kullanıcı adı
     }
     ```

### Maskeleme Türleri Açıklaması:
- **{name}**: Kişi isimleri (Örn: "ahmet", "merve melisa")
- **{surname}**: Kişi soyadları (Örn: "yılmaz", "erdoğan yılmaz")
- **{kullanici_adi}**: Sistem kullanıcı adları (Örn: "ali.kaya", "zeynep.demir")

### Önemli Notlar:
- İsimler ve soyadlar birleşik olabilir (Örn: "merve melisa", "erdoğan yılmaz")
- Kullanıcı adları genellikle "ad.soyad" formatındadır
- Türkçe karakterler korunur ve doğru şekilde işlenir
- Büyük/küçük harf duyarlılığı yoktur, tüm işlemler küçük harfe çevrilerek yapılır

## 🎯 Güçlü ve Zayıf Yanlar

### Güçlü Yanlar
1. Türkçe Ek Desteği
2. Çok Katmanlı Yaklaşım
3. Skorlama Sistemi
4. Fiil Kontrolü
5. Bağlam Koruma
6. Kombinasyon Desteği

### Zayıf Yanlar
1. Dil Bağımlılığı
2. Karmaşık Yapı
3. Yazım Hatalarına Duyarlılık

## 📄 Lisans
Bu proje MIT Lisansı altında lisanslanmıştır.

