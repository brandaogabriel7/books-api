class Publisher:
    def __init__(self, name):
        if not name:
            raise ValueError("Publisher name is required")
        self.name = name
