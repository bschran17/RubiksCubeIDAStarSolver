from rubik.cube import Cube
from Heuristic import heuristic as h
from heapq import heappush, heappop
import time
import random

SOLVED_CUBE = Cube("WWWWWWWWWGGGRRRBBBOOOGGGRRRBBBOOOGGGRRRBBBOOOYYYYYYYYY")
POSSIBLE_MOVES = [
    "F",
    "Fi",
    "F2",
    "B",
    "Bi",
    "B2",
    "U",
    "Ui",
    "U2",
    "D",
    "Di",
    "D2",
    "L",
    "Li",
    "L2",
    "R",
    "Ri",
    "R2",
]
F_MOVE_SET = [
    "F",
    "Fi",
    "F2",
]
B_MOVE_SET = [
    "B",
    "Bi",
    "B2",
]
U_MOVE_SET = [
    "U",
    "Ui",
    "U2",
]
D_MOVE_SET = [
    "D",
    "Di",
    "D2",
]
L_MOVE_SET = [
    "L",
    "Li",
    "L2",
]
R_MOVE_SET = [
    "R",
    "Ri",
    "R2",
]


class CubeNode:
    def __init__(self, cube, moves, depth):
        self.cube = cube
        self.moves = moves
        self.depth = depth


class PQCubeNode:
    def __init__(self, priority, cubenode):
        self.priority = priority
        self.cubenode = cubenode


class CubeNodePriorityQueue(PQCubeNode):
    def __init__(self):
        self.queue = []

    def __str__(self):
        s = ""
        for i in self.queue:
            s.join(str(i.cube))
            s.join("\n")
        return s

    def isEmpty(self):
        return len(self.queue) == 0

    def insert(self, pqcubenode):
        initLength = len(self.queue)
        for i in range(initLength):
            if pqcubenode.priority < self.queue[i].priority:
                self.queue.insert(i, pqcubenode)
        if initLength == len(self.queue):
            self.queue.append(pqcubenode)

    def pop(self):
        return self.queue.pop(0)


## Move/branch should be pruned if prevmove and move are in the same moveset, or if the prevmove is in B,D,R movesets and move is in the opposite moveset.
def prune(prevmove, move):
    prune = False
    if prevmove in F_MOVE_SET and move in F_MOVE_SET:
        prune = True
    elif prevmove in B_MOVE_SET and (move in B_MOVE_SET or move in F_MOVE_SET):
        prune = True
    elif prevmove in U_MOVE_SET and move in U_MOVE_SET:
        prune = True
    elif prevmove in D_MOVE_SET and (move in D_MOVE_SET or move in U_MOVE_SET):
        prune = True
    elif prevmove in L_MOVE_SET and move in L_MOVE_SET:
        prune = True
    elif prevmove in R_MOVE_SET and (move in R_MOVE_SET or move in L_MOVE_SET):
        prune = True
    return prune


## Given a cube and a string representing a move, performs the move on the cube and returns the cube object
def performMove(cube, move):
    if move == "F":
        cube.F()
        return cube
    elif move == "Fi":
        cube.Fi()
        return cube
    elif move == "F2":
        cube.F()
        cube.F()
        return cube
    elif move == "B":
        cube.B()
        return cube
    elif move == "Bi":
        cube.Bi()
        return cube
    elif move == "B2":
        cube.B()
        cube.B()
        return cube
    elif move == "U":
        cube.U()
        return cube
    elif move == "Ui":
        cube.Ui()
        return cube
    elif move == "U2":
        cube.U()
        cube.U()
        return cube
    elif move == "D":
        cube.D()
        return cube
    elif move == "Di":
        cube.Di()
        return cube
    elif move == "D2":
        cube.D()
        cube.D()
        return cube
    elif move == "L":
        cube.L()
        return cube
    elif move == "Li":
        cube.Li()
        return cube
    elif move == "L2":
        cube.L()
        cube.L()
        return cube
    elif move == "R":
        cube.R()
        return cube
    elif move == "Ri":
        cube.Ri()
        return cube
    elif move == "R2":
        cube.R()
        cube.R()
        return cube


def performMoves(cube, movelst):
    for move in movelst:
        performMove(cube, move)
    return cube


def idaStar(cube):
    nodeStack = []
    solved = False
    currBound = 0
    nextBound = h(cube)
    priorityQueue = CubeNodePriorityQueue()
    while not solved:
        if len(nodeStack) == 0:
            nodeStack.append(CubeNode(cube, [], 0))
            print(currBound)
            currBound = nextBound
            nextBound = 10000
        currNode = nodeStack.pop(0)
        if currNode.depth == currBound:
            if currNode.cube.is_solved():
                solveMoves = currNode.moves.copy()
                solved = True
        else:
            for move in POSSIBLE_MOVES:
                if currNode.moves == []:
                    prevMove = None
                else:
                    prevMove = currNode.moves[-1]
                if currNode.depth == 0 or not prune(prevMove, move):
                    newCube = Cube(currNode.cube.flat_str())
                    newCube = performMove(newCube, move)
                    depth = currNode.depth + 1
                    priority = depth + h(newCube)
                    newMoves = currNode.moves.copy()
                    newMoves.append(move)
                    newNode = CubeNode(newCube, newMoves, depth)
                    if priority <= currBound:
                        newPQNode = PQCubeNode(priority, newNode)
                        priorityQueue.insert(newPQNode)
                    elif priority > currBound and priority < nextBound:
                        nextBound = priority
            while not priorityQueue.isEmpty():
                newNodeStackNode = priorityQueue.pop()
                nodeStack.append(newNodeStackNode.cubenode)
    return solveMoves


c = Cube("WWWWWWWWWGGGRRRBBBOOOGGGRRRBBBOOOGGGRRRBBBOOOYYYYYYYYY")
"""c.R()
c.Di()
c.Li()
print(idaStar(c))"""


c.U()
c.L()
c.R()
c.U()
c.U()
c.D()
c.D()
c.L()
print(idaStar(c))


"""scrambleList = []
times = []
for i in range(1, 11):
    groupScramble = []
    groupTimes = []
    for j in range(10):
        indiviualScramble = []
        for k in range(i):
            r = random.randint(0, 17)
            indiviualScramble.append(POSSIBLE_MOVES[r])
        print(indiviualScramble)
        groupScramble.append(indiviualScramble)
        cube = Cube("WWWWWWWWWGGGRRRBBBOOOGGGRRRBBBOOOGGGRRRBBBOOOYYYYYYYYY")
        performMoves(cube, indiviualScramble)
        startTime = time.time()
        idaStar(cube)
        executionTime = time.time() - startTime
        del cube
        print("i = " + str(i))
        print("j = " + str(j))
        print(executionTime)
        groupTimes.append(executionTime)
    scrambleList.append(groupScramble)
    times.append(groupTimes)"""
