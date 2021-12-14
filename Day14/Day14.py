from typing import Tuple, List, Dict
from collections import Counter, defaultdict
import re


def get_re_lines(lines: List[str], regex) -> List[Tuple[str, str]]:
    for line in lines:
        if m := regex.match(line):
            yield (m.group(1), m.group(2))


def get_input(filename: str) -> Tuple[str, Tuple[Tuple[str, str]]]:

    lines = [line.strip() for line in open(filename)]

    return (
        lines[0],
        {
            l[0]: l[1]
            for l in get_re_lines(lines[2:], re.compile(r"^([A-Z]+) -> ([A-Z]+)$"))
        },
    )


def pairwise(s: str):
    for i in range(len(s) - 1):
        yield s[i : i + 2]


def one_pass_counts(polymer_cnts: Dict[str, int], rules) -> Dict[str, int]:

    newcnts = defaultdict(int)
    for key in polymer_cnts:
        if key in rules:
            newcnts[key[0] + rules[key]] += polymer_cnts[key]
            newcnts[rules[key] + key[1]] += polymer_cnts[key]
        else:
            newcnts[key] = polymer_cnts[key]

    return newcnts


def execute(filename: str, steps: int) -> int:

    polymer, rules = get_input(filename)

    polymer_cnts = {
        paired: cnt for paired, cnt in Counter(pairwise(polymer)).most_common()
    }
    for i in range(steps):
        polymer_cnts = one_pass_counts(polymer_cnts, rules)
    cnts = Counter()
    cnts[polymer[-1]] = 1
    for key in polymer_cnts:
        cnts[key[0]] += polymer_cnts[key]

    l = cnts.most_common()
    return l[0][1] - l[-1][1]


if __name__ == "__main__":

    print("A:")
    print(f"Testinput value is {execute('Day14/Day14TestInput.txt',10)}")
    print(f"Realinput value is {execute('Day14/Day14Input.txt',10)}")

    print("B:")
    print(f"Testinput value is {execute('Day14/Day14TestInput.txt',40)}")
    print(f"Realinput value is {execute('Day14/Day14Input.txt',40)}")
