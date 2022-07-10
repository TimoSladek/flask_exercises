class Snack:
    count = 0

    def __init__(self, name, kind):
        self.name = name
        self.kind = kind
        Snack.count += 1
        self.id = Snack.count
