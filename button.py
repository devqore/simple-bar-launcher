from pathlib import Path

from PySide6 import QtWidgets, QtGui, QtCore

from process import Process


class Button(QtWidgets.QPushButton):
    def __init__(self, iconSize, iconPath=None, command=None, name=None):
        super().__init__()
        self.setFlat(True)
        self.setToolTip(name)
        self.command = command
        self.iconSize = iconSize

        if Path(iconPath).exists():
            icon = QtGui.QIcon(iconPath)
        else:
            icon = QtGui.QIcon.fromTheme(iconPath)

        if icon.isNull():
            icon = QtGui.QIcon.fromTheme("help")
            self.setToolTip(f"{name} (icon is missing)")

        self.setIcon(icon)
        self.setIconSize(QtCore.QSize(self.iconSize, self.iconSize))
        self.setFixedSize(self.iconSize, self.iconSize)

        # to hide properly
        self.setMinimumSize(0, 0)

        self.clicked.connect(self.run)
        self.setStyleSheet(":hover { background-color: none;}")

        # effect to use on hover
        self.colorizeEffect = QtWidgets.QGraphicsColorizeEffect()
        self.setGraphicsEffect(self.colorizeEffect)
        self.colorizeEffect.setEnabled(False)

    def enterEvent(self, event):
        self.colorizeEffect.setStrength(0.3)
        self.colorizeEffect.setColor(QtCore.Qt.gray)
        self.colorizeEffect.setEnabled(True)
        return super().enterEvent(event)

    def leaveEvent(self, event):
        self.colorizeEffect.setEnabled(False)
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.colorizeEffect.setColor(QtCore.Qt.white)
            self.colorizeEffect.setStrength(0.5)
        super().mousePressEvent(event)

    def run(self):
        print(f'starting: {self.command}')
        proc = Process()
        proc.startDetached(self.command)
