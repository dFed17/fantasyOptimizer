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

def calcWeeklyWins(player1, player2):
    score1 = calcFantasyScorePositional(player1)
    score2 = calcFantasyScorePositional(player2)




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



class optiPlayer:
    name = ''

def makeWineMatrixAlt(players):

    db = nfldb.connect()

    # Get number of players in list
    size = len(players)
    playerInd = {}
    playerIndString = {}

    ind = 0
    allWins = []
    allLoses = []

    print '\n index\tname'
    for i, x in enumerate(players):
        x = x.split(' (')
        print str(ind) + '\t' + x[0]
        playerIndString[i] = x[0]


    for i, x in enumerate(playerIndString):
        for week in range(1,8):

            qd = nfldb.Query(db)
            qd.game(season_year=2015, week=week, season_type='Regular')

            # Get the player for which to calculate a row
            # Must get every week
            pp = qd.player( full_name=x.getValue() ).as_aggregate()
            for x in pp:
                    playerOut = x

            for x in playerIndString:
                qd2 = nfldb.Query(db)
                qd2.game(season_year=2015, week=week, season_type='Regular')
                print x
                pp2 = qd.player( full_name=x.getValue() ).as_aggregate()

                for x in pp2:
                    playerIn= x
                


                ind += 1

            xcord = 0


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


    for i in range(0, size-1):

        for j in range(i+1, size-1):
            pass
        pass




    return matrixWins, matrixLoses





def getB(wins, loses):


    invL = inv(numpy.matrix(loses))

    B = numpy.linalg.solve(numpy.matrix(loses), numpy.matrix(wins))

    print '\n + ---------- B Matrix----------'
    print(B)

    eVals, eVecs = eig(B)
    print '\n + ---------- Eigenvalues ----------'
    print eVals

    fairBets = eVecs[:,1]
    count = 0
    for w in eVals:
        if w > 0:
            print count
            print "Found fairbets"
            fairBets =  eVecs[:,count]
        count+=1

    print '\n + ---------- fairBets ----------'

    print fairBets
    return B