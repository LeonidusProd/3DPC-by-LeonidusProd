import sys
from PyQt5.QtCore import QTimer, QSettings
from gui import *
import icon

class PrintCalcApp(Ui_MainWindow):
    def __init__(self, dialog):
        Ui_MainWindow.__init__(self)
        self.setupUi(dialog)
        self.plastTable.setHorizontalHeaderItem(0, QtWidgets.QTableWidgetItem("Пластик"))
        self.plastTable.setHorizontalHeaderItem(1, QtWidgets.QTableWidgetItem("Цена"))

        self.settings = QSettings()

        self.plastList = {}
        self.firstPrintPrice = 0
        self.nextPrintPrice = 0
        self.postprocessingPrice = 0
        self.prototypePrice = 0
        self.modelPrice = 0
        self.lastPrice = 0
        self.curPlast = ""
        self.curPlastPrice = 0.0
        self.runFlag = 0
        self.allGood = True
        self.anyEmpty = False

        self.loadSettings()

        self.calcButt.clicked.connect(self.output)
        self.addPlastButt.clicked.connect(self.addPlastDef)
        self.delPlastButt.clicked.connect(self.delPlastDef)
        self.saveSettButt.clicked.connect(self.saveSettings)

        self.main_timer = QTimer()
        self.main_timer.timeout.connect(self.updateCurPlast)
        self.main_timer.start(500)

    def foolEmptyProof(self):
        self.tryChangeType = 0
        try: self.tryChangeType = float(self.massEdit.text().replace(',', '.'))
        except ValueError: self.allGood = False
        else: pass
        if (self.massEdit.text() == ""): self.anyEmpty = True

        try: self.tryChangeType = float(self.timeEdit.text().replace(',', '.'))
        except ValueError: self.allGood = False
        else: pass
        if (self.timeEdit.text() == ""): self.anyEmpty = True

        try: self.tryChangeType = int(float(self.amountEdit.text().replace(',', '.')))
        except ValueError: self.allGood = False
        else: pass
        if (self.amountEdit.text() == ""): self.anyEmpty = True

        if self.modelSwitch.isChecked():
            try: self.tryChangeType = float(self.modelEdit.text().replace(',', '.'))
            except ValueError: self.allGood = False
            else: pass
            if (self.modelEdit.text() == ""): self.anyEmpty = True
        else:
            pass

        if self.postprocessingSwitch.isChecked():
            try: self.tryChangeType = float(self.postprocessingEdit.text().replace(',', '.'))
            except ValueError: self.allGood = False
            else: pass
            if (self.postprocessingEdit.text() == ""): self.anyEmpty = True
        else:
            pass

        if self.prototypeSwitch.isChecked():
            try: self.tryChangeType = float(self.prototypeEdit.text().replace(',', '.'))
            except ValueError: self.allGood = False
            else: pass
            if (self.prototypeEdit.text() == ""): self.anyEmpty = True
        else:
            pass

        try: self.tryChangeType = float(self.difficultyFactorEdit.text().replace(',', '.'))
        except ValueError: self.allGood = False
        else: pass
        if (self.difficultyFactorEdit.text() == ""): self.anyEmpty = True

        try: self.tryChangeType = float(self.paybackFactorEdit.text().replace(',', '.'))
        except ValueError: self.allGood = False
        else: pass
        if (self.paybackFactorEdit.text() == ""): self.anyEmpty = True

        try: self.tryChangeType = float(self.printerPowerEdit.text().replace(',', '.'))
        except ValueError: self.allGood = False
        else: pass
        if (self.printerPowerEdit.text() == ""): self.anyEmpty = True

        try: self.tryChangeType = float(self.electricityPriceEdit.text().replace(',', '.'))
        except ValueError: self.allGood = False
        else: pass
        if (self.electricityPriceEdit.text() == ""): self.anyEmpty = True

        try: self.tryChangeType = float(self.amortEdit.text().replace(',', '.'))
        except ValueError: self.allGood = False
        else: pass
        if (self.amortEdit.text() == ""): self.anyEmpty = True

        if (self.curPlast == ""): self.allGood = False

    def calcPrices(self):
        if self.prototypeEdit.text() == "":
            self.prototypePrice = 0
        else:
            self.prototypePrice = float(self.prototypeEdit.text().replace(',', '.'))

        if self.modelEdit.text() == "":
            self.modelPrice = 0
        else:
            self.modelPrice = float(self.modelEdit.text().replace(',', '.'))

        if self.postprocessingEdit.text() == "":
            self.postprocessingPrice = 0
        else:
            self.postprocessingPrice = float(self.postprocessingEdit.text().replace(',', '.'))

        self.firstPrintPrice = (((float(self.massEdit.text().replace(',', '.')) * (self.curPlastPrice / 1000)) + ((float(self.timeEdit.text().replace(',', '.')) / 60) * float(self.amortEdit.text().replace(',', '.'))) + ((float(self.timeEdit.text().replace(',', '.')) / 60) * (float(self.printerPowerEdit.text().replace(',', '.')) / 1000) * float(self.electricityPriceEdit.text().replace(',', '.')))) * float(self.difficultyFactorEdit.text().replace(',', '.')) * float(self.paybackFactorEdit.text().replace(',', '.'))) + self.modelPrice

        self.nextPrintPrice = self.firstPrintPrice - self.modelPrice

        self.lastPrice = self.firstPrintPrice + self.nextPrintPrice * (int(float(self.amountEdit.text().replace(',','.'))) - 1) + self.prototypePrice + self.modelPrice + self.postprocessingPrice

    def output(self):
        self.foolEmptyProof()
        if self.anyEmpty == True:
            print('anyEmpty')
            self.calcOutput.clear()
            self.calcOutput.append("Недостаточно данных для расчёта.")
            self.anyEmpty = False
            self.allGood = True
        elif self.allGood == False:
            print('allGood')
            self.calcOutput.clear()
            self.calcOutput.append("Какое-то поле заполнено неправильно")
            self.anyEmpty = False
            self.allGood = True
        else:
            print('Good')
            self.calcPrices()
            self.calcOutput.clear()
            firstPrintPriceOut = "Стоимость первой печати: " + str(round(self.firstPrintPrice, 2))
            self.calcOutput.append(firstPrintPriceOut)
            nextPrintPriceOut = "Стоимость следующий печатей: " + str(round(self.nextPrintPrice, 2))
            self.calcOutput.append(nextPrintPriceOut)
            postprocessingPriceOut = "Стоимость постобработки: " + str(round(self.postprocessingPrice, 2))
            self.calcOutput.append(postprocessingPriceOut)
            prototypePriceOut = "Стоимость прототипа: " + str(round(self.prototypePrice, 2))
            self.calcOutput.append(prototypePriceOut)
            modelPriceOut = "Стоимость 3D модели: " + str(round(self.modelPrice, 2))
            self.calcOutput.append(modelPriceOut)
            lastPriceOut = "Полная стоимость: " + str(round(self.lastPrice, 2))
            self.calcOutput.append(lastPriceOut)

    def saveSettings(self):
        self.settings.setValue('paybackFactor', self.paybackFactorEdit.text())
        self.settings.setValue('difficultyFactor', self.difficultyFactorEdit.text())
        self.settings.setValue('electricityPrice', self.electricityPriceEdit.text())
        self.settings.setValue('printerPower', self.printerPowerEdit.text())
        self.settings.setValue('amort', self.amortEdit.text())

    def loadSettings(self):
        self.paybackFactorEdit.setText(self.settings.value('paybackFactor', '0'))
        self.difficultyFactorEdit.setText(self.settings.value('difficultyFactor', '0'))
        self.electricityPriceEdit.setText(self.settings.value('electricityPrice', '0'))
        self.printerPowerEdit.setText(self.settings.value('printerPower', '0'))
        self.amortEdit.setText(self.settings.value('amort', '0'))
        self.plastList = self.settings.value('plastList', {})
        self.updatePlasts()

    def addPlastDef(self):
        global plastList
        if self.plastNameEdit.text() != "" and self.plastPriceEdit.text() != "":
            self.plastList[self.plastNameEdit.text()] = float(self.plastPriceEdit.text().replace(',', '.'))
            self.settings.setValue('plastList', self.plastList)
            self.updatePlasts()
            self.plastNameEdit.clear()
            self.plastPriceEdit.clear()
        else:
            pass

    def delPlastDef(self):
        global plastList
        if self.plastTable.currentRow() >= 0:
            self.plastList.pop(self.plastTable.item(self.plastTable.currentRow(), 0).text())
            self.settings.setValue('plastList', self.plastList)
            self.updatePlasts()
        else:
            pass

    def updatePlasts(self):
        self.plastTable.setRowCount(0)
        self.plastCh.clear()
        plastNames = self.plastList.keys()
        i = 0
        for item in plastNames:
            self.plastTable.insertRow(i)
            self.plastTable.setItem(i, 0, QtWidgets.QTableWidgetItem(item))
            self.plastTable.setItem(i, 1, QtWidgets.QTableWidgetItem(str(self.plastList[item])))
            self.plastCh.addItem(item)
            i += 1

    def updateCurPlast(self):
        if (len(self.plastList) != 0):
            self.curPlast = self.plastCh.currentText()
            self.curPlastPrice = self.plastList[self.curPlast]
        else: self.curPlast = ""

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    app.setOrganizationName('LeonidusProd')
    app.setApplicationName('3DPC')
    app.setWindowIcon(QtGui.QIcon(':/new/icon/icon.ico'))
    dialog = QtWidgets.QMainWindow()

    gui = PrintCalcApp(dialog)

    dialog.show()
    sys.exit(app.exec_())