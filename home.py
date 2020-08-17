from PyQt5 import QtWidgets, QtGui
from PyQt5.QtGui import QFontMetrics

from ui_rule import Ui_MainWindow as rule_window
from ui_home import Ui_MainWindow as home_window
from ui_config import Ui_MainWindow as config_window

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
        msg.setIcon(QMessageBox.Warning)
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.buttonClicked.connect(self.popup_clicked)
        msg.exec_()

    def popup_clicked(self, b):
        if b.text() == '&Yes':
            generate()
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
        self.next_Button.clicked.connect(lambda: check_rule(self.b1))
        self.next_Button.clicked.connect(self.hide)
        self.back_Button.clicked.connect(self.hide)


class ConfigWindow(QtWidgets.QDialog, config_window):
    def __init__(self, parent=None):
        super(ConfigWindow, self).__init__(parent)
        self.setupUi(self)
        self.uploadfile_pushButton.clicked.connect(self.upload_config_file)
        self.next_Button.clicked.connect(lambda: self.load_file(self.checkBox))
        self.next_Button.clicked.connect(self.hide)
        self.back_pushButton.clicked.connect(self.hide)

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
                    cfg = yaml.safe_load(ymlfile)
                    ymlfile.close()
                list = [items for items in cfg]
                if 'age' in list:
                    try:
                        self.dist = cfg['age']['distribution']
                        if self.dist == 'normal':
                            self.avg = int(cfg['age']['average'])
                            self.sd = int(cfg['age']['sd'])
                        elif self.dist == 'binomial':
                            self.n = int(cfg['age']['n'])
                            self.p = int(cfg['age']['p'])
                        elif self.dist == 'poisson':
                            self.lam = int(cfg['age']['lam'])
                        print('success')
                    except TypeError:
                        MessageWindow().error_window('Missing age parameter(s). Do you want to use the default '
                                                     'settings instead?')
                if 'records' in list:
                    try:
                        self.num_records = cfg['records']['size']
                    except TypeError:
                        pass
            except AttributeError or FileNotFoundError:
                MessageWindow().error_window('No file path was found. Do you want to use the default settings?')
        else:
            generate()


class Manager:
    dt = 0
    df = 0

    def __init__(self):
        self.main = MainWindow()
        self.rule = RuleWindow()
        self.config = ConfigWindow()

        self.main.next_Button.clicked.connect(self.rule.show)
        self.rule.back_Button.clicked.connect(self.main.show)
        self.config.back_pushButton.clicked.connect(self.rule.show)


def check_rule(b):
    if b.isChecked():
        generate()
    else:
        Manager().config.show()


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


def generate():
    if Manager.dt == 0 and Manager.df == 0:
        rd.PatientRecord(rd.main(rd.m1, rd.m2), rd.PatientRecord.header_list).data_generate()
    elif Manager.dt == 0 and Manager.df == 1:
        OMOP_RD()
    elif Manager.dt == 1 and Manager.df == 0:
        rb.PatientRecord_RB(rd.main(rb.m1, rb.m2), rb.PatientRecord_RB.header_list).data_generate()
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
