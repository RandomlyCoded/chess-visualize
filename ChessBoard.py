from enum import Enum

class Piece:
    class Type(Enum):
        NoType = 0
        Pawn   = 1
        Bishop = 2
        Knight = 3
        Rook   = 4
        Queen  = 5
        King   = 6

    class Color(Enum):
        NoClr = 0
        White = 1
        Black = 2

    type = Type.NoType
    color = Color.NoClr

    def __init__(self, c = ' '):
        if (c.isupper()): # white pieces
            self.color = Piece.Color.White

        elif (c.islower()):
            self.color = Piece.Color.Black

        match c.lower():
            case 'p': self.type = Piece.Type.Pawn
            case 'b': self.type = Piece.Type.Bishop
            case 'n': self.type = Piece.Type.Knight
            case 'r': self.type = Piece.Type.Rook
            case 'q': self.type = Piece.Type.Queen
            case 'k': self.type = Piece.Type.King

    def isPiece(self):
        return (self.type != Piece.Type.NoType) and (self.color != Piece.Color.NoClr)

    def invalidate(self):
        self.type = Piece.Type.NoType
        self.color = Piece.Color.NoClr

    def set(self, other):
        self.type = other.type
        self.color = other.color

class ChessBoard:
    castleWKing = True
    castleWQueen = True
    castleBKing = True
    castleBQueen = True

    pieces  = [[Piece for i in range (8)] for i in range (8)] # can't just use operator* since it leads to each rank being the same
    attacks = [[0     for i in range (8)] for i in range (8)]

    pieceSelected = False
    selectedRank = -1
    selectedFile = -1

    def loadFEN (self, fen):
        rank = 0
        file = 0

        for c in fen:
            if (c == '/'):
                rank += 1
                file = 0
                continue

            if (c == ' '):
                return;

            if(c.isnumeric()):
                for i in range(int(c)):
                    self.pieces[rank][file] = Piece(c)
                    file += 1

                continue

            self.pieces[rank][file] = Piece(c);

            file += 1

    # "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    def __init__(self, fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"):
        self.loadFEN(fen)

    def calculateAttacks(self):
        self.attacks = [[0     for i in range (8)] for i in range (8)]

        for rankIndex in range(8):
            for fileIndex in range (8):
                piece = self.pieces[rankIndex][fileIndex]

                value = 1

                if (piece.color == Piece.Color.Black):
                    value = -1

                match piece.type:
                    case Piece.Type.Pawn   : self.addMovesPawn  (rankIndex, fileIndex, piece.color, value)
                    case Piece.Type.Bishop : self.addMovesBishop(rankIndex, fileIndex             , value)
                    case Piece.Type.Knight : self.addMovesKnight(rankIndex, fileIndex             , value)
                    case Piece.Type.Rook   : self.addMovesRook  (rankIndex, fileIndex             , value)
                    case Piece.Type.Queen  : self.addMovesQueen (rankIndex, fileIndex             , value)
                    case Piece.Type.King   : self.addMovesKing  (rankIndex, fileIndex             , value)

    def secureAddAttack (self, file, rank, value):
        if (file >= 0 and file < 8 and
            rank >= 0 and rank < 8):
                self.attacks[rank][file] += value
                return True

        return False

    def addMovesPawn(self, rank, file, color, value):
        if (color == Piece.Color.White):
            self.secureAddAttack(rank - 1, file - 1, value)
            self.secureAddAttack(rank - 1, file + 1, value)

        if (color == Piece.Color.Black):
            self.secureAddAttack(rank + 1, file - 1, value)
            self.secureAddAttack(rank + 1, file + 1, value)

    def addMovesBishop(self, rank, file, value):
        for i in range (1, 8): # start at 1 to skip own square
            if (self.secureAddAttack(rank + i, file + i, value)):
                if (not self.pieces[rank + i][file + i].type == Piece.Type.NoType):
                    break # if there is a piece on the square we are looking add, we add another attack and then finish the diagonal since we can't jump over pieces

            else:
                break # nothing more on this diagonal

        for i in range (1, 8): # start at 1 to skip own square
            if (self.secureAddAttack(rank + i, file - i, value)):
                if (not self.pieces[rank + i][file - i].type == Piece.Type.NoType):
                    break # if there is a piece on the square we are looking add, we add another attack and then finish the diagonal since we can't jump over pieces

            else:
                break # nothing more on this diagonal

        for i in range (1, 8): # start at 1 to skip own square
            if (self.secureAddAttack(rank - i, file + i, value)):
                if (not self.pieces[rank - i][file + i].type == Piece.Type.NoType):
                    break # if there is a piece on the square we are looking add, we add another attack and then finish the diagonal since we can't jump over pieces

            else:
                break # nothing more on this diagonal

        for i in range (1, 8): # start at 1 to skip own square
            if (self.secureAddAttack(rank - i, file - i, value)):
                if (not self.pieces[rank - i][file - i].type == Piece.Type.NoType):
                    break # if there is a piece on the square we are looking add, we add another attack and then finish the diagonal since we can't jump over pieces

            else:
                break # nothing more on this diagonal

    def addMovesKnight(self, rank, file, value):
        self.secureAddAttack(rank - 2, file - 1, value)
        self.secureAddAttack(rank - 1, file - 2, value)
        self.secureAddAttack(rank + 1, file - 2, value)
        self.secureAddAttack(rank + 2, file - 1, value)
        self.secureAddAttack(rank + 2, file + 1, value)
        self.secureAddAttack(rank + 1, file + 2, value)
        self.secureAddAttack(rank - 1, file + 2, value)
        self.secureAddAttack(rank - 2, file + 1, value)

    def addMovesRook(self, rank, file, value):
        for fileOffset in range (1, 8): # skip own square
            if (self.secureAddAttack(rank, file + fileOffset, value)):
                if (not self.pieces[rank][file + fileOffset].type == Piece.Type.NoType):
                    break # if there is a piece on the square we are looking add, we add another attack and then finish the rank since we can't jump over pieces

            else:
                break # nothing more on this rank

        for fileOffset in range (1, 8): # skip own square
            if (self.secureAddAttack(rank, file - fileOffset, value)):
                if (not self.pieces[rank][file - fileOffset].type == Piece.Type.NoType):
                    break # if there is a piece on the square we are looking add, we add another attack and then finish the rank since we can't jump over pieces

            else:
                break # nothing more on this rank

        for rankOffset in range (1, 8): # skip own square
            if (self.secureAddAttack(rank + rankOffset, file, value)):
                if (not self.pieces[rank + rankOffset][file].type == Piece.Type.NoType):
                    break # if there is a piece on the square we are looking add, we add another attack and then finish the file since we can't jump over pieces

            else:
                break # nothing more on this file

        for rankOffset in range (1, 8): # skip own square
            if (self.secureAddAttack(rank - rankOffset, file, value)):
                if (not self.pieces[rank - rankOffset][file].type == Piece.Type.NoType):
                    break # if there is a piece on the square we are looking add, we add another attack and then finish the file since we can't jump over pieces

            else:
                break # nothing more on this file

    def addMovesQueen(self, rank, file, value):
        # the queen is basically a combination of rook and bishop, so we treat it this way:
        self.addMovesRook  (rank, file, value)
        self.addMovesBishop(rank, file, value)

    def addMovesKing(self, rank, file, value):
        for rankOffset in range (-1, 2):
            for fileOffset in range (-1, 2):
                if (not (fileOffset == 0 and rankOffset == 0)):
                    self.secureAddAttack(rank + rankOffset, file + fileOffset, value)

    def clickedSquare(self, file, rank):
        if (self.pieceSelected):
            movedPiece = self.pieces[self.selectedRank][self.selectedFile]
            self.pieces[rank][file].set(movedPiece)

            self.pieces[self.selectedRank][self.selectedFile].invalidate()
            self.pieceSelected = False

            self.calculateAttacks()

            print("moved piece")

        else:
            if(not self.pieces[rank][file].isPiece()):
                return

            self.pieceSelected = True
            self.selectedRank = rank
            self.selectedFile = file

            print("selected piece")
