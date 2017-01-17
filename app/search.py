class SearchResult:
    def __init__(self, type, id, obj):
        self.type = type
        self.id = id
        self.obj = obj
        self.context = set()

    def copy(self):
        other = SearchResult(self.type, self.id, self.obj)
        return other

    def __eq__(self, other):
        return self.type == other.type and self.id == other.id

    def __hash__(self):
        return hash((self.type, self.id))
    
    def to_json(self):
        return {"type": self.type, "id": self.id, "context": list(self.context)}
