from collections import defaultdict


class GobangSolver:
    def __init__(self, ques: list[list[int]]):
        self.board = ques
        self.n = len(ques)

    def find_four_in_line(self) -> list[list[int]] | None:
        for line in self._iterate_lines():
            elements = [self.board[r][c] for r, c in line]
            freq = self._count_freq(elements)

            if 4 not in freq.values() or freq.get(0) == 4:
                continue

            correct_num = next(num for num, cnt in freq.items() if cnt == 4)

            try:
                zero_idx = elements.index(0)
            except ValueError:
                continue

            fill_pos = line[zero_idx]
            remove_pos = self._find_remove_candidate(correct_num, line)

            if remove_pos:
                return [[remove_pos[0], remove_pos[1]], [fill_pos[0], fill_pos[1]]]

    def _iterate_lines(self):
        # Rows and columns
        for row in range(self.n):
            yield [(row, c) for c in range(self.n)]
        for col in range(self.n):
            yield [(r, col) for r in range(self.n)]

        # Diagonals (both directions)
        diag_groups = defaultdict(list)
        for r in range(self.n):
            for c in range(self.n):
                diag_groups[r - c].append((r, c))
        for group in diag_groups.values():
            yield sorted(group, key=lambda x: x[0])

        diag_groups = defaultdict(list)
        for r in range(self.n):
            for c in range(self.n):
                diag_groups[r + c].append((r, c))
        for group in diag_groups.values():
            yield sorted(group, key=lambda x: x[0])

    @staticmethod
    def _count_freq(elements):
        freq = {}
        for num in elements:
            freq[num] = freq.get(num, 0) + 1
        return freq

    def _find_remove_candidate(self, target, exclude):
        exclude_set = set(exclude)
        for r in range(self.n):
            for c in range(self.n):
                if (r, c) not in exclude_set and self.board[r][c] == target:
                    return r, c
