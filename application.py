from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import QRunnable, QThreadPool
from ressources import CUR_DIR
from main import manualRun, autoRun

"""
 Warning : This application is currently in Alpha version which
means that code isn't optimized and their might have some bugs.
"""

class Runnable(QRunnable):
    def __init__(self, n, city, schedules=None):
        super().__init__()
        self.n = n
        self.city = city
        self.schedules = schedules

    def run(self):
        if self.n == 1:
            manualRun(self.city)
        elif self.n == 2:
            autoRun(self.city, self.schedules)

class App(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        # --- Windows settings ---
        self.setWindowIcon(QtGui.QIcon(CUR_DIR + '\\profil_pictures\\couvert.png'))
        self.setWindowTitle("Weather Bot - Publication")
        self.setMinimumSize(QtCore.QSize(330, 280))
        self.setMaximumSize(QtCore.QSize(400, 200))

        # --- Create components ---
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.lbl_city = QtWidgets.QLabel("Choisissez une ville :")
        self.le_city = QtWidgets.QLineEdit(self)
        self.cbox_use_schedule = QtWidgets.QCheckBox("Publier un Tweet seulement pour les horaires suivants")
        self.lbl_hour1 = QtWidgets.QLabel("Choisissez un horaire (optionnel) :")
        self.le_hour1 = QtWidgets.QLineEdit()
        self.lbl_hour2 = QtWidgets.QLabel("Choisissez un horaire (optionnel) :")
        self.le_hour2 = QtWidgets.QLineEdit()
        self.lbl_hour3 = QtWidgets.QLabel("Choisissez un horaire (optionnel) :")
        self.le_hour3 = QtWidgets.QLineEdit()
        self.btn_run = QtWidgets.QPushButton("Exécuter")

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

    def run(self):

        if self.cbox_use_schedule.isChecked():

            city = self.le_city.text()
            schedules = [self.le_hour1.text(),
                        self.le_hour2.text(),
                        self.le_hour3.text()]

            self.btn_run.setText("En cours...")
            self.disableAllComponents()

            runnable = Runnable(2, city, schedules)

        else:
            city = self.le_city.text()
            runnable = Runnable(1, city)

        pool = QThreadPool.globalInstance()
        pool.start(runnable)

    def showLeavingConfirmation(self):
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Attention")
        dlg.setText("Vous être sur le point d'arrêter un processus en cours.\nVoulez vous vraiment quitter ?")
        dlg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        dlg.setIcon(QMessageBox.Icon.Warning)
        button = dlg.exec()

        return button == QMessageBox.StandardButton.Yes

    def closeEvent(self, event):
        if QThreadPool.globalInstance().activeThreadCount() >= 1:
            if self.showLeavingConfirmation():
                event.accept()
                exit()
            else:
                event.ignore()

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    win = App()
    win.show()
    app.exec()
