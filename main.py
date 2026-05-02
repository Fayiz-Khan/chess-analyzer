import chess
import chess.pgn

with open("game.pgn") as pgn: 
    game = chess.pgn.read_game(pgn)

print(game)

board = game.board()

for move in game.mainline_moves():
    standard_algebraic_move = board.san(move) # if we don't standardize the notation it will say 1. e2e4 instead of the standard 1. e4 as an example

    move_number = board.fullmove_number

    print("Move:", standard_algebraic_move, "\n")

    if board.turn == chess.WHITE:
        print(f"{move_number}. {standard_algebraic_move}")
    else:
        print(f"{move_number}... {standard_algebraic_move}")
    
    board.push(move)

    print(board)
    print("--------------------")
