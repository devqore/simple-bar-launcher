import sys
import signal
import pathlib

from PySide6 import QtCore, QtWidgets
from Xlib import display

from button import Button
from config import Config

# fix ctrl+c
signal.signal(signal.SIGINT, signal.SIG_DFL)

try:  # temporary, needs to be fixed to use system themes
    import qdarktheme
except ImportError:
    qdarktheme = None

try:
    config = Config()
except EnvironmentError as err:
    print(err)
    sys.exit(1)

sys.path.append(pathlib.Path(__file__).parent)


class MyWidget(QtWidgets.QWidget):
    hidden = False

    def __init__(self):
        super().__init__()
        self.setWindowFlags(
            QtCore.Qt.Tool |
            QtCore.Qt.WindowStaysOnTopHint |
            QtCore.Qt.FramelessWindowHint |
            QtCore.Qt.Window
        )
        self.menu = QtWidgets.QMenu("Menu", self)
        self.setUpMenu()

        self.mainLayout = QtWidgets.QVBoxLayout(self)
        self.container = QtWidgets.QWidget(self)
        self.mainLayout.addWidget(self.container)
        self.layout = QtWidgets.QVBoxLayout(self.container)

        self.timer = QtCore.QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.hide)

        self.setupSpacing()
        self.setButtons()
        self.delayedHide()
        self.setNetWMWindowFlags()

    def setupSpacing(self):
        self.mainLayout.setContentsMargins(
            config.layoutSpacing, config.layoutSpacing,
            config.layoutSpacing, config.layoutSpacing
        )

        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(config.layoutSpacing)
        self.setMinimumSize(0, 0)

    def setButtons(self):
        for button in config.launchers:
            self.layout.addWidget(
                Button(
                    config.iconSize,
                    button.get('icon'),
                    button.get('cmd'),
                    button.get('name')
                )
            )

    def delayedHide(self):
        self.timer.setInterval(config.hideTimeoutMsec)
        self.timer.start()

    def leaveEvent(self, event):
        self.delayedHide()
        super().leaveEvent(event)

    def enterEvent(self, event):
        self.timer.stop()
        super().enterEvent(event)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            if self.hidden:
                self.restore()
        elif event.button() == QtCore.Qt.MouseButton.RightButton:
            self.showMenu(event)
        super().mousePressEvent(event)

    def setUpMenu(self):
        self.menu.addAction("Quit", app.quit)

    def showMenu(self, event):
        self.menu.exec(event.globalPosition().toPoint())

    def hide(self):
        self.container.hide()
        self.setFixedSize(config.hiddenWidth, HEIGHT)
        self.repaint()
        self.hidden = True

    def restore(self):
        self.container.show()
        self.setFixedSize(WIDTH, HEIGHT)
        self.hidden = False

    def setNetWMWindowFlags(self):
        d = display.Display()
        win = d.create_resource_object('window', self.window().winId())
        _ATOM = d.intern_atom("ATOM")
        _TYPE = d.intern_atom("_NET_WM_WINDOW_TYPE")
        _DOCK = d.intern_atom("_NET_WM_WINDOW_TYPE_DOCK")
        win.change_property(_TYPE, _ATOM, 32, [_DOCK])
        d.flush()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    if qdarktheme:
        app.setStyleSheet(qdarktheme.load_stylesheet())
    screen = app.primaryScreen()

    widget = MyWidget()
    widget.show()

    HEIGHT = widget.height()
    WIDTH = widget.width()

    pos = (screen.size().height() / 2) - (HEIGHT / 2)
    widget.setGeometry(0, pos, WIDTH, HEIGHT)
    sys.exit(app.exec())
