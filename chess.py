from pieces import Queen
from chessboard import chessboard
from collections import defaultdict
from engine import Engine
import copy
import random as rnd


class Chess:

    def __init__(self, depth: int = 2):
        """ Chess class that enables one to play a game of chess against their computer
        Attributes:
            chess_board (obj): chess baord from chessboard class, instantiated with regular starting position
            Engine (obj): chess engine from engine class
            depth (int): depth at which the engine plays at (num of moves it looks ahead by)
            turn (str): which color's turn it is (white or black)
            previous_piece_moved (obj): object representation of last piece that moved
            move_log (list): list of game moves
            valid_moves (list): valid moves for the current position
            checkmate (bool): whether either side has been checkmated
            stalemate (bool): whether either side has been stalemated
            draw (bool): whether game is a draw
        """
        self.black_pawn_locs = None
        self.white_pawn_locs = None
        self.chess_board = chessboard()
        self.turn = 'White'
        self.player_color = 'White'
        self.engine_color = 'Black'
        self.depth = depth
        self.previous_piece_moved = ''
        self.move_log = []
        self.valid_moves = []
        self.move_evaluations = {}
        self.checkmate = False
        self.stalemate = False
        self.draw = False

    # %% Helpful Chess Static Methods

    @staticmethod
    def coordinate(piece_location):
        """ Turn chess notation to 2d list indices (i.e. d4 --> (4, 3)) """
        column = piece_location[0]
        column = ord(column.upper()) - 65
        row = piece_location[1]
        row = 8 - int(row)
        return row, column

    @staticmethod
    def uncoordinate(piece_notation):
        """ Turn 2D list notation into chess notation (i.e. (4, 3) --> d4) """
        row = piece_notation[0]
        column = piece_notation[1]
        piece_column = chr(column + 65).lower()
        piece_row = 8 - row
        return piece_column + str(piece_row)

    @staticmethod
    def in_check(board, moves, turn):
        """ Check if king can be taken by any of the pieces on the board
        :param board: board position
        :param moves: list of possible moves
        :param turn: whose turn it is
        :return: boolean
        """
        # Go through all ending locations, if king_loc is in there,
        # return True (results in check)
        possible_takes = [x for move in moves.values() for x in move]
        king_loc = Chess.locate_piece(board, turn, 'King')
        if king_loc in possible_takes:
            return True
        return False

    @staticmethod
    def locate_piece(board, color, piece):
        """ Locate piece given board position, piece color, and piece name """
        for row in board:
            for square in row:
                if square != '--':
                    if square.name == piece and square.color == color:
                        return square.pos

    # %% Methods Inherent to a Chess Game

    def change_turn(self):
        """ Change turn: White --> Black, Black --> White"""
        if self.turn == 'White':
            self.turn = 'Black'
        else:
            self.turn = 'White'

    def check_mates(self):
        """ Check if player or engine has been checkmated or stalemated """
        moves = self.get_valid_moves()
        # Check player's current moves, if they don't have any...
        if not moves:
            self.change_turn()
            opp_moves = self.get_valid_moves()
            self.change_turn()

            # and they're in check, opponent has gotten checkmated
            if Chess.in_check(self.chess_board.board, opp_moves, self.turn):
                self.checkmate = True
            # if not, it's a stalemate
            else:
                self.stalemate = True

    def draw_by_rep(self):
        """ Check for draw by three-move repetition (player and engine repeat the same moves 3 times in a row) """
        if len(self.move_log) > 6:
            if self.move_log[-6] == self.move_log[-4] == self.move_log[-2] and \
                    self.move_log[-5] == self.move_log[-3] == self.move_log[1]:
                self.draw = True

    def check_gameover(self):
        """ Check if the game is over """
        self.check_mates()
        self.draw_by_rep()

    def promotion(self):
        """ Check for any promotions, automatically turn Pawns into Queens """
        self.chess_board.board[0] = [Queen('White', (0, i)) if piece != '--' and piece.name == 'Pawn' else piece
                                     for i, piece in enumerate(self.chess_board.board[0])]
        self.chess_board.board[7] = [Queen('Black', (7, i)) if piece != '--' and piece.name == 'Pawn' else piece
                                     for i, piece in enumerate(self.chess_board.board[7])]

    # %% Move Methods
    def try_move(self, start, end):
        """ Try a move on copy of the board
        :param start: piece's starting location
        :param end: piece's ending location
        :return: return new board position, player's control after the move,
                 and the opponent's possible responses to the move
        """
        # Create deep bopy of board position
        new_board = copy.deepcopy(self)

        # Try moving the piece from starting loc to ending loc, update piece loc
        piece = new_board.chess_board.board[start[0]][start[1]]
        new_board.chess_board.board[end[0]][end[1]] = piece
        new_board.chess_board.board[start[0]][start[1]] = "--"
        piece.pos = (end[0], end[1])
        piece.first_move = False
        player_control = new_board.get_possible_moves()

        # Get and return opponent's possible responses
        new_board.change_turn()
        opponent_responses = new_board.get_possible_moves()

        return new_board, player_control, opponent_responses

    def make_move(self, start_row, start_col, end_row, end_col):
        """ Make a move on the board given starting pos and ending pos """
        # Find the piece at the starting location
        piece = self.chess_board.board[start_row][start_col]

        # Override location with new piece, and place a blank where it left
        self.chess_board.board[end_row][end_col] = piece
        self.chess_board.board[start_row][start_col] = "--"

        # Update piece's position and first_move attribute
        piece.pos = (end_row, end_col)
        piece.first_move = False

        # Make final adjustments after the move
        self.previous_piece_moved = piece
        self.promotion()
        self.change_turn()
        self.check_gameover()

    def get_possible_moves(self):
        """ Get a list of all the possible moves that can be played """
        all_possible_moves = {}
        # Iterate through chessboard to find all the pieces
        for i in range(8):
            for j in range(8):
                if self.chess_board.board[i][j] != '--' and self.chess_board.board[i][j].color == self.turn:
                    piece = self.chess_board.board[i][j]
                    # Use each piece's valid_moves method to return their possible moves
                    piece_moves = self.chess_board.board[i][j].valid_moves(self.chess_board.board)
                    # Add piece's starting loc as key and their ending loc as value to possible moves
                    all_possible_moves[piece.pos] = []
                    for move in piece_moves:
                        all_possible_moves[piece.pos].append(move[1])

        possible_moves = {k: v for k, v in all_possible_moves.items() if len(v) > 0}

        return possible_moves

    def get_valid_moves(self):
        """ Return only valid moves that can be played, (no moves that endanger the king) """
        # Get list of all possible moves
        all_moves = self.get_possible_moves()

        valid_moves = defaultdict(list)
        # Ensure that any of our possible moves do not result in check, filter those that do out
        for start, possible_moves in all_moves.items():
            for move in possible_moves:
                board_copy, control, opp_moves = self.try_move(start, move)
                # Retrieve current player's king location
                if not Chess.in_check(board_copy.chess_board.board, opp_moves, self.turn):
                    valid_moves[start].append(move)

        # Get rid of default dict tag
        self.valid_moves = {k: v for k, v in valid_moves.items()}
        return self.valid_moves

    # %% Methods to Determine Best Move
    @staticmethod
    def control(engine_moves, player_moves):
        """ Positional evaluation of board control """
        return sum([len(control) for control in list(engine_moves.values())]) - \
               sum([len(control) for control in list(player_moves.values())])

    @staticmethod
    def center_control(engine_moves, player_moves):
        """ Positional evaluation of center control """
        center = [(3, 2), (3, 3), (3, 4), (3, 5), (4, 2), (4, 3), (4, 4), (4, 5)]
        return len([square for moves in list(engine_moves.values()) for square in moves if square in center]) - \
               len([square for moves in list(player_moves.values()) for square in moves if square in center])

    def game_phase(self):
        """ Extremely oversimplified way of determining the phase of the game """
        if self.chess_board.minor_pieces + self.chess_board.major_pieces > 11:
            return 'opening'
        elif self.chess_board.minor_pieces + self.chess_board.major_pieces > 5:
            return 'middle'
        else:
            return 'end'

    def material_eval(self):
        """ Return the pure piece evaluation of board """
        return self.chess_board.material_eval

    def get_pawn_locs(self):
        white_pawns = []
        black_pawns = []
        for i in range(0, 8):
            for j in range(0, 8):
                piece = self.chess_board.board[i][j]
                if piece != '--':
                    if piece.name == 'Pawn' and piece.color == 'White':
                        white_pawns.append(piece.pos)
                    elif piece.name == 'Pawn' and piece.color == 'Black':
                        black_pawns.append(piece.pos)

        self.white_pawn_locs = white_pawns
        self.black_pawn_locs = black_pawns

    def passed_pawns(self):
        """ Count the number of passed pawns """
        black_passers = 0
        white_passers = 0

        if len(self.white_pawn_locs) > 0:
            for row, file in self.white_pawn_locs:
                black_in_front = []
                for i in range(0, row):
                    if file - 1 >= 0:
                        left_piece = self.chess_board.board[i][file - 1]
                        if left_piece != '--':
                            black_in_front.append((left_piece.color, left_piece.name))
                    if file + 1 <= 7:
                        right_piece = self.chess_board.board[i][file + 1]
                        if right_piece != '--':
                            black_in_front.append((right_piece.color, right_piece.name))
                    front_piece = self.chess_board.board[i][file]
                    if front_piece != '--':
                        black_in_front.append((front_piece.color, front_piece.name))
                if ('Black', 'Pawn') not in black_in_front:
                    white_passers += 1
        if len(self.black_pawn_locs) > 0:
            for row, file in self.black_pawn_locs:
                white_in_front = []
                for i in range(row + 1, 8):
                    if file - 1 >= 0:
                        left_piece = self.chess_board.board[i][file - 1]
                        if left_piece != '--':
                            white_in_front.append((left_piece.color, left_piece.name))
                    if file + 1 <= 7:
                        right_piece = self.chess_board.board[i][file + 1]
                        if right_piece != '--':
                            white_in_front.append((right_piece.color, right_piece.name))
                    front_piece = self.chess_board.board[i][file]
                    if front_piece != '--':
                        white_in_front.append((front_piece.color, front_piece.name))
                if ('White', 'Pawn') not in white_in_front:
                    black_passers += 1

        if self.engine_color == 'White':
            return white_passers - black_passers
        else:
            return black_passers - white_passers

    def doubled_pawns(self):
        """ Count number of doubled pawns on the board """
        doubled_black = 0
        doubled_white = 0

        if len(self.white_pawn_locs) > 0:
            for row, file in self.white_pawn_locs:
                pieces_in_front = []
                for i in range(0, 8):
                    if i != row:
                        piece = self.chess_board.board[i][file]
                        if piece != '--':
                            pieces_in_front.append((piece.color, piece.name))

                if ('White', 'Pawn') not in pieces_in_front:
                    doubled_white += 1

        if len(self.black_pawn_locs) > 0:
            for row, file in self.black_pawn_locs:
                pieces_in_front = []
                for i in range(0, 8):
                    if i != row:
                        piece = self.chess_board.board[i][file]
                        if piece != '--':
                            pieces_in_front.append((piece.color, piece.name))

                if ('Black', 'Pawn') not in pieces_in_front:
                    doubled_black += 1

        if self.engine_color == 'White':
            return doubled_black - doubled_white
        else:
            return doubled_white - doubled_black

    def open_files(self):
        """ Return evaluation of open files on the board """
        pass

    def opening(self, engine_moves, player_moves):
        """ If in the opening phase, engine will value center control more """
        return self.material_eval() + Chess.center_control(engine_moves, player_moves) * .15 \
               + Chess.control(engine_moves, player_moves) * .1

    def middle_game(self, engine_moves, player_moves):
        """ If in the middle game, engine will value positional principals more """
        return self.material_eval() + Chess.control(engine_moves, player_moves) * .2 + self.doubled_pawns() * .1

    def end_game(self, engine_moves, player_moves):
        """ If in the end game, engine will value king activity and passed pawns more """
        return self.material_eval() * 1.2 + Chess.control(engine_moves, player_moves) * .1 + self.passed_pawns() * .25

    def get_eval(self, phase, engine_moves, player_moves):
        """ Get evaluation of board based on game state/game phase """
        self.check_gameover()
        if self.checkmate and self.turn == 'Black' and self.engine_color == 'White':
            return 100
        elif self.checkmate and self.turn == 'Black' and self.engine_color == 'Black':
            return -100
        elif self.checkmate and self.turn == 'White' and self.engine_color == 'Black':
            return 100
        elif self.checkmate and self.turn == 'White' and self.engine_color == 'White':
            return -100

        if phase == 'opening':
            return self.opening(engine_moves, player_moves)
        elif phase == 'middle':
            return self.middle_game(engine_moves, player_moves)
        else:
            return self.end_game(engine_moves, player_moves)

    # %% Engine Movement Methods
    def remove_dominated(self):
        pass

    def calculate_moves(self, moves, depth, worst_move = None):
        """ Do deep analysis of possible moves. Return evaluations of each move. """
        # Make our engine choose a move to play
        for start, move_list in moves.items():
            for move in move_list:
                new_board, engine_control, player_moves = self.try_move(start, move)
                self.get_pawn_locs()
                phase = self.game_phase()
                move_evaluation = self.get_eval(phase, engine_control, player_moves)
                if not worst_move:
                    worst_move = move_evaluation
                if move_evaluation <= worst_move:
                    continue
                else:
                    if depth == 0:
                        return move_evaluation
                    else:
                        self.move_evaluations[(start, move)] = new_board.calculate_moves(player_moves, depth - 1, worst_move)

    def evaluate_moves(self):
        """ Out of the new dictionary created, find which move produces the best results """
        self.calculate_moves(self.get_valid_moves(), copy.copy(self.depth))
        print(self.move_evaluations)
        return self.move_evaluations

    def make_engine_move(self):
        """ Get the move with the best eval, play it on the board """
        if self.engine_color == 'White':
            if len(self.move_log) == 0:
                return rnd.choice([((6, 2), (4, 2)), ((6, 3), (4, 3)), ((6, 4), (4, 4))])
        else:
            if len(self.move_log) == 1:
                return rnd.choice([((1, 2), (3, 2)), ((1, 3), (3, 3)), ((1, 4), (3, 4))])

        best_move = self.evaluate_moves()
        piece_start = best_move[0]
        piece_end = best_move[1]

        # Make the move, add move to move log
        self.make_move(piece_start[0], piece_start[1], piece_end[0], piece_end[1])
        self.move_log.append((Chess.uncoordinate(piece_start), Chess.uncoordinate(piece_end)))
