from collections import defaultdict


class GobangSolver:
    def __init__(self, ques: list[list[int]]):
        self.board = ques
        self.n = len(ques)

    def find_four_in_line(self) -> list[list[int]] | None:
        for line in self._iterate_lines():
            elements = [self.board[r][c] for r, c in line]
            freq = self._count_freq(elements)

            if self.n - 1 not in freq.values() or freq.get(0) == self.n - 1:
                continue

            correct_num = next(num for num, cnt in freq.items() if cnt == self.n - 1)
            try:
                zero_idx = elements.index(0)
            except ValueError:
                continue

            fill_pos = line[zero_idx]
            remove_pos = self._find_remove_candidate(correct_num, line)

            if remove_pos:
                return [[remove_pos[0], remove_pos[1]], [fill_pos[0], fill_pos[1]]]

    def _iterate_lines(self):
        for row in range(self.n):
            yield [(row, c) for c in range(self.n)]
        for col in range(self.n):
            yield [(r, col) for r in range(self.n)]

        for start_row in range(self.n):
            yield [(start_row + i, i) for i in range(self.n - start_row)]
        for start_col in range(1, self.n):
            yield [(i, start_col + i) for i in range(self.n - start_col)]
            
        for start_row in range(self.n):
            yield [(start_row - i, i) for i in range(start_row + 1)]
        for start_col in range(1, self.n):
            yield [(self.n - 1 - i, start_col + i) for i in range(self.n - start_col)]

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