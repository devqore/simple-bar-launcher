import sys
from pathlib import Path

from PySide6 import QtWidgets, QtGui, QtCore


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

        # when using pyinstaller we need to ensure we are restoring original LD_LIBRARY_PATH
        # more details here https://pyinstaller.readthedocs.io/en/stable/runtime-information.html
        env = QtCore.QProcessEnvironment.systemEnvironment()

        if getattr(sys, 'frozen', True):
            env.remove('LD_LIBRARY_PATH')
            if env.contains("LD_LIBRARY_PATH_ORIG"):
                env.insert("LD_LIBRARY_PATH", env.value("LD_LIBRARY_PATH_ORIG"))

        proc = QtCore.QProcess()
        proc.setProgram('/bin/sh')
        proc.setArguments(["-c", self.command])
        proc.setStandardOutputFile(QtCore.QProcess.nullDevice())
        proc.setStandardErrorFile(QtCore.QProcess.nullDevice())

        proc.setProcessEnvironment(env)
        proc.startDetached()
