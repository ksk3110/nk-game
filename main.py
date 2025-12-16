# X が先手、O が後手とする
# 添字は 0 始まりとする
from board import Boardø

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        
game = Board(3, 2)
game.mark([1,0])
game.mark([0,1])
game.mark([1,1])
game.mark([2,2])
game.mark([1,2])
game.mark([2,1])
print(game)
print(game.state())