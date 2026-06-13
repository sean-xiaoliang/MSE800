"""Board model for the Tic-tac-toe game.

Holds the 3x3 grid state and knows how to render itself. Contains no
game rules (who wins, whose turn) — that lives in game.py.
"""

EMPTY = " "
SIZE = 3
CELL_COUNT = SIZE * SIZE


class Board:
    """A 3x3 Tic-tac-toe grid stored as a flat list of 9 cells (index 0-8)."""

    def __init__(self):
        self.cells = [EMPTY] * CELL_COUNT

    def is_empty(self, index: int) -> bool:
        """Return True if the cell at index (0-8) is unoccupied."""
        return self.cells[index] == EMPTY

    def place(self, index: int, mark: str) -> None:
        """Place mark ('X' or 'O') at index. Raises ValueError if taken."""
        if not self.is_empty(index):
            raise ValueError(f"Cell {index + 1} is already taken.")
        self.cells[index] = mark

    def is_full(self) -> bool:
        """Return True if every cell is occupied."""
        return all(cell != EMPTY for cell in self.cells)

    def render(self) -> str:
        """Return the board as a printable string.

        Empty cells show their 1-based position number to guide input.
        """
        labels = [
            str(i + 1) if cell == EMPTY else cell
            for i, cell in enumerate(self.cells)
        ]
        rows = [
            f" {labels[r]} | {labels[r + 1]} | {labels[r + 2]} "
            for r in range(0, CELL_COUNT, SIZE)
        ]
        separator = "\n" + "-" * 11 + "\n"
        return separator.join(rows)
