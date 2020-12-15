from argparse import ArgumentParser
from fact import TFact
from parser import TParser
from solver import ESolverMode, TSolver


def main():
    parser = ArgumentParser(description='Facts solver')
    parser.add_argument('-d', '--database', help='path to facts and rules config', required=True)
    parser.add_argument('-t', '--true-facts', nargs='+', help='true facts', required=True)
    parser.add_argument('-T', '--target', help='target fact', required=True)
    parser.add_argument('--bfs', action='store_true', help='solve from data using BFS')
    parser.add_argument('--from-target', action='store_true', help='solve from target')
    args = parser.parse_args()

    facts, rules = TParser.parse_config(args.database)
    solver = TSolver(facts, rules)
    true_facts = [TFact(f) for f in args.true_facts]
    target = TFact(args.target)
    result = False
    if args.from_target:
        print('Solving from target:')
        result = solver.solve_from_target(true_facts, target)
    else:
        mode = ESolverMode.BFS if args.bfs else ESolverMode.DFS
        print('Solving from data using {}:'.format(str(mode)))
        result = solver.solve_from_data(true_facts, target, mode)
    print('Target fact {} is {}'.format(str(target), result))


if __name__ == '__main__':
    main()
