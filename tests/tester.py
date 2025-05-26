import pandas as pd
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.masking import NameMasker

def run_tests():
    # Test data
    name_list = ["Su","Melike","Caner","Erhan Avcı","Veli","Erhan","Ayşe","Halil","Cemal","Emine","Kadir","Zeynep","Emrah","Mustafa","Hasan","Mert","Aylin","Eda","Merve Melisa Ezgi","Yıldız","Muhammet","Yıldız","Deniz","Eda","Eda Su","Rıza",
                 "Ahmetcan","Sadık","Merve","Zeynep","Merve Melisa","Merve Melisa","Ahmet","Ulaş", "Ali", 
                 "Ahmet Can", "Mehmet", "Ayşe", "Melike", "Eda", "Büşra", "Sevim", "Merve", "Can Deniz", 
                 "Deniz", "Bekir Ali", "Can", "Deniz"]
    
    surname_list = ["Tekin","Akdere","Tunç","Yılmaz","Tunç","Avcı","Ramazan","Akca","Albora","Sandal","Kaya","Nur","Akça","Sanlı","Demir","Demir","Atamer","Karaca","Erdoğan Yılmaz","Muhammet","Yıldız","Deniz","Yıldız","Su Karaca","Karaca",
                    "Aydın","Akçakale","Turan","Demir Yılmaz","Bedir","Erdoğan","Yılmaz","Yılmaz","Ferit", 
                    "Demir", "Yılmaz", "Kaya Demir", "Demir", "Çelik", "Öztürk", "Salman", "Yılmaz", 
                    "Can Yılmaz", "Salman", "Demir Yılmaz", "Can Mert", "Alp", "Akça"]
    
    username_list = ["ayşe.ramazan","halil.akca","cemal.albora","emine.sandal","kadir.kaya","zeynep.nur","emrah.akca","mustafa.sanli","mert.demir","hasan.demir","aylin.atamer","eda.karaca",'can.salman', 'can.deniz.öztürk', 'ahmet.yılmaz', 'eda.demir', 
                     'büşra.çelik', "ali.kaya",'can.salman', 'can.deniz.öztürk', 'ahmet.yılmaz', 
                     'eda.demir', 'büşra.çelik', "ali.kaya",'can.salman', 'can.deniz.öztürk', 
                     'ahmet.yılmaz', 'eda.demir', 'büşra.çelik', "ali.kaya",'can.salman', 
                     'can.deniz.öztürk', 'ahmet.yılmaz', 'eda.demir', 'büşra.çelik', "ali.kaya",
                     'can.salman', 'can.deniz.öztürk', 'ahmet.yılmaz', 'eda.demir', 'büşra.çelik', 
                     "ali.kaya"]

    # Create masker instance
    masker = NameMasker(name_list, surname_list, username_list)

    # Test cases
    test_texts = [
        "ahmete geçen hafta atanan arızaların listesi nedir?",
        "ahmet'e geçen hafta atanan arızaların listesi nedir?",
        "Ahmet'e geçen hafta atanan arızaların listesi nedir?",
        "Ahmete geçen hafta atanan arızaların listesi nedir?",
        "ahmet yılmaza geçen hafta atanan arızaların listesi nedir?",
        "ahmet yılmaz'a geçen hafta atanan arızaların listesi nedir?",
        "ahmet can yılmaza geçen hafta atanan arızaların listesi nedir?",
        "merve melisa yılmaza geçen hafta atanan arızaların listesi nedir?",
        "Merve Melisa Ezgi Erdoğan Yılmaza geçen hafta atanan arızaların listesi nedir?",
        "merve can yılmaza geçen hafta atanan arızaların listesi nedir?",
        "eda'nın bu hafta çözdüğü arıza sayısı kaç?",
        "edanın bu hafta çözdüğü arıza sayısı kaç?",
        "eda-101 varlık koduna sahip cihazın bir ay önceki arıza kayıtları nelerdir?",
        "sevim hanım tarafından açılan arızaların tamamlanma süreleri nedir?",
        "büşra'nın açtığı arızalar arasında hangi tarihliler henüz çözülmedi?",
        'kullanıcı adı "ali.kaya" olan kişinin çözümlediği arızalar nelerdir?',
        "zeynep'in email adresi 'zeynep.uzun@example.com' olan kişinin çözdüğü arızalar nelerdir?",
        "eda.yilmaz@example.com adresine atanmış güncel arızalar nelerdir?",
        "melike tarafından açılan ama hala tamamlanmamış arızalar hangileri?",
        "2023-04-15 tarihinde başlayan ve ali'ye atanmış arızalar nelerdir?",
        "Merve Demir yılmazın geçen hafta talep ettiği arıza kodlarını listeie?",
        "Ulaşın ulaştırdığı malzemelerin adeti kaç?",
        "Ulaş'ın ulaştırdığı malzemelerin adeti kaç?",
        "ulaş'ın ulaştırdığı malzemelerin adeti kaç?",
        "Planlanan başlangıç tarihine sadık kalınan arıza sayısı nedir?",
        "Ahmet can tarafından açılan arızaların tamamlanma süreleri nedir?",
        "ahmetcan tarafından açılan arızaların tamamlanma süreleri nedir?",
        "Rızanın ulaştırdığı malzemelerin adeti kaçtır?",
        "Eda su karacanın ulaştırdığı malzemelerin adeti kaçtır?",
        "Eda Sunun oluşturduğu arızalar nedir?",
        "Eda Su'nun oluşturduğu arızalar nedir?",
        "Eda Su oluşturduğu arızalar nedir?",
        "Eda yılmazın oluşturduğu arızalar nedir?",
        "Eda Karacanın oluşturduğu arızalar nedir?",
        "Su Karacanın oluşturduğu arızalar nedir?",
        "Deniz Yıldızın ulaştırdığı malzemelerin adeti kaçtır?",
        "Muhammet yıldızın oluşturduğu malzemelerin adeti kaçtır?",
        "şubat 2023'te eda'ya atanmış olan arızalar nelerdir?",
        "2023 yılı boyunca ahmet tarafından açılan ve çözülen arızalar nelerdir?",
        "emrah k.'nın e-posta adresine atanmış olan arızalar nelerdi ve şu anki durumları nedir?",
        "cemal tarafından bildirilen arızaların şu anki durumu nedir?",
        "2023 yılında ahmet tarafından açılan arıza kayıtlarının sayısı nedir?",
        "geçen hafta hangi arıza süreçleri ahmet tarafından çözüldü?",
        "ahmet tarafından şu anda çözülmeyi bekleyen arızalar nelerdir?",
        "bir önceki gün eda tarafından başlatılan arızalar nelerdir?",
        "bugün ali tarafından kaç yeni arıza kaydedildi?",
        "geçen ay eda yılmaz tarafından açılan ve tamamlanmamış arızalar neler?",
        "hasan tarafından yönetilen arızalardan geçen ay planlananın altında tamamlanan işler nelerdir?",
        "hasandan yönetilen arızalardan geçen ay planlananın altında tamamlanan işler nelerdir?",
        "geçen ay, eda yılmaz tarafından açılan ve tamamlanmamış arızalar neler?",
        "2023 yılı boyunca ahmetden açılan ve çözülen arızalar nelerdir?",
        "hasan için yönetilen arızalardan geçen ay planlananın altında tamamlanan işler nelerdir?",
        "Ahmete geçen hafta atanan arızaların listesi nedir?",
        "Erhan Avcı'nın oluşturduğu arızalar nedir?",
        "Erhan Avcı Yılmazın oluşturduğu arızalar nedir?",
        "mert’in geçen hafta ilgilendiği tüm arızalar nelerdir?",
        "aylin’in planlanan ama tamamlanmayan arızaları nelerdir?",
    
    ]


    name_filtered_data = pd.read_excel('name_filtered_data.xlsx')

    # Run tests 1
    print("Running Turkish NER Masking Tests 1")
    print("=" * 80)
    
    for idx, text in enumerate(test_texts, 1):   # test_texts, (name_filtered_data["Question"].tolist())
        masked_text, original_text, masked_words = masker.mask_named_entities(text)
        
        print(f"\nTest {idx}:")
        print(f"Original : {original_text}")
        print(f"Masked   : {masked_text}")
        print(f"Detected : {masked_words}")
        print("-" * 80)

    print("=" * 80)


if __name__ == "__main__":
    run_tests() 
