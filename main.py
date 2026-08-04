import sys
import subprocess
import os


from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QFileDialog,
    QLineEdit,
    QMessageBox,
    QProgressBar,
)
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtCore import QUrl


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("OpenModelica Simulation Launcher")
        self.resize(750, 450)

        layout = QVBoxLayout()
        title = QLabel("OpenModelica Simulation Launcher")
        title.setStyleSheet("font-size:20px; font-weight:bold; padding:10px;")
        layout.addWidget(title)

        self.exePath = QLineEdit()
        self.exePath.setMinimumHeight(35)
        self.exePath.setPlaceholderText("Select executable")

        browseButton = QPushButton("Browse")
        browseButton.setMinimumHeight(40)
        browseButton.clicked.connect(self.browse)

        self.startTime = QLineEdit()
        self.startTime.setMinimumHeight(35)
        self.startTime.setPlaceholderText("Start Time")

        self.stopTime = QLineEdit()
        self.stopTime.setMinimumHeight(35)
        self.stopTime.setPlaceholderText("Stop Time")

        runButton = QPushButton("Run Simulation")
        runButton.setMinimumHeight(45)
        runButton.clicked.connect(self.runSimulation)

        self.resultButton = QPushButton("Open Results")
        self.resultButton.setMinimumHeight(40)
        self.resultButton.setEnabled(False)
        self.resultButton.clicked.connect(self.openResults)

        self.progress = QProgressBar()
        self.progress.setFormat("Ready")
        self.progress.setValue(0)

        layout.addWidget(QLabel("Executable"))
        layout.addWidget(self.exePath)
        layout.addWidget(browseButton)

        layout.addWidget(QLabel("Start Time"))
        layout.addWidget(self.startTime)

        layout.addWidget(QLabel("Stop Time"))
        layout.addWidget(self.stopTime)
        layout.addWidget(self.progress)
        layout.addWidget(runButton)
        layout.addWidget(self.resultButton)

        self.setLayout(layout)

    def browse(self):
        file, _ = QFileDialog.getOpenFileName(
            self,
            "Select Executable",
            "",
            "Executable (*.exe)"
        )

        if file:
            self.exePath.setText(file)

    def runSimulation(self):
        exe = self.exePath.text()
        start = self.startTime.text()
        stop = self.stopTime.text()

        if exe == "":
            QMessageBox.warning(self, "Error", "Please select an executable.")
            return

        command = [
            exe,
            f"-startTime={start}",
            f"-stopTime={stop}"
        ]

        try:
           self.progress.setValue(20)
           self.progress.setFormat("Running Simulation...")
           QApplication.processEvents()

           subprocess.run(
               command,
               cwd=os.path.dirname(exe),
               check=True
           )

           self.progress.setValue(100)
           self.resultButton.setEnabled(True)
           self.progress.setFormat("Completed!")
           QApplication.processEvents()
           QMessageBox.information(self, "Success", "Simulation Finished!")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
    def openResults(self):
        folder = os.path.dirname(self.exePath.text())
        QDesktopServices.openUrl(QUrl.fromLocalFile(folder))

app = QApplication(sys.argv)

window = MainWindow()
window.show()

sys.exit(app.exec())