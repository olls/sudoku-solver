import sys

from PyQt4 import QtGui
from PyQt4 import QtCore

import solver


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        puzzle = solver.randPuzzle()
        self.puzzle = Puzzle(puzzle)
        self.initUI()

    def initUI(self):
        self.setCentralWidget(self.puzzle)

        self.show()


class Puzzle(QtGui.QWidget):
    def __init__(self, puzzle):
        super(Puzzle, self).__init__()

        self.solver = solver.Puzzle(puzzle)
        self.initUI()

    def initUI(self):
        self.grid = QtGui.QGridLayout()
        self.grid.setHorizontalSpacing(15)
        self.grid.setVerticalSpacing(0)

        solveBtn = QtGui.QPushButton('Solve')
        solveBtn.clicked.connect(self.solve)
        self.grid.addWidget(solveBtn, 12, 0, 1, 11)

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

        self.setLayout(self.grid)
        self.show()

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
    app = QtGui.QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()