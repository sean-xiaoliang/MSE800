"""Command-line interface for a two-player Tic-tac-toe game.

Handles only input/output and the turn loop; all rules live in game.py.
Run with:  python main.py
"""

from board import CELL_COUNT
from game import Game


def _prompt_move(game: Game) -> int:
    """Ask the current player for a cell (1-9) and return its 0-based index.

    Re-prompts until the input is a valid, empty cell.
    """
    while True:
        raw = input(f"Player {game.current}, choose a cell (1-9): ").strip()
        if not raw.isdigit():
            print("  Please enter a number from 1 to 9.")
            continue
        position = int(raw)
        if not 1 <= position <= CELL_COUNT:
            print("  Out of range. Enter a number from 1 to 9.")
            continue
        index = position - 1
        if not game.board.is_empty(index):
            print("  That cell is already taken. Try another.")
            continue
        return index


def _announce_result(game: Game) -> None:
    """Print the final board and the outcome (win or draw)."""
    print("\n" + game.board.render())
    win = game.winner()
    if win is not None:
        print(f"\nPlayer {win} wins! 🎉")
    else:
        print("\nIt's a draw.")


def play() -> None:
    """Run a single game from empty board to a win or draw."""
    game = Game()
    print("=" * 30)
    print("   Tic-tac-toe — Two Players")
    print("=" * 30)
    print("X goes first. Pick cells by their number.\n")

    while not game.is_over():
        print(game.board.render())
        index = _prompt_move(game)
        game.play_turn(index)
        if game.is_over():
            break
        game.switch_player()
        print()

    _announce_result(game)


def main() -> None:
    """Entry point: play rounds until the player chooses to stop."""
    while True:
        play()
        again = input("\nPlay again? (y/n): ").strip().lower()
        if again != "y":
            print("Thanks for playing. Goodbye!")
            return
        print()


if __name__ == "__main__":
    main()
