from chess import Chess


def player_move(chessgame):
    """ Simulate user's move, ask for inputs, make a move if inputs are valid """
    chessgame.get_valid_moves()
    # Prompt the user to enter a location of the board
    piece_select = input(f"{chessgame.turn} to move \nEnter what piece you would like to move:")
    if len(piece_select) != 2 or not piece_select[0].isalpha() or \
            piece_select[0] > 'h' or int(piece_select[1]) > 8:
        print("---Canceled Move---\n---Select New Piece---")
        # Prompt the user to enter new location
        player_move(chessgame)
    else:
        # Find the piece and its coordinate
        row, column = Chess.coordinate(piece_select)
        piece = chessgame.chess_board.board[row][column]
        # Make player redo input if piece cannot move
        if (row, column) not in list(chessgame.valid_moves.keys()):
            print(f"---Move is Invalid, {piece} cannot move. Select Valid Piece---")
            player_move(chessgame)
        else:
            # Identify new location
            move_select = input(f"Enter where you would like to move {piece} to:")
            if len(move_select) != 2:
                print(f"---Move is Invalid, please try again---")
                player_move(chessgame)
            else:
                row1, column1 = Chess.coordinate(move_select)
                # Make player redo input if piece cannot move to specified space
                if (row1, column1) not in chessgame.valid_moves[(row, column)]:
                    print(f"---Move is Invalid, {piece} cannot move to {move_select}. "
                          f"Select Valid Position---")
                    player_move(chessgame)
                else:
                    # Make the move, add move to move log, set new previous moved piece
                    chessgame.make_move(row, column, row1, column1)
                    chessgame.move_log.append((piece_select, move_select))
                    chessgame.previous_piece_moved = piece


def check_game_over(chess_game):
    """ Check if chess game object is over, i.e. draw by repetition, stalemate, or checkmate

    :param chess_game: chess game object
    :return: Boolean
    """
    if chess_game.checkmate:
        chess_game.change_turn()
        chess_game.chess_board.print_board()
        print(chess_game.turn, 'wins by checkmate!')
        return True
    elif chess_game.stalemate:
        chess_game.chess_board.print_board()
        print('Draw by stalemate')
        return True
    elif chess_game.draw:
        print('Draw by 3-move Repetition')
        return True

    return False


def chess_inputs():
    player_color = input('Which color would you like to play?\n').lower()
    while player_color != 'white' and player_color != 'black':
        player_color = input('Which color would you like to play?\n').lower()

    engine_strength = input('What depth would you like to play against?\n')

    try:
        engine_strength = int(engine_strength)

    except:
        print('Engine depth must be an integer between 1 and 5')
        chess_inputs()

    return player_color, engine_strength


def main():
    chessgame = Chess()

    player_color, depth = chess_inputs()

    chessgame.chess_board.print_board()

    if player_color == 'white':
        chessgame.engine_color = 'Black'
        chessgame.player_color = 'White'
        chessgame.depth = depth
        while True:
            player_move(chessgame)
            if check_game_over(chessgame):
                break
            chessgame.chess_board.print_board()
            chessgame.make_engine_move()
            if check_game_over(chessgame):
                break
            chessgame.chess_board.print_board()
    else:
        chessgame.engine_color = 'White'
        chessgame.player_color = 'Black'
        chessgame.depth = depth
        while True:
            chessgame.make_engine_move()
            if check_game_over(chessgame):
                break
            chessgame.chess_board.print_board()
            player_move(chessgame)
            if check_game_over(chessgame):
                break
            chessgame.chess_board.print_board()


if __name__ == '__main__':
    main()
