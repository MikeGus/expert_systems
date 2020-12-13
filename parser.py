from fact import TFact
from rule import TRule, ERuleType


'''
expected config format is listed below
first line contains list of facts
other lines contain info about rules
& signals that rule_type is AND
| signals that rule_type is OR
> splits source facts from result

example:
f1 f2 f3 f4 f5
& f1 f2 f4 > f5
| f2 f4 > f3
'''


class TParser:
    @staticmethod
    def parse_config(path_to_config):
        with open(path_to_config, 'r') as source_file:
            facts = [TFact(fact) for fact in source_file.readline().split()]
            rules = []
            while True:
                line = source_file.readline()
                if not line:
                    break
                lhs, result_fact = line.split('>')
                type_and_facts = lhs.split()
                rule_type = ERuleType.AND if type_and_facts[0] == '&' else ERuleType.OR
                facts = [TFact(fact) for fact in type_and_facts[1:]]
                rules.append(TRule(rule_type, set(facts), TFact(result_fact.strip())))

            return facts, rules
