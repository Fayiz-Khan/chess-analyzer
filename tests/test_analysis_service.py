import io

import chess.pgn

from analyzer.analysis_service import normalize_pgn_text


def test_normalize_pgn_text_allows_extra_blank_lines_after_headers():
    pgn = """[Event "Curious George Open"]
[Site "Lichess"]
[Date "2026.05.02"]
[Round "1"]
[White "MoonSabellano"]
[Black "Fayizchess87"]
[Result "1-0"]


1. e4 g6 2. Nf3 Bg7 3. d4 d6 4. c4 Nc6 5. Nc3 Bd7 6. d5 Nb8 7. Be2 h6 8. O-O e5
9. dxe6 fxe6 10. Be3 Ne7 11. Qd2 g5 12. Rfd1 e5 13. Nd5 Ng6 14. g3 O-O 15. Kg2
Nc6 16. Ng1 Qc8 17. Kh1 Nd8 18. Bxg5 hxg5 19. Qxg5 Be8 20. Bh5 Nh8 21. Ne7+ Kh7
22. Nxc8 Rxc8 23. Bxe8 Rxe8 24. Qh5+ 1-0"""

    game = chess.pgn.read_game(io.StringIO(normalize_pgn_text(pgn)))

    assert game is not None
    assert len(list(game.mainline_moves())) == 47
    assert game.headers["Result"] == "1-0"
