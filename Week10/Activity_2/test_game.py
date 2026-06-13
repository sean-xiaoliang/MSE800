"""Unit tests for the Tic-tac-toe board and game logic.

Run with:  python -m pytest
"""
# pylint: disable=missing-function-docstring
#   Test function names (test_*) are self-documenting; per common pytest
#   convention, per-function docstrings are omitted to keep tests readable.

import pytest

from board import Board, EMPTY, CELL_COUNT
from game import Game, find_winner


# ── Board tests ──────────────────────────────────────────────────────────

def test_new_board_is_all_empty():
    board = Board()
    assert board.cells == [EMPTY] * CELL_COUNT
    assert not board.is_full()


def test_place_marks_a_cell():
    board = Board()
    board.place(0, "X")
    assert board.cells[0] == "X"
    assert not board.is_empty(0)


def test_place_on_taken_cell_raises():
    board = Board()
    board.place(4, "O")
    with pytest.raises(ValueError):
        board.place(4, "X")


def test_is_full_detects_full_board():
    board = Board()
    for i in range(CELL_COUNT):
        board.place(i, "X")
    assert board.is_full()


def test_render_shows_position_numbers_for_empty_cells():
    board = Board()
    rendered = board.render()
    for n in range(1, CELL_COUNT + 1):
        assert str(n) in rendered


# ── Winner detection ─────────────────────────────────────────────────────

@pytest.mark.parametrize("line", [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),   # rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8),   # columns
    (0, 4, 8), (2, 4, 6),              # diagonals
])
def test_find_winner_detects_every_winning_line(line):
    cells = [EMPTY] * CELL_COUNT
    for idx in line:
        cells[idx] = "X"
    assert find_winner(cells) == "X"


def test_find_winner_returns_none_when_no_winner():
    cells = [EMPTY] * CELL_COUNT
    assert find_winner(cells) is None


def test_find_winner_ignores_empty_line_match():
    # Three empties on a line must not count as a win.
    cells = [EMPTY] * CELL_COUNT
    assert find_winner(cells) is None


# ── Game flow ────────────────────────────────────────────────────────────

def test_game_starts_with_x():
    game = Game()
    assert game.current == "X"


def test_switch_player_alternates():
    game = Game()
    game.switch_player()
    assert game.current == "O"
    game.switch_player()
    assert game.current == "X"


def test_play_turn_places_current_mark():
    game = Game()
    game.play_turn(0)
    assert game.board.cells[0] == "X"


def test_winner_detected_through_game():
    game = Game()
    # X takes the top row: cells 0, 1, 2
    for index in (0, 1, 2):
        game.play_turn(index)
    assert game.winner() == "X"
    assert game.is_over()


def test_draw_is_detected():
    game = Game()
    # A full board with no three-in-a-row:
    #  X | O | X
    #  X | O | O
    #  O | X | X
    layout = ["X", "O", "X", "X", "O", "O", "O", "X", "X"]
    game.board.cells = layout
    assert game.is_draw()
    assert game.winner() is None
    assert game.is_over()


def test_not_over_on_fresh_board():
    game = Game()
    assert not game.is_over()
    assert not game.is_draw()
