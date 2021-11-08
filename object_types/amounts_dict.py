

class AmountsDict(dict):

    def add(self, item_name, amount):
        self[item_name] = self.get(item_name, 0) + amount

    def sub(self, other):
        if not isinstance(other, dict):
            raise ValueError(f'{repr(other)} not a dict')

        sub = AmountsDict(**self)
        for item, amount in other.items():
            sub.add(item, -amount)
        return sub
