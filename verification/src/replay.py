"""Independent prefix-maxcon census for all one-bit-per-block QBF matrices."""

from itertools import product

SOURCES = ({0}, {1}, {2, 3}, {4, 5, 6}, {7, 8})
BITS = (0, 1)
GOOD, BAD0, BAD1, REPAIR = ({5}, {4, 7}, {4, 8}, {4, 6})


def induces(truth_set, sources):
    return tuple(0 if source <= truth_set else
                 2 if source.isdisjoint(truth_set) else 1 for source in sources)


def maxcons(rows, sources, ranking):
    kept = rows
    prefix = set()
    for level in range(3):
        prefix.update(*(s for s, rank in zip(sources, ranking) if level == rank))
        all_restrictions = {r & prefix for r in rows}
        kept = [r for r in kept if not any(r & prefix < extension
                                          for extension in all_restrictions)]
    assert kept
    return kept


def stable_rankings(rows, sources):
    result = {}
    for ranking in {induces(row, sources) for row in rows}:
        preferred = maxcons(rows, sources, ranking)
        if all(induces(row, sources) == ranking for row in preferred):
            result[ranking] = preferred
    return result


def case_sets(x, y, repair):
    base = {x, 2 + y}
    return {name: frozenset(base | extra)
            for name, extra in (("Good", GOOD), ("Bad0", BAD0), ("Bad1", BAD1), ("Repair", REPAIR))
            if name != "Repair" or repair}


def census():
    matrices = 0
    cases = 0
    for matrix in product(BITS, repeat=8):
        outcomes = {(x, y): any(matrix[4*x+2*y+z] for z in BITS)
                    for x, y in product(BITS, repeat=2)}
        case = {xy: case_sets(*xy, repair) for xy, repair in outcomes.items()}
        rows = [frozenset()] + [row for modes in case.values() for row in modes.values()]
        stable = stable_rankings(rows, SOURCES)
        expected = {}
        for x in BITS:
            target = induces(case[x, 0]["Good"], SOURCES)
            rival = induces(case[x, 0]["Bad0"], SOURCES)
            target_maxcons = set(maxcons(rows, SOURCES, target))
            rival_maxcons = set(maxcons(rows, SOURCES, rival))
            required = set()
            for y in BITS:
                modes = case[x, y]
                required.add(modes["Good"])
                if outcomes[x, y]:
                    required.add(modes["Repair"])
                else:
                    required.update((modes["Bad0"], modes["Bad1"]))
                assert modes["Good"] in rival_maxcons
                cases += 1
            assert target_maxcons == required
            if all(outcomes[x, y] for y in BITS):
                expected[target] = required
        assert {ranking: set(sets) for ranking, sets in stable.items()} == expected
        matrices += 1
    return matrices, cases


def worked_example():
    witnesses = {(x, y): tuple(z for z in BITS if (x and z) or not y)
                 for x, y in product(BITS, repeat=2)}
    assert witnesses == {(0, 0): (0, 1), (0, 1): (), (1, 0): (0, 1), (1, 1): (1,)}
    for x, y in product(BITS, repeat=2):
        for t in BITS:
            assert witnesses[x, y] == tuple(z for z in BITS if (x and z) or not y or (0 and t))
    # The original source can use the same formula in multiple classes. A
    # repeated low-priority formula leaves all prefix membership sets intact.
    rows = [frozenset(row) for row in ({0}, {1}, {1, 2})]
    assert maxcons(rows, ({0}, {0, 1}, {1, 2}), (0, 1, 2)) == [rows[0]]
    assert maxcons(rows, ({0}, {1}, {2}), (0, 1, 2)) == [rows[0]]


if __name__ == "__main__":
    matrices, comparisons = census()
    print(f"All {matrices} one-bit-per-block QBF matrices match tripartition existence.")
    print(f"All {comparisons:,} fixed-challenge survivor and rival-Good checks passed.")
    worked_example()
    print("The worked repair witnesses and a repeated-priority formula case passed.")
