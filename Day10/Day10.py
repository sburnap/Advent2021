from typing import Optional, Union, List
from statistics import median


def match(line: str) -> Union[str, List[str]]:

    stack = []
    matching = {"(": ")", "[": "]", "{": "}", "<": ">"}

    for ch in line:
        if ch in "([{<":
            stack.append(ch)
        elif ch in ")]}>":
            if ch != matching[stack.pop()]:
                return ch
    return stack


def score_error(results: Union[str, List[str]]) -> int:
    score = {")": 3, "]": 57, "}": 1197, ">": 25137}

    return 0 if type(results) == list else score[str(results)]


def part_one(filename: str) -> int:
    return sum(score_error(match(line)) for line in [l.strip() for l in open(filename)])


def score_completion(results: List[str]) -> int:
    score = {"(": 1, "[": 2, "{": 3, "<": 4, None: 0}

    rc = 0
    for ch in results:
        rc *= 5
        rc += score[ch]

    return rc


def part_two(filename: str) -> int:
    goodlines = [
        stack[::-1]
        for stack in [match(line) for line in [l.strip() for l in open(filename)]]
        if type(stack) == list
    ]
    return int(median([score_completion(line) for line in goodlines]))


if __name__ == "__main__":
    print("A:")
    print(f"Testinput value is {part_one('Day10/Day10TestInput.txt')}")
    print(f"Realinput value is {part_one('Day10/Day10Input.txt')}")

    print("B:")
    print(f"Testinput value is {part_two('Day10/Day10TestInput.txt')}")
    print(f"Realinput value is {part_two('Day10/Day10Input.txt')}")
