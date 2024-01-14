from tkinter import Tk, Canvas, PhotoImage

from ChessBoard import Piece

# chess piece icons from: https://commons.wikimedia.org/wiki/Category:SVG_chess_pieces
pieceImages = [[""], #noColor has no assets
               ["", "assets/wpawn.png", "assets/wbishop.png", "assets/wknight.png", "assets/wrook.png", "assets/wqueen.png", "assets/wking.png"],
               ["", "assets/bpawn.png", "assets/bbishop.png", "assets/bknight.png", "assets/brook.png", "assets/bqueen.png", "assets/bking.png"]]

def highest(data):
    value = float('-inf')
    for row in data:
        for element in row:
            if (element > value):
                value = element

    return max(value, 1)

class Display(Tk):
    def __init__(self, board, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        self.board = board

        self.rows = 8
        self.columns = 8

        self.cellwidth = 48
        self.cellheight = self.cellwidth

        self.canvas = Canvas(self, width=self.cellwidth * self.columns, height=self.cellheight * self.rows, borderwidth=0, highlightthickness=0)
        self.canvas.pack(side="top", fill="both", expand="true")

        self.squares = [[0 for i in range (self.rows)] for i in range (self.columns)]

        self.bind("<Button-1>", self.tryMovePiece)

        for column in range(self.columns):
            for row in range(self.rows):
                x1 = column * self.cellwidth
                y1 = row    * self.cellheight
                x2 = x1 + self.cellwidth
                y2 = y1 + self.cellheight

                color = "black"

                if ((row + column) % 2 == 0):
                    color = "white"

                self.squares[row][column] = self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, tags="rect")


        # finish initializing the piece piece, so we don't need to generate them each time we draw the pieces
        for rowIndex in range (len (pieceImages)):
            for imageIndex in range (len (pieceImages[rowIndex])):
                pieceImages[rowIndex][imageIndex] = PhotoImage (file = pieceImages[rowIndex][imageIndex])

    def showAttacks(self):
        maxAttack = highest(self.board.attacks)

        for rankIndex in range(self.columns):
            for fileIndex in range(self.rows):
                x1 = rankIndex * self.cellwidth
                y1 = fileIndex * self.cellheight
                x2 = x1 + self.cellwidth
                y2 = y1 + self.cellheight

                self.squares[rankIndex][fileIndex] = self.canvas.create_rectangle(x1, y1, x2, y2,
                                                                                  fill=self.matchColor(self.board.attacks[rankIndex][fileIndex], maxAttack, (rankIndex + fileIndex) % 2 == 0), tags="rect")

    def matchColor(self, attack, maxAttack, isWhite):
        value = attack / maxAttack * 255

        if (value == 0):
            if (isWhite):
                return "#ffffff"

            return "#000000"

        hexVal = hex(int(value)).replace("0x", "")

        if (value > 0):
            return "#00" + hexVal + "00"

        else:
            return "#" + hexVal.replace("-", "") + "0000" # we need to replace the sign returned by hex()

    def showPieces(self):
        for rankIndex in range (self.rows):
            for fileIndex in range (self.columns):
                piece = self.board.pieces[rankIndex][fileIndex]
                pieceImage = pieceImages[piece.color.value][piece.type.value]

                x = fileIndex * self.cellwidth
                y = rankIndex * self.cellheight

                self.canvas.create_image(x, y, anchor = "nw", image = pieceImage)

    def tryMovePiece(self, event):
        self.board.clickedSquare (int(event.x / self.cellwidth), int(event.y / self.cellheight))

        self.showAttacks()
        self.showPieces()
