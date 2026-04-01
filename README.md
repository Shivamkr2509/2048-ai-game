# 2048 Game with AI

This is an implementation of the 2048 game in Python, featuring an AI player using Monte Carlo Tree Search (MCTS) to automatically play the game. The game includes a graphical user interface (GUI) built with Tkinter to visualize the gameplay.

## Features

- Complete 2048 game logic
- AI player that uses simulations to choose the best moves
- Real-time GUI visualization with color-coded tiles
- Automatic gameplay with move counter

## Requirements

- Python 3.x
- NumPy
- Tkinter (usually included with Python installations)

## Installation

1. Clone or download the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

Run the game:
```
python main.py
```

The AI will automatically start playing the game, and you can watch the GUI update in real-time.

## How it Works

The AI uses Monte Carlo Tree Search by simulating multiple random games for each possible move and selecting the move that leads to the highest average score in those simulations.

## Author

24AR10034