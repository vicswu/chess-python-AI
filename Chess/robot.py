import random

piecePoint = {"K": 0, "Q": 9, "R": 5, "B": 3, "N": 3, "p": 1}
checkmatePoint = 1000
stalematePoint = 0
maxDepth = 2

class Robot():

    def findRandomMove(validMoves):
        return validMoves[random.randint(0, len(validMoves)-1)] 

    def findBestMove(gs, validMoves):
        turnMultiplier = 1 if gs.whiteToMove else -1
        opponentMinMaxPoint = checkmatePoint
        bestPlayerMove = None
        random.shuffle(validMoves)
        for playerMove in validMoves:
            gs.makeMove(playerMove)
            opponentsMoves = gs.getValidMoves()
            if gs.isStalemate:
                opponentMaxPoint = stalematePoint
            elif gs.isCheckmate:
                opponentMaxPoint = -checkmatePoint
            else:
                opponentMaxPoint = -checkmatePoint
                for opponentsMove in opponentsMoves:
                    gs.makeMove(opponentsMove)
                    gs.getValidMoves()
                    if gs.isCheckmate:
                        point = checkmatePoint
                    elif gs.isStalemate:
                        point = stalematePoint
                    else:
                        point = -turnMultiplier*pointMaterial(gs.board)
                    if point > opponentMaxPoint:
                        opponentMaxPoint = point
                    gs.undoMove()
            if opponentMaxPoint < opponentMinMaxPoint:
                opponentMinMaxPoint = opponentMaxPoint
                bestPlayerMove = playerMove
            gs.undoMove()
        return bestPlayerMove

    def findBestMoveMinMax(gs, validMoves):
        global nextMove
        nextMove = None
        findMoveMinMax(gs, validMoves, maxDepth, gs.whiteToMove)
        return nextMove

def pointMaterial(board):
    point = 0
    for row in board:
        for square in row:
            if square[0] == "w":
                point += piecePoint[square[1]]
            elif square[0] == "b":
                point -= piecePoint[square[1]]
    return point 

def pointBoard(gs):
    if gs.isCheckmate:
        if gs.whiteToMove:
            return -checkmatePoint
        else:
            return checkmatePoint
    elif gs.isStalemate:
        return stalematePoint
    point = 0
    for row in gs.board:
        for square in row:
            if square[0] == "w":
                point += piecePoint[square[1]]
            elif square[0] == "b":
                point -= piecePoint[square[1]]
    return point 

def findMoveMinMax(gs, validMoves, depth, whiteToMove):
    global nextMove
    if depth == 0:
        return pointMaterial(gs.board)
    if whiteToMove:
        maxPoint = -checkmatePoint
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            point = findMoveMinMax(gs, nextMoves, depth-1, not whiteToMove)
            if point > maxPoint:
                maxPoint = point
                if depth == maxDepth:
                    nextMove = move
            gs.undoMove()
        return maxPoint
    else:
        minPoint = checkmatePoint
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            point = findMoveMinMax(gs, nextMoves, depth-1, not whiteToMove)
            if point < minPoint:
                minPoint = point
                if depth == maxDepth:
                    nextMove = move
            gs.undoMove()
        return minPoint