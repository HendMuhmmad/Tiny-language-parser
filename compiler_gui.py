from tiny_parser import Parser
from scanner import Scanner
import gui
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication,QFileDialog
import sys

class appGui(QtWidgets.QMainWindow):
    def __init__(self,parent = None):
        QtWidgets.QMainWindow.__init__(self,parent)
        self.ui = gui.Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.run_app)
        self.ui.pushButton_2.clicked.connect(self.upload_file)
        self.ui.tableWidget.horizontalHeader().setStretchLastSection(True) 
        self.error_dialog = QtWidgets.QMessageBox()
        self.error_dialog.setIcon(QtWidgets.QMessageBox.Critical)
        self.error_dialog.setStandardButtons(QtWidgets.QMessageBox.Cancel)
        self.error_dialog.setWindowTitle("Error")
        self.error_dialog.setText("Error")

    def showdialog(self,text):
        # self.ui.tableWidget.setRowCount(0)
        self.ui.label_5.setText('  ')
        self.error_dialog.setInformativeText(text)
        self.error_dialog.exec_()



    def upload_file(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.AnyFile)
        dialog.setFilter(QtCore.QDir.Files)
        if dialog.exec():
            files = dialog.selectedFiles()
            if files[0].endswith('.txt'):
                with open(files[0], 'r') as f:
                    code = f.read()
                    self.ui.textEdit.setPlainText(code)
                    f.close()
            else:
                self.ui.textEdit.setText("")
                self.ui.tableWidget.setRowCount(0)
                self.showdialog('Unknown File Format !!')
                
    
    def run_app(self):
        text = self.ui.textEdit.toPlainText()
        if text == '':
            self.ui.tableWidget.setRowCount(0)
            self.showdialog('No code found !!!')
        else:
            try:
                s = Scanner(text)
                output_table = s.get_tokens()
                rowN = len(output_table)
                keys = output_table[0].keys()
                self.ui.tableWidget.setColumnCount(2)
                self.ui.tableWidget.setRowCount(rowN)
                self.ui.tableWidget.setHorizontalHeaderLabels(keys)
                for i in range(rowN):
                    for j,col in enumerate(keys):
                        item = QtWidgets.QTableWidgetItem(output_table[i][col])
                        item.setTextAlignment(QtCore.Qt.AlignHCenter)
                        self.ui.tableWidget.setItem(i,j,item)

                parser = Parser(output_table)
                parser.stmt_sequence()
                if parser.counter < parser.max_counter:
                    raise Exception("error")
                self.ui.label_5.setPixmap(QtGui.QPixmap("syntax_tree.png"))

            except:
                self.showdialog("Syntax error code can't be parsed !!")


        
        



if __name__ == "__main__":
    app = QApplication(sys.argv)
    #adding css file
    styleSheet="styles.css"
    with open(styleSheet,"r") as f:
        app.setStyleSheet(f.read())
    gui = appGui()
    gui.show()
    sys.exit(app.exec_())