from typing import List, Any, Tuple, Union, Generator
import re

re_pair = re.compile(r"^\[(\d+),(\d+)\]")

re_digit = re.compile(r"(\[|,)(\d+)")


def read_input(filename: str) -> List[Any]:

    return [eval(line.strip()) for line in open(filename)]


def part_one(filename: str) -> int:

    testinput = read_input(filename)

    return 0


def add(left: str, right: str) -> str:

    return "[" + left + "," + right + "]"


def sum_snail(input: List[str]) -> str:

    gen = iter(input)
    a = next(gen)
    for b in gen:
        a = add(a, b)
        a = reduce_loop(a)

    return a


def add_right(num: str, val: int):
    start = None
    i = 0
    while i < len(num):
        if num[i].isdigit():
            start = i
            break
        i += 1

    if not start:
        return num

    end = start + 1
    while i < len(num):
        if not num[i].isdigit():
            end = i
            break
        i += 1

    left = num[:start]
    right = num[end:]
    middle = str(int(num[start:end]) + val)

    return left + middle + right


def add_left(num: str, val: int):
    end = None
    i = len(num) - 1
    while i >= 0:
        if num[i].isdigit():
            end = i + 1
            break
        i -= 1

    if not end:
        return num

    start = end - 1
    while i >= 0:
        if num[i].isdigit():
            start = i
        else:
            break
        i -= 1

    left = num[:start]
    right = num[end:]
    middle = str(int(num[start:end]) + val)

    return left + middle + right


def explode(num: str, pos: int, left: str, right: str) -> str:
    length = len(left) + len(right) + 3
    i = pos - 1
    leftside = add_left(num[:pos], int(left))
    rightside = add_right(num[pos + length :], int(right))
    return leftside + "0" + rightside


re_number = re.compile("(\d+)")


def pull_value(num: str, pos: int):
    if m := re_number.match(num[pos:]):
        left = num[:pos]
        right = num[pos + len(m.group(1)) :]
        val = int(m.group(1))

        return left, right, val


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

        if depth > 4 and num[i + 1] in "01234567890":
            m = re_pair.match(num[i:])
            if m:
                left = m.group(1)
                right = m.group(2)
                return True, explode(num, i, left, right)

    for i in range(len(num)):
        if num[i] in "01234567890" and num[i + 1] in "01234567890":
            return True, split(num, i)

    return False, num


def reduce_loop(num: str) -> str:
    while True:
        result, num = reduce_step(num)
        if not result:
            return num


def test_explode(src: str, target: str, pos: int):
    val = explode(src, pos)
    assert val == target, f"{val} vs {target}"


def test_split(src: str, target: str, pos: int):
    val = split(src, pos)
    assert val == target, f"{val} vs {target}"


def test_reduce_step(src: str, target: str):
    val = reduce_step(src)
    assert val == target, f"{val} vs {target}"


def magnitude(data: Union[int, List[Any]]) -> int:

    if type(data) == int:
        return data
    else:
        return magnitude(data[0]) * 3 + magnitude(data[1]) * 2


def run_tests() -> None:
    val = add("[1,2]", "[[3,4],5]")
    assert val == "[[1,2],[[3,4],5]]"

    val = reduce_loop(add("[[[[4,3],4],4],[7,[[8,4],9]]]", "[1,1]"))
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
        for j in range(len(input)):
            if i != j:
                val = sum_snail([input[i], input[j]])
                yield magnitude(eval(val))
                val = sum_snail([input[j], input[i]])
                mag = magnitude(eval(val))
                yield mag


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
