#   KeneticAlgorithm, an open source Qt project that aims to simulate genetic algorithm.
#   Copyright (C) 2023 İlkay Onay
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.

#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.

#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.





import sys
import numpy
import generatepop
import genaldef
import pickle
import random
from PyQt6.QtCore import QAbstractListModel,QVariant,Qt,pyqtSignal, QTimer
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QPushButton,QDialog,QScrollArea,QTextEdit,QVBoxLayout
from PyQt6.QtGui import QStandardItemModel, QStandardItem, QIcon, QIntValidator, QDoubleValidator

class ListModel(QAbstractListModel):
    dataChanged = pyqtSignal()

    def __init__(self, data, parent=None):
        super().__init__(parent)
        self._data = data

    def rowCount(self, parent):
        return len(self._data)

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            return str(self._data[index.row()])
        return QVariant()

    def updateData(self, new_data):
        self.beginResetModel()
        self._data = new_data
        self.endResetModel()
        self.dataChanged.emit()
def loadinputs():
    global equation_inputs, num_weights, low_par, high_par, sol_per_pop, num_generations, num_parents_mating
    ui.eqinput1.setText(str(equation_inputs[0]))
    ui.eqinput2.setText(str(equation_inputs[1]))
    ui.eqinput3.setText(str(equation_inputs[2]))
    ui.eqinput4.setText(str(equation_inputs[3]))
    ui.eqinput5.setText(str(equation_inputs[4]))
    ui.eqinput6.setText(str(equation_inputs[5]))
    ui.numweight.setText(str(num_weights))
    ui.solperpop.setText(str(sol_per_pop))
    ui.lownum.setText(str(low_par))
    ui.numhigh.setText(str(high_par))
    ui.numgen.setText(str(num_generations))
    ui.numparmate.setText(str(num_parents_mating))

def calculate():
    if (ui.eqinput1.text() and
    ui.eqinput2.text() and
    ui.eqinput3.text() and
    ui.eqinput4.text() and
    ui.eqinput5.text() and
    ui.eqinput6.text() and
    ui.numweight.text() and
    ui.solperpop.text() and
    ui.lownum.text() and
    ui.numhigh.text() and
    ui.numgen.text() and
    ui.numparmate.text()):
        equation_inputs[0] = float(ui.eqinput1.text())
        equation_inputs[1] = float(ui.eqinput2.text())
        equation_inputs[2] = float(ui.eqinput3.text())
        equation_inputs[3] = float(ui.eqinput4.text())
        equation_inputs[4] = float(ui.eqinput5.text())
        equation_inputs[5] = float(ui.eqinput6.text())
        num_weights= int(ui.numweight.text())
        sol_per_pop=int(ui.solperpop.text())
        low_par= float(ui.lownum.text())
        high_par=float(ui.numhigh.text())
        num_generations=int(ui.numgen.text())
        num_parents_mating=int(ui.numparmate.text())

        pop_size = (sol_per_pop, num_weights)
        new_population = numpy.random.uniform(low=low_par, high=high_par, size=pop_size)
        list_model = ListModel(new_population)
        ui.newpoptable.setModel(list_model)
        for generation in range(num_generations):

            gencount.append(generation)
            fitness = genaldef.cal_pop_fitness(equation_inputs, new_population)
            parents = genaldef.select_mating_pool(new_population, fitness, num_parents_mating)
            offspring_crossover = genaldef.crossover(parents,
            offspring_size=(pop_size[0] - parents.shape[0], num_weights))
            offspring_mutation = genaldef.mutation(offspring_crossover)
            new_population[0:parents.shape[0], :] = parents
            new_population[parents.shape[0]:, :] = offspring_mutation
            best_res.append(numpy.max(numpy.sum(new_population * equation_inputs, axis=1)))
            fitness = genaldef.cal_pop_fitness(equation_inputs, new_population)
            best_match_idx = numpy.where(fitness == numpy.max(fitness))
            best_sol.append(new_population[best_match_idx, :])
            best_sol_fit.append(fitness[best_match_idx])
            model.setItem(generation, 0, QStandardItem(str(best_res[generation])))
            model.setItem(generation, 2, QStandardItem(str(best_sol[generation])))
            model.setItem(generation, 1, QStandardItem(str(best_sol_fit[generation])))
            ui.calculationprogressbar.setValue(int((generation / num_generations) * 100))
        ui.calculationprogressbar.setValue(100)
    else:
        show_empty_line_warning()

def about():
    aboutbox = QMessageBox()
    aboutbox.setWindowIcon(QIcon("icon.ico"))
    aboutbox.setStyleSheet("QMessageBox { background-color: #333; color: white; } QLabel { color: white; } QPushButton { background-color: #555; color: white; }")

    aboutbox.setWindowTitle("KeneticAlgorithm Version 1.00")
    
    text = (
        "<b>About KeneticAlgorithm</b><br><br>"
        "KeneticAlgorithm <i>Copyright (C) 2023 İlkay Onay</i><br><br>"
        "This program comes with ABSOLUTELY NO WARRANTY; for details click the 'License' button.<br>"
        "This is free software, and you are welcome to redistribute it under certain conditions; click the 'License' button for details.</a>"
    )
    aboutbox.setText(text)
    license_button = QPushButton("License")
    aboutbox.addButton(license_button, QMessageBox.ButtonRole.ActionRole)
    aboutbox.addButton(QMessageBox.StandardButton.Ok)
    result = aboutbox.exec()
    if result == QMessageBox.StandardButton.Ok:
        pass
    elif aboutbox.clickedButton() == license_button:
        show_license()

def show_license():
    license_dialog = QDialog()
    license_dialog.setWindowTitle("GNU General Public License")
    license_dialog.setStyleSheet("background-color: #333; color: white;")
    license_dialog.setWindowIcon(QIcon("icon.ico"))

    scroll_area = QScrollArea(license_dialog)
    scroll_area.setWidgetResizable(True)

    license_text = QTextEdit()
    license_text.setReadOnly(True)
    
    try:
        with open("LICENSE.txt", "r", encoding="utf-8") as file:
            license_text_content = file.read()
    except FileNotFoundError:
        license_text_content = "License text not found."

    license_text.setPlainText(license_text_content)

    close_button = QPushButton("Close")
    close_button.setStyleSheet("background-color: #555; color: white;")
    close_button.clicked.connect(license_dialog.close)

    layout = QVBoxLayout()
    layout.addWidget(scroll_area)
    layout.addWidget(close_button)
    scroll_area.setWidget(license_text)

    license_dialog.setLayout(layout)
    license_dialog.setFixedSize(600, 400)

    license_dialog.exec()

def show_message_box():
    msg_box = QMessageBox()
    msg_box.setWindowIcon(QIcon("icon.ico"))
    msg_box.setIcon(QMessageBox.Icon.Information)
    msg_box.setWindowTitle("Confirmation")
    msg_box.setText("Are you sure you want to exit this program?")
    msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
    
    msg_box.setStyleSheet("QMessageBox { background-color: #333; color: white; } QLabel { color: white; } QPushButton { background-color: #555; color: white; }")


    save_and_exit_button = msg_box.addButton("Save and Exit", QMessageBox.ButtonRole.ActionRole)
    msg_box.setDefaultButton(save_and_exit_button)

    result = msg_box.exec()
    
    if msg_box.clickedButton() == save_and_exit_button:
        save_variables()
        save_to_file()
        Uygulama.quit()  
    elif result == QMessageBox.StandardButton.Yes:
        Uygulama.quit() 



def reset_variables():
    global equation_inputs, num_weights, low_par, high_par, sol_per_pop, num_generations, num_parents_mating
    ui.eqinput1.clear()
    ui.eqinput2.clear()
    ui.eqinput3.clear()
    ui.eqinput4.clear()
    ui.eqinput5.clear()
    ui.eqinput6.clear()
    ui.numgen.clear()
    ui.solperpop.clear()
    ui.numparmate.clear()
    ui.numweight.clear()
    ui.lownum.clear()
    ui.numhigh.clear()
    equation_inputs = [0, 0, 0, 0, 0, 0]
    num_weights = 0
    low_par = 0.0
    high_par = 0.0
    sol_per_pop = 0
    num_generations = 0
    num_parents_mating = 0

def save_variables():
    if (ui.eqinput1.text() and
    ui.eqinput2.text() and
    ui.eqinput3.text() and
    ui.eqinput4.text() and
    ui.eqinput5.text() and
    ui.eqinput6.text() and
    ui.numweight.text() and
    ui.solperpop.text() and
    ui.lownum.text() and
    ui.numhigh.text() and
    ui.numgen.text() and
    ui.numparmate.text()):
        equation_inputs[0] = float(ui.eqinput1.text())
        equation_inputs[1] = float(ui.eqinput2.text())
        equation_inputs[2] = float(ui.eqinput3.text())
        equation_inputs[3] = float(ui.eqinput4.text())
        equation_inputs[4] = float(ui.eqinput5.text())
        equation_inputs[5] = float(ui.eqinput6.text())
        num_weights= int(ui.numweight.text())
        sol_per_pop=int(ui.solperpop.text())
        low_par= float(ui.lownum.text())
        high_par=float(ui.numhigh.text())
        num_generations=int(ui.numgen.text())
        num_parents_mating=int(ui.numparmate.text())
        file_name, _ = QFileDialog.getSaveFileName(None, "Save Variables", "", "Python Pickle Files (*.pkl)")
        if file_name:
            with open(file_name, 'wb') as file:
                variables = {
                    'equation_inputs': equation_inputs,
                    'num_weights': num_weights,
                    'low_par': low_par,
                    'high_par': high_par,
                    'sol_per_pop': sol_per_pop,
                    'num_generations': num_generations,
                    'num_parents_mating': num_parents_mating
                }
                pickle.dump(variables, file)
    else:
        show_empty_line_warning()
def load_variables():
    file_name, _ = QFileDialog.getOpenFileName(None, "Load Variables", "", "Python Pickle Files (*.pkl)")
    if file_name:
        with open(file_name, 'rb') as file:
            loaded_variables = pickle.load(file)
            global equation_inputs, num_weights, low_par, high_par, sol_per_pop, num_generations, num_parents_mating
            equation_inputs = loaded_variables['equation_inputs']
            num_weights = loaded_variables['num_weights']
            low_par = loaded_variables['low_par']
            high_par = loaded_variables['high_par']
            sol_per_pop = loaded_variables['sol_per_pop']
            num_generations = loaded_variables['num_generations']
            num_parents_mating = loaded_variables['num_parents_mating']
    loadinputs()

def randomize():
    if(ui.randhigh.text() and
       ui.randlow.text()):
    
        roundup = ui.roundup.value()
        for i in range(len(equation_inputs)):
            if isitchecked[i] == 2:
                equation_inputs[i] = round(random.uniform(float(ui.randlow.text()), float(ui.randhigh.text())), roundup)
        if isitchecked[0] == 2:
                    ui.eqinput1.setText(str(equation_inputs[0]))
        if isitchecked[1] == 2:
                    ui.eqinput2.setText(str(equation_inputs[1]))
        if isitchecked[2] == 2:
                    ui.eqinput3.setText(str(equation_inputs[2]))
        if isitchecked[3] == 2:
                    ui.eqinput4.setText(str(equation_inputs[3]))
        if isitchecked[4] == 2:
                    ui.eqinput5.setText(str(equation_inputs[4]))
        if isitchecked[5] == 2:
                    ui.eqinput6.setText(str(equation_inputs[5]))
    else:
        show_empty_line_warning()
def toggle_checkboxes():
    if all([ui.randeqinput1.isChecked(), ui.randeqinput2.isChecked(), ui.randeqinput3.isChecked(), ui.randeqinput4.isChecked(), ui.randeqinput5.isChecked(), ui.randeqinput6.isChecked()]):
        ui.randeqinput1.setChecked(False)
        ui.randeqinput2.setChecked(False)
        ui.randeqinput3.setChecked(False)
        ui.randeqinput4.setChecked(False)
        ui.randeqinput5.setChecked(False)
        ui.randeqinput6.setChecked(False)
    else:
        ui.randeqinput1.setChecked(True)
        ui.randeqinput2.setChecked(True)
        ui.randeqinput3.setChecked(True)
        ui.randeqinput4.setChecked(True)
        ui.randeqinput5.setChecked(True)
        ui.randeqinput6.setChecked(True)

def save_to_file():
    if len(best_res) != 0:
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.FileMode.AnyFile)
        file_dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
        file_dialog.setNameFilter("Text Files (*.txt);;All Files (*)")

        if file_dialog.exec():
            file_path = file_dialog.selectedFiles()[0]

            with open(file_path, "w") as file:
                 for i, (res, sol) in enumerate(zip(best_res, best_sol)):
                    file.write(f"[{i}] best_res: {res}, best_sol: {sol}\n")
    else:
        show_non_action_warning()

def update_checkbox_state(index, state):
    isitchecked[index] = state

def show_empty_line_warning():
    msg = QMessageBox()
    msg.setStyleSheet("QMessageBox { background-color: #333; color: white; } QLabel { color: white; } QPushButton { background-color: #555; color: white; }")
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setText("Empty Line Error")
    msg.setInformativeText("Some of the required lines are empty. Please fill in all required fields.")
    msg.setWindowTitle("Error")
    msg.setWindowIcon(QIcon("icon.ico"))
    msg.exec()

def show_non_action_warning():
    msg = QMessageBox()
    msg.setStyleSheet("QMessageBox { background-color: #333; color: white; } QLabel { color: white; } QPushButton { background-color: #555; color: white; }")
    msg.setIcon(QMessageBox.Icon.Warning)
    msg.setText("No Results Error")
    msg.setInformativeText("There are no results to save. Please do the calculations with the tool first.")
    msg.setWindowTitle("Warning")
    msg.setWindowIcon(QIcon("icon.ico"))
    msg.exec()



equation_inputs = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
num_weights = 0
low_par = 0.0
high_par = 0.0
sol_per_pop = 0
num_generations = 0
num_parents_mating = 0
gencount = []
best_res = []
best_sol = []
best_sol_fit = []
int_validator = QIntValidator()
double_validator = QDoubleValidator()
Uygulama = QApplication(sys.argv)
homeWindow = QMainWindow()
icon = QIcon("icon.ico")
homeWindow.setWindowIcon(icon)
ui = generatepop.Ui_MainWindow()  
ui.setupUi(homeWindow)
model = QStandardItemModel()
ui.calculationprogressbar.setValue(0)
ui.calculationprogressbar.setMinimum(0)
ui.calculationprogressbar.setMaximum(100)
ui.genalgorithmtable.setModel(model)
ui.exitbutton.clicked.connect(show_message_box)
ui.resetbutton.clicked.connect(reset_variables)
ui.savebutton.clicked.connect(save_variables)
ui.loadbutton.clicked.connect(load_variables)
isitchecked = [None,None,None,None,None,None]
ui.randeqinput1.stateChanged.connect(lambda state, idx=0: update_checkbox_state(idx, state))
ui.randeqinput2.stateChanged.connect(lambda state, idx=1: update_checkbox_state(idx, state))
ui.randeqinput3.stateChanged.connect(lambda state, idx=2: update_checkbox_state(idx, state))
ui.randeqinput4.stateChanged.connect(lambda state, idx=3: update_checkbox_state(idx, state))
ui.randeqinput5.stateChanged.connect(lambda state, idx=4: update_checkbox_state(idx, state))
ui.randeqinput6.stateChanged.connect(lambda state, idx=5: update_checkbox_state(idx, state))
ui.checkuncheckall.clicked.connect(toggle_checkboxes)
ui.randbutton.clicked.connect(randomize)
ui.saveresultbutton.clicked.connect(save_to_file)
int_validator = QIntValidator()
double_validator = QDoubleValidator()
ui.lownum.setValidator(double_validator)
ui.numhigh.setValidator(double_validator)
ui.eqinput1.setValidator(double_validator)
ui.eqinput2.setValidator(double_validator)
ui.eqinput3.setValidator(double_validator)
ui.eqinput4.setValidator(double_validator)
ui.eqinput5.setValidator(double_validator)
ui.eqinput6.setValidator(double_validator)
ui.numgen.setValidator(int_validator)
ui.solperpop.setValidator(int_validator)
ui.numparmate.setValidator(int_validator)
ui.numweight.setValidator(int_validator)

model.setHorizontalHeaderLabels(['Best result', 'Best solution fitness', 'Best solution'])
ui.bhesapla.clicked.connect(calculate)
ui.actionAbout_KeneticAlgorithm.triggered.connect(about)
homeWindow.show()
timer = QTimer.singleShot(1000, about)
sys.exit(Uygulama.exec())
        