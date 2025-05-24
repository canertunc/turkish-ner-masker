from transformers import pipeline
import warnings
warnings.filterwarnings("ignore")

class NERModel:
    _instance = None
    _model = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(NERModel, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if NERModel._model is None:
            self.load_model()

    def load_model(self):
        """Load the NER model"""
        try:
            NERModel._model = pipeline("ner", 
                                     model="akdeniz27/bert-base-turkish-cased-ner", 
                                     aggregation_strategy="simple")
            print("NER model loaded successfully.")
        except Exception as e:
            print(f"Failed to load NER model: {e}")
            NERModel._model = None

    def get_model(self):
        """Get the loaded NER model"""
        return NERModel._model

    def analyze_text(self, text):
        """Analyze text with NER model"""
        if not NERModel._model:
            return []
        
        try:
            return NERModel._model(text)
        except Exception as e:
            print(f"Error analyzing text with NER model: {e}")
            return []

    def is_person_entity(self, text, word_pos, word_len):
        """Check if a word is a person entity in context"""
        if not NERModel._model:
            return False
        
        try:
            # Get context around the word (50 chars before and after)
            start_context = max(0, word_pos - 50)
            end_context = min(len(text), word_pos + word_len + 50)
            context = text[start_context:end_context]
            
            # Analyze context with NER
            entities = self.analyze_text(context)
            
            # Check if word position contains a person entity
            word_start_in_context = word_pos - start_context
            word_end_in_context = word_start_in_context + word_len
            
            for entity in entities:
                if (entity['start'] <= word_start_in_context <= entity['end'] or
                    entity['start'] <= word_end_in_context <= entity['end']):
                    return entity['entity_group'] == 'PER'
            
            return False
        except:
            return False 