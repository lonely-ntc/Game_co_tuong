import numpy as np
import copy
import math

class CoTuong:
    def __init__(self):
        self.board = np.array([
            ['r', 'n', 'b', 'a', 'k', 'a', 'b', 'n', 'r'],
            ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', 'c', '.', '.', '.', '.', '.', 'c', '.'],
            ['p', '.', 'p', '.', 'p', '.', 'p', '.', 'p'],
            ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
            ['P', '.', 'P', '.', 'P', '.', 'P', '.', 'P'],
            ['.', 'C', '.', '.', '.', '.', '.', 'C', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
            ['R', 'N', 'B', 'A', 'K', 'A', 'B', 'N', 'R']
        ])
        self.turn = 'r'  # Người chơi đánh quân đỏ

    def print_board(self):
        """ Hiển thị bàn cờ với số hàng và cột """
        print("\n   " + " ".join(str(i) for i in range(9)))
        print("  +" + "---+" * 9)
        for i, row in enumerate(self.board):
            print(f"{i} | " + " | ".join(row) + " |")
            print("  +" + "---+" * 9)
        print("\n")

    def get_valid_moves(self, color):
        """ Lấy danh sách nước đi hợp lệ cho quân cùng màu """
        moves = []
        for i in range(10):
            for j in range(9):
                piece = self.board[i][j]
                if (color == 'r' and piece.isupper()) or (color == 'b' and piece.islower()):
                    moves.extend(self.get_piece_moves(i, j))
        return moves

    def get_piece_moves(self, x, y):
        """ Lấy danh sách nước đi hợp lệ của quân cờ tại (x, y) """
        moves = []
        piece = self.board[x][y]
        directions = {
            'P': [(1, 0), (0, 1), (0, -1)],  # Tốt đỏ đi xuống
            'p': [(-1, 0), (0, 1), (0, -1)],  # Tốt đen đi lên
            'R': [(1, 0), (-1, 0), (0, 1), (0, -1)],  # Xe
            'r': [(1, 0), (-1, 0), (0, 1), (0, -1)],  # Xe
        }
        if piece.upper() in directions:
            for dx, dy in directions[piece.upper()]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < 10 and 0 <= ny < 9:
                    if self.board[nx][ny] == '.' or self.board[nx][ny].islower() != piece.islower():
                        moves.append(((x, y), (nx, ny)))

        if piece.upper() == 'N':
            moves.extend(self.get_knight_moves(x, y))
        return moves

    def get_knight_moves(self, x, y):
        """ Lấy danh sách nước đi hợp lệ của quân Mã """
        moves = []
        piece = self.board[x][y]
        knight_moves = [
            (-2, -1), (-2, 1), (2, -1), (2, 1),
            (-1, -2), (-1, 2), (1, -2), (1, 2)
        ]
        for dx, dy in knight_moves:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 10 and 0 <= ny < 9:
                if abs(dx) == 2:
                    if self.board[x + dx // 2][y] != '.':
                        continue
                else:
                    if self.board[x][y + dy // 2] != '.':
                        continue
                if self.board[nx][ny] == '.' or self.board[nx][ny].islower() != piece.islower():
                    moves.append(((x, y), (nx, ny)))
        return moves

    def make_move(self, move):
        """ Di chuyển quân cờ """
        (x1, y1), (x2, y2) = move
        new_game = copy.deepcopy(self)
        new_game.board[x2][y2] = new_game.board[x1][y1]
        new_game.board[x1][y1] = '.'
        new_game.turn = 'b' if self.turn == 'r' else 'r'
        return new_game

    def evaluate(self):
        """ Đánh giá bàn cờ """
        piece_values = {'P': 10, 'p': -10, 'R': 50, 'r': -50, 'N': 30, 'n': -30, 'K': 1000, 'k': -1000}
        score = 0
        for i in range(10):
            for j in range(9):
                cell = self.board[i][j]
                if cell in piece_values:
                    score += piece_values[cell]
        return score

def minimax(game, depth, alpha, beta, maximizing):
    if depth == 0:
        return game.evaluate(), None

    best_move = None
    moves = game.get_valid_moves(game.turn)

    if maximizing:
        max_eval = -math.inf
        for move in moves:
            new_game = game.make_move(move)
            eval, _ = minimax(new_game, depth - 1, alpha, beta, False)
            if eval > max_eval:
                max_eval = eval
                best_move = move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = math.inf
        for move in moves:
            new_game = game.make_move(move)
            eval, _ = minimax(new_game, depth - 1, alpha, beta, True)
            if eval < min_eval:
                min_eval = eval
                best_move = move
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval, best_move

def ai_move(game):
    """ AI tìm nước đi tốt nhất (đánh quân đen) """
    depth = 3
    _, best_move = minimax(game, depth, -math.inf, math.inf, False)  # AI đánh quân đen (minimizing)
    if best_move:
        game = game.make_move(best_move)
    return game

def play():
    """ Người chơi đấu với AI """
    game = CoTuong()

    while True:
        game.print_board()

        if game.turn == 'r':
            move_input = input("Nhập nước đi : ").strip()
            x1, y1, x2, y2 = map(int, move_input.split())
            game = game.make_move(((x1, y1), (x2, y2)))
        else:
            game = ai_move(game)

if __name__ == "__main__":
    play()
