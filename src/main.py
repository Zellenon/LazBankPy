import json
import random
import sys

from PySide2.QtCore import (Qt, Slot)
from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import *
from customGui import *
from dataClasses import *

library = Library('/media/boofsnorf/MOBILE HOME/Appdata/Lazbank/document_fixed.json')

class Widget(QWidget):

	def __init__(self):
		QWidget.__init__(self)

		#GUI Lists
		self.tickerDict = {}
		self.img = QPixmap()

		# Getting the Model
		self.data = read_data()
		self.allTags = self.data['allTags']

		# QWidget Layout
		self.main_layout = QHBoxLayout()

		size = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

		# Main image display
		self.label1 = QLabel("Alpha")
		self.display = MultiformatDisplay()
		self.main_layout.addWidget(self.label1)
		self.main_layout.addWidget(self.display)
		#self.label1.setStyleSheet("QLabel { background-color : red; color : blue; }") #Used to debug size

		self.sidebar = QWidget()
		self.sidebar_layout = QVBoxLayout()
		self.sidebar.setFixedSize(self.width(), self.height()*4)
		self.button = QPushButton("Next")
		self.button.setStyleSheet("QLabel { background-color : red; color : blue; }")
		self.button.setMinimumHeight(self.height()*0.05)
		self.sidebar_layout.addWidget(self.button)

		self.searchField = AutoCompleteEdit(self.allTags)
		self.sidebar_layout.addWidget(self.searchField)

		self.tagScroller = QScrollArea()
		self.tagScrollerWidget = QWidget()
		self.tagScrollerLayout = QVBoxLayout()
		self.tagScrollerWidget.setLayout(self.tagScrollerLayout)
		self.tagScroller.setWidget(self.tagScrollerWidget)
		self.sidebar_layout.addWidget(self.tagScroller)

		self.sidebar.setLayout(self.sidebar_layout)
		self.main_layout.addWidget(self.sidebar)

		self.button.clicked.connect(self.loadRandomImage)
		#self.searchField.returnPressed.connect(self.queueChange())

		# Set the layout to the QWidget

		self.setLayout(self.main_layout)

		self.loadRandomImage()

	def tickSize(self):
		self.img = self.img.scaled(self.label1.size(), aspectMode=Qt.KeepAspectRatio, mode=Qt.SmoothTransformation)
		#self.img = self.img.scaledToHeight(self.label1.height())
		self.label1.setPixmap(self.img)

	def loadRandomImage(self):
		# fetching the image
		if (self.searchField.changed):
			print("Changing Queue")
			library.queueFromString(self.searchField.text())

			"""self.queue = self.data['images']
			# addList = [w.objectName() for w in self.tickerDict.values() if w.status() == 1]
			# subList = [w.objectName() for w in self.tickerDict.values() if w.status() == -1]
			self.searchList = self.searchField.text().split(' ')
			if ('' in self.searchList):
				self.searchList.remove('')
			self.subList = [w for w in self.searchList if w[0] == '-']
			self.addList = list(set(self.searchList) - set(self.subList))
			if len(self.addList) > 0:
				self.queue = [w for w in self.queue if all(x in w['tags'] for x in self.addList)]
				print(self.addList)
			if len(self.subList) > 0:
				self.queue = [w for w in self.queue if all(x not in w['tags'] for x in self.subList)]
				print(self.subList)"""
			self.searchField.changed = False
		i = library.randomFromQueue()
		print(i.path)
		self.display.setMedia(i)
		self.img = QPixmap('/media/boofsnorf/MOBILE HOME/Appdata/Lazbank/' + i.path)
		self.tickSize()
		self.label1.setPixmap(self.img)

		# changing tagSlots



def read_data():
	data = json.load(open('/media/boofsnorf/MOBILE HOME/Appdata/Lazbank/document_fixed.json'))
	return data


class MainWindow(QMainWindow):

	def __init__(self, widget):
		QMainWindow.__init__(self)
		geometry = app.desktop().availableGeometry(self)
		self.setFixedSize(geometry.width() * 0.95, geometry.height() * 0.90)
		self.setWindowTitle("Lazbank")

		# Menu
		self.menu = self.menuBar()
		self.file_menu = self.menu.addMenu("File")

		# Exit QAction
		exit_action = QAction("Exit", self)
		exit_action.setShortcut("Ctrl+Q")
		exit_action.triggered.connect(self.exit_app)

		self.file_menu.addAction(exit_action)


		# Status Bar
		self.status = self.statusBar()
		self.status.showMessage("Loaded and plotted")

		widget.tickSize()
		self.setCentralWidget(widget)


	@Slot()
	def exit_app(self, checked):
		sys.exit()


if __name__ == "__main__":
	# Qt Application
	app = QApplication(sys.argv)

	# QWidget
	widget = Widget()

	# QMainWindow using QWidget as central widget
	window = MainWindow(widget)

	window.show()

	sys.exit(app.exec_())