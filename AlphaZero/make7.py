import math

class Make7:
    # Goal of the game is to have a row of column of numbers add to make 7
    # You are allowed to place a 1 or 2 tile each turn and a 3 tile on special squares
    def __init__(self, width: int = 7, height: int = 7, threepos: list = None):
        self.width = width
        self.height = height
        self.initstate = [[0] * self.height for _ in range(self.width)]
        self.actions = [i for i in range(self.width * 3)]
        # Places where you can place a 3 tile
        if threepos is None:
            self.threepos = [(0,2), (1,4), (2,5), (4,5), (5,4), (6,2)]
        else:
            self.threepos = threepos
    
    def reset(self):
        return

    def flipState(self, board: list) -> list:
        if board is None:
            return None
        return [[-sq for sq in col] for _, col in enumerate(board)]
    
    # Encoded as a tuple of 7 (board width) integers
    def encodeState(self, board: list) -> tuple:
        if board is None:
            return None
        # 7 different board pieces: -3, -2, -1, 0, 1, 2, 3
        return (sum([(sq+3) * 7 ** i for i,sq in enumerate(col)]) for col in board)
    
    def decode(self, encoding: tuple) -> list:
        if encoding is None:
            return None
        # 7 different board pieces: -3, -2, -1, 0, 1, 2, 3
        return [[math.floor(e / 7 ** i) % 7 - 3 for i in range(self.height)] for e in encoding]
    
    def move(self, action: int, board: list, player:int = 1) -> list:
        col = int(action // 3)
        if board is None or board[col][self.height - 1] != 0:
            return None
        newboard = []
        for c in range(self.width):
            if c != col:
                newboard.append(board[c])
            else:
                newcol = []
                placedpiece = False
                for i, sq in enumerate(board[col]):
                    if placedpiece or sq != 0:
                        newcol.append(sq)
                    elif sq == 0:
                        if action % 3 == 2 and (col, i) not in self.threepos:
                            return None
                        newcol.append(player * (action % 3 + 1))
                        placedpiece = True
                newboard.append(newcol) 
        return newboard
    
    def reward(self, board: list) -> int:
        # Invalid board state
        if board is None:
            return None
        # Check Columns
        for col in board:
            playersum = 0
            for sq in col:
                if sq == 0:
                    break
                if sq > 0:
                    if playersum < 0:
                        playersum = 0
                    else:
                        playersum += sq
                        if playersum == 7:
                            return 1
                else:
                    if playersum > 0:
                        playersum = 0
                    else:
                        playersum += sq
                        if playersum == -7:
                            return 0
        # Check Rows
        for i in range(self.height):
            playersum = 0
            for sq in [board[col][i] for col in range(self.width)]:
                if sq == 0:
                    playersum = 0
                if sq > 0:
                    if playersum < 0:
                        playersum = 0
                    else:
                        playersum += sq
                        if playersum == 7:
                            return 1
                else:
                    if playersum > 0:
                        playersum = 0
                    else:
                        playersum += sq
                        if playersum == -7:
                            return 0
        # Check for a draw
        isdraw = True
        for sq in [board[col][self.height-1] for col in range(self.width)]:
            if sq == 0:
                isdraw = False
                break
        if isdraw:
            return 0.5
        return None

    def printBoard(self, board: list) -> None:
        if board is None:
            print(f"Board is None")
            return
        for i in reversed(range(self.height)):
            print([board[col][i] for col in range(self.width)])

    def legalMoves(self, board: list) -> list:
        if board is None or self.reward(board) is not None:
            print("Entered first if statement")
            return []
        legalactions = []
        for i, col in enumerate(board):
            if col[-1] != 0:
                continue
            for j, sq in enumerate(col):
                if sq == 0:
                    legalactions.append(3*i)
                    legalactions.append(3*i+1)
                    if (i, j) in self.threepos:
                        legalactions.append(3*i+2)
                    break
        return legalactions
if __name__ == "__main__":
    env = Make7()
    board = [
        [0, 0, 0, 0, 0, 0, 0],
        [1, 1, -2, 0, 0, 0, 0],
        [-1, -2, 0, 0, 0, 0, 0],
        [1, 2, -2, 2, -2, 0, 0],
        [2, 0, 0, 0, 0, 0, 0],
        [-2, 0, 0, 0, 0, 0, 0],
        [1, 1, -3, 0, 0, 0, 0],
    ]
    env.printBoard(board)
    print(env.reward(board))
    print(env.legalMoves(board))