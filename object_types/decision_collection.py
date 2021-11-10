from object_types.amounts_dict import AmountsDict
from object_types.decision_type import DecisionType
from object_types.part_rate import PartRate


class DecisionCollection:

    def __init__(self):
        self._total_loss = 0
        self._total_deficiencies = AmountsDict()

    def is_empty(self):
        return self._total_loss == 0 and \
               len(self._total_deficiencies) == 0

    def get_remaining_decisions(self):
        deficiency_names = list(self._total_deficiencies.keys())
        for name in deficiency_names:
            amount = self._total_deficiencies.pop(name)
            yield DecisionType.DEFICIENCY, PartRate(name, amount)

        if self._total_loss > 0:
            loss = self._total_loss
            self._total_loss = 0
            yield DecisionType.LOSS, loss

    def compensate_loss(self, loss):
        self._total_loss += loss

    def deficiency(self, part: PartRate):
        self._total_deficiencies.add(part.name, part.amount)
