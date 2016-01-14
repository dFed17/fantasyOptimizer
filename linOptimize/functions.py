import nfldb
import pdb
import numpy
from numpy.linalg import inv, eig

import operator

RUSH_YDS_FACTOR = .1
RECEIVE_YDS_FACTOR = .1

FMBL_FACTOR = -2

TWO_POINT_FACTOR = 2
TD_PLAYER_FACTOR = 6


QB_YDS_FACTOR = .04
TD_QB_FACTOR = 4
QB_INT_FACTOR = -2



def printDict(dict):
    for x in dict:
        print x, dict[x]

def calcFantasyScorePositional(player):

    #General player stats ------------------
    score =  RUSH_YDS_FACTOR * player.rushing_yds
    #print player.player, player.rushing_yds

    score += RECEIVE_YDS_FACTOR * player.receiving_yds
    #print player.player, player.receiving_yds

    score += TD_PLAYER_FACTOR * player.rushing_tds
    #print player.player, player.rushing_tds

    score += TD_PLAYER_FACTOR * player.receiving_tds
    #print player.player, player.receiving_tds

    score += TWO_POINT_FACTOR * player.receiving_twoptm
    #print player.player, player.receiving_twoptm

    score += TWO_POINT_FACTOR * player.rushing_twoptm
    #print player.player, player.rushing_twoptm

    score += FMBL_FACTOR * player.fumbles_lost
    #print player.player, player.fumbles_lost


    #QB stats -------------------
    score += QB_YDS_FACTOR * player.passing_yds
    #print player.player, player.passing_yds

    score += TD_QB_FACTOR * player.passing_tds
    #print player.player, player.passing_tds

    score += TWO_POINT_FACTOR * player.passing_twoptm
    #print player.player, player.passing_twoptm


    return score

def calcWinForWeek(player1, player2):
    score1 = calcFantasyScorePositional(player1)
    score2 = calcFantasyScorePositional(player2)
    if score1 > score2:
        return True
    elif score1 == score2:
        if player1.player < player2.player:
            return True
    return False




def calcWins(player1, player2, loses):

    wins = 0
    if player1.rushing_yds > player2.rushing_yds:
        wins += 1
    elif player1.rushing_yds < player2.rushing_yds:
        loses += 1

    if player1.receiving_yds > player2.receiving_yds:
        wins += 1
    elif player1.receiving_yds < player2.receiving_yds:
        loses += 1

    if player1.rushing_tds > player2.rushing_tds:
        wins += 1
    elif player1.rushing_tds < player2.rushing_tds:
        loses += 1

    if player1.receiving_tds > player2.receiving_tds:
        wins += 1
    elif player1.receiving_tds < player2.receiving_tds:
        loses += 1

    if player1.receiving_twoptm > player2.receiving_twoptm:
        wins += 1
    elif player1.receiving_twoptm < player2.receiving_twoptm:
        loses += 1

    if player1.rushing_twoptm > player2.rushing_twoptm:
        wins += 1
    elif player1.rushing_twoptm < player2.rushing_twoptm:
        loses += 1



    if player1.passing_yds > player2.passing_yds:
        wins += 1
    elif player1.passing_yds < player2.passing_yds:
        loses += 1

    if player1.passing_tds > player2.passing_tds:
        wins += 1
    elif player1.passing_tds < player2.passing_tds:
        loses += 1

    if player1.passing_tds > player2.passing_tds:
        wins += 1
    elif player1.passing_twoptm < player2.passing_twoptm:
        loses += 1


    if player1.fumbles_lost < player2.fumbles_lost:
        wins += 1
    elif player1.fumbles_lost > player2.fumbles_lost:
        loses += 1

    return wins, loses

def getTop25(playerList):
    topPlayers = reversed(sorted(playerList.items(), key=operator.itemgetter(1)))
    top25 = {}
    count = 0
    for x in topPlayers:
        print x[0],x[1]
        top25[x[0]] = x[1]
        count += 1
        if count > 24:
            break

    return top25

def getRB():
    print "\n\n-------------------------- TOP RBs --------------------------"
    runningbacks = {}

    db = nfldb.connect()
    q = nfldb.Query(db)

    q.game(season_year=2015, season_type='Regular')

    for pp in q.sort('rushing_yds').limit(50).as_aggregate():
        if str(pp.player) not in runningbacks and str(pp.player)[-3:-1]== 'RB':
            runningbacks[str(pp.player)] = calcFantasyScorePositional(pp)

    # for player in runningbacks:
    #     print player, runningbacks.get(player)

    runningbacks = getTop25(runningbacks)
    print len(runningbacks)

    return runningbacks

def getQB():
    print "\n\n-------------------------- TOP QBs --------------------------"

    quarterbacks = {}

    db = nfldb.connect()
    q = nfldb.Query(db)

    q.game(season_year=2015, season_type='Regular')

    for pp in q.sort('passing_yds').limit(50).as_aggregate():
        if str(pp.player) not in quarterbacks and str(pp.player)[-3:-1] == 'QB':
            quarterbacks[str(pp.player)] = calcFantasyScorePositional(pp)

    # for player in quarterbacks:
    #     print player, quarterbacks.get(player)

    quarterbacks = getTop25(quarterbacks)
    print len(quarterbacks)

    return quarterbacks

def getWR():
    print "\n\n-------------------------- TOP WRs --------------------------"
    receivers = {}

    db = nfldb.connect()
    q = nfldb.Query(db)

    q.game(season_year=2015, season_type='Regular')

    for pp in q.sort('receiving_yds').limit(50).as_aggregate():
        if str(pp.player) not in receivers and str(pp.player)[-3:-1] == 'WR':
            receivers[str(pp.player)] = calcFantasyScorePositional(pp)

    # for player in receivers:
    #     print player, receivers.get(player)

    receivers = getTop25(receivers)
    print len(receivers)
    return receivers


def getTE():
    print "\n\n-------------------------- TOP TEs --------------------------"

    tightends = {}

    db = nfldb.connect()
    q = nfldb.Query(db)

    q.game(season_year=2015, season_type='Regular')

    for pp in q.sort('receiving_yds').limit(130).as_aggregate():
        if str(pp.player) not in tightends and str(pp.player)[-3:-1] == 'TE':
            tightends[str(pp.player)] = calcFantasyScorePositional(pp)

    # for player in tightends:
    #     print player, tightends.get(player)

    tightends = getTop25(tightends)
    print len(tightends)

    return tightends

def makeWinMatrix(players):

    db = nfldb.connect()

    # Get number of players in list
    size = len(players)
    playerInd = {}

    ind = 0

    print '\n index\tname'
    for x in players:
        x = x.split(' (')
        print str(ind) + '\t' + x[0]

        qd = nfldb.Query(db)
        qd.game(season_year=2015, season_type='Regular')
        pp = qd.player(full_name=x[0]).as_aggregate()
        for x in pp:
            playerInd[ind] = x
        ind += 1

    xcord = 0

    allWins = []
    allLoses = []
    while xcord < size-1:
        winsList = []
        losesList = []
        check = playerInd[xcord]
        loses = 0
        ycord = 0
        while ycord<size-1:
            losesList.append(0)
            if ycord != xcord:
                against = playerInd[ycord]
                wins, loses = calcWins(check, against, loses)
                winsList.append(wins)
            else:
                winsList.append(0)

            ycord += 1
        losesList[xcord] = loses
        rowWins = numpy.array([winsList])
        rowLoses = numpy.array([losesList])

        allWins.append(rowWins)
        allLoses.append(rowLoses)

        xcord += 1

    matrixWins = numpy.vstack(allWins)
    matrixLoses = numpy.vstack(allLoses)
    print '---------- Wins ----------'
    print(matrixWins)
    print '---------- Loses ----------'
    print(matrixLoses)

    return matrixWins, matrixLoses



def makeWinMatrixForWeek(players, week, first):
    db = nfldb.connect()

    # Get number of players in list
    size = len(players)
    playerInd = {}

    ind = 0

    if first:
        print '\n index\tname'

    for x in players:
        x = x.split(' (')
        if first:
            print str(ind) + '\t' + x[0]

        qd = nfldb.Query(db)
        qd.game(season_year=2015, week=week, season_type='Regular')
        pp = qd.player(full_name=x[0]).as_aggregate()
        for p in pp:
            playerInd[ind] = p
        ind += 1

    xcord = 0
    allWins = []
    allLoses = []

    while xcord < size:
        winsList = []
        losesList = []
        wasActive = False
        if playerInd.has_key(xcord):
            wasActive = True

        loses = 0
        ycord = 0
        while ycord < size:



            # Append a 0 for every position in the loses matrix
            # Then replace diagonal position later
            losesList.append(0)
            if ycord == xcord:
                winsList.append(0)
                # Append 0 along diagonal in wins matrix
            elif wasActive:
                # Both players played
                if playerInd.has_key(ycord):
                    check = playerInd[xcord]
                    against = playerInd[ycord]

                    if calcWinForWeek(check, against):
                        winsList.append(1)
                    else:
                        winsList.append(0)
                        loses += 1
                else:
                    # pdb.set_trace()
                    winsList.append(1)
            else:
                # pdb.set_trace()
                # Check player didn't play
                winsList.append(0)
                if playerInd.has_key(ycord):
                    # against player did play
                    loses+=1


            ycord += 1
        losesList[xcord] = loses


        # check weekly invariants
        # if winsList.count(0)-1 != loses:
        #     pdb.set_trace()

        rowWins = numpy.array([winsList])
        rowLoses = numpy.array([losesList])

        allWins.append(rowWins)
        allLoses.append(rowLoses)

        xcord += 1

    matrixWins = numpy.vstack(allWins)
    matrixLoses = numpy.vstack(allLoses)
    # print '---------- Wins ----------'
    # # print(matrixWins)
    # print '---------- Loses ----------'
    # print(matrixLoses)

    return matrixWins, matrixLoses



def getWeeklyMatrix(players, firstWeek, lastWeek):
    size = len(players)
    allWins = numpy.zeros( (size, size) )
    allLoses= numpy.zeros( (size, size) )

    first = True

    for i in range(firstWeek, lastWeek+1):
        weeklyWins, weeklyLoses = makeWinMatrixForWeek(players, i, first)
        print "calculations for WEEK " + str(i)
        first = False
        if i > 13:
            pdb.set_trace()
        checkInvariantsFull(weeklyWins, weeklyLoses)
        allWins = numpy.add( weeklyWins, allWins )
        allLoses = numpy.add( weeklyLoses, allLoses )
        # pdb.set_trace()


    print '---------- Wins ----------'
    print(allWins)
    print '---------- Loses ----------'
    print(allLoses)

    return allWins, allLoses





def getB(wins, loses):
    checkInvariantsFull(wins, loses)

    invL = inv(numpy.matrix(loses))

    B = numpy.linalg.solve(numpy.matrix(loses), numpy.matrix(wins))

    print '\n + ---------- B Matrix----------'
    print(B)

    eVals, eVecs = eig(B)
    print '\n + ---------- Eigenvalues ----------'
    print eVals

    fairBets = 'fairBets vector not found'

    count = 0
    foundFair = False
    for val in eVals:
        if val > 0:
            print count
            if foundFair == True:
                print "Too many positive eigenvalues"

            print '\n + ---------- fairBets ----------'
            fairBets =  eVecs[:,count]
            print eVecs[:,count]

            foundFair = True
        count+=1


    return B


def checkInvariantsFull(winsMatrix, losesMatrix):
    rowsW, colsW = winsMatrix.shape

    for i in range(0,colsW-1):
        col = winsMatrix[:,i]
        losesFromWins = col.sum()
        loses = losesMatrix[i, i]
        if losesFromWins != loses:
            print i
            losesMatrix[i,i] = losesFromWins

def makeMatlab(wins):
    rowsW, colsW = wins.shape
    matlabString = '['
    for i in range(0,rowsW):
        # print 'row is ' + str(i)
        for j in range(0, colsW):
            # print '\tcolumn is ' + str(j)
            matlabString = matlabString + ' ' + str(wins[i,j])
            if j == 24:
                print 'end of row'
                matlabString = matlabString + ';'
            else:
                matlabString = matlabString + ','

        if i == 24:
            print 'end of matrix'
            matlabString = matlabString + ']'


    print matlabString






