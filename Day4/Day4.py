from itertools import zip_longest

# From itertools docs
def grouper(iterable, n, fillvalue=None):
    "Collect data into non-overlapping fixed-length chunks or blocks"
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


testinput = [l.strip() for l in open("Day4/Day4testinput.txt")]
# realinput = [l.strip() for l in open("Day4Input.txt")]


def columns(board):
    for i in range(len(board[0])):
        yield [row[i] for row in board]


def board_wins(board):
    return any(all(l) for l in board) or any(all(c) for c in columns(board))


class Input:
    def __init__(self, inputfile):
        lines = [l.strip() for l in open(inputfile)]
        self.moves = lines[0].split(",")

        self.boards = [
            [line.split() for line in blines[:-1]] for blines in grouper(lines[2:], 6)
        ]

        self.plays = [
            [
                [False for _ in range(len(self.boards[0][0]))]
                for _ in range(len(self.boards[0]))
            ]
            for _ in range(len(self.boards))
        ]
        self.wins = set()

    def play(self, wincount):
        for move in self.moves:
            for b in range(len(self.boards)):
                for i in range(len(self.boards[0])):
                    for j in range(len(self.boards[0][0])):
                        if move == self.boards[b][i][j]:
                            self.plays[b][i][j] = True

            for b in range(len(self.boards)):
                if board_wins(self.plays[b]):
                    self.wins.add(b)
                    if len(self.wins) == wincount:
                        return b, int(move)

    def score(self, b):
        score = 0
        for i in range(len(self.boards[0])):
            for j in range(len(self.boards[0][0])):
                if not self.plays[b][i][j]:
                    score += int(self.boards[b][i][j])

        return score


def day_one(infile):
    input = Input(infile)
    winner, move = input.play(1)
    score = input.score(winner)
    return move * score


def day_two(infile):
    input = Input(infile)
    winner, move = input.play(len(input.boards))
    score = input.score(winner)
    return move * score


if __name__ == "__main__":
    print("A:")
    print(f"Testinput value is {day_one('Day4/Day4testinput.txt')}")
    print(f"Realinput value is {day_one('Day4/Day4Input.txt')}")
    print("B:")
    print(f"Testinput value is {day_two('Day4/Day4testinput.txt')}")
    print(f"Realinput value is {day_two('Day4/Day4Input.txt')}")
