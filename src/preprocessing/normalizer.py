import re

class Normalizer:
    def __init__(self):
        # Amharic character normalization mappings (homophone consolidation)
        # 1. 'h' sounds: ሐ, ሑ, ሒ, ሓ, ሔ, ሖ; ኀ, ኁ, ኂ, ኃ, ኄ, ኅ, ኆ; ኻ, ኺ, ኼ, ኽ, ኾ -> ሀ, ሁ, ሂ, ሃ, ሄ, ህ, ሆ
        self.amharic_h_map = {
            'ሐ': 'ሀ', 'ሑ': 'ሁ', 'ሒ': 'ሂ', 'ሓ': 'ሃ', 'ሔ': 'ሄ', 'ሕ': 'ህ', 'ሖ': 'ሆ',
            'ኀ': 'ሀ', 'ኁ': 'ሁ', 'ኂ': 'ሂ', 'ኃ': 'ሃ', 'ኄ': 'ሄ', 'ኅ': 'ህ', 'ኆ': 'ሆ',
            'ሃ': 'ሃ', 'ኃ': 'ሃ', 'ሐ': 'ሀ',
            'ኻ': 'ካ', 'ኺ': 'ኪ', 'ኼ': 'ኬ', 'ኽ': 'ክ', 'ኾ': 'ኮ'
        }
        
        # 2. 's' sounds: ሠ, ሡ, ሢ, ሣ, ሤ, ሥ, ሦ -> ሰ, ሱ, ሲ, ሳ, ሴ, ስ, ሶ
        self.amharic_s_map = {
            'ሠ': 'ሰ', 'ሡ': 'ሱ', 'ሢ': 'ሲ', 'ሣ': 'ሳ', 'ሤ': 'ሴ', 'ሥ': 'ስ', 'ሦ': 'ሶ'
        }
        
        # 3. 'a' sounds: ዐ, ዑ, ዒ, ዓ, ዔ, ዕ, ዖ -> አ, ኡ, ኢ, ኣ, ኤ, እ, ኦ
        self.amharic_a_map = {
            'ዐ': 'አ', 'ዑ': 'ኡ', 'ዒ': 'ኢ', 'ዓ': 'ኣ', 'ዔ': 'ኤ', 'ዕ': 'እ', 'ዖ': 'ኦ'
        }
        
        # 4. 'ts' sounds: ፀ, ፁ, ጺ, ጻ, ጼ, ፅ, ጾ -> ጸ, ጹ, ጺ, ጻ, ጼ, ጽ, ጾ
        self.amharic_ts_map = {
            'ፀ': 'ጸ', 'ፁ': 'ጹ', 'ጺ': 'ጺ', 'ጻ': 'ጻ', 'ጼ': 'ጼ', 'ፅ': 'ጽ', 'ጾ': 'ጾ'
        }

        # Try to import nltk for English stemming if available, otherwise fallback
        self.nltk_stemmer = None
        try:
            from nltk.stem import PorterStemmer
            self.nltk_stemmer = PorterStemmer()
        except ImportError:
            pass

    def normalize_amharic(self, word):
        """Normalize Amharic word by mapping homophones."""
        if not word:
            return ""
        
        normalized = []
        for char in word:
            if char in self.amharic_h_map:
                normalized.append(self.amharic_h_map[char])
            elif char in self.amharic_s_map:
                normalized.append(self.amharic_s_map[char])
            elif char in self.amharic_a_map:
                normalized.append(self.amharic_a_map[char])
            elif char in self.amharic_ts_map:
                normalized.append(self.amharic_ts_map[char])
            else:
                normalized.append(char)
                
        word = "".join(normalized)
        
        # Simple suffix stripping for Amharic plurals/possessives (optional and basic)
        # e.g., -ኦች (plurals) -> removing them can sometimes help.
        # But let's stick to stable character normalization as requested.
        return word

    def stem_english(self, word):
        """Stem English word using NLTK if available, else a simple rules-based stemmer."""
        if not word:
            return ""
        
        word = word.lower()
        if self.nltk_stemmer:
            return self.nltk_stemmer.stem(word)
        
        # Simple rule-based English stemmer fallback (plural/ing/ed stripping)
        if len(word) > 4:
            if word.endswith('sses'):
                return word[:-2]
            elif word.endswith('ies'):
                return word[:-3] + 'i'
            elif word.endswith('ss'):
                return word
            elif word.endswith('s') and not word.endswith('us') and not word.endswith('is') and not word.endswith('as'):
                return word[:-1]
            elif word.endswith('eed'):
                return word[:-1]
            elif word.endswith('ing'):
                return word[:-3]
            elif word.endswith('ed'):
                return word[:-2]
            elif word.endswith('ly'):
                return word[:-2]
        return word

    def normalize(self, word, language='english'):
        """Normalize word according to its language."""
        if language.lower() == 'amharic':
            return self.normalize_amharic(word)
        return self.stem_english(word)
