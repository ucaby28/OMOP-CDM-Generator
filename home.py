from PyQt5 import QtWidgets, QtGui
from PyQt5.QtGui import QFontMetrics
from PyQt5.QtWidgets import QMessageBox

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

    def msg_setup(self, title, message):
        self.msg = QMessageBox()
        self.msg.setWindowTitle(title)
        self.msg.setText(message)

    def info_window(self, title, message):
        self.msg_setup(title, message + 'Do you want to continue to rule customisation? \n \n (Click Ignore to use '
                                     'the default parameters instead.)')
        self.msg.setIcon(QMessageBox.Information)
        self.msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No | QMessageBox.Ignore)
        self.msg.buttonClicked.connect(self.popup_clicked)
        self.msg.exec_()

    def age_error_window(self, title, message):
        self.msg_setup(title, message)
        self.msg.setIcon(QMessageBox.Warning)
        self.msg.setStandardButtons(QMessageBox.Ok)
        self.msg.buttonClicked.connect(Manager().age.show)
        self.msg.exec_()

    def csv_error_window(self, title, message):
        self.msg_setup(title, message)
        self.msg.setIcon(QMessageBox.Warning)
        self.msg.setStandardButtons(QMessageBox.Ok)
        self.msg.buttonClicked.connect(Manager().csvW.show)
        self.msg.exec_()

    def gen_window(self, title, message):
        self.msg_setup(title, message)
        self.msg.setIcon(QMessageBox.Information)
        self.msg.setStandardButtons(QMessageBox.Ok)
        self.msg.exec_()

    def popup_clicked(self, btn):
        if btn.text() == '&Yes':
            Manager().age.show()
        elif btn.text() == "&No":
            Manager().config.show()
        elif btn.text() == "Ignore":
            gen().generate()


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

    def check_rule(self, btn):
        if btn.isChecked():
            Manager().csvW.show()
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
                    except Exception:
                        gen.b = 40
                        gen.c = 20
                        gen.d = 'normal'
                        MessageWindow().info_window('Notice', 'Missing distribution parameter(s).')
                if 'records' in list:
                    try:
                        gen.p_row = self.cfg['records']['size']
                    except Exception:
                        gen.p_row = 100
                        MessageWindow().info_window('Notice', 'Missing records parameter.')
            except Exception:
                MessageWindow().info_window('Notice', 'No file path was found.')
        else:
            Manager().age.show()

    def check_age_para(self):
        gen.d = self.cfg['age']['distribution']
        if gen.d == 'normal':
            if (self.cfg['age']['average'] > 0 and self.cfg['age']['sd']) > 0:
                gen.b = self.cfg['age']['average']
                gen.c = self.cfg['age']['sd']
        elif gen.d == 'binomial':
            if 1 >= self.cfg['age']['p'] >= 0 and self.cfg['age']['n'] >= 0:
                gen.b = int(self.cfg['age']['n'])
                gen.c = self.cfg['age']['p']
        elif gen.d == 'poisson':
            if self.cfg['age']['lam'] > 0:
                gen.b = self.cfg['age']['lam']


class AgeWindow(QtWidgets.QDialog, age_window):
    def __init__(self, parent=None):
        super(AgeWindow, self).__init__(parent)
        self.setupUi(self)
        self.comboBox.currentIndexChanged.connect(self.change_text)
        self.next_Button.clicked.connect(self.hide)
        self.next_Button.clicked.connect(lambda: self.check_rule(self.default_checkBox))
        self.back_Button.clicked.connect(self.hide)

    def check_rule(self, b):
        if not b.isChecked():
            self.get_para()
        else:
            Manager().csvW.show()

    def change_text(self):
        self.t = str(self.comboBox.currentText())
        if self.t.strip() == 'Normal distribution':
            self.para_label.setText('Mean:')
            self.para_label_2.setHidden(False)
            self.sd_lineEdit_2.setHidden(False)
            self.para_label_2.setText('Standard deviation:')
            gen.d = 'normal'
        elif self.t.strip() == 'Binomial distribution':
            self.para_label.setText('Probability (1 >= p >= 0):')
            self.para_label_2.setHidden(False)
            self.sd_lineEdit_2.setHidden(False)
            self.para_label_2.setText('Size (n):')
            gen.d = 'binomial'
        elif self.t.strip() == 'Poisson distribution':
            self.para_label.setText('Lambda (lam):')
            self.para_label_2.setHidden(True)
            self.sd_lineEdit_2.setHidden(True)
            gen.d = 'poisson'

    def get_para(self):
        self.change_text()
        b = self.mean_lineEdit.text()
        try:
            if self.t.strip() != 'Poisson distribution':
                c = self.sd_lineEdit_2.text()
                if self.validate_para(b, c):
                    gen.b = b
                    gen.c = c
                    Manager().csvW.show()
                else:
                    MessageWindow().age_error_window('Error', 'Please enter valid number(s).')
            elif self.t.strip() == 'Poisson distribution' and float(b) > 0:
                gen.b = b
                Manager().csvW.show()
        except Exception:
            MessageWindow().age_error_window('Error', 'Please enter valid number(s).')

    def validate_para(self, b, c):
        try:
            if self.t.strip() == 'Normal distribution':
                if float(b) > 0 and float(c) > 0:
                    return True
                else:
                    return False
            elif self.t.strip() == 'Binomial distribution':
                if 1 >= float(b) >= 0:
                    float(c)
                    return True
                else:
                    return False
        except Exception:
            return False


class CSVWindow(QtWidgets.QDialog, csv_window):
    def __init__(self, parent=None):
        super(CSVWindow, self).__init__(parent)
        self.setupUi(self)
        self.next_Button.clicked.connect(self.hide)
        self.next_Button.clicked.connect(lambda: self.check_rule(self.default_checkBox))
        self.back_Button.clicked.connect(self.hide)
        if Manager.df == 1:
            self.person_label.setHidden(False)
            self.person_lineEdit_2.setHidden(False)
            self.measurement_label.setHidden(False)
            self.measurement_lineEdit.setHidden(False)
            self.observation_label_2.setHidden(False)
            self.observation__lineEdit_2.setHidden(False)
        else:
            self.person_label.setHidden(True)
            self.person_lineEdit_2.setHidden(True)
            self.specimen_label_2.setText('Number of Rows to Generate:')
            self.measurement_label.setHidden(True)
            self.measurement_lineEdit.setHidden(True)
            self.observation_label_2.setHidden(True)
            self.observation__lineEdit_2.setHidden(True)

    def check_rule(self, checkbox):
        if not checkbox.isChecked():
            self.get_para()
        else:
            gen().generate()

    def get_para(self):
        p = self.person_lineEdit_2.text()
        s = self.specimen_lineEdit_3.text()
        m = self.measurement_lineEdit.text()
        o = self.observation__lineEdit_2.text()

        if Manager.df == 1 and self.validate_para(p, s, m, o):
            gen.p_row = p
            gen.s_row = s
            gen.m_row = m
            gen.o_row = o
            gen().generate()
        elif Manager.df == 0 and self.validate_para(p, s, m, o):
            gen.s_row = s
            gen().generate()
        else:
            MessageWindow().csv_error_window('Error', 'Please enter a number greater than 0 in each field.')

    def validate_para(self, p, s, m, o):
        try:
            if Manager.df == 1:
                if int(p) > 0 and int(s) > 0 and int(m) > 0 and int(o) > 0:
                    return True
            elif Manager.df == 0 and int(s) > 0:
                print('here')
                return True
        except Exception:
            return False


class Manager:
    dt = 0
    df = 0

    def __init__(self):
        self.main = MainWindow()
        self.rule = RuleWindow()
        self.config = ConfigWindow()
        self.age = AgeWindow()
        self.csvW = CSVWindow()

        self.main.next_Button.clicked.connect(self.rule.show)
        self.rule.back_Button.clicked.connect(self.main.show)
        self.config.back_Button.clicked.connect(self.rule.show)
        self.age.back_Button.clicked.connect(self.config.show)
        self.csvW.back_Button.clicked.connect(self.age.show)


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


class gen:
    b = 40
    c = 20
    d = 'normal'
    p_row = 100
    s_row = 100
    m_row = 100
    o_row = 100

    def generate(self):
        if Manager.dt == 0 and Manager.df == 0:
            rd.PatientRecord(rd.main(gen.s_row, rd.m2), rd.PatientRecord.header_list).data_generate()
            MessageWindow().gen_window('Successful', rd.m2)
        elif Manager.dt == 0 and Manager.df == 1:
            OMOP_RD(gen.p_row, gen.s_row, gen.m_row, gen.o_row)
            MessageWindow().gen_window('Successful', person.m2)
        elif Manager.dt == 1 and Manager.df == 0:
            rb.PatientRecord_RB(rd.main(gen.s_row, rb.m2), rb.PatientRecord_RB.header_list).data_generate(gen.b, gen.c,
                                                                                                          gen.d)
            MessageWindow().gen_window('Successful', rb.m2)
        elif Manager.dt == 1 and Manager.df == 1:
            OMOP_RB(gen.p_row, gen.s_row, gen.m_row, gen.o_row)
            MessageWindow().gen_window('Successful', person_rb.m2)
        sys.exit()


def OMOP_RD(p_row, s_row, m_row, o_row):
    person.OMOP_PatientRecord(rd.main(p_row, person.m2), person.OMOP_PatientRecord.header_list).data_generate()
    import OMOPSpecimen_RD as specimen

    specimen.OMOP_PatientRecord(s_row,
                                specimen.OMOP_PatientRecord.header_list).data_generate()
    import OMOPMeasurement_RD as measurement

    measurement.OMOP_PatientRecord(m_row,
                                   measurement.OMOP_PatientRecord.header_list).data_generate()
    import OMOPObservation_RD as observation

    observation.OMOP_PatientRecord(o_row,
                                   observation.OMOP_PatientRecord.header_list).data_generate()
    import OMOPLocation_RD as location

    location.OMOP_PatientRecord(len(location.location_id_list),
                                location.OMOP_PatientRecord.header_list).data_generate()


def OMOP_RB(p_row, s_row, m_row, o_row):
    person_rb.OMOP_PatientRecord(rd.main(p_row, person_rb.m2),
                                 person.OMOP_PatientRecord.header_list).data_generate(gen.b, gen.c, gen.d)
    import OMOPSpecimen_RD as specimen
    import OMOPSpecimen_RB as specimen_rb

    specimen_rb.OMOP_PatientRecord(s_row,
                                   specimen.OMOP_PatientRecord.header_list).data_generate()
    import OMOPMeasurement_RD as measurement
    import OMOPMeasurement_RB as measurement_rb

    measurement_rb.OMOP_PatientRecord(m_row,
                                      measurement.OMOP_PatientRecord.header_list).data_generate()
    import OMOPObservation_RD as observation
    import OMOPObservation_RB as observation_rb

    observation_rb.OMOP_PatientRecord(o_row,
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
