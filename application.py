from PyQt6 import QtCore, QtGui, QtWidgets
from ressources import CUR_DIR
from main import manualRun, autoRun
from PyQt6.QtCore import QObject, QThread, pyqtSignal
import threading, time
from functools import partial

class Worker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)

    def manualRun_(self, city):
        manualRun(city)
        self.finished.emit()

    def autoRun_(self, city, schedules):
        autoRun(city, schedules)
        self.finished.emit()

class App(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowIcon(QtGui.QIcon(CUR_DIR + '\\profil_pictures\\ciel_degage.png'))
        self.setWindowTitle("Generator")
        self.setupUserInterface()

    def setupUserInterface(self):

        # --- Create components ---
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.lbl_city = QtWidgets.QLabel(self)
        self.le_city = QtWidgets.QLineEdit(self)
        self.cbox_use_schedule = QtWidgets.QCheckBox(self)
        self.lbl_hour1 = QtWidgets.QLabel(self)
        self.le_hour1 = QtWidgets.QLineEdit(self)
        self.lbl_hour2 = QtWidgets.QLabel(self)
        self.le_hour2 = QtWidgets.QLineEdit(self)
        self.lbl_hour3 = QtWidgets.QLabel(self)
        self.le_hour3 = QtWidgets.QLineEdit(self)
        self.btn_run = QtWidgets.QPushButton(self)

        # --- Add components to layout ---
        self.main_layout.addWidget(self.lbl_city)
        self.main_layout.addWidget(self.le_city)
        self.main_layout.addWidget(self.cbox_use_schedule)
        self.main_layout.addWidget(self.lbl_hour1)
        self.main_layout.addWidget(self.le_hour1)
        self.main_layout.addWidget(self.lbl_hour2)
        self.main_layout.addWidget(self.le_hour2)
        self.main_layout.addWidget(self.lbl_hour3)
        self.main_layout.addWidget(self.le_hour3)
        self.main_layout.addWidget(self.btn_run)

        # --- Set components settings ---
        self.btn_run.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))

        # --- Set components text ---
        self.lbl_city.setText("Choose a city:")
        self.cbox_use_schedule.setText("Publish a Tweet only at the following hours")
        self.lbl_hour1.setText("Choose a first schedule (optional):")
        self.le_hour1.setPlaceholderText("09h00")
        self.lbl_hour2.setText("Choose a second schedule (optional):")
        self.le_hour2.setPlaceholderText("12h00")
        self.lbl_hour3.setText("Choose a third schedule (optional):")
        self.le_hour3.setPlaceholderText("19h30")
        self.btn_run.setText("Run")

        # --- Set component connexions ---
        self.btn_run.clicked.connect(self.run)

        # --- Create thread ---

    def run(self):
        self.thread = QThread() # Create a QThread object
        self.worker = Worker() # Create a worker object
        self.worker.moveToThread(self.thread) # Move worker to the thread
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        if self.cbox_use_schedule.isChecked():

            city = self.le_city.text()
            schedules = [self.le_hour1.text(),
                        self.le_hour3.text(),
                        self.le_hour3.text()]

            self.thread.started.connect(partial(self.worker.autoRun_, city, schedules))
            self.worker.finished.connect(self.thread.quit)
            self.thread.start() # Start the thread

            self.btn_run.setText("Stop")
            self.btn_run.clicked.connect(self.thread.terminate)

            self.thread.finished.connect(lambda: self.btn_run.clicked.connect(self.run))
            self.thread.finished.connect(lambda: self.btn_run.setText("Run"))

        else:
            city = self.le_city.text()

            self.thread.started.connect(partial(self.worker.manualRun_, city))
            self.worker.finished.connect(self.thread.quit)
            self.thread.start() # Start the thread

            self.btn_run.setEnabled(False)
            self.btn_run.setText("Running...")

            self.thread.finished.connect(lambda: self.btn_run.setEnabled(True))
            self.thread.finished.connect(lambda: self.btn_run.setText("Run"))

app = QtWidgets.QApplication([])
win = App()
win.show()
app.exec()