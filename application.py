from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import QObject, QThread, pyqtSignal
from ressources import CUR_DIR
from main import manualRun, autoRun
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

class LeavingConfirmation(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Do you really want to leave ?")

        QBtn = QtWidgets.QDialogButtonBox.StandardButton.Yes | QtWidgets.QDialogButtonBox.StandardButton.Cancel

        # --- Create components ---
        self.btn_box = QtWidgets.QDialogButtonBox(QBtn)
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.message = QtWidgets.QLabel("The application is running. Do you really want to leave ?")

        # --- Add components to layout ---
        self.main_layout.addWidget(self.message)
        self.main_layout.addWidget(self.btn_box)

        # --- Set components settings ---
        self.btn_box.accepted.connect(self.accept)
        self.btn_box.rejected.connect(self.reject)

class App(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowIcon(QtGui.QIcon(CUR_DIR + '\\profil_pictures\\ciel_degage.png'))
        self.setWindowTitle("Weather Bot - Publisher")
        self.setupUserInterface()

    def setupUserInterface(self):

        # --- Create components ---
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.lbl_city = QtWidgets.QLabel("Choose a city:")
        self.le_city = QtWidgets.QLineEdit(self)
        self.cbox_use_schedule = QtWidgets.QCheckBox("Publish a Tweet only at the following hours")
        self.lbl_hour1 = QtWidgets.QLabel("Choose a first schedule (optional):")
        self.le_hour1 = QtWidgets.QLineEdit()
        self.lbl_hour2 = QtWidgets.QLabel("Choose a second schedule (optional):")
        self.le_hour2 = QtWidgets.QLineEdit()
        self.lbl_hour3 = QtWidgets.QLabel("Choose a third schedule (optional):")
        self.le_hour3 = QtWidgets.QLineEdit()
        self.btn_run = QtWidgets.QPushButton("Run")

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

        # --- Set components text ---
        self.le_hour1.setPlaceholderText("07h30")
        self.le_hour2.setPlaceholderText("12h00")
        self.le_hour3.setPlaceholderText("19h30")

        # --- Set components settings ---
        self.btn_run.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))

        # --- Set component connexions ---
        self.btn_run.clicked.connect(self.run)

        # --- Create thread ---
        self.thread = QThread()
        self.worker = Worker()
        self.worker.moveToThread(self.thread)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

    def disableAllComponents(self):
        self.lbl_city.setDisabled(True)
        self.le_city.setDisabled(True)
        self.cbox_use_schedule.setDisabled(True)
        self.lbl_hour1.setDisabled(True)
        self.le_hour1.setDisabled(True)
        self.lbl_hour2.setDisabled(True)
        self.le_hour2.setDisabled(True)
        self.lbl_hour3.setDisabled(True)
        self.le_hour3.setDisabled(True)
        self.btn_run.setDisabled(True)

    def displayLeavingConfirmation(self):
        if LeavingConfirmation().exec():
            win.close()

    def run(self):

        if self.cbox_use_schedule.isChecked():

            city = self.le_city.text()
            schedules = [self.le_hour1.text(),
                        self.le_hour3.text(),
                        self.le_hour3.text()]

            # Start thread for autoRun
            self.thread.started.connect(partial(self.worker.autoRun_, city, schedules))
            self.worker.finished.connect(self.thread.quit)
            self.thread.start()

            # Disable components
            self.btn_run.setText("Stop")
            self.disableAllComponents()

        else:
            city = self.le_city.text()

            # Start thread for manualRun
            self.thread.started.connect(partial(self.worker.manualRun_, city))
            self.worker.finished.connect(self.thread.quit)
            self.thread.start()

            # Change btn_run text and disable btn_run when thread start
            self.btn_run.setEnabled(False)
            self.btn_run.setText("Running...")

            # Change btn_run text and disable btn_run when thread stop
            self.thread.finished.connect(lambda: self.btn_run.setEnabled(True))
            self.thread.finished.connect(lambda: self.btn_run.setText("Run"))

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    win = App()
    win.show()
    app.exec()