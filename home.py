from PyQt5 import QtWidgets, QtGui
from PyQt5.QtGui import QFontMetrics

from ui_home import Ui_MainWindow as home_window
from ui_config import Ui_Dialog as config_window
from ui_rule import Ui_Dialog as rule_window
from ui_age import Ui_Dialog as age_window
from ui_csv import Ui_Dialog as csv_window

import Random as rd
import RuleBased_normal as rb
import OMOPPerson_RD as person
import OMOPPerson_RB as person_rb

import yaml
import os


class MessageWindow:
    def error_window(self, item):
        QMessageBox = QtWidgets.QMessageBox
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle('Error')
        msg.setText(item)
        msg.setIcon(QMessageBox.Information)
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.buttonClicked.connect(self.popup_clicked)
        msg.exec_()

    def popup_clicked(self, b):
        if b.text() == '&Yes':
            Manager().age.show()
        elif b.text() == "&No":
            Manager().config.show()


class MainWindow(QtWidgets.QMainWindow, home_window):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.b3 = self.Random_radioButton
        self.b3.setChecked(True)
        self.b3.toggled.connect(lambda: selected_format(self.b3))
        self.next_Button.clicked.connect(self.hide)


class RuleWindow(QtWidgets.QDialog, rule_window):
    def __init__(self, parent=None):
        super(RuleWindow, self).__init__(parent)
        self.setupUi(self)
        self.b1 = self.RD_radioButton
        self.b1.setChecked(True)
        self.b1.toggled.connect(lambda: selected_type(self.b1))
        self.next_Button.clicked.connect(self.hide)
        self.next_Button.clicked.connect(lambda: self.check_rule(self.b1))
        self.back_Button.clicked.connect(self.hide)

    def check_rule(self, b):
        if b.isChecked():
            generate(40, 20, 'normal')
        else:
            Manager().config.show()


class ConfigWindow(QtWidgets.QDialog, config_window):
    def __init__(self, parent=None):
        super(ConfigWindow, self).__init__(parent)
        self.setupUi(self)
        self.uploadfile_pushButton.clicked.connect(self.upload_config_file)
        self.next_Button.clicked.connect(self.hide)
        self.next_Button.clicked.connect(lambda: self.load_file(self.checkBox))
        self.back_Button.clicked.connect(self.hide)

    def upload_config_file(self):
        self.file_name, _ = QtWidgets.QFileDialog.getOpenFileName(caption='Select File', directory=os.getcwd(),
                                                                  filter='Config files (*.yaml *.yml)')

        self.showpath_lineEdit.setText(self.file_name)
        fontMetrics = QFontMetrics(QtGui.QFont())
        textSize = fontMetrics.size(0, self.file_name)
        textWidth = textSize.width() + 30
        textHeight = textSize.height() + 30
        self.showpath_lineEdit.resize(textWidth, textHeight)

    def load_file(self, checkbox):
        if not checkbox.isChecked():
            try:
                with open(self.file_name, "r") as ymlfile:
                    self.cfg = yaml.safe_load(ymlfile)
                    ymlfile.close()
                list = [items for items in self.cfg]
                if 'age' in list:
                    try:
                        self.check_age_para()
                    except TypeError:
                        MessageWindow().error_window('Missing distribution parameter(s). Do you want to skip to rule '
                                                     'customisation?')
                    finally:
                        generate(self.b, self.c, self.dist)
                # if 'records' in list:
                #     try:
                #         self.num_records = cfg['records']['size']
                #     except TypeError:
                #         pass
            except Exception:
                MessageWindow().error_window('No file path was found. Do you want to skip to rule '
                                             'customisation?')
        else:
            Manager().age.show()

    def check_age_para(self):
        self.dist = self.cfg['age']['distribution']
        if self.dist == 'normal':
            if (self.cfg['age']['average'] and self.cfg['age']['sd']) > 0:
                self.b = self.cfg['age']['average']
                self.c = self.cfg['age']['sd']
        elif self.dist == 'binomial':
            if 1 > self.cfg['age']['p'] > 0 and self.cfg['age']['n'] > 0:
                self.b = int(self.cfg['age']['n'])
                self.c = self.cfg['age']['p']
        elif self.dist == 'poisson':
            if self.cfg['age']['lam'] > 0:
                self.b = self.cfg['age']['lam']
                self.c = None


class AgeWindow(QtWidgets.QDialog, age_window):
    def __init__(self, parent=None):
        super(AgeWindow, self).__init__(parent)
        self.setupUi(self)
        self.comboBox.currentIndexChanged.connect(self.change_text)
        self.next_Button.clicked.connect(self.hide)
        self.next_Button.clicked.connect(lambda: self.check_rule(self.default_checkBox))
        self.back_Button.clicked.connect(self.hide)

    def check_rule(self, b):
        if b.isChecked():
            print('here')
            # Manager().csv.show()
        else:
            pass

    def change_text(self):
        t = str(self.comboBox.currentText())
        if t.strip() == 'Normal distribution':
            self.para_label.setText('Mean:')
            self.para_label_2.setHidden(False)
            self.sd_lineEdit_2.setHidden(False)
            self.para_label_2.setText('Standard deviation:')
        elif t.strip() == 'Binomial distribution':
            self.para_label.setText('Probability (p):')
            self.para_label_2.setHidden(False)
            self.sd_lineEdit_2.setHidden(False)
            self.para_label_2.setText('Size (n):')
        elif t.strip() == 'Poisson distribution':
            self.para_label.setText('Lambda (lam):')
            self.para_label_2.setHidden(True)
            self.sd_lineEdit_2.setHidden(True)


class CSVWindow(QtWidgets.QDialog, csv_window):
    def __init__(self, parent=None):
        super(CSVWindow, self).__init__(parent)
        self.setupUi(self)
        self.change_text()

        self.next_Button.clicked.connect(self.hide)
        self.back_Button.clicked.connect(self.hide)

    def change_text(self):
        if Manager.df == 0:
            self.person_label.setHidden(False)
            self.person_lineEdit_2.setHidden(False)
            self.measurement_label.setHidden(False)
            self.measurement_lineEdit.setHidden(False)
            self.observation_label_2.setHidden(False)
            self.observation__lineEdit_2.setHidden(False)
        else:
            self.person_label.setHidden(True)
            self.person_lineEdit_2.setHidden(True)
            self.measurement_label.setHidden(True)
            self.measurement_lineEdit.setHidden(True)
            self.observation_label_2.setHidden(True)
            self.observation__lineEdit_2.setHidden(True)


class Manager:
    dt = 0
    df = 0

    def __init__(self):
        self.main = MainWindow()
        self.rule = RuleWindow()
        self.config = ConfigWindow()
        self.age = AgeWindow()
        self.csv = CSVWindow()

        self.main.next_Button.clicked.connect(self.rule.show)
        self.rule.back_Button.clicked.connect(self.main.show)
        self.config.back_Button.clicked.connect(self.rule.show)
        self.age.back_Button.clicked.connect(self.config.show)
        self.age.next_Button.clicked.connect(self.csv.show)
        self.csv.back_Button.clicked.connect(self.age.show)


def selected_type(b):
    if b.isChecked():
        Manager.dt = 0
    else:
        Manager.dt = 1


def selected_format(b):
    if b.isChecked():
        Manager.df = 0
    else:
        Manager.df = 1


def generate(b, c, d):
    if Manager.dt == 0 and Manager.df == 0:
        rd.PatientRecord(rd.main(rd.m1, rd.m2), rd.PatientRecord.header_list).data_generate()
    elif Manager.dt == 0 and Manager.df == 1:
        OMOP_RD()
    elif Manager.dt == 1 and Manager.df == 0:
        rb.PatientRecord_RB(rd.main(rb.m1, rb.m2), rb.PatientRecord_RB.header_list).data_generate(b, c, d)
    elif Manager.dt == 1 and Manager.df == 1:
        OMOP_RB()
    sys.exit()


def OMOP_RD():
    person.OMOP_PatientRecord(rd.main(person.m1, person.m2), person.OMOP_PatientRecord.header_list).data_generate()
    import OMOPSpecimen_RD as specimen

    specimen.OMOP_PatientRecord(len(specimen.person_id_list),
                                specimen.OMOP_PatientRecord.header_list).data_generate()
    import OMOPMeasurement_RD as measurement

    measurement.OMOP_PatientRecord(len(specimen.person_id_list),
                                   measurement.OMOP_PatientRecord.header_list).data_generate()
    import OMOPObservation_RD as observation

    observation.OMOP_PatientRecord(len(specimen.person_id_list),
                                   observation.OMOP_PatientRecord.header_list).data_generate()
    import OMOPLocation_RD as location

    location.OMOP_PatientRecord(len(location.location_id_list),
                                location.OMOP_PatientRecord.header_list).data_generate()


def OMOP_RB():
    person_rb.OMOP_PatientRecord(rd.main(person_rb.m1, person_rb.m2),
                                 person.OMOP_PatientRecord.header_list).data_generate()
    import OMOPSpecimen_RD as specimen
    import OMOPSpecimen_RB as specimen_rb

    specimen_rb.OMOP_PatientRecord(len(specimen_rb.person_id_list),
                                   specimen.OMOP_PatientRecord.header_list).data_generate()
    import OMOPMeasurement_RD as measurement
    import OMOPMeasurement_RB as measurement_rb

    measurement_rb.OMOP_PatientRecord(len(specimen_rb.person_id_list),
                                      measurement.OMOP_PatientRecord.header_list).data_generate()
    import OMOPObservation_RD as observation
    import OMOPObservation_RB as observation_rb

    observation_rb.OMOP_PatientRecord(len(specimen_rb.person_id_list),
                                      observation.OMOP_PatientRecord.header_list).data_generate()
    import OMOPLocation_RD as location
    import OMOPLocation_RB as location_rb

    location_rb.OMOP_PatientRecord(len(location.location_id_list),
                                   location.OMOP_PatientRecord.header_list).data_generate()


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    manager = Manager()
    manager.main.show()
    sys.exit(app.exec_())
