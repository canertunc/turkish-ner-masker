from typing import Dict, List, Tuple, Optional
import re
from .text_processor import TextProcessor
from .ner_model import NERModel

class NameMasker:
    def __init__(self, name_list: List[str], surname_list: List[str], username_list: Optional[List[str]] = None):
        self.name_list = name_list
        self.surname_list = surname_list
        self.username_list = username_list or []
        self.ner_model = NERModel()

    def mask_usernames(self, text: str) -> Tuple[str, List[str]]:
        """Mask usernames in text"""
        if not text or not isinstance(text, str):
            return text, []

        masked_usernames = []
        
        # Create regex pattern for exact word matches
        username_pattern = r'\b(' + '|'.join(map(re.escape, self.username_list)) + r')\b'
        
        def replace_username(match):
            username = match.group(1)
            masked_usernames.append(username)
            return "{kullanici_adi}"
        
        masked_text = re.sub(username_pattern, replace_username, text, flags=re.IGNORECASE)
        return masked_text, masked_usernames

    def enhanced_name_surname_mask(self, text: str) -> Tuple[str, Dict[str, List[str]]]:
        """Enhanced name/surname masking"""
        if not text or not isinstance(text, str):
            return text, {'name': [], 'surname': []}
        
        masked_words = {'name': [], 'surname': []}
        words = text.split()
        i = 0
        
        while i < len(words):
            # Skip already masked words
            if words[i].startswith('{') and words[i].endswith('}'):
                i += 1
                continue
            
            # Find best name-surname combination
            found_combination = TextProcessor.find_best_name_surname_combination(
                words, i, self.name_list, self.surname_list)
            
            if found_combination:
                name_part, surname_part, total_words, suffix = found_combination
                
                # Check for verbs
                if name_part and len(name_part.split()) == 1:
                    first_word = name_part.split()[0]
                    if TextProcessor.is_verb_or_common_word(first_word, self.name_list + self.surname_list):
                        i += 1
                        continue
                
                # Create mask
                mask_parts = []
                if name_part:
                    mask_parts.append("{name}")
                    masked_words['name'].append(name_part)
                if surname_part:
                    mask_parts.append("{surname}")
                    masked_words['surname'].append(surname_part)
                
                mask_text = " ".join(mask_parts)
                if suffix and not suffix.startswith("'"):
                    suffix = "'" + suffix
                mask_text += suffix
                
                # Replace words
                for k in range(total_words):
                    if k == 0:
                        words[i + k] = mask_text
                    else:
                        words[i + k] = ""
                
                i += total_words
            else:
                i += 1
        
        # Clean empty strings
        words = [w for w in words if w]
        masked_text = ' '.join(words)
        
        return masked_text, masked_words

    def analyze_with_ner(self, text: str) -> Tuple[str, Dict[str, List[str]]]:
        """Analyze text with NER model"""
        if not text or not isinstance(text, str):
            return text, {'name': [], 'surname': []}

        entities = self.ner_model.analyze_text(text)
        masked_words = {'name': [], 'surname': []}
        
        # Sort entities by length (longest first to avoid overlapping)
        person_entities = [e for e in entities if e['entity_group'] == 'PER']
        person_entities.sort(key=lambda x: x['end'] - x['start'], reverse=True)
        
        # Replace entities with masks
        for entity in person_entities:
            start = entity['start']
            end = entity['end']
            entity_text = text[start:end].strip()
            
            # Skip already masked text
            if entity_text.startswith('{') and entity_text.endswith('}'):
                continue
            
            parts = entity_text.split()
            if len(parts) > 1:
                # Try to identify name and surname parts
                found_combination = TextProcessor.find_best_name_surname_combination(
                    parts, 0, self.name_list, self.surname_list)
                
                if found_combination:
                    name_part, surname_part, _, suffix = found_combination
                    mask = []
                    if name_part:
                        mask.append("{name}")
                        masked_words['name'].append(name_part)
                    if surname_part:
                        mask.append("{surname}")
                        masked_words['surname'].append(surname_part)
                    
                    mask_text = " ".join(mask)
                    if suffix:
                        mask_text += suffix
                    
                    text = text[:start] + mask_text + text[end:]
            else:
                # Single word - try both name and surname lists
                word = parts[0]
                clean_word, suffix = TextProcessor.strip_turkish_suffixes(word)
                
                if clean_word.lower() in [n.lower() for n in self.name_list]:
                    mask = "{name}"
                    masked_words['name'].append(clean_word)
                elif clean_word.lower() in [s.lower() for s in self.surname_list]:
                    mask = "{surname}"
                    masked_words['surname'].append(clean_word)
                else:
                    # Default to name if uncertain
                    mask = "{name}"
                    masked_words['name'].append(clean_word)
                
                if suffix:
                    mask += suffix
                
                text = text[:start] + mask + text[end:]
        
        return text, masked_words

    def mask_named_entities(self, text: str) -> Tuple[str, str, Dict[str, List[str]]]:
        """Main function to mask named entities in text"""
        if not text or not isinstance(text, str):
            return text, text, {
                'kullanici_adi': [],
                'name': [],
                'surname': []
            }

        # Initialize result dictionary
        masked_words_dict = {
            'kullanici_adi': [],
            'name': [],
            'surname': []
        }

        # Store original text
        original_text = text

        # Step 1: Protect email addresses
        email_pattern = r'\b[\w\.-]+@[\w\.-]+\.\w+\b'
        email_placeholders = {}
        
        def protect_email(match):
            email = match.group(0)
            placeholder = f"{{EMAIL{len(email_placeholders)}}}"
            email_placeholders[placeholder] = email
            return placeholder
        
        text = re.sub(email_pattern, protect_email, text)

        # Step 2: Mask usernames
        text, usernames = self.mask_usernames(text)
        masked_words_dict['kullanici_adi'].extend(usernames)

        # Step 3: Enhanced name/surname masking
        text, name_surname_dict = self.enhanced_name_surname_mask(text)
        masked_words_dict['name'].extend(name_surname_dict['name'])
        masked_words_dict['surname'].extend(name_surname_dict['surname'])

        # Step 4: NER model analysis
        text, ner_dict = self.analyze_with_ner(text)
        masked_words_dict['name'].extend(ner_dict['name'])
        masked_words_dict['surname'].extend(ner_dict['surname'])

        # Step 5: Restore email addresses
        for placeholder, email in email_placeholders.items():
            text = text.replace(placeholder, email)

        # Clean up double spaces and remove duplicates
        text = ' '.join(text.split())
        for key in masked_words_dict:
            masked_words_dict[key] = list(dict.fromkeys(masked_words_dict[key]))

        return text, original_text, masked_words_dict 