from enum import Enum, auto
from itertools import combinations
import math

class BoardState(Enum):
    PLAYING = auto()
    WON = auto()
    DRAW = auto()

class Board:
    def __init__(self, n: int, d: int):
        self.width = n
        self.dimensions = d
        self.is_player_x = True
        self.cells_x = 0b0
        self.cells_o = 0b0

        # 勝利判定ビットマスクの作成、改良の余地あり
        self.win_masks = []

        axis_idxs = list(range(self.dimensions))

        for iter_axis_idxs in powerset_list(axis_idxs, include_empty=False):
            main_axis_idx = iter_axis_idxs[0]
            other_axis_idxs = [a for a in iter_axis_idxs if a != main_axis_idx]

            not_iter_axis_idxs = list(set(axis_idxs) - set(iter_axis_idxs))
            
            for v in range(self.width ** len(not_iter_axis_idxs)):
                base_pos = [None] * self.dimensions
                for idx, axis_idx in enumerate(not_iter_axis_idxs):
                    base_pos[axis_idx] = math.floor(v / (self.width ** idx)) % self.width

                for iter_forward_other_axis_idxs in powerset_list(other_axis_idxs, include_empty=True):
                    mask = 0
                    for i in range(self.width):
                        pos = base_pos

                        pos[main_axis_idx] = i
                        for idx in other_axis_idxs:
                            if idx in iter_forward_other_axis_idxs: pos[idx] = i
                            else: pos[idx] = self.width - 1 - i

                        mask |= self.bit_weight_by_pos(pos)

                    self.win_masks.append(mask)

    def state(self):
        if self.has_winner():
            return BoardState.WON
        elif self.cells_x ^ self.cells_o == 0: # おけるセルがない
            return BoardState.DRAW
        else:
            return BoardState.PLAYING

    def bit_shift_by_pos(self, pos: list):
        shift = 0
        for idx, p in enumerate(pos):
            shift += (p) * self.width ** idx

        return shift

    def bit_weight_by_pos(self, pos: list):
        return 1 << self.bit_shift_by_pos(pos)

    def bit_value_by_pos(self, cells: bin, pos: list):
        if cells & self.bit_weight_by_pos(pos) == 0:
            return 0
        else:
            return 1

    # 指定したセルに石を置く
    def mark(self, pos: list):
        if (self.bit_value_by_pos(self.cells_x, pos)
            or self.bit_value_by_pos(self.cells_o, pos)):
            return

        if self.is_player_x:
            self.cells_x |= self.bit_weight_by_pos(pos)
        else:
            self.cells_o |= self.bit_weight_by_pos(pos)

        self.is_player_x ^= True # 手番を反転

    def has_winner(self):
        for mask in self.win_masks:
            if self.cells_x & mask == mask \
            or self.cells_o & mask == mask:
                return True

        return False


    def __str__(self):
        if self.dimensions > 2: print("描画不可")
        else:
            board_str = ""
            for i in range(self.width ** self.dimensions):
                if i % self.width == 0:
                    board_str += "\n"

                if self.cells_x & 1 << i:
                    board_str += "X"
                elif self.cells_o & 1 << i:
                    board_str += "O"
                else:
                    board_str += "･"
        
        return board_str

def powerset_list(l, include_empty = True):
    """
    与えられた list の冪集合をlistで返す。
    include_empty == False なら、冪集合から空集合を除いた集合をlistで返す。
    """
    n = len(l)
    start = 0 if include_empty else 1
    result = []
    for r in range(start, n+1):
        for comb in combinations(l, r):
            result.append(list(comb))
    return result