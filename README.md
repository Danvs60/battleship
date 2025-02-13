# Battleship Game

## Overview
Battleship is a 1v1 strategy guessing game where players aim to sink their opponent's ships. This version includes traditional features with tweaks for a more fast-paced experience.
For the purposes of this take-home test, a GUI implementation is not provided and adjustments will need to be made to account for a more limited test environment.

## Game Rules and Mechanics
- **Objective**: Sink all of your opponent's ships.
- **Players**: Player vs Player or Player vs Naive AI.
- **Board Size**: 10x10 grid (Coordinates: A-J, 1-10).
- **Ships**:
  - Carrier: 5 cells
  - Battleship: 4 cells
  - Cruiser: 3 cells
  - Submarine: 3 cells
  - Destroyer: 2 cells
- **Ship Placement**:
  - Ships cannot be placed diagonally. Only Vertical and horizontal placement is allowed.
  - Ships cannot be off the grid.
  - Ships cannot overlap.
  - Ships cannot move.
- **Turns**: Each player starts with 1 guess per turn. Continue guessing if correct.
- **Guessing**: Players cannot guess the same coordinate twice in the same game.
- **Winning**: Sink all of the opponent's ships.

## User Interface
- **Input**: Command line text input.
- **Display**: Command line output.
- **Feedback**: Provided via command line.

## Game Modes
- **Single Player**: AI takes random guesses.
- **Multiplayer**: Local multiplayer only.

## AI and Difficulty Levels
- **AI Behavior**: Random guessing.
- **Difficulty Levels**: Single difficulty level.

## Additional Features
- **Save and Load**: Save game progress.
- **Statistics and Scores**: Leaderboard available.
- **Customization**: Options for game type, board size, random ship placement, and ship configurations.

## Technical Requirements
- **Language**: Python (OOP support).
- **Libraries**: None.
- **Platform**: Tested on Linux.

## Testing and Debugging
- **Testing**: Unit and integration tests.
- **Bug Tracking**: Error-handling with detailed bug locations.

## Documentation
- **User Manual**: Available at game startup.
- **Developer Documentation**: Included in the repository.

## Installation
Requires Python interpreter.

## Usage
Play via the command line interface.
