import numpy as np
import copy
import random
import tkinter as tk
from threading import Thread
import time

def boardMaking():
    board = np.zeros((4, 4), dtype=int)
    return board

def addingTile(board):
    emptyCells = []
    for r in range(4):
        for c in range(4):
            if board[r][c] == 0:
                emptyCells.append((r, c))

    if len(emptyCells) > 0:
        index = random.randint(0, len(emptyCells) - 1)
        r, c = emptyCells[index]

        probcontrol = random.random()
        if probcontrol < 0.9:
            board[r][c] = 2
        else:
            board[r][c] = 4

def gameStart():
    board = boardMaking()
    addingTile(board)
    addingTile(board)
    return board

def leftMove(board):
    for row in range(4):
        newRow = []
        for col in range(4):
            if board[row][col] != 0:
                newRow.append(board[row][col])

        MergedRow = []
        skip = False
        for i in range(len(newRow)):
            if skip:
                skip = False
                continue
            if i + 1 < len(newRow) and newRow[i] == newRow[i + 1]:
                MergedRow.append(newRow[i] * 2)
                skip = True
            else:
                MergedRow.append(newRow[i])

        while len(MergedRow) < 4:
            MergedRow.append(0)

        for col in range(4):
            board[row][col] = MergedRow[col]

def rightMove(board):
    for row in range(4):
        rowReversed = []
        for col in range(3, -1, -1):
            if board[row][col] != 0:
                rowReversed.append(board[row][col])

        MergedRow = []
        skip = False
        for i in range(len(rowReversed)):
            if skip:
                skip = False
                continue
            if i + 1 < len(rowReversed) and rowReversed[i] == rowReversed[i + 1]:
                MergedRow.append(rowReversed[i] * 2)
                skip = True
            else:
                MergedRow.append(rowReversed[i])

        while len(MergedRow) < 4:
            MergedRow.append(0)

        for col in range(4):
            board[row][3 - col] = MergedRow[col]

def transpose(board):
    for i in range(4):
        for j in range(i + 1, 4):
            board[i][j], board[j][i] = board[j][i], board[i][j]

def moveUp(board):
    transpose(board)
    leftMove(board)
    transpose(board)

def moveDown(board):
    transpose(board)
    rightMove(board)
    transpose(board)

def possibleMoves(board):
    moves = []
    origBoard = copy.deepcopy(board)

    for move, func in zip("8462", [moveUp, leftMove, moveDown, rightMove]):
        test = board.copy()
        func(test)
        if not np.array_equal(origBoard, test):
            moves.append(move)

    return moves

def gameSimulation(board):
    tempBoard = copy.deepcopy(board)
    score = 0

    while True:
        moves = possibleMoves(tempBoard)
        if not moves:
            break

        move = random.choice(moves)

        if move == '8':
            moveUp(tempBoard)
        elif move == '4':
            leftMove(tempBoard)
        elif move == '2':
            moveDown(tempBoard)
        elif move == '6':
            rightMove(tempBoard)

        addingTile(tempBoard)
        score = np.max(tempBoard)

    return score

def getbestMove(board, simulationpermove=20):
    moves = possibleMoves(board)
    bestScore = -1
    bestMove = None
    for move in moves:
        totalscore = 0
        for m in range(simulationpermove):
            tempBoard = copy.deepcopy(board)

            if move == '8':
                moveUp(tempBoard)
            elif move == '4':
                leftMove(tempBoard)
            elif move == '2':
                moveDown(tempBoard)
            elif move == '6':
                rightMove(tempBoard)

            addingTile(tempBoard)
            totalscore += gameSimulation(tempBoard)

        avgScore = totalscore / simulationpermove

        if avgScore > bestScore:
            bestScore = avgScore
            bestMove = move

    return bestMove

def visualizeBoard(board):
    window = tk.Tk()
    window.title("CODING TASK BY 24AR10034")
    cellLabels = [[tk.Label(window, width=5, height=2, font=("Arial", 24), bg="#cdc1b4", borderwidth=2, relief="groove") for _ in range(4)] for _ in range(4)]

    for i in range(4):
        for j in range(4):
            cellLabels[i][j].grid(row=i, column=j, padx=5, pady=5)

    statusLabel = tk.Label(window, text="Running...", font=("Arial", 16), fg="blue")
    statusLabel.grid(row=4, column=0, columnspan=4)

    def getColor(value):
        colors = {
            0: "#cdc1b4", 2: "#eee4da", 4: "#ede0c8", 8: "#f2b179",
            16: "#f59563", 32: "#f67c5f", 64: "#f65e3b", 128: "#edcf72",
            256: "#edcc61", 512: "#edc850", 1024: "#edc53f", 2048: "#edc22e"
        }
        return colors.get(value, "#3c3a32")

    def updateGui():
        for i in range(4):
            for j in range(4):
                val = board[i][j]
                cellLabels[i][j]['text'] = '' if val == 0 else str(val)
                cellLabels[i][j]['bg'] = getColor(val)
        window.update()

    def runAi():
        count = 0
        while True:
            updateGui()
            time.sleep(0.025)

            if 2048 in board:
                statusLabel.config(text=f"🎉 Victory in {count} moves!", fg="green")
                break

            move = getbestMove(board)
            if not move:
                statusLabel.config(text=f"☠️ Game Over in {count} moves", fg="red")
                return

            if move == '8':
                moveUp(board)
            elif move == '4':
                leftMove(board)
            elif move == '2':
                moveDown(board)
            elif move == '6':
                rightMove(board)

            count += 1
            addingTile(board)

            statusLabel.config(text=f"Moves: {count}", fg="blue")

        updateGui()

    Thread(target=runAi, daemon=True).start()
    window.mainloop()

if __name__ == "__main__":
    visualizeBoard(gameStart())