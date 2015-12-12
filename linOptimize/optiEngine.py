import nfldb
import functions



def main():

    rb = functions.getRB()
    # qb = functions.getQB()
    # wr = functions.getWR()
    # te = functions.getTE()

    wMatrixRB, lMatrixRB = functions.makeWinMatrix(rb)
    rbB = functions.getB(wMatrixRB, lMatrixRB)
    # wMatrixQB, lMatrixQB = functions.makeWinMatrix(qb)
    # qbB = functions.getB(wMatrixRB, lMatrixRB)
    # wMatrixWR, lMatrixWR  = functions.makeWinMatrix(wr)
    # wrB = functions.getB(wMatrixRB, lMatrixRB)
    # wMatrixTE, lMatrixTE = functions.makeWinMatrix(te)
    # teB = functions.getB(wMatrixRB, lMatrixRB)

    # print '\n'
    # print matrixRB
    # print '\n'
    # print matrixQB
    # print '\n'
    # print matrixWR
    # print '\n'
    # print matrixTE
    # print '\n'




if __name__ == "__main__":
    main()