from ChessBoard import ChessBoard
from Display import Display

# change this to modify the position, then run to view
fen =  "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

if __name__ == "__main__":
    board = ChessBoard(fen)
    board.calculateAttacks()

    root = Display(board)

    #we need to rotate the attacks by 270°, since the internal layout doesn't match with matplotlib
    attacks = [[0 for i in range (8)] for i in range (8)]

    for rankIndex in range (8):
        for pieceIndex in range (8):
            attacks[pieceIndex][7 - rankIndex] = board.attacks[rankIndex][pieceIndex]

    root.showAttacks()
    root.showPieces ()

    root.mainloop()
