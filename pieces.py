"""
Chess Pieces Library
DS3500 Final Project
"""


class Piece:
    """
    Superclass to represent a chess piece
    ...
    Attributes
    ----------
    name: str
        name of the piece
    value: int
        point value of the piece
    color: str
        color of the piece (white or black)
    moves: list
        list of legal moves for the piece
    """
    def __init__(self, color, name, value, pos=(0, 0)):
        self.color = color
        self.name = name
        self.val = value
        self.pos = pos
        self.first_move = True

    def get_pos(self):
        return self.pos

    def __repr__(self):
        if self.color:
            return f'{self.color[0].lower()} {self.name}'
        else:
            return self.name

    def vert_moves(self, board):
        """
        Compute all possible vertical moves
        Args:
            board: the current board/piece locations
            posn: the position of a piece that we want to move (tuple or list?)
        Returns:
            move_list: list of all vertical moves
        """
        x = self.pos[0]
        y = self.pos[1]

        # Directions: (left, down, right, up)
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))

        move_list = []

        for direction in directions:
            for i in range(1, 8):
                # Increment in the possible directions
                end_x = x + direction[0] * i
                end_y = y + direction[1] * i
                # Check if move is on the board
                if 0 <= end_x < 8 and 0 <= end_y < 8:
                    if board[end_x][end_y] == '--':
                        move_list.append((self.pos, (end_x, end_y)))
                    elif board[end_x][end_y].color != self.color:
                        move_list.append((self.pos, (end_x, end_y)))
                        break
                    else:
                        break
                else:
                    break

        return move_list

    def diag_moves(self, board):
        """
        Compute all possible diagonal moves
        Args:
            board: the current board/piece locations
            posn: the position of a piece that we want to move (tuple or list?)
        Returns:
            move_list: list of all diagonal moves
        """
        # Have delta_x/delta_y in the case we're looking at if a move is legal
        # delta_x = 1 if to[0] > start[0] else -1
        # delta_y = 1 if to[1] > start[1] else -1

        x = self.pos[0]
        y = self.pos[1]

        # Directions: (up right, up left, down right, down left)
        directions = [(1, 1), (-1, 1), (1, -1), (-1, -1)]

        move_list = []
        for direction in directions:
            for i in range(1, 8):
                # Increment in the possible directions
                end_x = x + direction[0] * i
                end_y = y + direction[1] * i
                # Check if move is on the board
                if 0 <= end_x < 8 and 0 <= end_y < 8:
                    if board[end_x][end_y] == '--':  # Or whatever we use to denote an empty position
                        move_list.append((self.pos, (end_x, end_y)))
                    elif board[end_x][end_y].color != self.color:
                        move_list.append((self.pos, (end_x, end_y)))
                        break
                    else:
                        break
                else:
                    break

        return move_list


class King(Piece):
    """
    Subclass of Piece Class, represents the King
    ...
    Attributes
    ----------
    name: str
        name of the piece
    value: int
        point value of the piece
    color: str
        color of the piece (white or black)
    moves: list
        list of legal moves for the piece
    """

    def __init__(self, color, pos):
        super().__init__(color, name='King', value=1000, pos=pos)
        self.moves = []

    def valid_moves(self, board):
        x = self.pos[0]
        y = self.pos[1]
        directions = [(0, -1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (1, 1), (1, 0), (1, -1)]

        move_list = []

        for direction in directions:
            # Increment in the possible directions
            end_x = x + direction[0]
            end_y = y + direction[1]
            # Check if move is on the board
            if 0 <= end_x < 8 and 0 <= end_y < 8:
                if board[end_x][end_y] == '--':
                    move_list.append((self.pos, (end_x, end_y)))
                elif board[end_x][end_y].color != self.color:
                    move_list.append((self.pos, (end_x, end_y)))

        self.moves = move_list

        return self.moves

    def castle(self, board, start, to, direction):
        pass


class Queen(Piece):
    """
    Subclass of Piece Class, represents the Queen
    ...
    Attributes
    ----------
    name: str
        name of the piece
    value: int
        point value of the piece
    color: str
        color of the piece (white or black)
    moves: list
        list of legal moves for the piece
    """
    # Not sure if this is necessary, as there is only one queen
    # But in the case of promotion, it would still be considered a queen, but self.value would only be 1

    def __init__(self, color, pos):
        super().__init__(color, name='Queen', pos=pos, value=9)
        self.moves = []

    def valid_moves(self, board):
        self.moves = self.vert_moves(board) + self.diag_moves(board)
        return self.moves


class Rook(Piece):
    """
    Subclass of Piece Class, represents a rook
    ...
    Attributes
    ----------
    name: str
        name of the piece
    value: int
        point value of the piece
    color: str
        color of the piece (white or black)
    moves: list
        list of legal moves for the piece
    """
    def __init__(self, color, pos):
        super().__init__(color, name='Rook', pos=pos, value=5)
        self.moves = []

    def valid_moves(self, board):
        self.moves = self.vert_moves(board)
        return self.moves


class Bishop(Piece):
    """
    Subclass of Piece Class, represents a bishop
    ...
    Attributes
    ----------
    name: str
        name of the piece
    value: int
        point value of the piece
    color: str
        color of the piece (white or black)
    moves: list
        list of legal moves for the piece
    """
    white_bishops = 0
    black_bishops = 0

    def __init__(self, color, pos):
        super().__init__(color, name='Bishop', pos=pos, value=3.25)
        self.moves = []

        if self.color == 'White':
            Bishop.white_bishops += 1
        else:
            Bishop.black_bishops += 1

    def valid_moves(self, board):
        self.moves = self.diag_moves(board)
        return self.moves


class Knight(Piece):
    """
    Subclass of Piece Class, represents a knight
    ...
    Attributes
    ----------
    name: str
        name of the piece
    value: int
        point value of the piece
    color: str
        color of the piece (white or black)
    moves: list
        list of legal moves for the piece
    """
    def __init__(self, color, pos):
        super().__init__(color, name='Knight', pos=pos, value=3)
        self.moves = []

    def valid_moves(self, board):
        """
        Returns a list of all possible knight moves

        board: the current board/piece locations
        posn: the position of a piece that we want to move (tuple)
        """
        x = self.pos[0]
        y = self.pos[1]

        # Directions: (a lot of complex movements)
        directions = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (2, 1), (2, -1), (1, -2), (1, 2)]

        move_list = []

        for direction in directions:
            # Increment in the possible directions
            end_x = x + direction[0]
            end_y = y + direction[1]
            # Check if move is on the board
            if 0 <= end_x < 8 and 0 <= end_y < 8:
                if board[end_x][end_y] == '--':
                    move_list.append((self.pos, (end_x, end_y)))
                elif board[end_x][end_y].color != self.color:
                    move_list.append((self.pos, (end_x, end_y)))

        self.moves = move_list
        return self.moves


class Pawn(Piece):
    """
    Subclass of Piece Class, represents a pawn
    ...
    Attributes
    ----------
    name: str
        name of the piece
    value: int
        point value of the piece
    color: str
        color of the piece (white or black)
    moves: list
        list of legal moves for the piece
    """
    def __init__(self, color, pos):
        super().__init__(color, name='Pawn', pos=pos, value=1)
        self.moves = []

    def valid_moves(self, board):
        x = self.pos[0]
        y = self.pos[1]

        move_list = []

        # Which colored pawn is moving?
        if self.color == 'White':
            # Make sure that the pawn knows whether it's moved already
            if self.pos[0] != 6:
                self.first_move = False
            takes = [(-1, -1), (-1, 1)]
            # Push moves
            if 0 <= x - 1 < 8 and 0 <= y < 8:
                if board[x-1][y] == '--':
                    move_list.append((self.pos, (x-1, y)))
                    # If it is the pawn's first move, add a new move to its possible move list
                    if self.first_move:
                        if board[x-2][y] == '--':
                            move_list.append((self.pos, (x-2, y)))
        else:
            if self.pos[0] != 1:
                self.first_move = False
            takes = [(1, -1), (1, 1)]
            if 0 <= x - 1 < 8 and 0 <= y < 8:
                if board[x+1][y] == '--':
                    move_list.append((self.pos, (x+1, y)))
                    if self.first_move:
                        if board[x+2][y] == '--':
                            move_list.append((self.pos, (x+2, y)))

        for direction in takes:
            end_x = x + direction[0]
            end_y = y + direction[1]
            if 0 <= end_x < 8 and 0 <= end_y < 8:
                if board[end_x][end_y] != '--':
                    if board[end_x][end_y].color != self.color:
                        move_list.append((self.pos, (end_x, end_y)))

        self.moves = move_list

        return self.moves