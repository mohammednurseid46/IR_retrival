# Unicode block ranges for Ethiopic script used in Amharic

ETHIOPIC_RANGE = (0x1200, 0x137F)      # Ethiopic main block
ETHIOPIC_SUPPLEMENT = (0x1380, 0x139F) # Ethiopic Supplement
ETHIOPIC_EXTENDED = (0x2D80, 0x2DDF)   # Ethiopic Extended
ETHIOPIC_EXTENDED_A = (0xAB00, 0xAB2F) # Ethiopic Extended-A

def is_char_in_ranges(char, *ranges):
    code = ord(char)
    for start, end in ranges:
        if start <= code <= end:
            return True
    return False
