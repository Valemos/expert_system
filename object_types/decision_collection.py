from object_types.amounts_dict import AmountsDict
from object_types.decision_type import DecisionType
from object_types.part_rate import PartRate


class DecisionCollection:

    def __init__(self):
        self._total_loss = 0
        self._total_deficiencies = AmountsDict()
        self._total_production_stopped = AmountsDict()
        self.reset()

    def reset(self):
        self._total_loss = 0
        self._total_deficiencies = AmountsDict()
        self._total_production_stopped = AmountsDict()

    def is_empty(self):
        return self._total_loss == 0 and \
               len(self._total_deficiencies) == 0 and \
               len(self._total_production_stopped) == 0

    def get_remaining_decisions(self):
        for name, amount in self._total_deficiencies:
            yield DecisionType.DEFICIENCY, PartRate(name, amount)

        for name, amount in self._total_production_stopped:
            yield DecisionType.NOT_PRODUCED, PartRate(name, amount)

        yield DecisionType.LOSS, self._total_loss

        self.reset()

    def compensate_loss(self, loss):
        self._total_loss += loss

    def deficiency(self, part: PartRate):
        self._total_deficiencies.add(part.name, part.amount)

    def production_stopped(self, part: PartRate):
        self._total_production_stopped.add(part.name, part.amount)
