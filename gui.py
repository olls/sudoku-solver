import sys

from PyQt4 import QtGui
from PyQt4 import QtCore

import solver


class MainWindow(QtGui.QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        puzzle = solver.randPuzzle()
        self.puzzle = Puzzle(puzzle)
        self.initUI()

        self.puzzleIn.setText(puzzle)

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
        self.puzzle.reset(str(self.puzzleIn.text()))


class Puzzle(QtGui.QWidget):
    def __init__(self, puzzle):
        super(Puzzle, self).__init__()

        self.start = puzzle
        self.solver = solver.Puzzle(puzzle)
        self.initUI()

    def initUI(self):
        self.grid = QtGui.QGridLayout()
        self.grid.setHorizontalSpacing(15)
        self.grid.setVerticalSpacing(0)

        for i in range(self.grid.count()): self.grid.itemAt(i).widget().close()

        self.cells = []
        for y, row in enumerate(self.solver.puzzle):
            for x, cell in enumerate(row):
                self.cells.append(Cell(cell.val))
                self.grid.addWidget(
                    self.cells[-1],
                    y + int((float(y) / 9) * 3),
                    x + int((float(x) / 9) * 3)
                )

        # Add blank labels to make spaces between boxes.
        for pos in range(11):
            self.grid.addWidget(QtGui.QLabel(' '), pos, 3)
            self.grid.addWidget(QtGui.QLabel(' '), pos, 7)
            self.grid.addWidget(QtGui.QLabel(' '), 3, pos)
            self.grid.addWidget(QtGui.QLabel(' '), 7, pos)

        self.setLayout(self.grid)
        self.show()

    def paintEvent(self, event):
        qp = QtGui.QPainter()
        qp.begin(self)

        pen = QtGui.QPen(QtCore.Qt.black, 2, QtCore.Qt.SolidLine)
        qp.setPen(pen)
        qp.drawLine((self.width() / 3),     0, (self.width() / 3),      self.height())
        qp.drawLine((self.width() / 3) * 2, 0, (self.width() / 3) * 2,  self.height())
        qp.drawLine(0,  (self.height() / 3),        self.width(), (self.height() / 3))
        qp.drawLine(0,  (self.height() / 3) * 2,    self.width(), (self.height() / 3) * 2)

        qp.end()

    def solve(self):
        stuck = False
        while not self.solver.solved and not stuck:
            stuck = self.solver.frame()

            self.update()

        if stuck:
            msg = QtGui.QMessageBox()
            msg.setText('Cannot solve puzzle.')
            msg.exec_()

    def update(self, new=False):
        # Flatten list
        cells = [item for sublist in self.solver.puzzle for item in sublist]

        for i, guiCell in enumerate(self.cells):
            if new:
                guiCell.set = bool(cells[i].val)
            guiCell.value = cells[i].val

    def reset(self, puzzle=None):
        if puzzle:
            self.start = puzzle

        self.solver = solver.Puzzle(self.start)
        self.update(new=True)

class Cell(QtGui.QLabel):
    def __init__(self, startValue):
        super(Cell, self).__init__('')

        self.set = bool(startValue)
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
            if self.set:
                self.setText('<b>' + str(self.value) + '</b>')
            else:
                self.setText(str(self.value))


def main():
    app = QtGui.QApplication(['Sudoku Solver'])
    ex = MainWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()