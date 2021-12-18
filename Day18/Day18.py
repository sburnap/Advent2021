from typing import List, Any


def read_input(filename: str) -> List[Any]:

    return [eval(line.strip()) for line in open(filename)]


Snailnum = List[Any]


def add(num1: Snailnum, num2: Snailnum) -> Snailnum:
    return [num1] + [num2]


def explode(num: Snailnum) -> Snailnum:

    for target in range(len(num)):
        if type(num[target]) == list:
            left = num[target][0]
            right = num[target][1]
            num[target] = 0

            prev = target
            while prev > 0:
                prev -= 1
                if type(num[prev]) == int:
                    num[prev] += left
                    break

            next = target
            while next < len(num) - 1:
                next += 1
                if type(num[next]) == int:
                    num[next] += right
                    break
            break

    return num


def reduce(num: Snailnum, depth: int = 0) -> Snailnum:
    if type(num) == list:
        if depth == 3:
            return explode(num)
        for i in range(len(num)):
            num[i] = reduce(num[i], depth + 1)

    return num


def part_one(filename: str) -> int:

    testinput = read_input(filename)

    print(add(testinput[0], testinput[1]))
    return 0


def test_reduce(num1: Snailnum, num2: Snailnum) -> None:
    ex = reduce(num1)
    assert ex == num2, ex


def run_tests() -> None:
    ex1 = add([1, 2], [[3, 4], 5])
    assert ex1 == [[1, 2], [[3, 4], 5]], ex1

    ex2 = explode([[9, 8], 1])
    assert ex2 == [0, 9], ex2

    test_reduce([[[[[9, 8], 1], 2], 3], 4], [[[[0, 9], 2], 3], 4])
    test_reduce([7, [6, [5, [4, [3, 2]]]]], [7, [6, [5, [7, 0]]]])

    test_reduce([[6, [5, [4, [3, 2]]]], 1], [[6, [5, [7, 0]]], 3])

    test_reduce(
        [[3, [2, [1, [7, 3]]]], [6, [5, [4, [3, 2]]]]],
        [[3, [2, [8, 0]]], [9, [5, [4, [3, 2]]]]],
    )
    test_reduce(
        [[3, [2, [8, 0]]], [9, [5, [4, [3, 2]]]]], [[3, [2, [8, 0]]], [9, [5, [7, 0]]]]
    )


if __name__ == "__main__":
    run_tests()

    print("A:")
    # print(f"Testinput value is {part_one('Day18/Day18TestInput1.txt')}")
    # print(f"Realinput value is {part_one(realinput)}")

    print("B:")
    # print(f"Testinput value is {part_two(testinput)}")
    # print(f"Realinput value is {part_two(realinput)}")
