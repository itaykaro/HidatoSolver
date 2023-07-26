import copy
import os 
import time

board = [
    [17, 0, 3, 0, 1],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 9, 0, 0, 0],
    [0, 0, 13, 11, 0, 0, 0, 0],
    [21, 0, 0, 0, 52, 0, 0, 0, 0],
    [23, 0, 45, 50, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 61],
    [0, 26, 43, 31, 0, 0],
    [0, 0, 0, 0, 0]
]

class Pointer:
    def __init__(self, board):
        self.board = board
        startingPoint = self.findStartingPoint()
        self.currentRow = startingPoint[0]
        self.currentCol = startingPoint[1]
        self.initialNums = self.getInitialNums()
        self.nextNum = 2
        self.solved = False
        self.moves = [] # row, col, didWrite
    
    def getInitialNums(self):
        numsList = []
        board = self.board
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] != 0:
                    numsList.append(board[i][j])
        return numsList

    def findStartingPoint(self):
        currentRow = 0
        for row in self.board:
            if 1 in row:
                return [currentRow, row.index(1)]
            currentRow += 1
        return False

    def getSpot(self, spot):
        row = self.currentRow
        col = self.currentCol
        if row == 0:
            if spot < 3:
                return False
            if col == 0 and spot == 6:
                return False
            if col == 4 and spot == 3:
                return False
        if row == 8:
            if spot == 4 or spot == 5:
                return False
            if col == 0 and spot == 6:
                return False
            if col == 4 and spot == 3:
                return False
        if col == 0:
            if spot == 6 :
                return False
            if row <= 4 and spot == 1:
                return False
            if row > 4 and spot == 5:
                return False
        if len(board[row]) - 1 == col:
            if spot == 3 :
                return False
            if row <= 4 and spot == 2:
                return False
            if row >= 4 and spot == 4:
                return False
        if row < 4:
            if spot == 1:
                return [row - 1, col - 1]
            if spot == 2:
                return [row - 1, col]
            if spot == 3:
                return [row, col + 1]
            if spot == 4:
                return [row + 1, col + 1]
            if spot == 5:
                return [row + 1, col]
            if spot == 6:
                return [row, col - 1]
        elif row == 4:
            if spot == 1:
                return [row - 1, col - 1]
            if spot == 2:
                return [row - 1, col]
            if spot == 3:
                return [row, col + 1]
            if spot == 4:
                return [row + 1, col]
            if spot == 5:
                return [row + 1, col - 1]
            if spot == 6:
                return [row, col - 1]
        else:
            if spot == 1:
                return [row - 1, col]
            if spot == 2:
                return [row - 1, col + 1]
            if spot == 3:
                return [row, col + 1]
            if spot == 4:
                return [row + 1, col]
            if spot == 5:
                return [row + 1, col - 1]
            if spot == 6:
                return [row, col - 1]

    def getAround(self):
        around = []
        for i in range(1, 7):
            spot = self.getSpot(i)
            if spot == False:
                around.append(-1)
            else:
                around.append(self.board[spot[0]][spot[1]])
        return around 

    def makeMove(self, prevSpot=0):
        around = self.getAround()
        if self.nextNum in self.initialNums:
            if self.nextNum in around:
                if self.nextNum == 61:
                    self.solved == True
                else:
                    self.move(around.index(self.nextNum) + 1, False)
            else:
                self.makeMove(self.goBackGetSpot())
        else:
            if 0 in around[prevSpot:]:
                self.move(around.index(0, prevSpot) + 1, True)
            else: 
                self.makeMove(self.goBackGetSpot())


    def move(self, spot, write):
        newSpot = self.getSpot(spot)
        self.moves.append([self.currentRow, self.currentCol, spot, int(write)])
        self.currentRow = newSpot[0]
        self.currentCol = newSpot[1]
        if write:
            self.board[newSpot[0]][newSpot[1]] = self.nextNum
        self.nextNum += 1

    def goBackGetSpot(self):
        if len(self.moves) > 0:
            lastMove = self.moves.pop()
            subtract = 1
            if lastMove[3] == False:
                while lastMove[3] == False:
                    self.currentRow = lastMove[0]
                    self.currentCol = lastMove[1]
                    lastMove = self.moves.pop()
                    subtract += 1
            self.board[self.currentRow][self.currentCol] = 0
            self.currentRow = lastMove[0]
            self.currentCol = lastMove[1]
            self.nextNum -= subtract
            return lastMove[2]
        
        
    def isSolved(self):
        return self.solved

    def printBoard(self):
        boardCopy = copy.deepcopy(self.board)
        printRows = []
        currentRow = ''
        for i in range(len(boardCopy)):
            for j in range(len(boardCopy[i])):
                if boardCopy[i][j] == 0:
                    boardCopy[i][j] = '--'
                elif boardCopy[i][j] < 10:
                    boardCopy[i][j] = '0' + str(boardCopy[i][j])
                else:
                    boardCopy[i][j] = str(boardCopy[i][j])
                currentRow += boardCopy[i][j] + ' | '
            currentRow = currentRow[0:-2]
            printRows.append(currentRow)
            currentRow = ''
        
        print(f'        / {printRows[0]} \\\n')
        print(f'      / {printRows[1]} \\\n')
        print(f'    / {printRows[2]} \\\n')
        print(f'  / {printRows[3]} \\\n')
        print(f'| {printRows[4]} |\n')
        print(f'  \ {printRows[5]} /\n')
        print(f'    \ {printRows[6]} /\n')
        print(f'      \ {printRows[7]} /\n')
        print(f'        \ {printRows[8]} /')

solution = copy.deepcopy(board)

pointer = Pointer(solution)
print('\n solving... please wait\n')
while not pointer.isSolved():
    pointer.makeMove()
os.system('cls' if os.name == 'nt' else 'clear')
print('solved!')
pointer.printBoard()