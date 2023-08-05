from state import State
from tree import Tree
from tree import TreeNode
from copy import copy, deepcopy
from time import time
import math
from hashmap import LinearHashMap

positive_inf = 10_000_000
negative_inf = -10_000_000


class Game(object):
    __slots__ = "_current_state", "_future_states", "_BLACK_PIECE", "_WHITE_PIECE", "_player_turn",\
                "_visited_states_hash", "_depth"

    def __init__(self):

        self._current_state = State()
        self._future_states = Tree()
        self._depth = 3

        self._BLACK_PIECE = "⚪"
        self._WHITE_PIECE = "⚫"
        self._player_turn = self._BLACK_PIECE
        self._visited_states_hash = LinearHashMap()
        self._future_states.root = TreeNode(self._current_state, None)

    def switch_player(self):
        if self._player_turn == self.BLACK_PIECE:
            self._player_turn = self.WHITE_PIECE
        else:
            self._player_turn = self.BLACK_PIECE

    @property
    def depth(self):
        return self._depth

    @depth.setter
    def depth(self, value):
        self._depth = value

    @property
    def BLACK_PIECE(self):
        return self._BLACK_PIECE

    @property
    def WHITE_PIECE(self):
        return self._WHITE_PIECE

    @property
    def future_states(self):
        return self._future_states

    @property
    def visited_states_hash(self):
        return self._visited_states_hash

    @property
    def current_state(self):
        return self._current_state

    @current_state.setter
    def current_state(self, value):
        self._current_state = value

    @property
    def player_turn(self):
        return self._player_turn

    def create_future_states(self, depth, my_piece, opp_piece):
        self._visited_states_hash.clear()
        # samo lisnim čvorovima su potrebni podaci za poredjenje
        self.future_states.root = TreeNode(self.current_state, None)
        self._create_future_states(depth, self._future_states.root, my_piece, opp_piece, self._current_state)

    def _create_future_states(self, depth, node, my_piece, opp_piece, state):
        if depth == 0 or node.data.is_end():
            return None
        for move in state.valid_positions(my_piece, opp_piece):
            # dodavanje u stablo izmenjeno stanje
            new_state = copy(state)
            new_state.set_value(move[0], move[1], my_piece, opp_piece)
            # ako se vec nalazi u hashmap-i samo se doda taj čvor i više se ne razgranava
            if self._visited_states_hash.get(new_state.to_hash()) is not None:
                new_node = TreeNode(new_state, self._visited_states_hash[new_state.to_hash()])
                node.add_child(new_node)
            # u suprotnom dalje se razgranava i dodaje
            else:
                new_node = TreeNode(new_state, None)
                node.add_child(new_node)

                self.visited_states_hash[new_state.to_hash()] = None

                self._create_future_states(depth - 1, new_node, opp_piece, my_piece, new_state)

            # ako je list treba da ima heurističku vrednost za poredjenje
            if new_node.is_leaf():
                new_node.comparison_data = new_node.data.heuristic_value()

    def play(self):
        while True:

            if self.current_state.is_end():
                print(self._current_state)
                print("The game is over, result is", self.current_state.determine_winner())
                break

            if self.player_turn == self.BLACK_PIECE and\
                    len(self._current_state.valid_positions(self.BLACK_PIECE, self.WHITE_PIECE)) != 0:
                self.current_state.print_with_avaliable_moves(self.BLACK_PIECE, self.WHITE_PIECE)
                while True:

                    # ovo se može zakomentarisati a ono ispod odkomentarisati kako bi crni igrao po nekom obrascu

                    y = coor_input("Input Y coordinate: ")
                    if y is None:
                        print("Invalid input, try again.")
                        continue
                    x = coor_input("Input X coordinate: ")
                    if x is None:
                        print("Invalid input, try again.")
                        continue

                    if self.current_state.is_move_valid(y, x, self.BLACK_PIECE, self.WHITE_PIECE):
                        self.current_state.set_value(y, x, self.BLACK_PIECE, self.WHITE_PIECE)
                        break
                    else:
                        print("Invalid move, try again.")

                    # moves = self.current_state.valid_positions(self.BLACK_PIECE, self.WHITE_PIECE)
                    #
                    # coeficient_of_move = 2
                    # if len(moves) > coeficient_of_move:
                    #     move = moves[coeficient_of_move-1]
                    # else:
                    #     move = moves[0]
                    #
                    # self.current_state.set_value(move[0], move[1], self.BLACK_PIECE, self.WHITE_PIECE)
                    #
                    # break

            elif self.player_turn == self.WHITE_PIECE\
                    and len(self._current_state.valid_positions(self.WHITE_PIECE, self.BLACK_PIECE)) != 0:

                # ispis dostupnih poteza
                self.current_state.print_with_avaliable_moves(self.WHITE_PIECE, self.BLACK_PIECE)

                start = time()
                # varijabilna dubina
                if len(self._current_state.valid_positions(self.WHITE_PIECE, self.BLACK_PIECE)) > 11:
                    depth = self._depth - 1
                else:
                    depth = self._depth
                self.create_future_states(depth, self.WHITE_PIECE, self.BLACK_PIECE)
                # nalazenje cvora sa minimalnom vrednoscu
                min_node = self.minimax(depth, True)
                # nalazenje pretka da bi se znalo koji sledeci potez da se odigra
                parent_root_child = self.future_states.find_parent_root_child(min_node)
                # stanje se podesava na stanje tog pretka
                self.current_state = parent_root_child.data
                end = time()
                print("Executed for :{0:f}s".format(end - start))

            self.switch_player()

    def minimax(self, depth, is_max):
        return self._minimax(depth, negative_inf, positive_inf, is_max, self.future_states.root)

    def _minimax(self, depth, alpha, beta, is_max, node):

        if depth == 0 or node.is_leaf():
            return node

        if is_max:
            max_node = TreeNode(None, negative_inf)
            for child in node.children:
                child_node = self._minimax(depth - 1, alpha, beta, False, child)
                max_node = max(child_node, max_node)

                alpha = max(alpha, child_node.comparison_data)
                if beta <= alpha:
                    break

            return max_node
        else:
            min_node = TreeNode(None, positive_inf)
            for child in node.children:
                child_node = self._minimax(depth - 1, alpha, beta,  True, child)
                min_node = min(child_node, min_node)

                beta = min(alpha, child_node.comparison_data)
                if beta <= alpha:
                    break

            return min_node


def coor_input(input_text):
    value = input(input_text)
    if not is_int(value):
        return None
    else:
        value = int(value)
    if not (0 <= value <= 7):
        return None
    return value


def is_int(value):
    try:
        int(value)
        return True
    except ValueError:
        return False


if __name__ == '__main__':
    game1 = Game()
    game1.play()
    # game1.create_future_states(3, game1.BLACK_PIECE, game1.WHITE_PIECE)
    # print("")
    # start = time()
    # game1.create_future_states(5, "⚪", "⚫")
    # end = time()
    #
    # print(game1.future_states.root)
    # print("Izvrseno za {0:f}".format(end - start))

    # root = TreeNode(None,100)
    #
    # fc1 = TreeNode(None,30)
    # fc2 = TreeNode(None, 40)
    #
    # root.add_child(fc1)
    # root.add_child(fc2)
    #
    # n1 = TreeNode(None, -1)
    # n2 = TreeNode(None, 3)
    # n3 = TreeNode(None, 5)
    # n4 = TreeNode(None, 1)
    #
    # n5 = TreeNode(None, -6)
    # n6 = TreeNode(None, -4)
    # n7 = TreeNode(None, 7)
    # n8 = TreeNode(None, 9)
    #
    # fc1.add_child(n1)
    # fc1.add_child(n2)
    # fc1.add_child(n3)
    # fc1.add_child(n4)
    #
    # fc2.add_child(n5)
    # fc2.add_child(n6)
    # fc2.add_child(n7)
    # fc2.add_child(n8)
    #
    # nn9 = TreeNode(None, -10)
    # n8.add_child(nn9)
    #
    # nn10 = TreeNode(None, -11)
    # n8.add_child(nn10)
    #
    # game1.future_states.root = root
    # print(game1._minimax(3, True, root).comparison_data)


