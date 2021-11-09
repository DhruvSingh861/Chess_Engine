#responsible for taking user input
#graphic related things

import pygame as p
from Chess import ChessEngine, AIBestMove

#p.init() can also initialize here if we want to load pices or anything before loading main
WIDTH = HEIGHT = 656
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS= 15
#eg. saying IMAGES["wK"] return white king.
IMAGES={}


#initialize global dictionary of Images
def loadImages():
    pieces=["wp","wR","wN","wB","wQ","wK","bp","bR","bN","bB","bQ","bK"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))


#Main Driver
def main():
    p.init()
    screen = p.display.set_mode((WIDTH,HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color('white'))
    gs = ChessEngine.GameState()
    global pawnPromotion
    pawnPromotion = False
    validMoves=gs.getValidMoves()
    moveMade = False
    animationFlag=False #flag for animation
    global gameOver
    gameOver=False
    global pawnPromotionType
    pawnPromotionType = ""

    #----------------------------------------------------
    #False if AI is playing else True
    playerOne=True #white
    playerTwo=False #black
    #----------------------------------------------------

    print(gs.board)
    loadImages() #only once
    running =True

    sqSelected = ()
    playerClicks = []
    Choice=False
    while running:
        humanTurn =(gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            #Mouse Events
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver and humanTurn and not pawnPromotion:
                    #get (x,y) where mouse is clicked
                    location = p.mouse.get_pos()
                    #getting indexes i and j from x and y
                    col = location[0]//SQ_SIZE  #x-axis decides column
                    row = location[1]//SQ_SIZE  #y-axis decides row
                    if sqSelected == (row, col):
                        sqSelected=()
                        playerClicks=[]
                    else:
                        sqSelected=(row,col)
                        playerClicks.append(sqSelected)
                    if len(playerClicks)==2:
                        move = ChessEngine.Move(playerClicks[0],playerClicks[1],gs.board)
                        print(move.getChessNotation()+" - "+str(move.moveID))
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                if move.isPawnPromotion:
                                    pawnPromotion=True
                                    print("draw SCREEEEEENNNNNNNNNnnn")
                                #while pawnPromotion:
                                if not pawnPromotion:
                                    gs.makeMove(validMoves[i],pawnPromotionType)
                                    moveMade =True
                                    animationFlag=True
                                    sqSelected=()
                                    playerClicks=[]
                        if not moveMade:
                            playerClicks=[sqSelected]
            #handler for Undo
            #undo when pressed (ctrl+z)
            elif e.type==p.KEYDOWN:
                if len(gs.moveLog)!=0 and e.key == p.K_z and p.key.get_mods() & p.KMOD_CTRL:
                    gs.undoMove()
                    moveMade=True
                    animationFlag=False
                    pawnPromotion=False
                if e.key==p.K_r: #Reset game
                    gs = ChessEngine.GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    animationFlag = False
                    gameOver = False

        #-------AI--Logic-------------------------------
        if not gameOver and not humanTurn:
            AIMove = AIBestMove.minMaxStarter(gs,validMoves)
            if AIMove==None:
                AIMove = AIBestMove.findRandomMoves(validMoves)
            gs.makeMove(AIMove,"Q")
            moveMade=True
            animationFlag=True
        #-----------------------------------------------

        if moveMade:
            if animationFlag:
                animation(gs.moveLog[-1],screen,gs.board,clock)
            validMoves=gs.getValidMoves()
            moveMade=False


        drawGameState(screen,gs,sqSelected,validMoves,pawnPromotion)
        if pawnPromotion:
            gameOver=True
            x,y,z=choosePawnPromotion(gs, screen,move,moveMade,animationFlag,sqSelected)
            moveMade, animationFlag, sqSelected=x,y,z
            gameOver=False

        if gs.checkMate:
            gameOver=True
            if gs.whiteToMove:
                drawText(screen,"Black Wins!! CHECKMATE")
            else:
                drawText(screen, "White Wins!! CHECKMATE")
        elif gs.staleMate:
            gameOver=True
            drawText(screen,"STALEMATE")

        clock.tick(MAX_FPS)
        p.display.flip()

def choosePawnPromotion(gs,screen,move,moveMade,animationFlag,sqSelected):
        global pawnPromotionType, pawnPromotion
        pawnPromotion=True
        s = p.Surface((WIDTH, HEIGHT))
        s.set_alpha(100)
        s.fill(p.Color("white"))
        screen.blit(s, (0, 0))
        s = p.Surface((WIDTH/2, HEIGHT/2))
        pawnPromotionType=""
        s.set_alpha(150)
        s.fill(p.Color("blue"))
        Loc = p.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH / 2 - s.get_width() / 2,
                                                   HEIGHT / 2 - s.get_height() / 2)
        screen.blit(s, Loc)
        if gs.whiteToMove:
            ally="w"
        else:
            ally="b"
        img=p.transform.scale(p.image.load("images/" +ally+ "Q" + ".png"), (s.get_width()//2, s.get_width()//2))
        screen.blit(img, p.Rect( 2 * SQ_SIZE, 2 * SQ_SIZE, s.get_width(), s.get_height()))
        img = p.transform.scale(p.image.load("images/" +ally+ "R" + ".png"), (s.get_width() // 2, s.get_width() // 2))
        screen.blit(img, p.Rect(2 * SQ_SIZE, 4 * SQ_SIZE, s.get_width(), s.get_height()))
        img = p.transform.scale(p.image.load("images/" +ally+ "B" + ".png"), (s.get_width() // 2, s.get_width() // 2))
        screen.blit(img, p.Rect(4 * SQ_SIZE, 2 * SQ_SIZE, s.get_width(), s.get_height()))
        img = p.transform.scale(p.image.load("images/" +ally+ "N" + ".png"), (s.get_width() // 2, s.get_width() // 2))
        screen.blit(img, p.Rect(4 * SQ_SIZE, 4 * SQ_SIZE, s.get_width(), s.get_height()))
        for e in p.event.get():
            if e.type==p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                # getting indexes i and j from x and y
                col = location[0] // SQ_SIZE  # x-axis decides column
                row = location[1] // SQ_SIZE  # y-axis decides row
                if 1<row<4 and 1<col<4:
                    print("Queen")
                    pawnPromotionType = "Q"
                    gs.makeMove(move, pawnPromotionType)
                    moveMade = True
                    animationFlag = True
                    sqSelected = ()
                    playerClicks = []
                    pawnPromotion = False
                    close=True
                elif 1<row<4 and 3<col<6:
                    print("Bishop")
                    pawnPromotionType = "B"
                    gs.makeMove(move, pawnPromotionType)
                    moveMade = True
                    animationFlag = True
                    sqSelected = ()
                    playerClicks = []
                    pawnPromotion = False
                    close = True
                elif 3 < row < 6 and 1<col<4:
                    print("Rook")
                    pawnPromotionType = "R"
                    gs.makeMove(move, pawnPromotionType)
                    moveMade = True
                    animationFlag = True
                    sqSelected = ()
                    playerClicks = []
                    pawnPromotion = False
                    close = True
                elif 3 < row < 6 and 3<col<6:
                    print("Knight")
                    pawnPromotionType = "N"
                    gs.makeMove(move, pawnPromotionType)
                    moveMade = True
                    animationFlag = True
                    sqSelected = ()
                    playerClicks = []
                    pawnPromotion = False
                    close = True
        return moveMade,animationFlag,sqSelected

#==========================================================================================================
def drawYellow(screen,gs,sqSelected,validMoves):
    if sqSelected!=():
        i,j=sqSelected
        if (gs.board[i][j][0]=="w" and gs.whiteToMove) or (gs.board[i][j][0]=="b" and not gs.whiteToMove):
            s=p.Surface((SQ_SIZE,SQ_SIZE))
            s.set_alpha(100)
            s.fill(p.Color("blue"))
            screen.blit(s,(j*SQ_SIZE,i*SQ_SIZE))
            s.set_alpha(180)
            s.fill(p.Color("yellow"))
    for mo in validMoves:
        if sqSelected == mo.startSq:
            #print(mo.endSq)
            screen.blit(s, (mo.endSq[1]*SQ_SIZE,mo.endSq[0]*SQ_SIZE))
            #p.draw.rect(screen,p.Color("yellow"),p.Rect(mo.endSq[1]*SQ_SIZE,mo.endSq[0]*SQ_SIZE, SQ_SIZE, SQ_SIZE))
#==========================================================================================================


def drawGameState(screen,gs,sqSelected,validMoves,pawnPromotion):
    #draw squares on board
    drawBoard(screen)
    #king in check?
    drawCheck(screen,gs)
    #yellow
    if not pawnPromotion:
        drawYellow(screen,gs,sqSelected,validMoves)
    #pieces on board
    drawPieces(screen, gs.board)

def drawBoard(screen):
    global colors
    colors=[p.Color("#f0f0f0"), p.Color('#6da151')]
    for i in range(DIMENSION):
        for j in range(DIMENSION):
            color = colors[((i+j)%2)]
            p.draw.rect(screen,color,p.Rect(j*SQ_SIZE, i*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawCheck(screen,gs):
    if gs.inCheck:
        if gs.whiteToMove:
            p.draw.rect(screen, "red", p.Rect(gs.whiteKingLocation[1]*SQ_SIZE,gs.whiteKingLocation[0]*SQ_SIZE,SQ_SIZE,SQ_SIZE))
        else:
            p.draw.rect(screen,"red",p.Rect(gs.blackKingLocation[1]*SQ_SIZE,gs.blackKingLocation[0]*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawPieces(screen,board):
    for i in range(DIMENSION):
        for j in range(DIMENSION):
            piece = board[i][j]
            if piece != "--":
                screen.blit(IMAGES[piece],p.Rect(j*SQ_SIZE, i*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def animation(move,screen,board,clock):
    global colors
    dR=move.endSq[0]-move.startSq[0]
    dC=move.endSq[1]-move.startSq[1]
    framePerBlock=5
    frameCount=framePerBlock*(abs(dR)+abs(dC))
    for frame in range(frameCount+1):
        r,c = (move.startSq[0]+ dR*frame/frameCount, move.startSq[1]+ dC*frame/frameCount)
        drawBoard(screen)
        drawPieces(screen,board)

        #erase piece from end square on board
        color=colors[(move.endSq[0]+move.endSq[1])%2]
        endSquare=p.Rect(move.endSq[1]*SQ_SIZE,move.endSq[0]*SQ_SIZE,SQ_SIZE,SQ_SIZE)
        p.draw.rect(screen,color,endSquare)

        #dwaw enemy piece onto square again
        if move.pieceMoved!="--":
            if move.enpassant:
                enpassantRow=(move.endSq[0]+1) if move.pieceMoved[0]=="b" else (move.endSq[0]-1)
                endSquare = p.Rect(move.endSq[1] * SQ_SIZE, enpassantRow * SQ_SIZE, SQ_SIZE, SQ_SIZE)
            screen.blit(IMAGES[move.pieceMoved],endSquare)

        #moving piece drawn
        screen.blit(IMAGES[move.pieceSelected], p.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE))
        p.display.flip()
        clock.tick(60)

def drawText(screen,text):
    font=p.font.SysFont("Helvitca",52,True,False)
    #textObj=font.render(text,0,p.Color("Black"))
    s = p.Surface((WIDTH, HEIGHT))
    s.set_alpha(100)
    s.fill(p.Color("white"))
    screen.blit(s, (0, 0))
    textObj=font.render(text,0,p.Color("black"))
    textLoc = p.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH / 2 - textObj.get_width() / 2,
                                               HEIGHT / 2 - textObj.get_height() / 2)
    screen.blit(textObj,textLoc.move(2,2))



if __name__ == "__main__":
    main()






