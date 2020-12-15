from collections import deque
from enum import Enum
from rule import ERuleType


class ESolverMode(Enum):
    BFS = 0
    DFS = 1


class TSolver:
    def __init__(self, facts, rules):
        self.facts = facts
        self.rules = rules
        self.memory = set()
        self.mode = None
        self.rules_container = deque()
        self.unprocessed_rules = set()

    def _get_next_rule(self):
        if self.mode == ESolverMode.BFS:
            return self.rules_container.popleft()
        elif self.mode == ESolverMode.DFS:
            return self.rules_container.pop()
        raise ValueError('Unknown solver mode {}'.format(self.mode))

    def _add_rules_to_container(self):
        for rule in [x for x in self.unprocessed_rules]:
            if rule.rule_type == ERuleType.AND:
                matched = True
                for fact in rule.source_facts:
                    if fact not in self.memory:
                        matched = False
                        break
            elif rule.rule_type == ERuleType.OR:
                matched = False
                for fact in rule.source_facts:
                    if fact in self.memory:
                        matched = True
                        break
            if matched:
                self.rules_container.append(rule)
                self.unprocessed_rules.remove(rule)

    def solve_from_data(self, true_facts, target, mode):
        self.memory = set(true_facts)
        self.mode = mode
        self.unprocessed_rules = set([r for r in self.rules])
        self._add_rules_to_container()

        cycle = 0
        print('\nCycle {}:'.format(cycle))
        print('True facts: {}'.format(sorted([str(f) for f in self.memory])))
        print('Rules to process: {}'.format([str(r) for r in self.rules_container]))
        while len(self.rules_container):
            cycle += 1
            rule = self._get_next_rule()
            self.memory.add(rule.result_fact)
            if rule.result_fact == target:
                return True
            self._add_rules_to_container()
            print('\nCycle {}:'.format(cycle))
            print('True facts: {}'.format(sorted([str(f) for f in self.memory])))
            print('Rules to process: {}'.format([str(r) for r in self.rules_container]))

        return False

    def _check_rule(self, true_facts, rule):
        print('Checking {}'.format(rule))
        if rule.rule_type == ERuleType.AND:
            for source_fact in rule.source_facts:
                if not self._check_fact(true_facts, source_fact):
                    return False
            return True
        elif rule.rule_type == ERuleType.OR:
            for source_fact in rule.source_facts:
                if self._check_fact(true_facts, source_fact):
                    return True
            return False
        raise ValueError('Unknown rule type: {}'.format(rule.rule_type))

    def _get_rules_by_result_fact(self, result_fact):
        return [r for r in self.rules if r.result_fact == result_fact]

    def _check_fact(self, true_facts, target):
        print('Checking {}'.format(target))
        if target in true_facts:
            return True
        for rule in self._get_rules_by_result_fact(target):
            if self._check_rule(true_facts, rule):
                print('True {}'.format(str(rule)))
                return True
        return False

    def solve_from_target(self, true_facts, target):
        return self._check_fact(true_facts, target)
