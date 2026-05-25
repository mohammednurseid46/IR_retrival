class SearchRequestModel:
    def __init__(self, query, method='bm25', target_lang='both', use_expansion=False, use_feedback=False):
        self.query = query
        self.method = method
        self.target_lang = target_lang
        self.use_expansion = use_expansion
        self.use_feedback = use_feedback

    @classmethod
    def from_dict(cls, data):
        return cls(
            query=data.get('query', ''),
            method=data.get('method', 'bm25'),
            target_lang=data.get('target_lang', 'both'),
            use_expansion=data.get('use_expansion', False) in [True, 'true', 1, '1'],
            use_feedback=data.get('use_feedback', False) in [True, 'true', 1, '1']
        )
