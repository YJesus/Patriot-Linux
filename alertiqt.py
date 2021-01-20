import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

	
def showDialog(text):
	
	x = text.split(": ")
	
	app = QApplication(sys.argv)
	win = QWidget()
	msgBox = QMessageBox()
	msgBox.setIcon(QMessageBox.Warning)
	msgBox.setText(x[0])
	msgBox.setDetailedText(x[1])
	msgBox.setWindowTitle("Patriot Linux 1.0")
	msgBox.setStandardButtons(QMessageBox.Ok)

	returnValue = msgBox.exec()
   
if __name__ == '__main__': 
   showDialog(sys.argv[1])
