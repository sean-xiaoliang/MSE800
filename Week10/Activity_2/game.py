"""Game rules for Tic-tac-toe.

Pure logic: detecting a winner, detecting a draw, and tracking whose
turn it is. Knows nothing about input/output (that lives in main.py).
"""

from typing import List, Optional

from board import Board, EMPTY

# The eight winning lines, as index triples into the flat 9-cell board.
WINNING_LINES = (
    (0, 1, 2), (3, 4, 5), (6, 7, 8),   # rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8),   # columns
    (0, 4, 8), (2, 4, 6),              # diagonals
)


def find_winner(cells: List[str]) -> Optional[str]:
    """Return the winning mark ('X' or 'O'), or None if there is no winner."""
    for a, b, c in WINNING_LINES:
        if cells[a] != EMPTY and cells[a] == cells[b] == cells[c]:
            return cells[a]
    return None


class Game:
    """Coordinates two players taking turns on a single board."""

    PLAYERS = ("X", "O")

    def __init__(self):
        self.board = Board()
        self.current = self.PLAYERS[0]

    def play_turn(self, index: int) -> None:
        """Place the current player's mark at index (0-8)."""
        self.board.place(index, self.current)

    def switch_player(self) -> None:
        """Hand the turn to the other player."""
        self.current = self.PLAYERS[1] if self.current == self.PLAYERS[0] \
            else self.PLAYERS[0]

    def winner(self) -> Optional[str]:
        """Return the winning mark, or None if nobody has won yet."""
        return find_winner(self.board.cells)

    def is_draw(self) -> bool:
        """Return True if the board is full with no winner."""
        return self.board.is_full() and self.winner() is None

    def is_over(self) -> bool:
        """Return True if the game has ended (win or draw)."""
        return self.winner() is not None or self.board.is_full()
