import sys

from PySide6 import QtCore


class Process:
    def __init__(self):
        # when using pyinstaller we need to ensure we are restoring original LD_LIBRARY_PATH
        # more details here https://pyinstaller.readthedocs.io/en/stable/runtime-information.html
        self.env = QtCore.QProcessEnvironment.systemEnvironment()

        if getattr(sys, 'frozen', True):
            self.env.remove('LD_LIBRARY_PATH')
            if self.env.contains("LD_LIBRARY_PATH_ORIG"):
                self.env.insert("LD_LIBRARY_PATH", self.env.value("LD_LIBRARY_PATH_ORIG"))

        self.proc = QtCore.QProcess()

    def startDetached(self, command):
        self.proc.setProgram('/bin/sh')
        self.proc.setArguments(["-c", command])
        self.proc.setStandardOutputFile(QtCore.QProcess.nullDevice())
        self.proc.setStandardErrorFile(QtCore.QProcess.nullDevice())

        self.proc.setProcessEnvironment(self.env)
        self.proc.startDetached()
