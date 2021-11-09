#responsible for storing states of game
#demining valid moves
#maintain move log

class GameState():
    def __init__(self):
        self.board=[
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.pawnCount=[8,8]
        self.rookCount=[2,2]
        self.knightCount=[2,2]
        self.bishopCount=[2,2]
        self.queenCount=[1,1]

        self.pieceCountLog=[pieceCount(self.pawnCount,self.knightCount,self.bishopCount,self.rookCount,self.queenCount)]

        self.boardLog=[self.board]
        self.whiteToMove = True
        self.moveLog = []
        #kings locations
        self.whiteKingLocation=(7,4)
        self.blackKingLocation=(0,4)
        self.inCheck= False
        self.pins=[] #pices which are pinning attack from other pieces
        self.checks=[] #any piece putting another piece in check
        self.checkMate=False
        self.staleMate=False
        self.enpassantPossible=()#sqare coordinates where enpassant is possible
        self.enpassantPossibleLog=[self.enpassantPossible]
        self.wcKs=True
        self.wcQs=True
        self.bcKs=True
        self.bcQs=True
        self.castellingLog=[CastleRules(self.wcKs,self.wcQs,self.bcKs,self.bcQs)]

    def printBoard(self):
        str=""
        for row in self.board:
            for square in row:
                str+=square+" "
            print(str)
            str=""
        print("\n")



    #swap board values and update move log (change the turn)
    def makeMove(self,move,pawnPromotionType):
        type=move.pieceMoved
        if type!="--":
            if type[0] == "w":
                c = 0
            else:
                c = 1
            if type[1]=="p":
                self.pawnCount[c]+=-1
            elif type[1]=="R":
                self.rookCount[c]+=-1
            elif type[1]=="B":
                self.bishopCount[c]+=-1
            elif type[1]=="Q":
                self.queenCount[c]+=-1
            elif type[1]=="N":
                self.knightCount[c]+=-1




        #print(move.castle)
        self.board[move.endSq[0]][move.endSq[1]] = move.pieceSelected
        self.board[move.startSq[0]][move.startSq[1]] = "--"
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove

        #update kings location whenever king moves
        if move.pieceSelected == "wK":
            self.whiteKingLocation=(move.endSq[0],move.endSq[1])
        elif move.pieceSelected == "bK":
            self.blackKingLocation=(move.endSq[0],move.endSq[1])


        #Pawn Promotion
        if move.isPawnPromotion:
            if move.pieceSelected[0]=="w":
                self.queenCount[0]+=1
                self.pawnCount[0]+=-1
            else:
                self.queenCount[1]+=1
                self.pawnCount[1]+=-1
            self.board[move.endSq[0]][move.endSq[1]]=move.pieceSelected[0]+pawnPromotionType

        #enpassant
        #when pawn move 2 squares, next move can be enpassant
        if move.pieceSelected[1] == "p" and abs(move.startSq[0] - move.endSq[0]) == 2:
            self.enpassantPossible = ((move.startSq[0] + move.endSq[0]) // 2, move.endSq[1])
            #print("enpassant Block=> " + str(self.enpassantPossible))
        else:
            self.enpassantPossible = ()

        self.enpassantPossibleLog.append(self.enpassantPossible)

        #enpassant kill
        if move.enpassant:
            self.board[move.startSq[0]][move.endSq[1]]="--"

        # make castle moves
        if move.castle:
            #print("dhskjhfsdjkfhjasgdasihdagjfkashkjfhskajkfkwoiuieou")
            if move.endSq[1] - move.startSq[1] == 2:  # kingSide
                self.board[move.endSq[0]][move.endSq[1] - 1] = self.board[move.endSq[0]][move.endSq[1] + 1]
                #print(self.board[move.endSq[0]][move.endSq[1] + 1])
                self.board[move.endSq[0]][move.endSq[1] + 1] = "--"
            else:  # Queenside
                self.board[move.endSq[0]][move.endSq[1] + 1] = self.board[move.endSq[0]][move.endSq[1] - 2]
                self.board[move.endSq[0]][move.endSq[1] - 2] = "--"

        #update castelling rights.
        if move.pieceSelected=="wK":
            self.wcKs=False
            self.wcQs=False
        elif move.pieceSelected=="bK":
            self.bcKs=False
            self.bcQs=False
        elif move.pieceSelected=="wR":
            if move.startSq[0]==7:
                if move.startSq[1]==0:
                    self.wcQs=False
                elif move.startSq[1]==7:
                    self.wcKs = False
        elif move.pieceSelected=="bR":
            if move.startSq[0]==0:
                if move.startSq[1] == 0:
                    self.bcQs = False
                elif move.startSq[1] == 7:
                    self.bcKs= False

        #print("0---------------0-00-0-0-0-00-0-0-")
        #for log in self.castellingLog:
            #print(log.bKingSide, log.bQueenSide,
             #     log.wKingSide, log.wQueenSide, end=", ")
            #print()

        #print("makemove->"+str(self.wcKs)+","+str(self.wcQs)
         #                               +","+str(self.bcKs)+","+str(self.bcQs))
        self.castellingLog.append(CastleRules(self.wcKs,self.wcQs,self.bcKs,self.bcQs))
        self.boardLog.append(self.board)
        #self.printBoard()
        newpieceCount=pieceCount(self.pawnCount,self.knightCount,self.bishopCount,self.rookCount,self.queenCount)
        self.pieceCountLog.append(newpieceCount)






    #undo the moves made and delete it from move log (change the turn alternatively)
    def undoMove(self):
        if len(self.moveLog)!=0:
            move=self.moveLog.pop()
            self.board[move.startSq[0]][move.startSq[1]]=move.pieceSelected
            self.board[move.endSq[0]][move.endSq[1]]=move.pieceMoved
            self.whiteToMove=not self.whiteToMove
            #update kings location whenever king moves undone
            if move.pieceSelected == "wK":
                self.whiteKingLocation = (move.startSq[0], move.startSq[1])
            elif move.pieceSelected == "bK":
                self.blackKingLocation = (move.startSq[0], move.startSq[1])
            #undo enpassant
            if move.enpassant:
                self.board[move.endSq[0]][move.endSq[1]]="--"
                self.board[move.startSq[0]][move.endSq[1]]=move.pieceMoved
                #print(move.pieceMoved)
                #print(move.pieceSelected)
            self.enpassantPossibleLog.pop()
            self.enpassantPossible = self.enpassantPossibleLog[-1]

        #undo castling.
        self.castellingLog.pop()
        #print("undomovelast->"+str(self.castellingLog[len(self.castellingLog)-1].wKingSide)+","+str(self.castellingLog[len(self.castellingLog)-1].wQueenSide)
         #     +","+str(self.castellingLog[len(self.castellingLog)-1].bKingSide)+","+str(self.castellingLog[len(self.castellingLog)-1].bQueenSide))
        castleRules=self.castellingLog[-1]
        self.wcKs=castleRules.wKingSide
        self.wcQs = castleRules.wQueenSide
        self.bcKs = castleRules.bKingSide
        self.bcQs = castleRules.bQueenSide

        #undo castle move
        if move.castle:
            if move.endSq[1]-move.startSq[1]==2: #kingside
                self.board[move.endSq[0]][move.endSq[1] + 1] = self.board[move.endSq[0]][move.endSq[1] - 1]
                self.board[move.endSq[0]][move.endSq[1] - 1] = "--"
            else: #queenside
                self.board[move.endSq[0]][move.endSq[1] - 2] = self.board[move.endSq[0]][move.endSq[1] + 1]
                self.board[move.endSq[0]][move.endSq[1] + 1] = "--"
           # print("whiteking undo ------")
            #print(self.whiteKingLocation)
            #print("blackking------")
            #print(self.blackKingLocation)
        self.boardLog.pop()
        self.boardLog.pop()
        self.boardLog.append(self.board)
        #self.printBoard()
        self.pieceCountLog.pop()
        currentPieceCountLog=self.pieceCountLog[-1]
        self.pawnCount[0]=currentPieceCountLog.wpc
        self.rookCount[0]=currentPieceCountLog.wrc
        self.knightCount[0]=currentPieceCountLog.wnc
        self.bishopCount[0]=currentPieceCountLog.wbc
        self.queenCount[0]=currentPieceCountLog.wqc
        self.pawnCount[1] = currentPieceCountLog.bpc
        self.rookCount[1] = currentPieceCountLog.brc
        self.knightCount[1] = currentPieceCountLog.bnc
        self.bishopCount[1] = currentPieceCountLog.bbc
        self.queenCount[1] = currentPieceCountLog.bqc



    #valid moves without considering check
    def getAllPossibleMoves(self):
        moves = []
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                turn = self.board[i][j][0]
                if (turn =='w' and self.whiteToMove) or (turn =='b' and not self.whiteToMove):
                    piece = self.board[i][j][1]
                    if piece == 'p':
                        self.getPawnMoves(i,j,moves)
                    elif piece == 'R':
                        self.getRookMoves(i,j,moves)
                    elif piece == 'B':
                        self.getBishopMoves(i,j,moves)
                    elif piece == 'N':
                        self.getKnightMoves(i,j,moves)
                    elif piece == 'Q':
                        self.getQueenMoves(i,j,moves)
                    elif piece == 'K':
                        self.getKingMoves(i, j, moves)
        return moves


    def getPawnMoves(self,i,j,moves):
        piecePinned = False
        pinDirection = ()
        for x in range(len(self.pins)-1,-1,-1):
            if i==self.pins[x][0] and j==self.pins[x][1]:
                piecePinned=True
                pinDirection=(self.pins[x][2],self.pins[x][3])
                self.pins.remove(self.pins[x])
                break

        if self.whiteToMove:
            if (i-1)>=0:
                if (self.board[i-1][j]=="--"):
                    if not piecePinned or pinDirection == (-1, 0):
                        moves.append(Move((i,j),(i-1,j),self.board))
                if (j-1)>=0:
                    if not piecePinned or pinDirection == (-1, -1):
                        if self.board[i-1][j-1][0]=="b":
                            moves.append(Move((i,j),(i-1,j-1),self.board))
                        if (i-1,j-1)==self.enpassantPossible:
                            #------------enpassant-bug-fix--------------------------------------
                            attackingPiece, blockingPiece = self.unpassantBugFix(i,j,"b")
                            #----------------------------------------------------------------------
                            if not attackingPiece or blockingPiece:
                                moves.append(Move((i,j),(i-1,j-1),self.board,enpassant=True))
                if (j+1)<=7:
                    if not piecePinned or pinDirection == (-1, 1):
                        if self.board[i - 1][j + 1][0] == "b":
                            moves.append(Move((i,j),(i-1,j+1),self.board))
                        if (i-1,j+1)==self.enpassantPossible:
                            #------------enpassant-bug-fix--------------------------------------
                            attackingPiece, blockingPiece = self.unpassantBugFix(i, j, "b")
                            #----------------------------------------------------------------------
                            if not attackingPiece or blockingPiece:
                                moves.append(Move((i,j),(i-1,j+1),self.board,enpassant=True))
            if ((i==6) and self.board[i-2][j]=="--" and self.board[i-1][j]=="--"):
                if not piecePinned or pinDirection == (-1, 0):
                    moves.append(Move((i,j),(i-2,j),self.board))
        else:
            if(i+1)<=7:
                if(self.board[i+1][j]=="--"):
                    if not piecePinned or pinDirection == (1, 0):
                        moves.append(Move((i,j),(i+1,j),self.board))
                if (j-1)>=0:
                    if not piecePinned or pinDirection == (1, -1):
                        if self.board[i + 1][j - 1][0] == "w":
                            moves.append(Move((i,j),(i+1,j-1),self.board))
                        if (i+1,j-1)==self.enpassantPossible:
                            #------------enpassant-bug-fix--------------------------------------
                            attackingPiece, blockingPiece = self.unpassantBugFix(i, j, "w")
                            #----------------------------------------------------------------------
                            if not attackingPiece or blockingPiece:
                                moves.append(Move((i,j),(i+1,j-1),self.board,enpassant=True))
                if (j+1)<=7:
                    if not piecePinned or pinDirection == (1, 1):
                        if self.board[i+1][j+1][0]=="w":
                            moves.append(Move((i,j),(i+1,j+1),self.board))
                        if (i+1,j+1)==self.enpassantPossible:
                            #------------enpassant-bug-fix--------------------------------------
                            attackingPiece, blockingPiece = self.unpassantBugFix(i, j, "w")
                            #----------------------------------------------------------------------
                            if not attackingPiece or blockingPiece:
                                moves.append(Move((i,j),(i+1,j+1),self.board,enpassant=True))
            if ((i==1) and self.board[i+2][j]=="--" and self.board[i+1][j]=="--"):
                if not piecePinned or pinDirection == (1, 0):
                    moves.append(Move((i,j),(i+2,j),self.board))

    def unpassantBugFix(self,i,j,enemy):
        attackingPiece = blockingPiece = False
        if (i+1,j-1)==self.enpassantPossible or (i-1,j-1)==self.enpassantPossible:
            kingRow, kingCol = self.whiteKingLocation if enemy == "b" else self.blackKingLocation
            if kingRow == i:
                if kingCol < j:  # king is in left of pawn
                    insideRange = range(kingCol + 1, j - 1)  # see between king and pawn
                    outsideRange = range(j + 1, 8)  # see between pawn and border
                else:  # king is in right of pawn
                    insideRange = range(kingCol - 1, j, -1)
                    outsideRange = range(j - 2, -1, -1)
                for x in insideRange:
                    if self.board[i][x] != "--":  # some piece is blocking enpassant
                        blockingPiece = True
                for x in outsideRange:
                    square = self.board[i][x]
                    if square != "--" and square[1]!="R" and square[1]!="Q":
                        blockingPiece = True
                        break
                    elif square[0] == enemy and (square[1] == "R" or square[1] == "Q"):
                        attackingPiece = True
                        break
            #print("left capture--->" + str(attackingPiece) + " " + str(blockingPiece))
        else: #right capture
            kingRow, kingCol = self.whiteKingLocation if enemy == "b" else self.blackKingLocation
            if kingRow == i:
                if kingCol < j:  # king is in left of pawn
                    insideRange = range(kingCol + 1, j)  # see between king and pawn
                    outsideRange = range(j+2, 8)  # see between pawn and border
                else:  # king is in right of pawn
                    insideRange = range(kingCol - 1, j+1, -1)
                    outsideRange = range(j - 1, -1, -1)
                for x in insideRange:
                    if self.board[i][x] != "--":  # some piece is blocking enpassant
                        blockingPiece = True
                for x in outsideRange:
                    square = self.board[i][x]
                    if square != "--" and square[1] != "R" and square[1] != "Q":
                        blockingPiece = True
                        break
                    elif square[0] == enemy and (square[1] == "R" or square[1] == "Q"):
                        attackingPiece = True
                        break
            #print("right capture--->"+str(attackingPiece)+" "+str(blockingPiece))

        return attackingPiece, blockingPiece


    def getRookMoves(self,i,j,moves):
        piecePinned = False
        pinDirection = ()
        for x in range(len(self.pins) - 1, -1, -1):
            if i == self.pins[x][0] and j == self.pins[x][1]:
                piecePinned = True
                pinDirection = (self.pins[x][2], self.pins[x][3])
                if self.board[i][j][1]!="Q": # prevent removing Queen when this function is called by getQueenMoves()
                    self.pins.remove(self.pins[x])
                break

        kill = 'w'
        if self.whiteToMove:
            kill = 'b'
        direction = [(-1,0),(1,0),(0,-1),(0,1)]
        for d in direction:
            for p in range(1,8):
                x = i + d[0]*p
                y = j + d[1]*p
                if 0 <= x <= 7 and 0 <= y <= 7:
                    if not piecePinned or pinDirection==d or pinDirection==(-d[0],-d[1]):
                        if self.board[x][y]=="--":
                            moves.append(Move((i, j),(x, y), self.board))
                        elif self.board[x][y][0]==kill:
                            moves.append(Move((i, j),(x, y), self.board))
                            break
                        else:
                            break
                else:
                    break

    def getKnightMoves(self,i,j,moves):
        piecePinned = False
        pinDirection = ()
        for x in range(len(self.pins) - 1, -1, -1):
            if i == self.pins[x][0] and j == self.pins[x][1]:
                piecePinned = True
                pinDirection = (self.pins[x][2], self.pins[x][3])
                self.pins.remove(self.pins[x])
                break

        kill = 'w'
        if self.whiteToMove:
            kill = 'b'
        direction = [(2, -1), (2, 1), (-2, -1), (-2, 1), (-1,-2), (1,-2), (-1,2), (1,2)]
        for d in direction:
            x = i + d[0]
            y = j + d[1]
            if 0 <= x <= 7 and 0 <= y <= 7:
                if not piecePinned:
                    if self.board[x][y] == "--":
                        moves.append(Move((i, j), (x, y), self.board))
                    elif self.board[x][y][0] == kill:
                        moves.append(Move((i, j), (x, y), self.board))

    def getBishopMoves(self,i,j,moves):
        piecePinned = False
        pinDirection = ()
        for x in range(len(self.pins) - 1, -1, -1):
            if i == self.pins[x][0] and j == self.pins[x][1]:
                piecePinned = True
                pinDirection = (self.pins[x][2], self.pins[x][3])
                if self.board[i][j][1] != "Q":  # prevent removing Queen when this function is called by getQueenMoves()
                    self.pins.remove(self.pins[x])
                break

        kill = 'w'
        if self.whiteToMove:
            kill = 'b'
        direction = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for d in direction:
            for p in range(1, 8):
                x = i + d[0] * p
                y = j + d[1] * p
                if 0 <= x <= 7 and 0 <= y <= 7:
                    if not piecePinned or pinDirection==d or pinDirection==(-d[0],-d[1]):
                        if self.board[x][y] == "--":
                            moves.append(Move((i, j), (x, y), self.board))
                        elif self.board[x][y][0] == kill:
                            moves.append(Move((i, j), (x, y), self.board))
                            break
                        else:
                            break
                else:
                    break


    def getQueenMoves(self,i,j,moves):
        self.getRookMoves(i,j,moves)
        self.getBishopMoves(i,j,moves)

    def getKingMoves(self,i,j,moves):
        kill = 'w'
        if self.whiteToMove:
            kill = 'b'
        direction = [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]
        for d in direction:
            x = i + d[0]
            y = j + d[1]
            if 0 <= x <= 7 and 0 <= y <= 7:
                if self.board[x][y] == "--" or self.board[x][y][0] == kill:
                    #we are just placing my king to respective positions and see if a check mate
                    #i.e. we are generating a phantom king
                    if kill == "b":
                        self.whiteKingLocation = (x, y)
                    else:
                        self.blackKingLocation = (x, y)
                    inChecK, pins, checks = self.checkForPinsAndChecks()
                    if not inChecK:
                        moves.append(Move((i, j), (x, y), self.board))
                    #placing king back again to its original coordinates
                    if kill == "b":
                        self.whiteKingLocation = (i, j)
                    else:
                        self.blackKingLocation = (i, j)
        self.getCastleMoves(i,j,moves,kill)


    def getCastleMoves(self,i,j,moves,kill):
        if self.inCheck:
            #print("INNNNNN CHECKKKKKKKKKKKK")
            return
        #print(self.wcKs)
        if (self.whiteToMove and self.wcKs and self.board[i][j+3]=="wR") or\
                (not self.whiteToMove and self.bcKs and self.board[i][j+3]=="bR"):
            #print("andar king")
            self.getKingSideCatleMoves(i,j,moves,kill)
        if (self.whiteToMove and self.wcQs and self.board[i][j-4]=="wR")or\
                (not self.whiteToMove and self.bcQs and self.board[i][j-4]=="bR"):
            #print("andar Queen")
            self.getQueenSideCatelMoves(i,j,moves,kill)

    def getKingSideCatleMoves(self,i,j,moves,kill):
        if self.board[i][j+1]=="--" and self.board[i][j+2]=="--":
            # i.e. we are generating a phantom king
            if kill == "b":
                self.whiteKingLocation = (i, j+1)
                inChecK, pins, checks = self.checkForPinsAndChecks()
                if inChecK != []:
                    self.whiteKingLocation = (i, j)
                    return
                self.whiteKingLocation = (i, j + 2)
                inChecK, pins, checks = self.checkForPinsAndChecks()
                if inChecK != []:
                    self.whiteKingLocation = (i, j)
                    #print(":(  "+str(i)+","+str(j+2))
                    return
            else:
                self.blackKingLocation = (i, j+1)
                inChecK, pins, checks = self.checkForPinsAndChecks()
                if inChecK != []:
                    self.blackKingLocation = (i, j)
                    #print(":(  " + str(i) + "," + str(j + 1))
                    return
                self.blackKingLocation = (i, j + 2)
                inChecK, pins, checks = self.checkForPinsAndChecks()
                if inChecK != []:
                    self.blackKingLocation = (i, j)
                    return
            if kill=="w":
                self.blackKingLocation = (i, j)
            else:
                self.whiteKingLocation = (i, j)
            #print("King side CASTLING ALLOWED")
            moves.append(Move((i,j),(i,j+2),self.board,castle=True))


    def getQueenSideCatelMoves(self,i,j,moves,kill):
        if self.board[i][j-1]=="--" and self.board[i][j-2]=="--" and self.board[i][j-3]=="--":
            # i.e. we are generating a phantom king
            if kill == "b":
                self.whiteKingLocation = (i, j - 1)
                inChecK, pins, checks = self.checkForPinsAndChecks()
                if inChecK != []:
                    self.whiteKingLocation = (i, j)
                    return
                self.whiteKingLocation = (i, j - 2)
                inChecK, pins, checks = self.checkForPinsAndChecks()
                if inChecK != []:
                    self.whiteKingLocation = (i, j)
                    return
            else:
                self.blackKingLocation = (i, j - 1)
                inChecK, pins, checks = self.checkForPinsAndChecks()
                if inChecK != []:
                    self.blackKingLocation = (i, j)
                    return
                self.blackKingLocation = (i, j - 2)
                inChecK, pins, checks = self.checkForPinsAndChecks()
                if inChecK != []:
                    self.blackKingLocation = (i, j)
                    return
            if kill == "w":
                self.blackKingLocation = (i, j)
            else:
                self.whiteKingLocation = (i, j)
            #print("Queen side CASTLING ALLOWED")
            moves.append(Move((i, j), (i, j - 2),self.board,castle=True))
            #print(inChecK)




    # valid moves considering check
    def getValidMoves(self):
        #for log in self.castellingLog:
         #   print(log.wKingSide, log.wQueenSide,
          #        log.bKingSide, log.bQueenSide, end=", ")
           # print()

        moves=[]
        self.inCheck, self.pins, self.checks = self.checkForPinsAndChecks()
        #print("checks=> " + str(self.checks))
        #print("pins=> " + str(self.pins))
        if self.whiteToMove:
            kingRow=self.whiteKingLocation[0]
            kingCol=self.whiteKingLocation[1]
        else:
            kingRow = self.blackKingLocation[0]
            kingCol = self.blackKingLocation[1]

        if self.inCheck:
            if len(self.checks)==1:
                moves=self.getAllPossibleMoves()
                check=self.checks[0]
                checkRow=check[0]
                checkCol=check[1]
                pieceChecking = self.board[checkRow][checkCol]
                validSquares=[]
                if pieceChecking[1]=="N":
                    validSquares=[(checkRow,checkCol)]
                else:
                    for i in range(1,8):
                        validSquare = (kingRow+check[2]*i, kingCol+check[3]*i)
                        validSquares.append(validSquare)
                        if validSquare[0]==checkRow and validSquare[1]==checkCol:
                            break
                for i in range(len(moves)-1,-1,-1):
                    if moves[i].pieceSelected[1]!="K":
                        if not(moves[i].endSq[0],moves[i].endSq[1]) in validSquares:
                            moves.remove(moves[i])
            else:
                self.getKingMoves(kingRow,kingCol,moves)
        else:
            moves=self.getAllPossibleMoves()


        # CheckMate or StaleMate
        if len(moves) == 0:
            if self.checks!=[]:
                self.checkMate = True
                #print("====CHECK MATE====")
            else:
                self.staleMate = True
                #print("====STALE MATE====")
        else:
            # undo move should not create any problem
            self.checkMate = False
            self.staleMate = False

        return moves

    def checkForPinsAndChecks(self):
        pins=[]
        checks=[]
        inCheck=[]
        if self.whiteToMove:
            enemyColor="b"
            allyColor="w"
            startRow=self.whiteKingLocation[0]
            startCol=self.whiteKingLocation[1]
        else:
            enemyColor = "w"
            allyColor = "b"
            startRow = self.blackKingLocation[0]
            startCol = self.blackKingLocation[1]
        directions = ((-1,0), (0,-1), (1,0), (0,1), (-1,-1), (-1,1), (1,-1), (1,1))
        for j in range(len(directions)):
            d=directions[j]
            possiblePins=()
            for i in range(1,8):
                endRow=startRow + d[0]*i
                endCol=startCol + d[1]*i
                if 0<=endRow<=7 and 0<=endCol<=7:
                    endPiece = self.board[endRow][endCol]
                    #and 2nd condition because my phantom king generated by getKingMoves() should not be blocked by my original king
                    if endPiece[0] == allyColor and endPiece[1]!="K":
                        if possiblePins==():
                            possiblePins = ((endRow,endCol,d[0],d[1]))
                        else:
                            break
                    elif endPiece[0]== enemyColor:
                        type = endPiece[1]
                        """
                        possibilities---->
                        1. orthogonally rook is present
                        2. diagonally bishop is present
                        3. diagonally, 1 piece away from king pawn is present
                        4. diagonally or orthogonally queen is present
                        5. Enemy king is present 1 piece away from ally king
                        """
                        if (0<=j<=3 and type=="R") or (4<=j<=7 and type=="B") or \
                                (i==1 and type=="p" and ((enemyColor=="w" and 6<=j<=7) or (enemyColor=="b" and 4<=j<=5))) or \
                                (type=="Q") or (i==1 and type=="K"):
                            if possiblePins==():
                                inCheck=True
                                checks.append((endRow,endCol,d[0],d[1]))
                                break
                            else:
                                pins.append(possiblePins)
                                break
                        else:
                            break
                else:
                    break
        #check for Knight
        knightMoves=[(2, -1), (2, 1), (-2, -1), (-2, 1), (-1,-2), (1,-2), (-1,2), (1,2)]
        for m in knightMoves:
            endRow = startRow + m[0]
            endCol = startCol + m[1]
            if 0<=endRow<=7 and 0<=endCol<=7:
                endPiece=self.board[endRow][endCol]
                if endPiece[0]==enemyColor and endPiece[1]=="N":
                    inCheck=True
                    checks.append((endRow,endCol,m[0],m[1]))
        return inCheck,pins,checks


class CastleRules():
    def __init__(self,wKingSide,wQueenSide,bKingSide,bQueenSide):
        self.wKingSide=wKingSide
        self.bKingSide=bKingSide
        self.wQueenSide=wQueenSide
        self.bQueenSide=bQueenSide

class pieceCount():
    def __init__(self,pc,nc,bc,rc,qc):
        self.wpc=pc[0]
        self.wnc=nc[0]
        self.wbc=bc[0]
        self.wrc=rc[0]
        self.wqc=qc[0]
        self.bpc = pc[1]
        self.bnc = nc[1]
        self.bbc = bc[1]
        self.brc = rc[1]
        self.bqc = qc[1]

"""
#--------------------------------------------------------------------------------------------------------------------------
    #RECURSIVE MAKE EVERY MOVE APPROACH
    #valid moves considering check
    def getValidMoves(self):
    
        #ALGORITHM ----------------------------------------------------->>>
        #1) generate all possible moves
        #2) for each move make the move
        #3) for above generated moves make all opponents moves
        #4) for each opponents move see if king is attacked
        #5) if so then its not a valid move (remove it from moves list)
        #<<<-----------------------------------------------------------------
        #step-1
        moves = self.getAllPossibleMoves()
        #step-2
        for i in range(len(moves)-1,-1,-1):
            self.makeMove(moves[i])
            #step-3
            self.whiteToMove = not self.whiteToMove
            if self.inCheck():
                # step-4
                moves.remove(moves[i])
            self.whiteToMove = not self.whiteToMove
            self.undoMove()

        #CheckMate or StaleMate
        if len(moves)==0:
            if self.inCheck():
                self.checkMate=True
            else:
                self.staleMate=True
        else:
            #undo move should not create any problem
            self.checkMate = False
            self.staleMate = False

        return moves

    #check if current player is in check
    def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0],self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0],self.blackKingLocation[1])

    #determine if enemy can attack the square r,c
    def squareUnderAttack(self,r,c):
        self.whiteToMove=not self.whiteToMove
        oppMoves=self.getAllPossibleMoves()
        self.whiteToMove=not self.whiteToMove
        for move in oppMoves:
            if move.endSq[0]==r and move.endSq[1]==c:#under attack
                return True
        return False
#--------------------------------------------------------------------------------------------------------------------------
"""


#----------------------------------------------------------------------------------------------------------------
class Move():

    rankToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    rowsToRanks = {v: k for k, v in rankToRows.items()}
    colsToFiles = {v: k for k, v in filesToCols.items()}


    def __init__(self,startSq,endSq,board, enpassant=False,castle=False):
        self.startSq=startSq
        self.endSq=endSq
        self.pieceSelected = board[startSq[0]][startSq[1]]
        self.pieceMoved = board[endSq[0]][endSq[1]]
        #unique hash foe every move
        self.moveID = self.startSq[0]*1000+self.startSq[1]*100+self.endSq[0]*10+self.endSq[1]
        #pawn promorion
        self.isPawnPromotion=False
        if (self.pieceSelected=="wp" and self.endSq[0]==0) or (self.pieceSelected=="bp" and self.endSq[0]==7):
            self.isPawnPromotion=True
        #enpassant
        self.enpassant=enpassant
        if enpassant:
            self.pieceMoved="wp" if self.pieceSelected=="bp" else "bp"

        self.castle=castle


    #Overriding equals class (like isEquals() class in java)
    def __eq__(self, other):
        if isinstance(other,Move):
            return self.moveID==other.moveID


    def getChessNotation(self):
        return self.getRankFile(self.startSq[0],self.startSq[1]) + self.getRankFile(self.endSq[0],self.endSq[1])

    def getRankFile(self,r,c):
        return self.colsToFiles[c] + self.rowsToRanks[r]

    def toString(self):
        return str(self.startSq)+" ("+str(self.pieceSelected)+")--("+str(self.pieceMoved)+") "+str(self.endSq)








