import json
import random
import sys

from PySide2.QtCore import (Qt, Slot, SIGNAL, QObject)
import PySide2.QtCore
from PySide2.QtMultimedia import *
from PySide2.QtMultimediaWidgets import *
from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import *
from dataClasses import *


class MultiformatDisplay(QWidget):

	def __init__(self):
		QWidget.__init__(self)

		self.media = None

		self.displayLayout = QStackedLayout()

		self.staticImageDisplay = QLabel()

		#self.gifDisplay = MoviePlayer()
		self.gifDisplay = QLabel("TEMP")

		self.movieDisplay = QVideoWidget()
		self.movieHolder = QMediaPlayer()
		self.movieHolder.setVideoOutput(self.movieHolder)

		self.displayLayout.addWidget(self.staticImageDisplay)
		self.displayLayout.addWidget(self.gifDisplay)
		self.displayLayout.addWidget(self.movieDisplay)

		self.displayLayout.setCurrentIndex(0)
		self.setLayout(self.displayLayout)

	def setMedia(self, media):
		self.media = media

		if ("movie" in self.media.tags):
			self.movieHolder.setMedia(self.media.path)
			self.displayLayout.setCurrentIndex(2)
		elif ("gif" in self.media.tags):
			#gif handling
			self.displayLayout.setCurrentIndex(1)
		else:
			img = QPixmap('/media/boofsnorf/MOBILE HOME/Appdata/Lazbank/' + self.media.path)
			img = img.scaled(self.staticImageDisplay.size(), aspectMode=Qt.KeepAspectRatio, mode=Qt.SmoothTransformation)
			self.staticImageDisplay.setPixmap(img)
			self.displayLayout.setCurrentIndex(0)


class AutoCompleteEdit(QLineEdit):
	def __init__(self, model, separator=' ', addSpaceAfterCompleting=True):
		super(AutoCompleteEdit, self).__init__()
		self.changed = True
		self._separator = separator
		self._addSpaceAfterCompleting = addSpaceAfterCompleting
		self._completer = QCompleter(model)
		self._completer.setWidget(self)
		self.connect(
			self._completer,
			SIGNAL('activated(QString)'),
			self._insertCompletion)
		self._keysToIgnore = [Qt.Key_Enter,
		                      Qt.Key_Return,
		                      Qt.Key_Escape,
		                      Qt.Key_Tab]

	def _insertCompletion(self, completion):
		"""
        This is the event handler for the QCompleter.activated(QString) signal,
        it is called when the user selects an item in the completer popup.
        """
		extra = len(completion) - len(self._completer.completionPrefix())
		extra_text = completion[-extra:]
		if (extra==0):
			extra_text = ''
		if self._addSpaceAfterCompleting:
			extra_text += ' '
		self.setText(self.text()[:self.cursorPosition()] + extra_text + self.text()[self.cursorPosition():])

	def textUnderCursor(self):
		text = self.text()
		textUnderCursor = ''
		i = self.cursorPosition() - 1
		while i >= 0 and text[i] != self._separator and text[i] != '-':
			textUnderCursor = text[i] + textUnderCursor
			i -= 1
		return textUnderCursor

	def keyPressEvent(self, event):
		if self._completer.popup().isVisible():
			if event.key() in self._keysToIgnore:
				event.ignore()
				return
		super(AutoCompleteEdit, self).keyPressEvent(event)
		completionPrefix = self.textUnderCursor()
		if completionPrefix != self._completer.completionPrefix():
			self._updateCompleterPopupItems(completionPrefix)
		if len(event.text()) > 0 and len(completionPrefix) > 0:
			self._completer.complete()
		if len(completionPrefix) == 0:
			self._completer.popup().hide()
		self.changed = True

	def _updateCompleterPopupItems(self, completionPrefix):
		"""
        Filters the completer's popup items to only show items
        with the given prefix.
        """
		self._completer.setCompletionPrefix(completionPrefix)
		self._completer.popup().setCurrentIndex(
			self._completer.completionModel().index(0, 0))

class tagSlot(QPushButton):

	def __init__(self, name: str, type: int):
		QPushButton.__init__(self)
		self.setObjectName(name)

		self.tagName = name
		self.type = type

		self.nameLabel = QLabel(name)
		# nameLabel.setMinimumHeight(self.height())
		self.removeButton = QCheckBox("-")
		self.removeButton.setObjectName("-")

		self.layout = QHBoxLayout()
		self.layout.addWidget(self.nameLabel)
		self.layout.addWidget(self.removeButton)
		self.setLayout(self.layout)
		self.neutButton.setChecked(False)

class tagTicker(QPushButton):

	def __init__(self, name):
		QPushButton.__init__(self)

		self.setProperty("checkable", True)
		self.setObjectName(name)

		self.nameLabel = QLabel(name)
		# nameLabel.setMinimumHeight(self.height())
		self.addButton = QCheckBox("")
		self.addButton.setObjectName("1")
		self.neutButton = QCheckBox("")
		self.neutButton.setObjectName("0")
		self.subButton = QCheckBox("")
		self.subButton.setObjectName("-1")

		self.buttongroup = QButtonGroup()
		self.buttongroup.addButton(self.addButton)
		self.buttongroup.addButton(self.neutButton)
		self.buttongroup.addButton(self.subButton)

		self.layout = QHBoxLayout()
		self.layout.addWidget(self.nameLabel)
		self.layout.addWidget(self.addButton)
		self.layout.addWidget(self.neutButton)
		self.layout.addWidget(self.subButton)
		self.setLayout(self.layout)
		self.neutButton.setChecked(True)

	def status(self):
		return int(self.buttongroup.checkedButton().objectName())


import sys
from PySide2.QtCore import *
from PySide2.QtGui import *

class MoviePlayer(QWidget):
	def __init__(self, parent=None):
		QWidget.__init__(self, parent)
		# setGeometry(x_pos, y_pos, width, height)
		self.setGeometry(200, 200, 400, 400)
		self.setWindowTitle("QMovie to show animated gif")

		# set up the movie screen on a label
		self.movie_screen = QLabel()
		# expand and center the label
		self.movie_screen.setSizePolicy(QSizePolicy.Expanding,
		                                QSizePolicy.Expanding)
		self.movie_screen.setAlignment(Qt.AlignCenter)
		self.btn_start = QPushButton("Start Animation")
		self.btn_start.clicked.connect(self.start)
		self.btn_stop = QPushButton("Stop Animation")
		self.btn_stop.clicked.connect(self.stop)
		# positin the widgets
		main_layout = QVBoxLayout()
		main_layout.addWidget(self.movie_screen)
		main_layout.addWidget(self.btn_start)
		main_layout.addWidget(self.btn_stop)
		self.setLayout(main_layout)

		# use an animated gif file you have in the working folder
		# or give the full file path
		ag_file = "AG_Dog.gif"
		self.movie = QMovie(ag_file, QByteArray(), self)
		self.movie.setCacheMode(QMovie.CacheAll)
		self.movie.setSpeed(100)
		self.movie_screen.setMovie(self.movie)
		# optionally display first frame
		self.movie.start()
		self.movie.stop()

	def start(self):
		"""sart animnation"""
		self.movie.start()

	def stop(self):
		"""stop the animation"""
		self.movie.stop()