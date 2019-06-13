
# ADD THIS TO PORTFOLIO
# - Jayson Manlapaz Tiongco
# - Made in February 2019
# - Practice project using PyQt5 module in Python3

from PyQt5.QtWidgets import (QApplication, QWidget, QToolTip, QPushButton, QTextEdit, 
	QLineEdit, QHBoxLayout, QVBoxLayout, QRadioButton, QButtonGroup, QDesktopWidget,
	QComboBox, QMessageBox)
from PyQt5.QtGui import QIcon, QFont, QColor, QIntValidator
from PyQt5.QtCore import Qt
import sys
import string
import re

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)

app_name = 'Cipher App'
icon = 'eat.png'


class ciphering_app(QWidget):

	def __init__(self):
		
		super().__init__()
		self.initUI()


	def initUI(self):

		QToolTip.setFont(QFont('SansSerif', 10))

		encipher_btn = QPushButton('Encipher', self)
		encipher_btn.setToolTip('Enciphers the message.')

		decipher_btn = QPushButton('Decipher', self)
		decipher_btn.setToolTip('Deciphers the message.')

		encipher_btn.clicked.connect(self.encipher)
		decipher_btn.clicked.connect(self.decipher)

		hbox = QHBoxLayout()
		hbox.addStretch(1)
		hbox.addWidget(encipher_btn)
		hbox.addWidget(decipher_btn)

		vbox = QVBoxLayout()
		vbox.addStretch(1)
		vbox.addLayout(hbox)

		self.setLayout(vbox)

		ceasar = QRadioButton('Ceasar Cipher', self)
		ceasar.move(20, 100)
		self.combo_box = QComboBox(self)
		self.combo_box.addItem('Key')
		for i in range(1, 26):
			self.combo_box.addItem(str(i))
		self.combo_box.resize(45, 20)
		self.combo_box.move(40, 125)
		ceasar.setChecked(True)

		vigenere = QRadioButton('Vigenere Cipher', self)
		vigenere.move(130, 100)
		self.vigenere_key = QLineEdit(self)
		self.vigenere_key.resize(100, 20)
		self.vigenere_key.move(150, 125)
		self.vigenere_key.setPlaceholderText('Key')

		playfair = QRadioButton('Playfair Cipher', self)
		playfair.move(290, 100)
		self.playfair_key = QLineEdit(self)
		self.playfair_key.resize(100, 20)
		self.playfair_key.move(310, 125)
		self.playfair_key.setPlaceholderText('Key')

		railfence = QRadioButton('Railfence Cipher', self)
		railfence.move(450, 100)
		self.railfence_rows = QLineEdit(self)
		self.railfence_rows.setValidator(QIntValidator())
		self.railfence_rows.resize(100, 20)
		self.railfence_rows.move(470, 125)
		self.railfence_rows.setPlaceholderText('Rows')

		self.radio_group = QButtonGroup()
		self.radio_group.addButton(ceasar)
		self.radio_group.addButton(vigenere)
		self.radio_group.addButton(playfair)
		self.radio_group.addButton(railfence)

		self.message_edit = QTextEdit(self)
		self.message_edit.setPlaceholderText('Message here')
		self.message_edit.zoomIn(3)
		self.message_edit.resize(580, 80)
		self.message_edit.move(10, 10)

		self.log = QTextEdit(self)
		self.log.setToolTip('Ctrl + scroll to zoom in and out')
		self.log.setFontFamily('Consolas')
		self.log.setPlainText('Console')
		self.log.setStyleSheet('background-color: rgb(12, 12, 12); color: rgb(204, 204, 204);')
		self.log.zoomIn(3)
		self.log.setReadOnly(True)
		self.log.resize(580, 400)
		self.log.move(10, 160)

		self.setGeometry(600, 600, 600, 600)
		self.setFixedSize(self.size())
		self.setWindowTitle(app_name)
		self.setWindowIcon(QIcon(icon))
		self.center()

		self.show()


	def center(self):
		fg = self.frameGeometry()
		ce = QDesktopWidget().availableGeometry().center()	
		fg.moveCenter(ce)
		self.move(fg.topLeft())


	def ceasar_function(self, m, msg):
		new_msg = ''
		key = self.combo_box.currentIndex()

		if key == 0:
			QMessageBox.about(self, 'Error', 'No key chosen.')
			return

		if m == 0:
			method = 'Encipher'
		else:
			method = 'Decipher'
		c_log = 'Method: Ceasar Cipher - '+method+'\nKey: '+str(key)+'\n\n'

		for i in msg:
			num_value = ord(i)
			
			if num_value == 32:
				new_msg += ' '
				c_log += '\n'
				continue

			if m == 0:
				num_value += key
			elif m == 1:
				num_value -= key

			if i.istitle():
				if num_value < 65:
					num_value += 26
				if num_value > 90:
					num_value -= 26
			else:
				if num_value < 97:
					num_value += 26
				if num_value > 122:
					num_value -= 26

			new_msg += chr(num_value)
			c_log += str(i)+'   =>   '+chr(num_value)+'\n'
		
		self.log.setPlainText(c_log)
		self.message_edit.setPlainText(new_msg)


	def vigenere_function(self, m, msg):
		new_msg = ''
		key = self.vigenere_key.text().replace(' ', '').lower()

		if len(key) == 0:
			QMessageBox.about(self, 'Oops', 'It seems you forgot to set the key!')
			return

		if not all(i.isalpha() or i.isspace() for i in key):
			QMessageBox.about(self, 'Oops', 'Vigenere Cipher key cannot contain special characters or numbers!')
			return

		if m == 0:
			method = 'Encipher'
		else:
			method = 'Decipher'
		c_log = 'Method: Vigenere Cipher - '+method+'\nKey: '+key+'\n\n'

		# ik_subtract is for shifting index when white space is found on message
		ik_subtract = 0

		for i in range(0, len(msg)):
			if msg[i] == ' ':
				new_msg += ' '
				ik_subtract += 1
				c_log += '\n'
				continue

			if i >= len(key):
				ik = (i % len(key)) - ik_subtract
			else:
				ik = i - ik_subtract

			num_value_key = ord(key[ik]) - 96
			num_value_char = ord(msg[i])

			if m == 0:
				new_value = num_value_char + num_value_key
			elif m == 1:
				new_value = num_value_char - num_value_key

			if msg[i].istitle():
				if new_value < 65:
					new_value += 26
				if new_value > 90:
					new_value -= 26
			else:
				if new_value < 97:
					new_value += 26
				if new_value > 122:
					new_value -= 26

			new_msg += chr(new_value)
			c_log += msg[i]+'  +  key:'+key[ik]+'   =>   '+chr(new_value)+'\n'

		self.log.setPlainText(c_log)
		self.message_edit.setPlainText(new_msg)


	def playfair_function(self, m, msg):
		new_msg = ''
		key = self.playfair_key.text().replace(' ', '').lower()

		if len(key) == 0:
			QMessageBox.about(self, 'Oops', 'It seems you forgot to set the key!')
			return

		if not all(i.isalpha() or i.isspace() for i in key):
			QMessageBox.about(self, 'Oops', 'Playfair Cipher key cannot contain special characters or numbers!')
			return

		if m == 0:
			method = 'Encipher'
		else:
			method = 'Decipher'
		c_log = 'Method: Playfair Cipher - '+method+'\nKey: '+key+'\n'
		c_log += '<!> Spaces will be removed when using Playfair Cipher\n\n'

		key = list(dict.fromkeys(key))

		if 'j' in key and 'i' not in key:
			c_log += '<!> "j" found in key, please note that "i" is also "j" in the table.\n\n'
			remove_i = True
		elif 'j' in key and 'i' in key:
			key.remove('j')
			c_log += '<!> "j" found in key, please note that "i" is also "j" in the table.\n\n'
			remove_i = False
		else:
			remove_i = False

		for char in string.ascii_lowercase:
			if remove_i:
				if char == 'i':
					continue
			else:
				if char == 'j':
					continue
			if char not in key:
				key.append(char)

		grid = [[x for x in key[5*y:(5*y)+5]] for y in range(5)]

		for i in grid:
			for x in i:
				c_log += x + '  '
			c_log += '\n'

		no_space_msg = msg.replace(' ', '')

		split_msg = [no_space_msg[i:i+2] for i in range(0, len(no_space_msg), 2)]
		if len(split_msg[-1]) == 1:
			split_msg[-1] += 'x'

		c_log += '\n'

		# index_1, index_2 = None, None
		# grid_index_1, grid_index_2 = None, None

		for i in split_msg:
			letter_1 = i[0]
			letter_2 = i[1]
			
			in_li = False

			for li in grid:

				if remove_i:
					if letter_1 == 'i':
						letter_1 = 'j'
					if letter_2 == 'i':
						letter_2 = 'j'
				else:
					if letter_1 == 'j':
						letter_1 = 'i'
					if letter_2 == 'j':
						letter_2 = 'i'

				if letter_1 in li and letter_2 in li and not letter_1 == letter_2:

					if m == 0:
						index_1 = li.index(letter_1) + 1
						index_2 = li.index(letter_2) + 1

						if index_1 > 4:
							index_1 = 0
						if index_2 > 4:
							index_2 = 0

					else:
						index_1 = li.index(letter_1) - 1
						index_2 = li.index(letter_2) - 1

						if index_1 < 0:
							index_1 = 4
						if index_2 < 0:
							index_2 = 4

					letter_1 = li[index_1]
					letter_2 = li[index_2]

					new_msg += letter_1+letter_2
					in_li = True
					continue

				else:
					if letter_1 in li:
						index_1 = li.index(letter_1)
						grid_index_1 = grid.index(li)

					if letter_2 in li:
						index_2 = li.index(letter_2)
						grid_index_2 = grid.index(li)

			# Unknown bug occurs sometimes...
			try:

				if index_1 == index_2:
					if m == 0:
						grid_index_1 += 1
						grid_index_2 += 1

						if grid_index_1 > 4:
							grid_index_1 = 0
						if grid_index_2 > 4:
							grid_index_2 = 0

						if grid_index_1 == grid_index_2:
							index_1 += 1
							index_2 += 1

							if index_1 > 4:
								index_1 = 0
							if index_2 > 4:
								index_2 = 0

					else:
						grid_index_1 -= 1
						grid_index_2 -= 1

						if grid_index_1 < 0:
							grid_index_1 = 4
						if grid_index_2 < 0:
							grid_index_2 = 4

						if grid_index_1 == grid_index_2:
							index_1 -= 1
							index_2 -= 1

							if index_1 < 0:
								index_1 = 4
							if index_2 < 0:
								index_2 = 4

					letter_1 = grid[grid_index_1][index_1]
					letter_2 = grid[grid_index_2][index_2]
					new_msg += letter_1+letter_2

				else:
					if not in_li:
						letter_1 = grid[grid_index_1][index_2]
						letter_2 = grid[grid_index_2][index_1]
						new_msg += letter_1+letter_2

			except:
				QMessageBox.about(self, 'Oh no', 'A bug just flew by, causing an error D: Please try again!')
				return

			c_log += i+'  =>  '+letter_1+letter_2+'\n'

		self.log.setPlainText(c_log)
		self.message_edit.setPlainText(new_msg)


	def railfence_function(self, m, msg):
		new_msg = ''

		try:
			rows = int(self.railfence_rows.text())
			if rows < 2:
				QMessageBox.about(self, 'Oops', 'Number of rows should be more than one!')
				return
		except:
			QMessageBox.about(self, 'Oops', 'It seems you forgot to set the key!')
			return

		if m == 0:
			method = 'Encipher'
		else:
			method = 'Decipher'
		c_log = 'Method: Railfence Cipher - '+method+'\nRows: '+str(rows)+'\n\n'

		grid = [[] for i in range(0, rows)]

		grid_index = 0
		down = True

		for i in msg:
			if m == 0:
				grid[grid_index].append(i)
				c_log += ('  ' * grid_index) + i + '\n'
			else:
				grid[grid_index].append(' ')

			if grid_index == rows-1:
				down = False
			elif grid_index == 0:
				down = True

			if down:
				grid_index += 1
			else:
				grid_index -= 1

		if m == 0:
			for row in grid:
				for i in row:
					new_msg += i

			for i in range(rows):
				c_log += '\nRow ' + str(i+1) + ': ' + re.sub('\[|\]', '', str(grid[i]))

		else:
			index = 0
			for row in grid:
				for i in range(0, len(row)):
					row[i] = msg[index]
					index += 1

			for i in range(rows):
				c_log += '\nRow ' + str(i+1) + ': ' + re.sub('\[|\]', '', str(grid[i]))

			down = True
			row_ind, col_ind = 0, 0

			for l in range(len(msg)):
				char = '*'
				col_ind = 0
				
				for i in grid[row_ind]:
					if not i == '*':
						new_msg += i
						grid[row_ind][grid[row_ind].index(i)] = '*'
						break

				if row_ind == rows-1:
					down = False
				elif row_ind == 0:
					down = True

				if down:
					row_ind += 1
				else:
					row_ind -= 1

		self.log.setPlainText(c_log)
		self.message_edit.setPlainText(new_msg)


	def encipher(self):
		msg = self.message_edit.toPlainText()

		if not self.valid_input(msg):
			return

		rbtn_name = self.radio_group.checkedButton().text()

		if rbtn_name == 'Ceasar Cipher':
			self.ceasar_function(0, msg)
		elif rbtn_name == 'Vigenere Cipher':
			self.vigenere_function(0, msg)
		elif rbtn_name == 'Playfair Cipher':
			self.playfair_function(0, msg)
		elif rbtn_name == 'Railfence Cipher':
			self.railfence_function(0, msg)


	def decipher(self):
		msg = self.message_edit.toPlainText()

		if not self.valid_input(msg):
			return

		rbtn_name = self.radio_group.checkedButton().text()

		if rbtn_name == 'Ceasar Cipher':
			self.ceasar_function(1, msg)
		elif rbtn_name == 'Vigenere Cipher':
			self.vigenere_function(1, msg)
		elif rbtn_name == 'Playfair Cipher':
			self.playfair_function(1, msg)
		elif rbtn_name == 'Railfence Cipher':
			self.railfence_function(1, msg)


	def valid_input(self, msg):
		if len(msg.strip()) == 0:
			QMessageBox.about(self, 'Oops', 'Empty message!')
			self.message_edit.setPlainText('')
			return False

		if self.radio_group.checkedButton().text() == "Railfence Cipher":
			return True

		if not all(i.isalpha() or i.isspace() for i in msg):
			QMessageBox.about(self, 'Oops', 'Message cannot contain special characters or numbers!')
			return False

		return True


if __name__ == '__main__':
	
	app = QApplication(sys.argv)
	runapp = ciphering_app()
	sys.exit(app.exec_())

# END OF CODE
