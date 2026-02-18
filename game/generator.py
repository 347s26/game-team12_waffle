import random
from collections import defaultdict
from django.conf import settings

GRID_SIZE = 5

# waffle word positions
H_ROWS = [0, 2, 4]
V_COLS = [0, 2, 4]


class WafflePuzzle:
    def __init__(self, grid, h_words, v_words):
        self.grid = grid
        self.h_words = h_words
        self.v_words = v_words

    def __str__(self):
        lines = []
        for row in self.grid:
            line = " ".join(ch if ch else " " for ch in row)
            lines.append(line)
        grid_str = "\n".join(lines)

        h_str = "H: " + ", ".join(self.h_words)
        v_str = "V: " + ", ".join(self.v_words)

        return f"{grid_str}\n\n{h_str}\n{v_str}"


def load_words():
    word_file = settings.BASE_DIR / "game" / "wordlist" / "words.txt"

    with open(word_file) as f:
        return [w.strip().upper() for w in f if len(w.strip()) == 5]


def build_index(words):
    """
    index[pos][letter] -> set(words)
    speeds up vertical matching
    """
    index = [defaultdict(set) for _ in range(5)]
    for w in words:
        for i, ch in enumerate(w):
            index[i][ch].add(w)
    return index


def generate_waffle(words):
    index = build_index(words)

    while True:
        # pick 3 horizontal words
        h_words = random.sample(words, 3)

        # required vertical patterns
        patterns = []
        for col in V_COLS:
            pattern = [
                h_words[0][col],
                None,
                h_words[1][col],
                None,
                h_words[2][col],
            ]
            patterns.append(pattern)

        v_words = []

        valid = True
        for p in patterns:
            candidates = set(words)

            for pos, letter in enumerate(p):
                if letter:
                    candidates &= index[pos][letter]

            if not candidates:
                valid = False
                break

            v_words.append(random.choice(list(candidates)))

        if not valid:
            continue

        # build grid
        grid = [[None] * GRID_SIZE for _ in range(GRID_SIZE)]

        # place horizontals
        for r, word in zip(H_ROWS, h_words):
            for c, ch in enumerate(word):
                grid[r][c] = ch

        # place verticals
        for c, word in zip(V_COLS, v_words):
            for r, ch in enumerate(word):
                if grid[r][c] and grid[r][c] != ch:
                    valid = False
                    break
                grid[r][c] = ch
            if not valid:
                break

        if not valid:
            continue

        return WafflePuzzle(grid, h_words, v_words)


WORDS = load_words()
print(WORDS[10])
