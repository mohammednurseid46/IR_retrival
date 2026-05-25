class QueryExpander:
    def __init__(self):
        # Local thesaurus for query expansion
        self.english_synonyms = {
            "coffee": ["brew", "bean", "arabica", "buna"],
            "ceremony": ["ritual", "celebration"],
            "traditional": ["cultural", "heritage", "native"],
            "church": ["churches", "cathedral", "monastery", "temple"],
            "king": ["emperor", "monarch", "ruler"],
            "obelisk": ["monument", "stela", "stele", "pillar"],
            "runner": ["athlete", "sprinter", "marathoner", "running"],
            "running": ["athletics", "runner", "race"],
            "victory": ["triumph", "defeat", "battle"],
            "waterfall": ["falls", "cascade", "cataract"],
            "river": ["water", "stream", "flow"],
            "dam": ["reservoir", "barrage"],
            "food": ["cuisine", "dish", "meal", "injera"]
        }

        self.amharic_synonyms = {
            "ቡና": ["ጀበና", "መቁላት", "ሲኒ"],
            "ቤተክርስቲያን": ["አብያተ ክርስቲያናት", "ገዳም", "ቤተ መቅደስ"],
            "ቤተ ክርስቲያን": ["አብያተ ክርስቲያናት", "ገዳም", "ቤተ መቅደስ"],
            "ንጉስ": ["ንጉሥ", "አፄ", "አጼ", "መሪ"],
            "ንጉሥ": ["ንጉስ", "አፄ", "አጼ", "መሪ"],
            "ሐውልት": ["ሃውልት", "መታሰቢያ"],
            "ሩጫ": ["አትሌቲክስ", "ሯጭ", "አትሌት", "ውድድር"],
            "ሯጭ": ["ሩጫ", "አትሌት", "አትሌቶች"],
            "ወንዝ": ["ውኃ", "ውሃ", "ተፋሰስ"],
            "ፏፏቴ": ["ጥስ እሳት", "ጥስ አባይ"],
            "ምግብ": ["እንጀራ", "ወጥ", "ማዕድ"],
            "ግድብ": ["ውኃ", "ኤሌክትሪክ", "ኃይል"],
            "ነጻነት": ["ነፃነት", "ሉዓላዊነት", "ድል"],
            "ጦርነት": ["ዘመቻ", "ውጊያ", "ድል"]
        }

    def expand(self, query_tokens, language='english'):
        """
        Takes a list of preprocessed query tokens and returns an expanded list 
        with synonyms from the local thesaurus.
        """
        if not query_tokens:
            return []
            
        synonyms_dict = self.amharic_synonyms if language.lower() == 'amharic' else self.english_synonyms
        
        expanded_tokens = list(query_tokens)
        
        for token in query_tokens:
            token_lower = token.lower()
            if token_lower in synonyms_dict:
                for synonym in synonyms_dict[token_lower]:
                    if synonym not in expanded_tokens:
                        expanded_tokens.append(synonym)
                        
        return expanded_tokens
