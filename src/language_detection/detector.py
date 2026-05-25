from .char_ranges import ETHIOPIC_RANGE, ETHIOPIC_SUPPLEMENT, ETHIOPIC_EXTENDED, ETHIOPIC_EXTENDED_A, is_char_in_ranges

class LanguageDetector:
    def __init__(self, threshold=0.1):
        """
        Threshold represents the proportion of characters that must be in Ethiopic range 
        to classify the text as Amharic.
        """
        self.threshold = threshold

    def detect(self, text):
        """
        Detects language. Returns 'amharic' or 'english'.
        """
        if not text:
            return 'english' # default fallback
        
        # Strip digits, space, common Latin punctuation to get accurate count of letters
        chars = [c for c in text if c.isalpha() or c in ['፡', '።', '፣', '፤']]
        if not chars:
            return 'english'
            
        ethiopic_count = sum(1 for c in chars if is_char_in_ranges(c, 
            ETHIOPIC_RANGE, ETHIOPIC_SUPPLEMENT, ETHIOPIC_EXTENDED, ETHIOPIC_EXTENDED_A))
            
        ratio = ethiopic_count / len(chars)
        
        if ratio >= self.threshold:
            return 'amharic'
        return 'english'
