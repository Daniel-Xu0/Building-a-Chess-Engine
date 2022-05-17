"""
Chessboard Class
DS 3500 Final Project
"""

from pieces import King, Queen, Rook, Bishop, Knight, Pawn
from tabulate import tabulate

pieces = ['', Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]


class chessboard():
    """Generate an 8x8 chessboard"""
    """b = Black Piece, w = White Pieces
    R = Rook, N = Knight, B = Bishop, Q = Queen,
    K= King, P= Pawn, __ = Blank"""

    def __init__(self):
        """ Chessboard constructor. Contains white and black chess pieces similar to a normal chessboard

        Attributes:
            board: 2d list containing the pieces
            material_eval: strict material evaluation of the board
        """
        self.board = [[pieces[file + 1]('Black', (rank, file)) if rank == 0
                       else Pawn('Black', (rank, file)) if rank == 1
                       else Pawn('White', (rank, file)) if rank == 6
                       else pieces[file + 1]('White', (rank, file)) if rank == 7
                       else '--' for file in range(0, 8)] for rank in range(0, 8)]

        self.flattened = sum(self.board, [])
        self.material_eval = self.piece_eval()
        self.minor_pieces = self.num_minor()
        self.major_pieces = self.num_major()

    def print_board(self):
        board_rep = [[piece for piece in self.board[i]] + [8 - i] for i in range(0, 8)]
        board_rep.insert(0, ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', ' '])
        print(tabulate(board_rep, headers='firstrow', tablefmt='fancy_grid', stralign='center'))

    def piece_eval(self):
        return sum([piece.val for piece in self.flattened if piece != '--' and piece.color == 'White']) - \
               sum([piece.val for piece in self.flattened if piece != '--' and piece.color == 'Black'])

    def num_minor(self):
        return len([piece for piece in self.flattened if piece != '--' and
                    (piece.name == 'Knight' or piece.name == 'Bishop')])

    def num_major(self):
        return len([piece for piece in self.flattened if piece != '--' and
                    (piece.name == 'Rook' or piece.name == 'Queen')])

    def pawn_count(self):
        return len([piece for piece in self.flattened if piece != '--' and
                    (piece.name == 'Pawn')])

