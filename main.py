from ChessBoard import ChessBoard
from Display import Display

# change this to modify the position, then run to view
fen =  "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

if __name__ == "__main__":
    board = ChessBoard(fen)
    board.calculateAttacks()

    root = Display(board)

    root.showAttacks()
    root.showPieces ()

    root.mainloop()
