from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QMessageBox, QMenuBar, QMenu
from PyQt6.QtCore import QRunnable, QThreadPool, QObject, pyqtSignal, pyqtSlot
from main import manualRun, autoRun
from utils import CUR_DIR
import json, os, sys, subprocess

class ResultSignal(QObject):
    result = pyqtSignal(bool)

class Runnable(QRunnable):
    def __init__(self, n, city, schedules=None):
        super().__init__()
        self.n = n
        self.city = city
        self.schedules = schedules
        self.signals = ResultSignal()

    @pyqtSlot()
    def run(self): # overwritten function
        if self.n == 1:
            result = manualRun(self.city)
            self.signals.result.emit(result)
        elif self.n == 2:
            result = autoRun(self.city, self.schedules)
            self.signals.result.emit(result)

class App(QtWidgets.QWidget):

    def lang(self):
        with open(f"{CUR_DIR}\\data\\settings.json") as s:
            settings = json.load(s)

        with open(f"{CUR_DIR}\\data\\languages.json", encoding='utf-8') as l:
            languages = json.load(l)

        cur_lang = settings['language']
        return languages[cur_lang]

    def setLanguage(self, new_language):

        nbr_thread = QThreadPool.globalInstance().activeThreadCount()
        if  nbr_thread != 0 and self.displayLeavingConfirmation(self.lang()['dialog'][3]) or nbr_thread == 0:
                with open(f"{CUR_DIR}\\data\\settings.json", 'r') as s:
                    settings = json.load(s)
                settings["language"] = str(new_language)

                with open(f"{CUR_DIR}\\data\\settings.json", 'w') as s:
                    json.dump(settings, s, indent=2)
                os.execv(sys.executable, [sys.executable] + sys.argv)  # restart the app

    def openInExplorer(self, path):
        FILEBROWSER_PATH = os.path.join(os.getenv('WINDIR'), 'explorer.exe')
        if os.path.isdir(path):
            subprocess.run([FILEBROWSER_PATH, path])
        elif os.path.isfile(path):
            subprocess.run([FILEBROWSER_PATH, '/select,', os.path.normpath(path)])

    def __init__(self):
        super().__init__()

        # --- Windows settings ---
        self.setWindowIcon(QtGui.QIcon(CUR_DIR + '\\profil_pictures\\couvert.png'))
        self.setWindowTitle(self.lang()['win-title'])
        self.setMinimumSize(QtCore.QSize(330, 280))
        self.setMaximumSize(QtCore.QSize(400, 200))

        # --- Create components ---
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.lbl_city = QtWidgets.QLabel(self.lang()['city'])
        self.le_city = QtWidgets.QLineEdit(self)
        self.cbox_use_schedule = QtWidgets.QCheckBox(self.lang()['use-schedule'])
        self.lbl_hour1 = QtWidgets.QLabel(self.lang()['hour'])
        self.le_hour1 = QtWidgets.QLineEdit()
        self.lbl_hour2 = QtWidgets.QLabel(self.lang()['hour'])
        self.le_hour2 = QtWidgets.QLineEdit()
        self.lbl_hour3 = QtWidgets.QLabel(self.lang()['hour'])
        self.le_hour3 = QtWidgets.QLineEdit()
        self.btn_run = QtWidgets.QPushButton(self.lang()['run'][0])

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

        # --- Create toolbar ---
        self.menu_bar = QMenuBar()

        self.language_menu = QMenu(self.lang()['menubar'][0])
        ICON_DIR = CUR_DIR + '\\icons\\'
        self.language_menu.addAction(QtGui.QIcon(f"{ICON_DIR}uk_flag.png"),
                                     "English", lambda: self.setLanguage('EN'))
        self.language_menu.addAction(QtGui.QIcon(f"{ICON_DIR}france_flag.png"),
                                     "Français", lambda: self.setLanguage('FR'))
        self.language_menu.addAction(QtGui.QIcon(f"{ICON_DIR}spain_flag.png"),
                                     "Español", lambda: self.setLanguage('ES'))
        self.language_menu.addAction(QtGui.QIcon(f"{ICON_DIR}japan_flag.png"),
                                     "日本語", lambda: self.setLanguage('JA'))
        self.file_menu = QMenu(self.lang()['menubar'][1])
        self.file_menu.addAction(QtGui.QIcon(f"{ICON_DIR}folder_icon"),
                                 self.lang()['menubar'][2],
                                 lambda: self.openInExplorer(f"{CUR_DIR}\\data\\main.log"))

        self.menu_bar.addMenu(self.file_menu)
        self.menu_bar.addMenu(self.language_menu)
        self.main_layout.setMenuBar(self.menu_bar)

    def disableAllComponents(self):
        self.le_city.setDisabled(True)
        self.cbox_use_schedule.setDisabled(True)
        self.le_hour1.setDisabled(True)
        self.le_hour2.setDisabled(True)
        self.le_hour3.setDisabled(True)
        self.btn_run.setDisabled(True)

    @pyqtSlot()
    def run(self):

        if self.cbox_use_schedule.isChecked():

            city = self.le_city.text()
            schedules = [self.le_hour1.text(),
                        self.le_hour2.text(),
                        self.le_hour3.text()]

            self.btn_run.setText(self.lang()['run'][1])
            self.disableAllComponents()

            runnable = Runnable(2, city, schedules)

        else:
            city = self.le_city.text()
            runnable = Runnable(1, city)

        runnable.signals.result.connect(self.displayStatusMessage)
        pool = QThreadPool.globalInstance()
        pool.start(runnable)

    def displayLeavingConfirmation(self, content):
        dlg = QMessageBox(self)
        dlg.setWindowTitle(self.lang()['dialog'][0])
        dlg.setText(content)
        dlg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        dlg.setIcon(QMessageBox.Icon.Warning)
        button = dlg.exec()

        return button == QMessageBox.StandardButton.Yes

    def displayStatusMessage(self, result):
        dlg = QMessageBox(self)
        dlg.setStandardButtons(QMessageBox.StandardButton.Ok)

        if result:
            dlg.setWindowTitle(self.lang()['dialog'][1])
            dlg.setText(self.lang()['dialog'][5])
            dlg.setIcon(QMessageBox.Icon.Information)

        else:
            dlg.setWindowTitle(self.lang()['dialog'][0])
            dlg.setText(self.lang()['dialog'][4])
            dlg.setIcon(QMessageBox.Icon.Warning)

        button = dlg.exec()
        return button == QMessageBox.StandardButton.Yes

    def closeEvent(self, event): # overwritten function
        if QThreadPool.globalInstance().activeThreadCount() >= 1:
            if self.displayLeavingConfirmation(self.lang()['dialog'][2]):
                event.accept()
                exit()
            else:
                event.ignore()

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    win = App()
    win.show()
    app.exec()
