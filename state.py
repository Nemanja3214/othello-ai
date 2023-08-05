import copy
import math


class State(object):
    __slots__ = "_board"

    def __init__(self):
        self._board = []
        for i in range(8):
            self._board.append(8*[None])

        self._board[3][4] = "⚪"
        self._board[3][3] = "⚫"
        self._board[4][3] = "⚪"
        self._board[4][4] = "⚫"

    @property
    def board(self):
        return self._board

    def get_value(self, i, j):
        return self._board[i][j]

    def set_value(self, i, j, my_piece, opp_piece):
        valid = self.is_move_valid(i, j, my_piece, opp_piece)
        if valid:
            self._board[i][j] = my_piece
            self._flip(i, j, my_piece, opp_piece)

    def _flip(self, i, j, my_piece, opp_piece):
        original_i = i
        original_j = j
        for direction_i in range(-1, 2):
            for direction_j in range(-1, 2):
                if direction_j == 0 and direction_i == 0:  # nema pomeranja, beskonacna petlja
                    continue
                i = original_i
                j = original_j
                if 0 <= i <= 7 and 0 <= j <= 7 and\
                        self._move_and_check(i, j, direction_i, direction_j, my_piece, opp_piece):
                    self._move_and_flip(i, j, direction_i, direction_j, my_piece, opp_piece)

    def is_move_valid(self, i, j, my_piece, opp_piece):
        if self._board[i][j] is not None:
            return False

        for direction_i in range(-1, 2):
            for direction_j in range(-1, 2):
                if direction_j == 0 and direction_i == 0:  # nema pomeranja, beskonacna petlja
                    continue
                if self._move_and_check(i, j, direction_i, direction_j, my_piece, opp_piece):
                    return True

        return False

    def _move_and_check(self, i, j, increment_i, increment_j, my_piece, opp_piece):
        i = i + increment_i
        j = j + increment_j
        if not (0 <= i <= 7 and 0 <= j <= 7):
            return False
        next_cell = self._board[i][j]

        if next_cell == opp_piece:
            while 0 <= i <= 7 and 0 <= j <= 7:
                next_cell = self._board[i][j]
                if next_cell is None:
                    return False

                if next_cell == my_piece:
                    return True
                else:
                    i = i + increment_i
                    j = j + increment_j

        return False

    def _move_and_flip(self, i, j, direction_i, direction_j, my_piece, opp_piece):
        i = i + direction_i
        j = j + direction_j
        if not (0 <= i <= 7 and 0 <= j <= 7):
            return False
        next_cell = self._board[i][j]

        if next_cell == opp_piece:
            while 0 <= i <= 7 and 0 <= j <= 7:
                next_cell = self._board[i][j]
                if next_cell is None:
                    return False

                if next_cell == my_piece:
                    return True
                else:
                    self._board[i][j] = my_piece
                    i = i + direction_i
                    j = j + direction_j

        return False

    def mark_valid_moves(self, my_piece, opp_piece):
        for i in range(8):
            for j in range(8):
                valid = self.is_move_valid(i, j, my_piece, opp_piece)
                if valid:
                    self._board[i][j] = "͸"

    def count_valid_moves(self, my_piece, opp_piece):
        k = 0
        for i in range(8):
            for j in range(8):
                valid = self.is_move_valid(i, j, my_piece, opp_piece)
                if valid:
                    k += 1
        return k

    def valid_positions(self, my_piece, opp_piece):
        moves = []
        for i in range(8):
            for j in range(8):
                valid = self.is_move_valid(i, j, my_piece, opp_piece)
                if valid:
                    moves.append((i, j))
        return moves

    def is_end(self):

        if len(self.valid_positions("⚪", "⚫")) == 0 and len(self.valid_positions("⚫", "⚪")) == 0:
            return True
        return False

    def determine_winner(self):
        black_tiles = 0
        white_tiles = 0
        for i in range(8):
            for j in range(8):
                tile = self._board[i][j]
                if tile == "⚪":
                    black_tiles += 1
                elif tile == "⚫":
                    white_tiles += 1
        if white_tiles > black_tiles:
            return "white is winner, winning by {0}".format(white_tiles-black_tiles)
        elif white_tiles == black_tiles:
            return "no one, it's a draw"
        else:
            return "black is winner, winning by {0}".format(black_tiles-white_tiles)

    def __eq__(self, other):
        return self.to_hash() == other.to_hash()

    def __str__(self):
        ret = "    0   1   2   3   4   5   6   7 "
        ret += "\n  ---------------------------------\n"
        for i in range(8):
            ret += str(i) + " |"
            for j in range(8):
                if self._board[i][j] is None:
                    ret += "   |"
                else:
                    ret += " %s |" % self._board[i][j]
            ret += "\n  ---------------------------------\n"
        return ret

    def __copy__(self):
        new_state = State()
        for i in range(8):
            for j in range(8):
                new_state.board[i][j] = self._board[i][j]
        return new_state

    def print_with_avaliable_moves(self, my_piece, opp_piece):
        new_state = copy.deepcopy(self)
        new_state.mark_valid_moves(my_piece, opp_piece)
        print(new_state)

    def to_hash(self):
        hash_value = 0
        mod = 109345121
        p = 31
        p_powered = 1
        for i in range(8):
            for j in range(8):
                piece = self._board[i][j]
                if piece == "⚪":
                    # hash_code += "1"
                    hash_value =(hash_value + 1 * p_powered) % mod
                elif piece == "⚫":
                    # hash_code += "0"
                    hash_value = (hash_value + 2 * p_powered) % mod
                else:
                    # hash_code += "."
                    hash_value = (hash_value + 3 * p_powered) % mod
                p_powered = (p_powered * p) % mod
        return hash_value

    def heuristic_value(self):
        opp_piece, my_piece = "⚪", "⚫"
        my_tiles, opp_tiles, my_front_tiles, opp_front_tiles, p, c, l, m, f, d = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        x1 = [-1, -1, 0, 1, 1, 1, 0, -1]
        y1 = [0, 1, 1, 1, 0, -1, -1, -1]

        for i in range(8):
            for j in range(8):
                if self._board[i][j] == my_piece:
                    d += 1
                    my_tiles += 1
                elif self._board[i][j] == opp_piece:
                    d -= 1
                    opp_tiles += 1
                if self._board[i][j] is not None:
                    for k in range(8):
                        x = i + x1[k]
                        y = j + y1[k]
                        if 0 <= x < 8 and 0 <= y < 8 and self._board[i][j] is None:
                            if self._board[i][j] == my_piece:
                                my_front_tiles += 1
                            else:
                                opp_front_tiles += 1
                            break
        if my_tiles > opp_tiles:
            p = (100.0 * my_tiles) / (my_tiles + opp_tiles)
        elif my_tiles < opp_tiles:
            p = -(100.0 * opp_tiles) / (my_tiles + opp_tiles)
        else:
            p = 0

        if my_front_tiles > opp_front_tiles:
            f = -(100.0 * my_front_tiles) / (my_front_tiles + opp_front_tiles)
        elif my_front_tiles < opp_front_tiles:
            f = (100.0 * opp_front_tiles) / (my_front_tiles + opp_front_tiles)
        else:
            f = 0

        my_tiles = opp_tiles = 0
        if self._board[0][0] == my_piece:
            my_tiles += 1
        elif self._board[0][0] == opp_piece:
            opp_tiles += 1
        if self._board[0][7] == my_piece:
            my_tiles += 1
        elif self._board[0][7] == opp_piece:
            opp_tiles += 1
        if self._board[7][0] == my_piece:
            my_tiles += 1
        elif self._board[7][0] == opp_piece:
            opp_tiles += 1
        if self._board[7][7] == my_piece:
            my_tiles += 1
        elif self._board[7][7] == opp_piece:
            opp_tiles += 1
        c = 25 * (my_tiles - opp_tiles)

        my_tiles = opp_tiles = 0
        if self._board[0][0] is None:
            if self._board[0][1] == my_piece:
                my_tiles += 1
            elif self._board[0][1] == opp_piece:
                opp_tiles += 1
            if self._board[1][1] == my_piece:
                my_tiles += 1
            elif self._board[1][1] == opp_piece:
                opp_tiles += 1
            if self._board[1][0] == my_piece:
                my_tiles += 1
            elif self._board[1][0] == opp_piece:
                opp_tiles += 1

        if self._board[0][7] is None:
            if self._board[0][6] == my_piece:
                my_tiles += 1
            elif self._board[0][6] == opp_piece:
                opp_tiles += 1
            if self._board[1][6] == my_piece:
                my_tiles += 1
            elif self._board[1][6] == opp_piece:
                opp_tiles += 1
            if self._board[1][7] == my_piece:
                my_tiles += 1
            elif self._board[1][7] == opp_piece:
                opp_tiles += 1

        if self._board[7][0] is None:
            if self._board[7][1] == my_piece:
                my_tiles += 1
            elif self._board[7][1] == opp_piece:
                opp_tiles += 1
            if self._board[6][1] == my_piece:
                my_tiles += 1
            elif self._board[6][1] == opp_piece:
                opp_tiles += 1
            if self._board[6][0] == my_piece:
                my_tiles += 1
            elif self._board[6][0] == opp_piece:
                opp_tiles += 1

        if self._board[7][7] is None:
            if self._board[6][7] == my_piece:
                my_tiles += 1
            elif self._board[6][7] == opp_piece:
                opp_tiles += 1
            if self._board[6][6] == my_piece:
                my_tiles += 1
            elif self._board[6][6] == opp_piece:
                opp_tiles += 1
            if self._board[7][6] == my_piece:
                my_tiles += 1
            elif self._board[7][6] == opp_piece:
                opp_tiles += 1

        l = -12.5 * (my_tiles - opp_tiles)

        my_tiles = self.count_valid_moves(my_piece, opp_piece)
        opp_tiles = self.count_valid_moves(opp_piece, my_piece)
        if my_tiles > opp_tiles:
            m = (100.0 * my_tiles) / (my_tiles + opp_tiles)
        elif my_tiles < opp_tiles:
            m = -(100.0 * opp_tiles) / (my_tiles + opp_tiles)
        else:
            m = 0

        score = (10 * p) + (801.724 * c) + (382.026 * l) + (78.922 * m) + (74.396 * f) + (10 * d)
        return round(score)



if __name__ == '__main__':
    my_new_state = State()
    my_new_state.set_value(3, 2, "⚪", "⚫")

    my_new_state1 = State()
    my_new_state1.set_value(3, 2, "⚪", "⚫")
    print(my_new_state.to_hash() == my_new_state1.to_hash())

    my_new_state.set_value(2, 2, "⚫", "⚪")
    #
    my_new_state.set_value(1, 2, "⚪", "⚫")
    my_new_state.set_value(4, 2, "⚫", "⚪")
    #
    my_new_state.set_value(5, 2, "⚪", "⚫")
    my_new_state.set_value(4, 1, "⚫", "⚪")
    #
    my_new_state.set_value(3, 0, "⚪", "⚫")
    my_new_state.set_value(3, 5, "⚫", "⚪")

    my_new_state.set_value(3, 6, "⚪", "⚫")
    # my_new_state.set_value(0, 2, "⚫", "⚪")

    # my_new_state.set_value(1, 1, "⚪", "⚫")
    # my_new_state.set_value(1, 0, "⚫", "⚪")

    # my_new_state.mark_valid_moves("⚪", "⚫")
    # my_new_state.mark_valid_moves("⚫", "⚪")

    # print(my_new_state)
    # print(my_new_state.heuristic_value())
