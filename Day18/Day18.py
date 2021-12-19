from typing import List, Any, Tuple, Union, Generator
import re
from functools import reduce

re_pair = re.compile(r"^\[(\d+),(\d+)\]")
re_number = re.compile("(\d+)")


def add_snail(left: str, right: str) -> str:

    return "[" + left + "," + right + "]"


def sum_snail(input: List[str]) -> str:

    return reduce(lambda x, y: reduce_loop(add_snail(x, y)), input)


def add_right(num: str, val: int) -> str:

    if m := re_number.search(num):

        start = m.start()
        end = m.end()

        return num[:start] + str(int(num[start:end]) + val) + num[end:]

    return num


def add_left(num: str, val: int):
    if m := re_number.search(num[::-1]):

        end = len(num) - m.start()
        start = len(num) - m.end()

        return num[:start] + str(int(num[start:end]) + val) + num[end:]

    return num


def explode(num: str, pos: int, left: str, right: str) -> str:
    return (
        add_left(num[:pos], int(left))
        + "0"
        + add_right(num[pos + len(left) + len(right) + 3 :], int(right))
    )


def pull_value(num: str, pos: int) -> Tuple[str, str, int]:
    if m := re_number.match(num[pos:]):
        return num[:pos], num[pos + len(m.group(1)) :], int(m.group(1))

    raise Exception("Should never happen")


def split(num: str, pos: int) -> str:
    leftstr, rightstr, val = pull_value(num, pos)
    left = val // 2
    right = val - left

    return leftstr + "[" + str(left) + "," + str(right) + "]" + rightstr


def reduce_step(num: str) -> Tuple[bool, str]:

    depth = 0
    i = 0
    for i in range(len(num)):
        if num[i] == "[":
            depth += 1
        elif num[i] == "]":
            depth -= 1

        if depth > 4 and (m := re_pair.match(num[i:])):
            return True, explode(num, i, m.group(1), m.group(2))

    for i in range(len(num)):
        if num[i].isdigit() and num[i + 1].isdigit():
            return True, split(num, i)

    return False, num


def reduce_loop(num: str) -> str:

    result = True
    while result:
        result, num = reduce_step(num)

    return num


def magnitude(data: Union[int, List[Any]]) -> int:

    return (
        data if type(data) == int else magnitude(data[0]) * 3 + magnitude(data[1]) * 2
    )


def test_reduce_step(src: str, target: str):
    val = reduce_step(src)
    assert val == target, f"{val} vs {target}"


def run_tests() -> None:
    val: Any = add_snail("[1,2]", "[[3,4],5]")
    assert val == "[[1,2],[[3,4],5]]"

    val = reduce_loop(add_snail("[[[[4,3],4],4],[7,[[8,4],9]]]", "[1,1]"))
    assert val == "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]", val

    val = sum_snail([f"[{i+1},{i+1}]" for i in range(4)])
    assert val == "[[[[1,1],[2,2]],[3,3]],[4,4]]"

    val = sum_snail([f"[{i+1},{i+1}]" for i in range(5)])
    assert val == "[[[[3,0],[5,3]],[4,4]],[5,5]]"

    val = sum_snail([f"[{i+1},{i+1}]" for i in range(6)])
    assert val == "[[[[5,0],[7,4]],[5,5]],[6,6]]"

    large_test = [
        "[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]",
        "[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]",
        "[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]",
        "[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]",
        "[7,[5,[[3,8],[1,4]]]]",
        "[[2,[2,2]],[8,[8,1]]]",
        "[2,9]",
        "[1,[[[9,3],9],[[9,0],[0,7]]]]",
        "[[[5,[7,4]],7],1]",
        "[[[[4,2],2],6],[8,7]]",
    ]
    val = sum_snail(large_test)
    assert val == "[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]"

    mag_data = [
        ("[9,1]", 29),
        ("[[9,1],[1,9]]", 129),
        ("[[1,2],[[3,4],5]]", 143),
        ("[[[[0,7],4],[[7,8],[6,0]]],[8,1]]", 1384),
        ("[[[[1,1],[2,2]],[3,3]],[4,4]]", 445),
        ("[[[[3,0],[5,3]],[4,4]],[5,5]]", 791),
        ("[[[[5,0],[7,4]],[5,5]],[6,6]]", 1137),
        ("[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]", 3488),
    ]
    for input, res in mag_data:
        val = magnitude(eval(input))
        assert val == res, val


testinput = [
    "[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]",
    "[[[5,[2,8]],4],[5,[[9,9],0]]]",
    "[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]",
    "[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]",
    "[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]",
    "[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]",
    "[[[[5,4],[7,7]],8],[[8,3],8]]",
    "[[9,3],[[9,9],[6,[4,9]]]]",
    "[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]",
    "[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]",
]

realinput = [line.strip() for line in open("Day18/Day18Input.txt")]


def part_one(input: List[str]) -> int:

    val = sum_snail(input)
    mag = magnitude(eval(val))
    return mag


def pairwise_sum_magnitudes(input: List[str]) -> Generator[int, None, None]:
    for i in range(len(input)):
        for j in range(i + 1, len(input)):
            yield magnitude(eval(sum_snail([input[i], input[j]])))
            yield magnitude(eval(sum_snail([input[j], input[i]])))


def part_two(input: List[str]) -> int:

    return max([mag for mag in pairwise_sum_magnitudes(input)])


if __name__ == "__main__":
    run_tests()

    print("A:")
    print(f"Testinput value is {part_one(testinput)}")

    print(f"Realinput value is {part_one(realinput)}")

    print("B:")
    print(f"Testinput value is {part_two(testinput)}")
    print(f"Realinput value is {part_two(realinput)}")
