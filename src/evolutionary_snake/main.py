"""Main entry point to run evolutionary-snake"""
from evolutionary_snake import enums


def main(game_mode: enums.GameMode) -> None:
    """Main entry point to run evolutionary-snake."""
    if game_mode == enums.GameMode.HUMAN_PLAYER:
        print("Human player starting...")
    elif game_mode == enums.GameMode.TRAINING:
        print("Training starting...")
    elif game_mode == enums.GameMode.AI_PLAYER:
        print("AI player starting...")
    else:
        print(
            f"Invalid game-mode '{game_mode}' given. "
            f"Choose from {[e.value for e in enums.GameMode]}"
        )
