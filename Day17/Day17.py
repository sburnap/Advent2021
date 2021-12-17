from typing import Tuple, Generator, List

testinput: Tuple[Tuple[int, int], Tuple[int, int]] = ((20, 30), (-10, -5))
realinput: Tuple[Tuple[int, int], Tuple[int, int]] = ((155, 182), (-117, -67))


def positionx(
    position: int, velocity: int, minimum: int, maximum: int
) -> Generator[int, None, None]:
    step = 0
    while velocity > 0 and position <= maximum:
        position += velocity
        if position >= minimum and position <= maximum:
            yield step, position
        velocity -= 1
        step += 1


def positiony(
    position: int, velocity: int, minimum: int, maximum: int
) -> Generator[int, None, None]:
    step = 0
    while position >= minimum:
        position += velocity
        if position >= minimum and position <= maximum:
            yield step, position
        velocity -= 1
        step += 1


def run(vx: int, vy: int, targetx: int, targety: int) -> int:
    x = y = 0
    maxheight = 0
    while y >= min(targety):
        x += vx
        y += vy
        if y > maxheight:
            maxheight = y

        if vx > 0:
            vx -= 1
        vy -= 1

        if x in targetx and y in targety:
            return maxheight

    return None


def get_heights(targetx, targety, minvx, minvy, maxvx, maxvy) -> List[int]:
    heights = []
    for vx in range(minvx, maxvx):
        for vy in range(minvy, maxvy):
            if (height := run(vx, vy, targetx, targety)) != None:
                heights.append(height)

    return heights


def part_one(target: Tuple[Tuple[int, int], Tuple[int, int]]) -> int:

    targetx = set(range(target[0][0], target[0][1] + 1))
    targety = set(range(target[1][0], target[1][1] + 1))
    return max(get_heights(targetx, targety, 0, 0, 200, 200))


def part_two(target: Tuple[Tuple[int, int], Tuple[int, int]]) -> int:

    targetx = set(range(target[0][0], target[0][1] + 1))
    targety = set(range(target[1][0], target[1][1] + 1))
    return len(get_heights(targetx, targety, 0, -117, 200, 200))


if __name__ == "__main__":
    print("A:")
    print(f"Testinput value is {part_one(testinput)}")
    print(f"Realinput value is {part_one(realinput)}")

    print("B:")
    print(f"Testinput value is {part_two(testinput)}")
    print(f"Realinput value is {part_two(realinput)}")
