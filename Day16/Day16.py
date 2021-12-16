from typing import Tuple, Dict, Any, List

testinput = [
    "D2FE28",
    "38006F45291200",
    "EE00D40C823060",
    "8A004A801A8002F478",
    "620080001611562C8802118E34",
    "C0015000016115A2E0802F182340",
    "A0016C880162017C3686B18A3D4780",
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
    results = {}

    results["version"], binary = parse_version(binary)
    results["typeid"], binary = parse_version(binary)
    if results["typeid"] == 4:
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
            f"{'    '*tabs} {results['version']} - {results['typeid']} {results['literal']}"
        )
    elif "subpacketLength" in results:
        print(
            f"{'    '*tabs} {results['version']} - {results['typeid']} LEN {results['subpacketLength']}"
        )
    elif "subpacketNumber" in results:
        print(
            f"{'    '*tabs} {results['version']} - {results['typeid']} NUM {results['subpacketNumber']}"
        )
    if "packets" in results:
        for packet in results["packets"]:
            print_packet(packet, tabs + 1)


def part_one(inp: str, display: bool) -> int:
    parsed, _ = parse_component(bin(int(inp, 16))[2:].zfill(len(inp * 4)))
    if display:
        print_packet(parsed)
    return version_sum(parsed)


if __name__ == "__main__":

    print("A:")
    for line in testinput:
        print(f"Testinput value is {part_one(line, True)}")
    print(
        f"Realinput value is {part_one(next(line.strip() for line in open('Day16/Day16Input.txt')), False)}"
    )

    print("B:")
    # print(f"Testinput value is {day_two('Day16/Day16TestInput.txt')}")
    # print(f"Realinput value is {day_two('Day16/Day16Input.txt')}")
