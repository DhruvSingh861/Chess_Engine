import random as rand
import time

pieceScore = {"p": 100,"N":300,"B":300,"R":500,"K":0,"Q":900}
CHECKMATE = 1000000
STALEMATE = 0
MAX_DEPTH = 3
Endgame = False
pawnScores = [0, 0, 0, 0, 0, 0, 0, 0,
                   50, 50, 50, 50, 50, 50, 50, 50,
                   10, 10, 20, 30, 30, 20, 10, 10,
                   5, 5, 10, 25, 25, 10, 5, 5,
                   0, 0, 0, 20, 20, 0, 0, 0,
                   5, -5, -10, 0, 0, -10, -5, 5,
                   5, 10, 10, -20, -20, 10, 10, 5,
                   0, 0, 0, 0, 0, 0, 0, 0
                   ]
knightScores = [-50, -40, -30, -30, -30, -30, -40, -50,
                             -40, -20,   0,   0,   0,   0, -20, -40,
                             -30,   0,  10,  15,  15,  10,   0, -30,
                             -30,   5,  15,  20,  20,  15,   5, -30,
                             -30,   0,  15,  20,  20,  15,   0, -30,
                             -30,   5,  10,  15,  15,  10,   5, -30,
                             -40, -20,   0,   5,   5,   0, -20, -40,
                             -50, -90, -30, -30, -30, -30, -90, -50
                             ]

bishopScores = [-20, -10, -10, -10, -10, -10, -10, -20,
                             -10,  0,    0,   0,   0,   0,   0, -10,
                             -10,  0,    5,  10,  10,   5,   0, -10,
                             -10,  5,    5,  10,  10,   5,   5, -10,
                             -10,  0,   10,  10,  10,  10,   0, -10,
                             -10, 10,   10,  10,  10,  10,  10, -10,
                             -10,  5,    0,   0,   0,   0,   5, -10,
                             -20, -10, -90, -10, -10, -90, -10, -20
                             ]

rookScores = [0,  0,  0,  0,  0,  0,  0, 0,
                           5, 10, 10, 10, 10, 10, 10, 5,
                           -5, 0,  0,  0,  0,  0,  0, -5,
                           -5, 0,  0,  0,  0,  0,  0, -5,
                           -5, 0,  0,  0,  0,  0,  0, -5,
                           -5, 0,  0,  0,  0,  0,  0, -5,
                           -5, 0,  0,  0,  0,  0,  0, -5,
                            0, 0,  0,  5,  5,  0,  0,  0
                           ]
queenScores = [-20, -10, -10, -5, -5, -10, -10, -20,
               -10,   0,   0,  0,  0,   0,   0, -10,
               -10,   0,   5,  5,  5,   5,   0, -10,
                -5,   0,   5,  5,  5,   5,   0,  -5,
                 0,   0,   5,  5,  5,   5,   0,  -5,
               -10,   5,   5,  5,  5,   5,   0, -10,
               -10,   0,   5,  0,  0,   0,   0, -10,
               -20, -10, -10, 70, -5, -10, -10, -20]

kingScores = [-30, -40, -40, -50, -50, -40, -40, -30,
              -30, -40, -40, -50, -50, -40, -40, -30,
              -30, -40, -40, -50, -50, -40, -40, -30,
              -30, -40, -40, -50, -50, -40, -40, -30,
              -20, -30, -30, -40, -40, -30, -30, -20,
              -10, -20, -20, -20, -20, -20, -20, -10,
               20,  20,   0,   0,   0,   0,  20,  20,
               20,  30,  10,   0,   0,  10,  30,  20]

kingEndgameScore = [-50, -40, -30, -20, -20, -30, -40, -50,
                      -30, -20, -10,   0,   0, -10, -20, -30,
                      -30, -10,  20,  30,  30,  20, -10, -30,
                      -30, -10,  30,  40,  40,  30, -10, -30,
                      -30, -10,  30,  40,  40,  30, -10, -30,
                      -30, -10,  20,  30,  30,  20, -10, -30,
                      -30, -30,   0,   0,   0,   0, -30, -30,
                      -50, -30, -30, -30, -30, -30, -30, -50]

piecePositionScores = {"N":knightScores,"K":kingScores,"B":bishopScores,"p":pawnScores,"R":rookScores,
                       "Q":queenScores, "KE":kingEndgameScore}



def findRandomMoves(validMoves):
    return validMoves[rand.randint(0,len(validMoves)-1)]



def minMaxStarter(gs,validMoves):
    global nextMove, counter,whiteCounter,blackCounter
    nextMove=None
    rand.shuffle(validMoves)
    counter=0
    whiteCounter=0
    blackCounter=0
    execution_time=time.process_time()
    minMax(gs,validMoves,0,gs.whiteToMove,-100000,100000)
    print(time.process_time()-execution_time)
    print("NO OF MOVES CHECKED PER MOVE=====>>>  "+str(whiteCounter)+" "+str(blackCounter))
    return nextMove



def minMax(gs,validMoves, depth, whiteToMove,alpha,beta):
    global nextMove, whiteCounter,blackCounter

    if depth==MAX_DEPTH:
        return boardScore(gs)

    if whiteToMove:
        maxScore=-CHECKMATE
        for move in validMoves:
            whiteCounter+=1
            #print("white move-> "+move.toString())
            gs.makeMove(move,"Q")
            score=minMax(gs,gs.getValidMoves(),depth+1,not whiteToMove,alpha,beta)
            if score>maxScore:
                maxScore=score
                if depth==0:
                    nextMove=move
            gs.undoMove()
            alpha=max(score,alpha)
            if beta<=alpha:
                break
        return maxScore
    else:
        minScore=CHECKMATE
        for move in validMoves:
            blackCounter += 1
            #print("black move-> " + move.toString())
            gs.makeMove(move,"Q")
            score = minMax(gs, gs.getValidMoves(), depth + 1, not whiteToMove,alpha,beta)
            if score < minScore:
                minScore = score
                if depth == 0:
                    nextMove = move
            gs.undoMove()
            beta=min(score,beta)
            if beta<=alpha:
                break
        return minScore

"""
white is maximising
black is minimising
if our score is +ve (white is winning)
if our score is -ve (black is winning)
if zero (neigter one is winning)
"""
def boardScore(gs):
    noOfPieces=0
    if gs.checkMate:
        if gs.whiteToMove:
            return -CHECKMATE
        else:
            return CHECKMATE
    if gs.staleMate:
        return STALEMATE
    score=0
    for row in range(len(gs.board)):
        for col in range(len(gs.board[row])):
            square=gs.board[row][col]
            if square!="--":
                noOfPieces+=1
                #position Scoring
                piecePosScore = piecePositionScores[square[1]][(row*8)+col]
                if square[0]=="w":
                    score+=pieceScore[square[1]] + piecePosScore
                elif square[0]=="b":
                    score-=pieceScore[square[1]] + piecePosScore
    return score


def evaluate(gs):
    material=0
    material += gs.pawnCount[0]
    material += gs.knightCount[0]*3
    material += gs.bishopCount[0]*3
    material += gs.rookCount[0]*5
    material += gs.queenCount[0]*9
    material -= gs.pawnCount[1]
    material -= gs.knightCount[1] * 3
    material -= gs.bishopCount[1] * 3
    material -= gs.rookCount[1] * 5
    material -= gs.queenCount[1] * 9
    return material