from enum import Enum


class ERuleType(Enum):
    AND = 0
    OR = 1


class TRule:
    def __init__(self, rule_type, source_facts, result_fact):
        self.rule_type = rule_type
        self.source_facts = source_facts
        self.result_fact = result_fact

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.rule_type == other.rule_type and \
            self.source_facts == other.source_facts and self.result_fact == other.result_fact

    def __str__(self):
        delimeter = ' & ' if self.rule_type == ERuleType.AND else ' | '
        left_side = delimeter.join([str(f) for f in self.source_facts])
        return 'Rule[{} -> {}]'.format(left_side, self.result_fact)
