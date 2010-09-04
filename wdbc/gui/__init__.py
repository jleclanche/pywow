#!/usr/bin/python
# -*- coding: utf-8 -*-

import operator
import os
import signal
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from binascii import hexlify
from pywow import wdbc

def main():
	signal.signal(signal.SIGINT, signal.SIG_DFL)
	app = QApplication(sys.argv)
	
	name = sys.argv[1]
	build = len(sys.argv) > 2 and int(sys.argv[2]) or 0
	file = wdbc.fopen(name, build=build)
	
	w = MainWindow()
	w.setFile(file, name)
	w.show()
	sys.exit(app.exec_())


class MainWindow(QMainWindow):
	def __init__(self, *pargs):
		QMainWindow.__init__(self, *pargs)
		self.resize(1332, 886)
		
		exit = QAction(QIcon("icons/exit.png"), "Exit", self)
		exit.setShortcut("Ctrl+Q")
		exit.setStatusTip("Exit application")
		self.connect(exit, SIGNAL("triggered()"), SLOT("close()"))
		
		open = QAction(QIcon("icons/open.png"), "Open", self)
		open.setShortcut("Ctrl+O")
		open.setStatusTip("Open a new file")
		openFileDialog = QFileDialog()
		openFileDialog.connect(open, SIGNAL("triggered()"), SLOT("open()"))
		
		menubar = self.menuBar()
		mfile = menubar.addMenu("&File")
		mfile.addAction(open)
		mfile.addAction(exit)
		
		self.centralwidget = QWidget(self)
		self.verticalLayout = QVBoxLayout(self.centralwidget)
		
		self.maintable = MainTable(self.centralwidget)
		
		self.verticalLayout.addWidget(self.maintable)
		self.setCentralWidget(self.centralwidget)
	
	def setFile(self, file, name):
		self.setWindowTitle("%s - Sigrie Reader" % (name))
		self.maintable.model.setFile(file)


class MainTable(QWidget):
	def __init__(self, *pargs):
		QWidget.__init__(self, *pargs)
		
		# create table
		#self.get_table_data()
		table = self.createTable()
		
		# layout
		layout = QVBoxLayout()
		layout.addWidget(table)
		self.setLayout(layout)
	
	def createTable(self):
		# create the view
		tv = QTableView()
		
		# set the table model
		self.model = MainTableModel(self)
		tv.setModel(self.model)
		
		# set the minimum size
		tv.setMinimumSize(400, 300)
		
		# hide vertical header
		vh = tv.verticalHeader()
		vh.setVisible(True)
		
		# set horizontal header properties
		hh = tv.horizontalHeader()
#		hh.setStretchLastSection(True)
		
		# enable sorting
		tv.setSortingEnabled(True)

		return tv


class MainTableModel(QAbstractTableModel):
	def __init__(self, *pargs):
		super(MainTableModel, self).__init__(*pargs)
		self.table_data = []
		self.header_data = []
	
	def setFile(self, file):
		self.emit(SIGNAL("layoutAboutToBeChanged()"))
		self.table_data = file.rows()
		self.header_data = file.structure.column_names
		self.structure = file.structure
		self.emit(SIGNAL("layoutChanged()"))
	
	def rowCount(self, parent):
		return len(self.table_data)

	def columnCount(self, parent):
		return len(self.header_data)
	
	def data(self, index, role):
		if not index.isValid():
			return QVariant()
		elif role != Qt.DisplayRole:
			return QVariant()
		
		cell = self.table_data[index.row()][index.column()]
		field = self.structure[index.column()]
		if isinstance(field, wdbc.structures.HashField) or isinstance(field, wdbc.structures.DataField):
			cell = hexlify(cell)
		if isinstance(cell, str) and len(cell) > 200:
			cell = cell[:200] + "..."
		return QVariant(cell)
	
	def headerData(self, col, orientation, role):
		if orientation == Qt.Horizontal and role == Qt.DisplayRole:
			return QVariant(self.header_data[col])
		return QAbstractTableModel.headerData(self, col, orientation, role)

	def sort(self, Ncol, order):
		self.emit(SIGNAL("layoutAboutToBeChanged()"))
		self.table_data = sorted(self.table_data, key=operator.itemgetter(Ncol))
		if order == Qt.AscendingOrder:
			self.table_data.reverse()
		self.emit(SIGNAL("layoutChanged()"))


if __name__ == "__main__":
	main()
