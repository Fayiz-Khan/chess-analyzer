import chess


PIECE_VALUES = {
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3,
    chess.ROOK: 5,
    chess.QUEEN: 9,
}


def extract_features_from_fen(fen: str) -> list[float]:
    board = chess.Board(fen)

    return [
        material_balance(board),
        int(board.turn == chess.WHITE),
        bishop_count(board, chess.WHITE),
        bishop_count(board, chess.BLACK),
        int(board.has_kingside_castling_rights(chess.WHITE)),
        int(board.has_queenside_castling_rights(chess.WHITE)),
        int(board.has_kingside_castling_rights(chess.BLACK)),
        int(board.has_queenside_castling_rights(chess.BLACK)),
        isolated_pawns(board, chess.WHITE),
        isolated_pawns(board, chess.BLACK),
        doubled_pawns(board, chess.WHITE),
        doubled_pawns(board, chess.BLACK),
        open_files(board),
        semi_open_files(board, chess.WHITE),
        semi_open_files(board, chess.BLACK),
    ]


def material_balance(board: chess.Board) -> float:
    white_score = 0
    black_score = 0

    for piece_type, value in PIECE_VALUES.items():
        white_score += len(board.pieces(piece_type, chess.WHITE)) * value
        black_score += len(board.pieces(piece_type, chess.BLACK)) * value

    return float(white_score - black_score)


def bishop_count(board: chess.Board, color: chess.Color) -> int:
    return len(board.pieces(chess.BISHOP, color))


def isolated_pawns(board: chess.Board, color: chess.Color) -> int:
    pawns = board.pieces(chess.PAWN, color)
    pawn_files = {chess.square_file(square) for square in pawns}

    count = 0

    for square in pawns:
        file = chess.square_file(square)
        if file - 1 not in pawn_files and file + 1 not in pawn_files:
            count += 1

    return count


def doubled_pawns(board: chess.Board, color: chess.Color) -> int:
    file_counts: dict[int, int] = {}

    for square in board.pieces(chess.PAWN, color):
        file = chess.square_file(square)
        file_counts[file] = file_counts.get(file, 0) + 1

    return sum(count - 1 for count in file_counts.values() if count > 1)


def open_files(board: chess.Board) -> int:
    count = 0

    for file in range(8):
        if not file_has_pawn(board, file, chess.WHITE) and not file_has_pawn(board, file, chess.BLACK):
            count += 1

    return count


def semi_open_files(board: chess.Board, color: chess.Color) -> int:
    opponent = not color
    count = 0

    for file in range(8):
        if not file_has_pawn(board, file, color) and file_has_pawn(board, file, opponent):
            count += 1

    return count


def file_has_pawn(board: chess.Board, file: int, color: chess.Color) -> bool:
    for square in board.pieces(chess.PAWN, color):
        if chess.square_file(square) == file:
            return True

    return False
