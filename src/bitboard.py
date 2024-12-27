from turtledemo.chaos import jumpto

import numpy as np
class ChessEngine:
    FILE_A = 0x0101010101010101
    FILE_H = 0x8080808080808080
    RANK_1 = 0x00000000000000FF
    RANK_8 = 0xFF00000000000000

    def __init__(self):
        # Khởi tạo vị trí ban đầu
        self.BLACK_KING = None
        self.BLACK_BISHOPS = None
        self.BLACK_KNIGHTS = None
        self.BLACK_PAWNS = None
        self.WHITE_KING = None
        self.WHITE_QUEENS = None
        self.WHITE_ROOKS = None
        self.WHITE_BISHOPS = None
        self.WHITE_KNIGHTS = None
        self.WHITE_PAWNS = None
        self.BLACK_ROOKS = None
        self.BLACK_QUEENS = None
        self.reset_board()

        self.is_white_turn: bool = True #1: white, 0: Black
        self.en_passant = None

    def reset_board(self):
        # Thiết lập vị trí ban đầu cho tất cả quân cờ
        # Tốt trắng
        self.WHITE_PAWNS = 0xFF00
        # Mã trắng 
        self.WHITE_KNIGHTS = 0x42
        # Tượng trắng
        self.WHITE_BISHOPS = 0x24
        # Xe trắng
        self.WHITE_ROOKS = 0x81
        # Hậu trắng
        self.WHITE_QUEENS = 0x8
        # Vua trắng
        self.WHITE_KING = 0x10

        # Tốt đen
        self.BLACK_PAWNS = 0xFF000000000000
        # Mã đen
        self.BLACK_KNIGHTS = 0x4200000000000000
        # Tượng đen  
        self.BLACK_BISHOPS = 0x2400000000000000
        # Xe đen
        self.BLACK_ROOKS = 0x8100000000000000
        # Hậu đen
        self.BLACK_QUEENS = 0x800000000000000
        # Vua đen
        self.BLACK_KING = 0x1000000000000000

    @staticmethod
    def get_bit(bitboard: int, square: int) -> bool:
        """Lấy giá trị bit tại một ô cờ"""
        return (bitboard & (1 << square)) != 0

    @staticmethod 
    def set_bit(bitboard: int, square: int) -> int:
        """Đặt bit 1 tại một ô cờ"""
        return bitboard | (1 << square)

    @staticmethod
    def clear_bit(bitboard: int, square: int) -> int:
        """Xóa bit (đặt về 0) tại một ô cờ"""
        return bitboard & ~(1 << square)

    def get_white_pieces(self) -> int:
        return self.WHITE_PAWNS | self.WHITE_KNIGHTS | self.WHITE_BISHOPS | self.WHITE_ROOKS | self.WHITE_QUEENS | self.WHITE_KING
    def get_black_pieces(self) -> int:
        return self.BLACK_PAWNS | self.BLACK_KNIGHTS | self.BLACK_BISHOPS | self.BLACK_ROOKS | self.BLACK_QUEENS | self.BLACK_KING

    def get_all_pieces(self) -> int:
        return self.get_white_pieces() | self.get_black_pieces()

    def get_empty_squares(self) -> int:
        return ~self.get_all_pieces() & 0xFFFFFFFFFFFFFFFF

    def get_white_pawns(self) -> int:
        return self.WHITE_PAWNS

    def get_black_pawns(self) -> int:
        return self.BLACK_PAWNS

    def get_white_knights(self):
        return self.WHITE_KNIGHTS

    def get_black_knights(self):
        return self.BLACK_KNIGHTS

    def get_white_bishops(self):
        return self.WHITE_BISHOPS
    def get_black_bishops(self):
        return self.BLACK_BISHOPS
    def get_white_rooks(self):
        return self.WHITE_ROOKS
    def get_black_rooks(self):
        return self.BLACK_ROOKS
    def get_white_queens(self):
        return self.WHITE_QUEENS
    def get_black_queens(self):
        return self.BLACK_QUEENS
    def get_white_king(self):
        return self.WHITE_KING
    def get_black_king(self):
        return self.BLACK_KING
    def get_piece_at(self, square: int) -> str:
        """Lấy ký tự đại diện cho quân cờ tại một ô"""
        position = 1 << square

        if position & self.get_white_pawns(): return 'P'
        if position & self.get_black_pawns(): return 'p'
        if position & self.get_white_knights(): return 'N'
        if position & self.get_black_knights(): return 'n'
        if position & self.get_white_bishops(): return 'B'
        if position & self.get_black_bishops(): return 'b'
        if position & self.get_white_rooks(): return 'R'
        if position & self.get_black_rooks(): return 'r'
        if position & self.get_white_queens(): return 'Q'
        if position & self.get_black_queens(): return 'q'
        if position & self.get_white_king(): return 'K'
        if position & self.get_black_king(): return 'k'
        return '.'

    def print_position(self):
        """In ra trạng thái hiện tại của bàn cờ"""
        for rank in range(7, -1, -1):
            print(f"{rank + 1} |", end="")
            for file in range(8):
                square = rank * 8 + file
                piece = self.get_piece_at(square)
                print(f" {piece}", end="")
            print()
        print("  ----------------")
        print("    a b c d e f g h")

    '''
        POSITION
    '''

    def update_knight_position(self, is_white: bool, from_square: int, to_square: int):
        """Cập nhật vị trí quân mã trên bàn cờ."""
        if is_white:
            self.WHITE_KNIGHTS = self.clear_bit(self.WHITE_KNIGHTS, from_square)
            self.WHITE_KNIGHTS = self.set_bit(self.WHITE_KNIGHTS, to_square)
        else:
            self.BLACK_KNIGHTS = self.clear_bit(self.BLACK_KNIGHTS, from_square)
            self.BLACK_KNIGHTS = self.set_bit(self.BLACK_KNIGHTS, to_square)
            
    '''
        POSITION UPDATES
    '''
    def update_pawn_position(self, is_white: bool, from_square: int, to_square: int):
        """Cập nhật vị trí quân tốt."""
        if is_white:
            self.WHITE_PAWNS = self.clear_bit(self.WHITE_PAWNS, from_square)
            self.WHITE_PAWNS = self.clear_bit(self.WHITE_PAWNS, to_square)
            self.WHITE_PAWNS = self.set_bit(self.WHITE_PAWNS, to_square)
        else:
            self.BLACK_PAWNS = self.clear_bit(self.BLACK_PAWNS, from_square)
            self.BLACK_PAWNS = self.clear_bit(self.BLACK_PAWNS, to_square)
            self.BLACK_PAWNS = self.set_bit(self.BLACK_PAWNS, to_square)

    def update_bishop_position(self, is_white: bool, from_square: int, to_square: int):
        """Cập nhật vị trí quân tượng."""
        if is_white:
            self.WHITE_BISHOPS = self.clear_bit(self.WHITE_BISHOPS, from_square)
            self.WHITE_BISHOPS = self.set_bit(self.WHITE_BISHOPS, to_square)
        else:
            self.BLACK_BISHOPS = self.clear_bit(self.BLACK_BISHOPS, from_square)
            self.BLACK_BISHOPS = self.set_bit(self.BLACK_BISHOPS, to_square)

    def update_rook_position(self, is_white: bool, from_square: int, to_square: int):
        """Cập nhật vị trí quân xe."""
        if is_white:
            self.WHITE_ROOKS = self.clear_bit(self.WHITE_ROOKS, from_square)
            self.WHITE_ROOKS = self.set_bit(self.WHITE_ROOKS, to_square)
        else:
            self.BLACK_ROOKS = self.clear_bit(self.BLACK_ROOKS, from_square)
            self.BLACK_ROOKS = self.set_bit(self.BLACK_ROOKS, to_square)

    def update_queen_position(self, is_white: bool, from_square: int, to_square: int):
        """Cập nhật vị trí quân hậu."""
        if is_white:
            self.WHITE_QUEENS = self.clear_bit(self.WHITE_QUEENS, from_square)
            self.WHITE_QUEENS = self.set_bit(self.WHITE_QUEENS, to_square)
        else:
            self.BLACK_QUEENS = self.clear_bit(self.BLACK_QUEENS, from_square)
            self.BLACK_QUEENS = self.set_bit(self.BLACK_QUEENS, to_square)

    def update_king_position(self, is_white: bool, from_square: int, to_square: int):
        """Cập nhật vị trí quân vua."""
        if is_white:
            self.WHITE_KING = self.clear_bit(self.WHITE_KING, from_square)
            self.WHITE_KING = self.set_bit(self.WHITE_KING, to_square)
        else:
            self.BLACK_KING = self.clear_bit(self.BLACK_KING, from_square)
            self.BLACK_KING = self.set_bit(self.BLACK_KING, to_square)

    '''
        MOVE
    '''

    def move_knights(self, is_white: bool, from_square: int, to_square: int) -> bool:
        """
        Di chuyển quân mã từ `from_square` đến `to_square` nếu hợp lệ.
        :param is_white: True nếu là quân trắng, False nếu là quân đen.
        :param from_square: Vị trí bắt đầu (0-63).
        :param to_square: Vị trí kết thúc (0-63).
        :return: True nếu di chuyển hợp lệ, False nếu không hợp lệ.
        """
        # Lấy danh sách các nước đi hợp lệ cho quân mã
        valid_moves = self.get_knight_moves(is_white, from_square)

        # Nếu không có nước đi hợp lệ
        if not valid_moves:
            return False

        # Kiểm tra nếu nước đi đến `to_square` là hợp lệ
        if to_square not in valid_moves:
            return False

        # Di chuyển quân mã nếu nước đi hợp lệ
        if 0 <= to_square < 64:
            self.update_knight_position(is_white, from_square, to_square)
            return True

        return False

    def move_pawns(self, is_white: bool, from_square: int, to_square: int) -> bool:
        """Di chuyển tốt."""
        pawns = self.get_white_pawns() if is_white else self.get_black_pawns()
        owns_pieces = self.get_white_pieces() if is_white else self.get_black_pieces()
        opponent_pieces = self.get_black_pieces() if is_white else self.get_white_pieces()

        # Kiểm tra có tốt ở ô xuất phát không
        if not self.get_bit(pawns, from_square):
            return False

        # Hướng di chuyển (lên hay xuống)
        direction = 8 if is_white else -8
        
        # Di chuyển 1 ô thẳng
        if to_square == from_square + direction:
            if not self.get_bit(self.get_all_pieces(), to_square):
                return True

        # Di chuyển 2 ô (chỉ ở nước đầu)
        start_rank = 1 if is_white else 6
        if from_square // 8 == start_rank:
            if to_square == from_square + 2 * direction:
                if not self.get_bit(self.get_all_pieces(), to_square):
                    if not self.get_bit(self.get_all_pieces(), from_square + direction):
                        return True

        # Ăn chéo
        captures = [-7, -9] if is_white else [7, 9]
        for capture in captures:
            if to_square == from_square + capture:
                if self.get_bit(opponent_pieces, to_square):
                    return True

        return False

    def move_bishops(self, is_white: bool, from_square: int, to_square: int) -> bool:
        """Di chuyển tượng."""
        bishops = self.get_white_bishops() if is_white else self.get_black_bishops()
        owns_pieces = self.get_white_pieces() if is_white else self.get_black_pieces()

        # Kiểm tra có tượng ở ô xuất phát không
        if not self.get_bit(bishops, from_square):
            return False

        # Kiểm tra đường chéo
        diff = to_square - from_square
        if abs(diff % 7) == 0 or abs(diff % 9) == 0:  # Đường chéo
            # TODO: Kiểm tra không có quân cản đường
            if not self.get_bit(owns_pieces, to_square):
                return True

        return False

    def move_rooks(self, is_white: bool, from_square: int, to_square: int) -> bool:
        """Di chuyển xe."""
        rooks = self.get_white_rooks() if is_white else self.get_black_rooks()
        owns_pieces = self.get_white_pieces() if is_white else self.get_black_pieces()

        # Kiểm tra có xe ở ô xuất phát không
        if not self.get_bit(rooks, from_square):
            return False

        # Kiểm tra ngang dọc
        from_rank = from_square // 8
        from_file = from_square % 8
        to_rank = to_square // 8
        to_file = to_square % 8

        if from_rank == to_rank or from_file == to_file:  # Ngang hoặc dọc
            # TODO: Kiểm tra không có quân cản ��ường
            if not self.get_bit(owns_pieces, to_square):
                return True

        return False

    def move_queens(self, is_white: bool, from_square: int, to_square: int) -> bool:
        """Di chuyển hậu (kết hợp xe và tượng)."""
        # Hậu di chuyển được như cả xe và tượng
        return (self.move_rooks(is_white, from_square, to_square) or 
                self.move_bishops(is_white, from_square, to_square))

    def move_king(self, is_white: bool, from_square: int, to_square: int) -> bool:
        """Di chuyển vua."""
        king = self.get_white_king() if is_white else self.get_black_king()
        owns_pieces = self.get_white_pieces() if is_white else self.get_black_pieces()

        # Kiểm tra có vua ở ô xuất phát không
        if not self.get_bit(king, from_square):
            return False

        # Vua đi được 1 ô theo mọi hướng
        diff = abs(to_square - from_square)
        valid_moves = [1, 7, 8, 9]  # Các bước đi hợp lệ của vua
        if diff in valid_moves:
            if not self.get_bit(owns_pieces, to_square):
                # TODO: Kiểm tra ô đích không bị chiếu
                return True

        return False

    '''
        DISPLAY MOVE
    '''

    def get_knight_moves(self, is_white: bool, from_square: int) -> list:
        """Lấy danh sách các nước đi khả dụng cho quân mã."""
        valid_moves = []

        knight_moves = [6, 15, 17, 10, -6, -15, -17, -10]  # Hướng di chuyển của mã
        owns_pieces = self.get_white_pieces() if is_white else self.get_black_pieces()

        knights = self.get_white_knights() if is_white else self.get_black_knights()

        # Có mã của mình ở đó không
        if not self.get_bit(knights, from_square):
            return valid_moves

        # Tính chỉ số hàng và cột từ vị trí hiện tại
        from_rank = from_square // 8
        from_file = from_square % 8

        # Logic
        for move in knight_moves:
            to_square = from_square + move

            # Kiểm tra biên cột (cột a = 0, cột h = 7)
            to_rank = to_square // 8
            to_file = to_square % 8

            # Nếu nước đi ra ngoài bàn cờ, bỏ qua
            if not (0 <= to_rank < 8 and 0 <= to_file < 8):
                continue

            # Nếu nước đi không trúng quân của mình
            if not self.get_bit(owns_pieces, to_square):
                # Đảm bảo quân mã không nhảy qua các cột không hợp lệ
                if abs(from_file - to_file) > 2:  # Quân mã chỉ có thể di chuyển tối đa 2 cột
                    continue
                valid_moves.append(to_square)

        return valid_moves

    def get_pawn_moves(self, is_white: bool, from_square: int) -> list:
        """
           Di chuyển quân Tốt từ `from_square` đến `to_square` nếu hợp lệ.
           :param is_white: True nếu là quân trắng, False nếu là quân đen.
           :param from_square: Vị trí bắt đầu (0-63).
           :return: Danh sách các nước đi hợp lệ.
        """
        valid_moves = []
        pawns = self.get_white_pawns() if is_white else self.get_black_pawns()
        owns_pieces = self.get_white_pieces() if is_white else self.get_black_pieces()
        opponent_pieces = self.get_black_pieces() if is_white else self.get_white_pieces()

        if not self.get_bit(pawns, from_square):
            return valid_moves

        direction = 8 if is_white else -8

        # Di chuyển 1 ô về phía trước
        square_ahead = from_square + direction
        if 0 <= square_ahead < 64 and not (
                self.get_bit(owns_pieces, square_ahead) or self.get_bit(opponent_pieces, square_ahead)):
            valid_moves.append(square_ahead)

            # Di chuyển 2 ô nếu chưa di chuyển
            double_jump = from_square + 2 * direction
            if 0 <= double_jump < 64 and not (
                    self.get_bit(owns_pieces, double_jump) or self.get_bit(opponent_pieces, double_jump)):
                start_rank = 1 if is_white else 6
                if from_square // 8 == start_rank:
                    self.en_passant = double_jump  # Lưu vị trí En Passant có thể thực hiện
                    valid_moves.append(double_jump)

        # Diagonal captures (tấn công chéo)
        captures = [7, 9] if is_white else [-7, -9]
        from_file = from_square % 8  # Cột của quân Tốt
        for capture in captures:
            capture_square = from_square + capture
            to_file = capture_square % 8  # Cột của ô mà quân Tốt có thể bắt
            if self.get_bit(opponent_pieces, capture_square) and 0 <= capture_square < 64 and abs(
                    from_file - to_file) == 1:
                valid_moves.append(capture_square)

        # En Passant
        if self.en_passant is not None:
            if self.en_passant == from_square + 1 or self.en_passant == from_square - 1:
                ep_capture = self.en_passant - 8 if is_white else self.en_passant + 8
                if 0 <= ep_capture < 64:
                    valid_moves.append(ep_capture)  # Thêm nước đi En Passant
                    self.en_passant = None  # Xóa En Passant sau khi thực hiện

        return valid_moves


def display_knight_moves(board: ChessEngine, is_white: bool, from_square: int):
    """Hiển thị các nước đi khả dụng cho quân mã."""
    moves = board.get_knight_moves(is_white, from_square)
    print(f"Các nước đi khả dụng cho {'trắng' if is_white else 'đen'} tại ô {from_square}:")
    for move in moves:
        print(f"Ô {move} (Tọa độ: {chr(move % 8 + ord('a'))}{move // 8 + 1})")
def display_pawn_moves(board: ChessEngine, is_white: bool, from_square: int):
    """Hiển thị các nước đi khả dụng cho quân mã."""
    moves = board.get_pawn_moves(is_white, from_square)
    print(f"Các nước đi khả dụng cho {'trắng' if is_white else 'đen'} tại ô {from_square}:")
    for move in moves:
        print(f"Ô {move} (Tọa độ: {chr(move % 8 + ord('a'))}{move // 8 + 1})")

if __name__ == "__main__":
    board = ChessEngine()
    print(board.move_knights(True, 6, 21))
    print(board.move_knights(True, 21, 36))
    print(board.move_knights(True, 36, 51))
    # print(board.move_knights(False, 57, 47))
    print(board.print_position())
    
    # Hiển thị các nước đi khả dụng cho quân mã tại ô 1
    display_knight_moves(board, True, 36)  # Thay đổi True thành False để kiểm tra cho quân mã đen
    # display_pawn_moves(board, False, 49)  # Thay đổi True thành False để kiểm tra cho quân mã đen