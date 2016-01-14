import nfldb
import functions


START_WEEK = 1
END_WEEK = 10
def main():


    rb = functions.getRB()
    qb = functions.getQB()
    wr = functions.getWR()
    te = functions.getTE()

    wMatrixRB, lMatrixRB = functions.makeWinMatrix(rb)
    rbB = functions.getB(wMatrixRB, lMatrixRB)
    wMatrixQB, lMatrixQB = functions.makeWinMatrix(qb)
    qbB = functions.getB(wMatrixRB, lMatrixRB)
    wMatrixWR, lMatrixWR  = functions.makeWinMatrix(wr)
    wrB = functions.getB(wMatrixRB, lMatrixRB)
    wMatrixTE, lMatrixTE = functions.makeWinMatrix(te)
    teB = functions.getB(wMatrixRB, lMatrixRB)

    wMatrixRB_weekly, lMatrixRB_weekly = functions.getWeeklyMatrix(rb, START_WEEK, END_WEEK)
    functions.checkInvariantsFull(wMatrixRB_weekly, lMatrixRB_weekly)
    rbB = functions.getB(wMatrixRB_weekly, lMatrixRB_weekly)

    wMatrixQB_weekly, lMatrixQB_weekly = functions.getWeeklyMatrix(qb, START_WEEK, END_WEEK)
    functions.checkInvariantsFull(wMatrixQB_weekly, lMatrixQB_weekly)
    qbB = functions.getB(wMatrixQB_weekly, lMatrixQB_weekly)

    wMatrixWR_weekly, lMatrixWR_weekly = functions.getWeeklyMatrix(wr, START_WEEK, END_WEEK)
    functions.checkInvariantsFull(wMatrixWR_weekly, lMatrixWR_weekly)
    wrB = functions.getB(wMatrixWR_weekly, lMatrixWR_weekly)

    wMatrixTE_weekly, lMatrixTE_weekly = functions.getWeeklyMatrix(te, START_WEEK, END_WEEK)
    functions.checkInvariantsFull(wMatrixTE_weekly, lMatrixTE_weekly)
    teB = functions.getB(wMatrixTE_weekly, lMatrixTE_weekly)


if __name__ == "__main__":
    main()