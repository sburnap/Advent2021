from itertools import zip_longest
import operator

# From itertools docs
def grouper(iterable, n, fillvalue=None):
    "Collect data into non-overlapping fixed-length chunks or blocks"
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


def columns(board):
    for i in range(len(board[0])):
        yield [row[i] for row in board]


class Bingo:
    def __init__(self, inputfile):
        lines = [l.strip() for l in open(inputfile)]
        self.moves = lines[0].split(",")

        self.boards = [
            [line.split() for line in blines[:-1]] for blines in grouper(lines[2:], 6)
        ]

        self.wins = set()

    @staticmethod
    def board_wins(board):
        return any(all(i == 0 for i in l) for l in board) or any(
            all(i == 0 for i in c) for c in columns(board)
        )

    @staticmethod
    def play_on_board(move, board):
        for i in range(len(board)):
            for j in range(len(board[0])):
                if move == board[i][j]:
                    board[i][j] = 0
                    break

    def play_to_bingo(self):
        for move in self.moves:
            for b, board in enumerate(self.boards):
                if b not in self.wins:
                    self.play_on_board(move, board)
                    if self.board_wins(board):
                        self.wins.add(b)
                        yield int(move) * self.score(board)

    @staticmethod
    def score(board):
        return sum(int(s) for s in sum(board, []))


def run_bingo(infile, order):
    return list(Bingo(infile).play_to_bingo())[order]


def day_one(infile):
    return run_bingo(infile, 0)


def day_two(infile):
    return run_bingo(infile, -1)


if __name__ == "__main__":
    print("A:")
    print(f"Testinput value is {day_one('Day4/Day4testinput.txt')}")
    print(f"Realinput value is {day_one('Day4/Day4Input.txt')}")
    print("B:")
    print(f"Testinput value is {day_two('Day4/Day4testinput.txt')}")
    print(f"Realinput value is {day_two('Day4/Day4Input.txt')}")
