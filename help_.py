import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtWebKit import QWebView
import markdown
import codecs


class Win(QtGui.QMainWindow):

    def __init__(self, text, style):
        super(Win, self).__init__()

        with open(style) as f:
            style = f.read()

        with open(text) as f:
            mrkDn = f.read()
        html = markdown.markdown(mrkDn)

        self.html = (
            '<!DOCTYPE html>\n\n'
            '<html>\n'
            '\t<head>\n'
            '\t\t<title>Help</title>\n'
            '\t\t<style>\n\n'
        ) + style + (
            '\n\n\t</style>\n'
            '\t</head>\n'
            '\t<body>\n\n'
        ) + html + (
            '\n\n\t</body>\n'
            '</html>\n'
        )

        self.initUI()

    def initUI(self):
        view = QWebView()
        view.setHtml(self.html)

        self.setCentralWidget(view)
        self.resize(450, 550)
        self.setWindowTitle('Help')


def main():
    app = QtGui.QApplication(sys.argv)
    win = Win('help.md', 'help.css')
    win.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
