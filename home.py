from PyQt5 import QtWidgets
from ui_home import Ui_MainWindow as home_window
from ui_format import Ui_MainWindow as format_window

import Random as rd
import RuleBased_normal as rb
import OMOPRandomPerson as person
import OMOPPerson_RB as person_rb


class MainWindow(QtWidgets.QMainWindow, home_window):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.b1 = self.Random_radioButton
        self.b1.setChecked(True)
        self.b1.toggled.connect(lambda: selected_type(self.b1))
        self.next_Button.clicked.connect(self.hide)


class FormatWindow(QtWidgets.QDialog, format_window):
    def __init__(self, parent=None):
        super(FormatWindow, self).__init__(parent)
        self.setupUi(self)
        self.b2 = self.Random_radioButton
        self.b2.setChecked(True)
        self.b2.toggled.connect(lambda: selected_format(self.b2))
        self.next_Button.clicked.connect(self.hide)
        self.back_pushButton.clicked.connect(self.hide)


class Manager:
    dt = 0
    df = 0

    def __init__(self):
        self.main = MainWindow()
        self.format = FormatWindow()

        self.main.next_Button.clicked.connect(self.format.show)
        self.format.back_pushButton.clicked.connect(self.main.show)
        self.format.next_Button.clicked.connect(generate)

        self.main.show()


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
        person.OMOP_PatientRecord(rd.main(person.m1, person.m2),
                                  person.OMOP_PatientRecord.header_list).data_generate()
        import OMOPRandomSpecimen as specimen
        specimen.OMOP_PatientRecord(len(specimen.person_id_list),
                                    specimen.OMOP_PatientRecord.header_list).data_generate()
    elif Manager.dt == 1 and Manager.df == 0:
        rb.PatientRecord_RB(rd.main(rb.m1, rb.m2), rb.PatientRecord_RB.header_list).data_generate()
    elif Manager.dt == 1 and Manager.df == 1:
        person_rb.OMOP_PatientRecord(rd.main(person_rb.m1, person_rb.m2),
                                     person.OMOP_PatientRecord.header_list).data_generate()
        import OMOPSpecimen_RB as specimen_rb
        specimen_rb.OMOP_PatientRecord(len(specimen_rb.person_id_list),
                                       specimen_rb.OMOP_PatientRecord.header_list).data_generate()
    sys.exit()


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    manager = Manager()
    sys.exit(app.exec_())
