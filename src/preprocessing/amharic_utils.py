def is_ethiopic_char(char):
    """Check if a character falls within the Ethiopic Unicode block (U+1200 to U+137F, plus extensions)."""
    code_point = ord(char)
    # Ethiopic Unicode range: U+1200 - U+137F
    # Ethiopic Supplement: U+1380 - U+139F
    # Ethiopic Extended: U+2D80 - U+2DDF
    # Ethiopic Extended-A: U+AB00 - U+AB2F
    return (0x1200 <= code_point <= 0x137F or 
            0x1380 <= code_point <= 0x139F or 
            0x2D80 <= code_point <= 0x2DDF or 
            0xAB00 <= code_point <= 0xAB2F)

def get_ethiopic_ratio(text):
    """Calculate the ratio of Ethiopic characters in the given text."""
    if not text:
        return 0.0
    
    # Filter out whitespace and digits to avoid skewing ratio
    ignored_chars = set([' ', '\t', '\n', '\r', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'])
    filtered_text = [char for char in text if char not in ignored_chars]
    
    if not filtered_text:
        return 0.0
        
    ethiopic_count = sum(1 for char in filtered_text if is_ethiopic_char(char))
    return ethiopic_count / len(filtered_text)
