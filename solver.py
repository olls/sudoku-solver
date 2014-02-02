import sys
import time
import copy
import random


class Puzzle(object):
    def __init__(self, puzzle):

        puzzle = ''.join(['0' if i == '.' else i for i in puzzle])

        #                    Number,    (y pos, xpos)
        puzzle = [Cell(puzzle[i], (int(i / 9), i % 9)) for i in range(81)]
        # Split puzzle into rows.
        self.puzzle = [puzzle[:9], puzzle[9:18], puzzle[18:27],
                       puzzle[27:36], puzzle[36:45], puzzle[45:54],
                       puzzle[54:63], puzzle[63:72], puzzle[72:81]]

        self.lastframe = None

    def __str__(self):
        out = '\n'
        for y, row in enumerate(self.puzzle):
            for x, cell in enumerate(row):
                if x % 3 == 0:
                    out += '| '
                out += str(cell) + ' '
            if (y + 1) % 3 == 0:
                out += '\n' + ('-' * 24)
            out += '\n'
        return out[:-1]  # To get rid of final linebreak

    @property
    def solved(self):
        """ Returns True if all the cells are solved. """
        solved = True
        for row in self.puzzle:
            for cell in row:
                if not cell.solved:
                    solved = False
        return solved

    def stuck(self):
        """
            Returns True if the lastframe is the same as the current puzzle.
        """
        same = True
        for y in range(len(self.puzzle)):
            for x in range(len(self.puzzle[y])):
                if not self.puzzle[y][x].val == self.lastframe[y][x].val:
                    same = False
        return same

    def frame(self):
        """ Does a pass on the puzzle removing conflicts for each cell """

        self.lastframe = copy.deepcopy(self.puzzle)

        for y, row in enumerate(self.puzzle):
            for x, cell in enumerate(row):
                if not cell.solved:
                    cell.removeConflicts(self.puzzle)

        # If nothing changed, then stuck.
        return self.stuck()


class Cell(object):
    def __init__(self, num, pos):
        self.num = int(num)
        if self.num == 0:
            self.candidates = [i for i in range(1, 10)]
        else:
            self.candidates = [num]
        self.pos = pos

    def __str__(self):
        if self.num == 0:
            return ' '
        else:
            return str(self.num)

    @property
    def val(self):
        if self.num == 0:
            return False
        else:
            return self.num

    @property
    def cands(self):
        return self.candidates

    @property
    def solved(self):
        if len(self.candidates) == 1:
            return True
        else:
            return False

    def removeConflicts(self, puzzle):
        # Check all solved cells in our row for confilcts.
        for x, cell in enumerate(puzzle[self.pos[0]]):
            if cell.solved:
                # Check all of our candidates against the cell.
                for candidate in self.candidates:
                    if cell.val == candidate:
                        # If cell conflicts with one of our candidates, remove
                        #   candidate.
                        self.candidates.remove(candidate)

        # Check all solved cells in our column for conflicts.
        for y, row in enumerate(puzzle):
            cell = row[self.pos[1]]

            if cell.solved:
                # Check all of our candidates against the cell.
                for candidate in self.candidates:
                    if cell.val == candidate:
                        # If cell conflicts with one of our candidates, remove
                        #   candidate.
                        self.candidates.remove(candidate)

        # Get coords of top left cell in box of our cell.
        boxY = int(self.pos[0] / 3) * 3
        boxX = int(self.pos[1] / 3) * 3
        # Check all solved cells in our box for conflicts.
        for y in range(3):
            for x in range(3):
                cell = puzzle[y + boxY][x + boxX]
                if cell.solved:
                    # Check all of our candidates against the cell.
                    for candidate in self.candidates:
                        if cell.val == candidate:
                            # If cell conflicts with one of our candidates,
                            #   remove candidate.
                            self.candidates.remove(candidate)

        # If only one candidate, set us as solved.
        # Naked Candidate
        if self.solved:
            self.num = self.candidates[0]

        # If only cell in row or column or box with a particular candidate,
        #   set us solved.
        # Hidden Candidate

        # Check row, column, box for other cells with our candidates.
        for candidate in self.candidates:
            # 'only' gets set to false if any other cells in row, column,
            #   box contain this candidate.

            only = True
            # Check row for other cells with candidate.
            for x, cell in enumerate(puzzle[self.pos[0]]):
                # If it has our candidate and it isn't us, not solved
                if candidate in cell.cands and not cell.pos == self.pos:
                    only = False
            if only:
                self.candidates = [candidate]
                self.num = self.candidates[0]

            only = True
            # Check column for other cells with candidate.
            for y, row in enumerate(puzzle):
                cell = row[self.pos[1]]
                # If it has our candidate and it isn't us, not solved
                if candidate in cell.cands and not cell.pos == self.pos:
                    only = False
            if only:
                self.candidates = [candidate]
                self.num = self.candidates[0]

            only = True
            boxY = int(self.pos[0] / 3) * 3
            boxX = int(self.pos[1] / 3) * 3
            # Check box for other cells with candidate.
            for y in range(3):
                for x in range(3):
                    cell = puzzle[y + boxY][x + boxX]
                    # If it has our candidate and it isn't us, not solved
                    if candidate in cell.cands and not cell.pos == self.pos:
                        only = False
            if only:
                self.candidates = [candidate]
                self.num = self.candidates[0]


def randPuzzle():
    """ From http://magictour.free.fr/msk_009 """

    with open('puzzles.sdm') as afile:
        line = next(afile)
        for num, aline in enumerate(afile):
            if random.randrange(num + 2): continue
            line = aline
        return line

    # If above fails.
    return random.choice([
        '000508060000700010000021970060000002009147800500000090014370000070002000020805000', # Mild s
        '007600002040010000850007040006051000083000760000360200070400059000020080900003400', # Mild s
        '000801003000020401004000070010200040000030000050008060020000500407060000800903000', # Modest s
        '290000040013600070600009000000070001000408000500090000000500007030001980080000012', # Mean n
        '150000000002000000004360007006024050000050000030190800700016400000000300000000018', # Maniac n
        '000080000001706800060502030047000310100000006085000720030901040009803200000050000', # Nightmare n
        '065000008700860400000020009040001002000207000300500070400050000001079003900000260', # n
        '000070940000090005300005070007400100463000000000007080800000000700000028050260000', # n
        '000000010400000000020000000000050407008000300001090000300400200050100000000806000', # s
        '000386005002100700590020000081000000060000000000008000000005000600000308000400017', # n
        '000409670000076900000000003000001740640000018021600000100000000004320000062904000', # n
        '218439675400076902006002403000201746640000128021640009100060294004320061062914007', # n
        '000000000000003085001020000000507000004000100090000000500000073002010000000040009', # n
        '050000000000040003010092600000024080007000060400810700001407056005080094000000800', # s
        '000070506060000000000000020000000000080200000000050307001900080705000090300000000', # n
        '245139786389267451671845932793452618164783529528916374432678195817594263956321840', # s
        '018209006300000915504030087007942060023708009900015024041000570800500001030670400', # s
        '007600500000300700450000080000000020605803000009000051000009000020005100300200600', # s
        '000001000200000409000307108083000007000092000000038040408000920070000500001804000', # s
        '000021600003078500904000070008300000400009000100004208000000004640010020000005083', # s
        '000080010070000000930000000060900300001050040000000000002700000000003000004000051', # 17 L2 n
        '000150320000000050408009000000008004000000000023000000800005000000000000037200010' # 18 L1 s
    ])


def main():
    try:
        if sys.argv[1] == '-t':
            step = False
            time_ = True
        elif sys.argv[1] == '-s':
            step = True
            time_ = False
    except:  # If arg doesn't exist, don't step, or time.
        step = False
        time_ = False


    puzzle = Puzzle(randPuzzle())

    print(puzzle)
    stuck = False

    start = time.time()
    while not puzzle.solved and not stuck:
        stuck = puzzle.frame()
        if step:
            raw_input()
        elif not time_:
            time.sleep(.1)
        if not time_:
            print(puzzle)
    end = time.time()

    if time_:
        print(puzzle)
    if stuck:
        print('Can not solve any further.')
    else:
        print('Finished in ' + str(round((end - start), 5)) + 's.')
        return end - start

if __name__ == '__main__':
    main()
