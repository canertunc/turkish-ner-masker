from typing import Dict, List, Tuple, Optional
from src.database import get_people_data

# Turkish verb roots and common words that might be mistaken as names
COMMON_VERB_ROOTS = [
    "ulaş", "gön", "yap", "git", "gel", "ver", "bul", "gör", "bil",
    "çık", "gir", "dur", "otur", "kalk", "yat", "koş", "yürü", "uç", "düş",
    "öl", "yaşa", "sev", "nefret", "iste", "ara", "çağır", "konuş", "dinle",
    "oku", "yaz", "çiz", "boyar", "kes", "dik", "yık", "temizle", "pişir",
    "ye", "iç", "sat", "satın", "aç", "kapat", "başla", "bitir", "devam",
    "dur", "bekle", "seç", "karar", "düşün", "hatırla", "unut", "öğren",
    "öğret", "anlat", "açıkla", "sor", "cevap", "gül", "ağla", "şarkı",
    "dans", "oyna", "çal", "çek", "it", "taşı", "koy", "çıkar", "tak"
]

# Turkish postpositions and conjunctions that should be preserved
# Bu şuan kullanılmıyor çünkü daha önce alınan bazı hatalar için deneme amaçlı kullanıldığından
# şuan kullanınılmıyor bundan dolayı içi boş!
TURKISH_POSTPOSITIONS = [
   "ve","ile"
]

"""
# Database'den veri çekme işlemi uygulanacaksa bu kod bloğu kullanılabilir.
# Fakat bir aşağıdaki Tester.py için kullanılan name_list ve surname_list silinmeli veya yorum satırına alınmalı

people_data = get_people_data()

# Extract name and surname lists
name_list = people_data['name'].tolist() if 'name' in people_data.columns else []
surname_list = people_data['surname'].tolist() if 'surname' in people_data.columns else []

"""

name_list = ["Salim","Kerim","Kerime","Su","Melike","Caner","Erhan Avcı","Veli","Erhan","Ayşe","Halil","Cemal","Emine","Kadir","Zeynep","Emrah","Mustafa","Hasan","Mert","Aylin","Eda","Merve Melisa Ezgi","Yıldız","Muhammet","Yıldız","Deniz","Eda","Eda Su","Rıza",
            "Ahmetcan","Sadık","Merve","Zeynep","Merve Melisa","Merve Melisa","Ahmet","Ulaş", "Ali", 
            "Ahmet Can", "Mehmet", "Ayşe", "Melike", "Eda", "Büşra", "Sevim", "Merve", "Can Deniz", 
            "Deniz", "Bekir Ali", "Can", "Deniz"]

surname_list = ["Turan","Yılmaz","Atınç","Tekin","Akdere","Tunç","Yılmaz","Tunç","Avcı","Ramazan","Akca","Albora","Sandal","Kaya","Nur","Akça","Sanlı","Demir","Demir","Atamer","Karaca","Erdoğan Yılmaz","Muhammet","Yıldız","Deniz","Yıldız","Su Karaca","Karaca",
            "Aydın","Akçakale","Turan","Demir Yılmaz","Bedir","Erdoğan","Yılmaz","Yılmaz","Ferit", 
            "Demir", "Yılmaz", "Kaya Demir", "Demir", "Çelik", "Öztürk", "Salman", "Yılmaz", 
            "Can Yılmaz", "Salman", "Demir Yılmaz", "Can Mert", "Alp", "Akça"]

# Küçük harfe çevir
name_list = [name.lower() for name in name_list]
surname_list = [surname.lower() for surname in surname_list]

# Çoklu kelimeleri boşluklardan bölerek listeye ekle
def split_and_extend(word_list):
    new_words = []
    for item in word_list:
        parts = item.split()
        if len(parts) > 1:
            new_words.extend(parts)
    word_list.extend(new_words)
    return word_list

name_list = split_and_extend(name_list)
surname_list = split_and_extend(surname_list)

class TextProcessor:
    @staticmethod
    def strip_turkish_suffixes(word: str) -> Tuple[str, str]:
        """Remove Turkish suffixes from a word"""
        # Önce kesme işaretlerini standardize et
        word = word.replace('\u2019', "'")  # Unicode kesme işaretini ASCII kesme işaretine çevir
        
        suffixes = [
            "'nın", "'nin", "'ın", "'in", "'a", "'e", "'da", "'de", 
            "'dan", "'den", "'i", "'ı", "'ya", "'ye", "'nun", 
            "'nün", "'un", "'ün", "'lar", "'ler", "'nda", "'nde",
            "'tan", "'ten", "'sın", "'sin", "'sız", "'siz","nun",
            "nın", "nin", "ın", "in", "da", "de", 
            "dan", "den", "ya", "ye", 
            "nün", "un", "ün", "lar", "ler", "nda", "nde",
            "tan", "ten", "sın", "sin", "sız", "siz",
            "a", "e", "i", "ı", "u", "ü" 
        ]
        
        word_lower = word.lower()
            
        # Önce 3 ve daha uzun ekleri dene
        for suffix in sorted([s for s in suffixes if len(s) >= 3], key=len, reverse=True):
            if word_lower.endswith(suffix.lower()):
                base = word[:len(word)-len(suffix)]
                if len(base) <= 1 or (base.lower() not in name_list and base.lower() not in surname_list):  # Çok kısa kalan kökleri alma
                    continue
                remaining_suffix = word[len(word)-len(suffix):]
                return base, remaining_suffix
        
        # Sonra 2 harfli ekleri dene
        for suffix in [s for s in suffixes if len(s) == 2]:
            if word_lower.endswith(suffix.lower()):
                base = word[:len(word)-len(suffix)]
                if len(base) <= 2:  # Çok kısa kalan kökleri alma
                    continue
                remaining_suffix = word[len(word)-len(suffix):]
                return base, remaining_suffix
        
        # En son tek harfli ekleri dene
        for suffix in [s for s in suffixes if len(s) == 1]:
            if word_lower.endswith(suffix.lower()):
                base = word[:len(word)-len(suffix)]
                if len(base) <= 2:  # Çok kısa kalan kökleri alma
                    continue
                remaining_suffix = word[len(word)-len(suffix):]
                return base, remaining_suffix
        
        
        return word, ""

    @staticmethod
    def is_verb_or_common_word(word: str, name_surname_lists: List[str]) -> bool:
        """Check if word is a verb root or common word"""
        if not word:
            return False
            
        word_clean, _ = TextProcessor.strip_turkish_suffixes(word.lower())
        
        # Check verb roots
        for root in COMMON_VERB_ROOTS:
            if word_clean.startswith(root) and len(word_clean) > len(root):
                # Name has priority if in name list
                if word.lower() in [n.lower() for n in name_surname_lists]:
                    return False
                return True
        
        return False

    @staticmethod
    def is_postposition(word: str) -> bool:
        """Check if word is a Turkish postposition"""
        return word.lower() in TURKISH_POSTPOSITIONS

    @staticmethod
    def try_name_surname_combinations(phrase: str, name_list: List[str], 
                                    surname_list: List[str]) -> Optional[Tuple[str, str, int]]:
        """Try different name-surname combinations"""
        words = phrase.split()
        
        # Single word case
        if len(words) == 1:
            word = words[0]
            # Önce tam kelimeyi kontrol et
            if word.lower() in [n.lower() for n in name_list]:
                return (word, None, 10)
            elif word.lower() in [s.lower() for s in surname_list]:
                return (None, word, 8)
            
            # Tam kelime eşleşmezse, ek ayrılmış halini dene
            base, suffix = TextProcessor.strip_turkish_suffixes(word)
            
            # Eğer base name listesinde varsa kabul et
            if base and base.lower() in [n.lower() for n in name_list]:
                return (base, None, 8)
            elif base and base.lower() in [s.lower() for s in surname_list]:
                return (None, base, 6)
            
            return None
        
        # Try full phrase as name or surname
        full_phrase = ' '.join(words)
        if full_phrase.lower() in [n.lower() for n in name_list]:
            return (full_phrase, None, 100)
        if full_phrase.lower() in [s.lower() for s in surname_list]:
            return (None, full_phrase, 90)
        
        # Try combinations
        best_score = 0
        best_combination = None
        
        for split_point in range(1, len(words)):
            name_part = ' '.join(words[:split_point])
            surname_part = ' '.join(words[split_point:])
            name_match = name_part.lower() in [n.lower() for n in name_list]
            surname_match = surname_part.lower() in [s.lower() for s in surname_list]
            if name_match and surname_match:
                score = 50 + len(words) * 5
                if score > best_score:
                    best_score = score
                    best_combination = (name_part, surname_part, score)
            elif name_match:
                score = 20 + len(words) * 3
                if score > best_score:
                    best_score = score
                    best_combination = (name_part, None, score)
            elif surname_match:
                score = 15 + len(words) * 3
                if score > best_score:
                    best_score = score
                    best_combination = (None, surname_part, score)
        return best_combination

    @staticmethod
    def find_best_name_surname_combination(words: List[str], start_idx: int, 
                                         name_list: List[str], surname_list: List[str]) -> Optional[Tuple[str, str, int, str]]:
        """Find best name-surname combination"""
        max_words = min(6, len(words) - start_idx)
        best_combination = None
        best_score = 0
        total_words2 = 0
        last_suffix_word = ""
        
        # First check if current word is a postposition
        if TextProcessor.is_postposition(words[start_idx]):
            return None
        
        for end_idx in range(start_idx, start_idx + max_words):
            # Stop if we hit a postposition
            if end_idx > start_idx and TextProcessor.is_postposition(words[end_idx]):
                break
                
            phrase = ' '.join(words[start_idx:end_idx + 1])
            
            # Check suffixes
            last_word = words[end_idx]
            clean_last_word, suffix = TextProcessor.strip_turkish_suffixes(last_word)
            
            # Create clean phrase
            phrase_words = phrase.split()
            phrase_words[-1] = clean_last_word
            clean_phrase = ' '.join(phrase_words)
            
            # Try combinations
            combination = TextProcessor.try_name_surname_combinations(clean_phrase, name_list, surname_list)
            
            if combination:
                name_part, surname_part, score = combination
                total_words = end_idx - start_idx + 1
                
                # Check if next word is a postposition
                if end_idx + 1 < len(words) and TextProcessor.is_postposition(words[end_idx + 1]):
                    # Reduce score if followed by postposition to prefer shorter match
                    score = score * 0.8
                
                if score > best_score:
                    if(name_part != None and surname_part != None):
                        total_words2 = len(name_part.split()) + len(surname_part.split())
                        last_word_best = words[start_idx + total_words2 - 1]
                        clean_last_word_best, suffix_best = TextProcessor.strip_turkish_suffixes(last_word_best)
                        last_suffix_word = suffix_best
                        if(surname_part == last_word_best):
                            last_suffix_word = ""

                    elif(name_part != None and surname_part == None):
                        total_words2 = len(name_part.split())
                        last_word_best = words[start_idx + total_words2 - 1]
                        clean_last_word_best, suffix_best = TextProcessor.strip_turkish_suffixes(last_word_best)
                        last_suffix_word = suffix_best
                        if(name_part == last_word_best):
                            last_suffix_word = ""
                    elif(name_part == None and surname_part != None):
                        total_words2 = len(surname_part.split())
                        last_word_best = words[start_idx + total_words2 - 1]
                        clean_last_word_best, suffix_best = TextProcessor.strip_turkish_suffixes(last_word_best)
                        last_suffix_word = suffix_best
                        if(surname_part == last_word_best):
                            last_suffix_word = ""
                    else:
                        total_words2 = 0
                    best_combination = (name_part, surname_part, total_words, suffix)
                    best_score = score
        if(best_combination != None):
            best_combination = (best_combination[0], best_combination[1], total_words2, last_suffix_word)
        return best_combination

    @staticmethod
    def mask_names_in_text(text: str, name_list: List[str], surname_list: List[str]) -> Tuple[str, Dict[str, List[str]]]:
        """Mask names in text while preserving sentence structure"""
        words = text.split()
        masked_words = words.copy()
        detected = {'kullanici_adi': [], 'name': [], 'surname': []}
        
        i = 0
        while i < len(words):
            # Try to find name-surname combinations
            combination = TextProcessor.find_best_name_surname_combination(words, i, name_list, surname_list)
            
            if combination:
                name_part, surname_part, word_count, suffix = combination
                
                if name_part:
                    detected['name'].append(name_part)
                    masked_words[i:i+word_count] = ["{name}" + suffix] + words[i+1:i+word_count]
                
                if surname_part:
                    detected['surname'].append(surname_part)
                    masked_words[i:i+word_count] = ["{surname}" + suffix] + words[i+1:i+word_count]
                
                i += word_count
            else:
                i += 1
            
        return ' '.join(masked_words), detected 
