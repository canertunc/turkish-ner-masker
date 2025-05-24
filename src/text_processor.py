from typing import Dict, List, Tuple, Optional

# Turkish verb roots and common words that might be mistaken as names
COMMON_VERB_ROOTS = [
    "ulaş", "gön", "yap", "git", "gel", "al", "ver", "bul", "gör", "bil",
    "çık", "gir", "dur", "otur", "kalk", "yat", "koş", "yürü", "uç", "düş",
    "öl", "yaşa", "sev", "nefret", "iste", "ara", "çağır", "konuş", "dinle",
    "oku", "yaz", "çiz", "boyar", "kes", "dik", "yık", "temizle", "pişir",
    "ye", "iç", "sat", "satın", "aç", "kapat", "başla", "bitir", "devam",
    "dur", "bekle", "seç", "karar", "düşün", "hatırla", "unut", "öğren",
    "öğret", "anlat", "açıkla", "sor", "cevap", "gül", "ağla", "şarkı",
    "dans", "oyna", "çal", "çek", "it", "taşı", "koy", "çıkar", "tak"
]

class TextProcessor:
    @staticmethod
    def strip_turkish_suffixes(word: str) -> Tuple[str, str]:
        """Remove Turkish suffixes from a word"""
        suffixes = [
            "'nın", "'nin", "'ın", "'in", "'a", "'e", "'da", "'de", 
            "'dan", "'den", "'i", "'ı", "'ya", "'ye", "'nun", 
            "'nün", "'un", "'ün", "'lar", "'ler", "'nda", "'nde",
            "'tan", "'ten", "'sın", "'sin", "'sız", "'siz", "'lık", "'lik",
            "nın", "nin", "ın", "in", "a", "e", "da", "de", 
            "dan", "den", "i", "ı", "ya", "ye", "nun", 
            "nün", "un", "ün", "lar", "ler", "nda", "nde",
            "tan", "ten", "sın", "sin", "sız", "siz", "lık", "lik"
        ]
        
        word_lower = word.lower()
        
        for suffix in suffixes:
            if word_lower.endswith(suffix.lower()):
                base = word[:len(word)-len(suffix)]
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
    def try_name_surname_combinations(phrase: str, name_list: List[str], 
                                    surname_list: List[str]) -> Optional[Tuple[str, str, int]]:
        """Try different name-surname combinations"""
        words = phrase.split()
        
        # Single word case
        if len(words) == 1:
            word = words[0]
            name_match = any(word.lower() == n.lower() for n in name_list)
            surname_match = any(word.lower() == s.lower() for s in surname_list)
            
            if name_match and surname_match:
                return (word, None, 10)  # Name has priority
            elif name_match:
                return (word, None, 8)
            elif surname_match:
                return (None, word, 8)
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
        
        for end_idx in range(start_idx, start_idx + max_words):
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
                
                if score > best_score:
                    best_combination = (name_part, surname_part, total_words, suffix)
                    best_score = score
        
        return best_combination 