from time import sleep
import ai
import time
import graphics
from graphics import Point
import model

#Window settings
width = 500
height = 500
offset_x = width / 8
offset_y = height / 8
win = graphics.GraphWin("Checkers", width, height)

#Difficulty means how deep do you want the algorithms to go
ai.DIFFICULTY = 2
print("Current AI Difficulty/Depth Level: "+ str(ai.DIFFICULTY))
print()
print()


#Run a tally of which algorithm is chosen.
chosen_minimax = 0
chosen_alpha_beta = 0
move = 1


def drawBoard():
    color_offset = False
    for x in range(0, 8):
        if x % 2 == 1:
            color_offset = True
        else:
            color_offset = False
        for y in range(0, 8):
            point = Point(x * offset_x, y * offset_y)
            box = graphics.Rectangle(point, Point(point.x + offset_x, point.y + offset_y))
            box.setFill("Gray")
            if color_offset:
                if x % 2 == 0 or y % 2 == 0:
                    box.setFill("#c2ab56")
            elif x % 2 == 1 or y % 2 == 1:
                box.setFill("#c2ab56")
            box.draw(win)


def drawCheckers():
    for piece in model.board.flat:
        if piece.checker is not None:
            circle = graphics.Circle(Point(piece.center[0], piece.center[1]), 15)
            if piece.checker.black:
                circle.setFill("Black")
            else:
                circle.setFill("White")
            circle.draw(win)


def findPiece(click):
    click_x = click.x/62.5
    click_y = click.y/62.5
    for x in range(0, 8):
        for y in range(0, 8):
            if (click_x > x and click_y > y) and (click_x < x+1 and click_y < y+1):
                return (x, y)
    return None





def redraw():
    for child in win.children:
        child.undraw()
    drawBoard()
    drawCheckers()


def runAI(color):
    global chosen_minimax
    global chosen_alpha_beta
    global move
    print()
    print("MOVE "+ str(move))
    print("----------------------------------------------------")

    #MODIFY HERE TO SWITCH ALGORITHMS
    #Alpha-beta pruning
    t1 = time.time()
    ai_move_alpha_beta = ai.minimax_alpha_beta(0, color, model.board, float("-inf"), float("inf"))
    print("Current weight of the board using Alpha-Beta: " + str(ai_move_alpha_beta.weight))
    t2 = time.time()
    print("Time taken to calculate the move using Alpha-Beta:" + str(t2-t1))

    #Regular
    # t3 = time.time()
    # ai_move_minimax = ai.minimax(0, color, model.board)
    # print("Current weight of the board using Regular: " + str(ai_move_minimax.weight))
    # t4 = time.time()
    # print("Time taken to calculate the move using Regular:" + str(t4-t3))

    #model.ttable.save()
    model.ttable.hashtable = {}


    #MODIFY HERE TO SWITCH ALGORITHMS
    #ai_move = ai_move_minimax
    ai_move = ai_move_alpha_beta
    ai_move.apply(model.board)
    redraw()

    move += 1
    return ai_move


# def chooseDif():
#     difwin = graphics.GraphWin("Choose Difficulty")
#     difwin.focus()
#     entry = graphics.Entry(Point(100, 100), 20)
#     entry.setText("2")
#     entry.draw(difwin)
#     difwin.getMouse()
#     ai.DIFFICULTY = int(entry.getText())
#     difwin.close()


def playerTurn(color):
    while True:
        click1 = win.getMouse()
        checker = findPiece(click1)
        if checker is None or model.board[int(checker[0]), int(checker[1])].checker is None or model.board[int(checker[0]), int(checker[1])].checker.black is not color:
            continue
        click2 = win.getMouse()
        piece = findPiece(click2)
        if piece is None or (piece[0] == checker[0] and piece[1] == checker[1]):
            continue
        partial_move = ai.Move(model.board[int(checker[0]), int(checker[1])].checker, model.board[int(piece[0]), int(piece[1])],"?")
        partial_move.checker.x = checker[0]
        partial_move.checker.y = checker[1]
        move = model.getFullMove(partial_move)
        if move is None:
            continue
        else:
            move.apply(model.board)
            redraw()
            return

def draw():
    drawBoard()
    drawCheckers()
    while model.hasWon(model.board) == 0:
        sleep(0.01)
        model.King(model.board)
        #playerTurn(False)
        runAI(False)
        model.King(model.board)
        win.update()
        runAI(True)
    winWindow = graphics.GraphWin("Game over")
    if model.hasWon(model.board) == 1:
        text = graphics.Text(Point(winWindow.width/2, winWindow.height/2), "You Won!!")
        text.draw(winWindow)
        sleep(3)
    elif model.hasWon(model.board) == -1:
        text = graphics.Text(Point(winWindow.width / 2, winWindow.height / 2), "You Lost :(")
        text.draw(winWindow)
        sleep(3)
    return




