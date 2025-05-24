import pandas as pd
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.masking import NameMasker

def run_tests():
    # Test data
    name_list = ["Eda","Merve Melisa Ezgi","Yıldız","Muhammet","Yıldız","Deniz","Eda","Eda Su","Rıza",
                 "Ahmetcan","Sadık","Merve","Zeynep","Merve Melisa","Merve Melisa","Ahmet","Ulaş", "Ali", 
                 "Ahmet Can", "Mehmet", "Ayşe", "Melike", "Eda", "Büşra", "Sevim", "Merve", "Can Deniz", 
                 "Deniz", "Bekir Ali", "Can", "Deniz"]
    
    surname_list = ["Karaca","Erdoğan Yılmaz","Muhammet","Yıldız","Deniz","Yıldız","Su Karaca","Karaca",
                    "Aydın","Akçakale","Turan","Demir Yılmaz","Bedir","Erdoğan","Yılmaz","Yılmaz","Ali", 
                    "Demir", "Yılmaz", "Kaya Demir", "Demir", "Çelik", "Öztürk", "Salman", "Yılmaz", 
                    "Can Yılmaz", "Salman", "Demir Yılmaz", "Can Mert", "Alp", "Akça"]
    
    username_list = ["eda.karaca",'can.salman', 'can.deniz.öztürk', 'ahmet.yılmaz', 'eda.demir', 
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
        "Eda sunun oluşturduğu arızalar nedir?",
        "Eda Karacanın oluşturduğu arızalar nedir?",
        "Su Karacanın oluşturduğu arızalar nedir?",
        "Deniz Yıldızın ulaştırdığı malzemelerin adeti kaçtır?",
        "Muhammet yıldızın oluşturduğu malzemelerin adeti kaçtır?",
    ]


    # Run tests
    print("Running Turkish NER Masking Tests")
    print("=" * 80)
    
    for idx, text in enumerate(test_texts, 1):
        masked_text, original_text, masked_words = masker.mask_named_entities(text)
        
        print(f"\nTest {idx}:")
        print(f"Original : {original_text}")
        print(f"Masked   : {masked_text}")
        print(f"Detected : {masked_words}")
        print("-" * 80)

if __name__ == "__main__":
    run_tests() 