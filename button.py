import os
import sys
import shlex
import subprocess
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
        self.effect = QtWidgets.QGraphicsColorizeEffect()
        self.setGraphicsEffect(self.effect)
        self.effect.setColor(QtCore.Qt.gray)
        self.effect.setStrength(0.3)
        self.effect.setEnabled(False)

    def enterEvent(self, event):
        self.effect.setEnabled(True)
        return super().enterEvent(event)

    def leaveEvent(self, event):
        self.effect.setEnabled(False)
        super().leaveEvent(event)

    def run(self):
        commandSplitted = shlex.split(self.command)
        print(f'starting: {commandSplitted}')

        # when using pyinstaller we need to ensure we are restoring original LD_LIBRARY_PATH
        # more details here https://pyinstaller.readthedocs.io/en/stable/runtime-information.html
        if getattr(sys, 'frozen', True):
            env = dict(os.environ)
            lpKey = 'LD_LIBRARY_PATH'
            lpOrig = env.get(lpKey + '_ORIG')
            if lpOrig is not None:
                env[lpKey] = lpOrig
            else:
                # This happens when LD_LIBRARY_PATH was not set.
                # Remove the env var as a last resort:
                env.pop(lpKey, None)

        subprocess.Popen(commandSplitted,
                         start_new_session=True,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT,
                         env=env)
