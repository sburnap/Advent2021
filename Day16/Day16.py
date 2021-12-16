from typing import Tuple, Dict, Any, List
import operator
from functools import reduce

testinput1 = [
    "D2FE28",
    "38006F45291200",
    "EE00D40C823060",
    "8A004A801A8002F478",
    "620080001611562C8802118E34",
    "C0015000016115A2E0802F182340",
    "A0016C880162017C3686B18A3D4780",
]

testinput2 = [
    "C200B40A82",
    "04005AC33890",
    "880086C3E88112",
    "CE00C43D881120",
    "D8005AC2A8F0",
    "F600BC2D8F",
    "9C005AC2F8F0",
    "9C0141080250320F1802104A08",
]


def parse_version(binary: str) -> Tuple[int, str]:
    return int(binary[:3], 2), binary[3:]


def parse_typeid(binary: str) -> Tuple[int, str]:
    return int(binary[:3], 2), binary[3:]


def parse_literal(binary: str) -> Tuple[int, str]:
    literal = ""
    endval = False
    while not endval:
        endval = binary[0] == "0"
        literal += binary[1:5]
        binary = binary[5:]
    return int(literal, 2), binary


def parse_mode(binary: str) -> Tuple[int, str]:
    return int(binary[:1], 2), binary[1:]


def parse_length(binary: str) -> Tuple[int, str]:
    return int(binary[:15], 2), binary[15:]


def parse_number(binary: str) -> Tuple[int, str]:
    return int(binary[:11], 2), binary[11:]


def parse_component(binary: str) -> Tuple[Dict[str, Any], str]:
    opcodes = ["+", "*", "min", "max", "LIT", ">", "<", "="]
    results = {}

    results["version"], binary = parse_version(binary)
    typeid, binary = parse_version(binary)
    results["opcode"] = opcodes[typeid]
    if results["opcode"] == "LIT":
        results["literal"], binary = parse_literal(binary)
    else:
        results["mode"], binary = parse_mode(binary)

        if results["mode"] == 0:
            results["subpacketLength"], binary = parse_length(binary)

            results["packets"], binary = parse_components_by_length(
                binary, results["subpacketLength"]
            )
        else:
            results["subpacketNumber"], binary = parse_number(binary)

            results["packets"], binary = parse_components_by_number(
                binary, results["subpacketNumber"]
            )

    return results, binary


def parse_components_by_length(binary: str, length: int) -> List[Any]:
    to_parse = binary[:length]
    results = []
    while len(to_parse) > 0:
        result, to_parse = parse_component(to_parse)
        results.append(result)

    return results, binary[length:]


def parse_components_by_number(binary: str, number: int) -> List[Any]:
    results = []
    for i in range(number):
        result, binary = parse_component(binary)
        results.append(result)

    return results, binary


def version_sum(results: Dict[str, Any]) -> int:
    if "packets" in results:
        return results["version"] + sum(
            version_sum(subpacket) for subpacket in results["packets"]
        )
    else:
        return results["version"]


def print_packet(results, tabs=0):
    literal = results["literal"] if "literal" in results else "*"
    if "literal" in results:
        print(
            f"{'    '*tabs} {results['version']} : {results['opcode']} {results['literal']}"
        )
    elif "subpacketLength" in results:
        print(
            f"{'    '*tabs} {results['version']} : [{results['subpacketLength']}] {results['opcode']}"
        )
    elif "subpacketNumber" in results:
        print(
            f"{'    '*tabs} {results['version']} : #{results['subpacketNumber']} {results['opcode']}"
        )
    if "packets" in results:
        for packet in results["packets"]:
            print_packet(packet, tabs + 1)


def calculate(results: Dict[str, Any]) -> int:

    opcode = results["opcode"]

    if opcode == "LIT":
        return results["literal"]

    data = [calculate(packet) for packet in results["packets"]]

    if opcode == "+":
        return sum(data)
    elif opcode == "*":
        return reduce(operator.mul, data, 1)
    elif opcode == "min":
        return min(data)
    elif opcode == "max":
        return max(data)
    elif opcode == ">":
        return 1 if data[0] > data[1] else 0
    elif opcode == "<":
        return 1 if data[0] < data[1] else 0
    elif opcode == "=":
        return 1 if data[0] == data[1] else 0


def part_one(inp: str, display: bool) -> int:
    parsed, _ = parse_component(bin(int(inp, 16))[2:].zfill(len(inp * 4)))
    if display:
        print_packet(parsed)
    return version_sum(parsed)


def part_two(inp: str, display: bool) -> int:
    parsed, _ = parse_component(bin(int(inp, 16))[2:].zfill(len(inp * 4)))
    if display:
        print_packet(parsed)
    return calculate(parsed)


if __name__ == "__main__":

    print("A:")
    for line in testinput1:
        print(f"Testinput value is {part_one(line, False)}")
    print(
        f"Realinput value is {part_one(next(line.strip() for line in open('Day16/Day16Input.txt')), False)}"
    )

    print("B:")
    for line in testinput2:
        print(f"Testinput value {line} is {part_two(line, False)}")
    print(
        f"Realinput value is {part_two(next(line.strip() for line in open('Day16/Day16Input.txt')), False)}"
    )
