import sys
import copy

from PyQt4 import QtGui
from PyQt4 import QtCore

import solver


class MainWindow(QtGui.QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        puzzle = solver.randPuzzle()
        self.puzzle = Puzzle(puzzle)
        self.initUI()

    def initUI(self):
        vbox = QtGui.QVBoxLayout()

        hbox = QtGui.QHBoxLayout()
        self.puzzleIn = QtGui.QLineEdit()
        hbox.addWidget(self.puzzleIn)
        loadBtn = QtGui.QPushButton('Load')

        loadBtn.clicked.connect(self.reset)
        hbox.addWidget(loadBtn)
        vbox.addLayout(hbox)

        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(self.puzzle)
        vbox.addLayout(hbox)

        hbox = QtGui.QHBoxLayout()
        solveBtn = QtGui.QPushButton('Solve')
        solveBtn.clicked.connect(self.puzzle.solve)
        hbox.addWidget(solveBtn)
        vbox.addLayout(hbox)

        self.setLayout(vbox)
        self.setWindowTitle('Sudoku Solver')
        self.setFixedSize(self.sizeHint())
        self.show()

    def reset(self):
        self.puzzle.reset(self.puzzleIn.text())


class Puzzle(QtGui.QWidget):
    def __init__(self, puzzle):
        super(Puzzle, self).__init__()

        self.start = copy.deepcopy(puzzle)
        self.solver = solver.Puzzle(puzzle)
        self.initUI()

    def initUI(self):
        self.grid = QtGui.QGridLayout()
        self.grid.setHorizontalSpacing(15)
        self.grid.setVerticalSpacing(0)

        self.display()

        self.setLayout(self.grid)
        self.show()

    def display(self):
        for i in range(self.grid.count()): self.grid.itemAt(i).widget().close()

        self.cells = []
        for y, row in enumerate(self.solver.puzzle):
            for x, cell in enumerate(row):
                self.cells.append(Cell(cell.val))
                self.grid.addWidget(
                    self.cells[-1],
                    y + int((y / 9) * 3),
                    x + int((x / 9) * 3)
                )

        for pos in range(11):
            char = '┼' if pos == 3 or pos == 7 else '│─'
            self.grid.addWidget(QtGui.QLabel(char[0]), pos, 3)
            self.grid.addWidget(QtGui.QLabel(char[0]), pos, 7)
            self.grid.addWidget(QtGui.QLabel(char[-1]), 3, pos)
            self.grid.addWidget(QtGui.QLabel(char[-1]), 7, pos)

    def solve(self):
        stuck = False
        while not self.solver.solved and not stuck:
            stuck = self.solver.frame()
            cells = [item for sublist in self.solver.puzzle for item in sublist]
            for i, guiCell in enumerate(self.cells):
                guiCell.value = cells[i].val
        if stuck:
            msg = QtGui.QMessageBox()
            msg.setText('Cannot solve puzzle.')
            msg.exec_()

    def reset(self, puzzle=None):
        if not puzzle is None:
            self.start = puzzle
        self.solver = solver.Puzzle(copy.deepcopy(self.start))
        self.display()


class Cell(QtGui.QLabel):
    def __init__(self, startValue):
        super(Cell, self).__init__('')

        self.value = startValue

    @property
    def value(self):
        return self._value if self._value is not None else ''

    @value.setter
    def value(self, value):
        if not int(value):
            self._value = None
            self.setText('')
        else:
            self._value = int(value)
            self.setNum(self.value)


def main():
    app = QtGui.QApplication(['Sudoku Solver'])
    ex = MainWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()