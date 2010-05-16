#!/usr/bin/python
# -*- coding: utf-8 -*-

import operator
import os
import signal
import sys

from binascii import hexlify
from PyQt4 import QtCore, QtGui

from pywow import wdbc

def main():
	signal.signal(signal.SIGINT, signal.SIG_DFL)
	app = QtGui.QApplication(sys.argv)
	
	name = sys.argv[1]
	build = len(sys.argv) > 2 and int(sys.argv[2]) or 0
	try:
		file = wdbc.fopen(name, build=build)
	except Exception, e:
		print "%s could not be read: %s" % (name, e)
		exit(1)
	
	w = MainWindow()
	w.setFile(file, name)
	w.show()
	sys.exit(app.exec_())


class MainWindow(QtGui.QMainWindow):
	def __init__(self, *pargs):
		QtGui.QMainWindow.__init__(self, *pargs)
		self.resize(1332, 886)
		
		exit = QtGui.QAction(QtGui.QIcon('icons/exit.png'), 'Exit', self)
		exit.setShortcut('Ctrl+Q')
		exit.setStatusTip('Exit application')
		self.connect(exit, QtCore.SIGNAL('triggered()'), QtCore.SLOT('close()'))
		
		menubar = self.menuBar()
		mfile = menubar.addMenu('&File')
		mfile.addAction(exit)
		
		
		self.centralwidget = QtGui.QWidget(self)
		self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
		
		self.maintable = MainTable(self.centralwidget)
		
		self.verticalLayout.addWidget(self.maintable)
		self.setCentralWidget(self.centralwidget)
	
	def setFile(self, file, name):
		self.setWindowTitle("%s - Sigrie Reader" % (name))
		self.maintable.model.setFile(file)


class MainTable(QtGui.QWidget):
	def __init__(self, *pargs):
		QtGui.QWidget.__init__(self, *pargs)
		
		# create table
		#self.get_table_data()
		table = self.createTable()
		
		# layout
		layout = QtGui.QVBoxLayout()
		layout.addWidget(table)
		self.setLayout(layout)
	
	def createTable(self):
		# create the view
		tv = QtGui.QTableView()
		
		# set the table model
		self.model = MainTableModel(self)
		tv.setModel(self.model)
		
		# set the minimum size
		tv.setMinimumSize(400, 300)
		
		# hide grid
#		tv.setShowGrid(False)
		
		# hide vertical header
		vh = tv.verticalHeader()
		vh.setVisible(True)
		
		# set horizontal header properties
		hh = tv.horizontalHeader()
#		hh.setStretchLastSection(True)
		
		# enable sorting
		tv.setSortingEnabled(True)

		return tv


class MainTableModel(QtCore.QAbstractTableModel):
	def __init__(self, *pargs):
		super(MainTableModel, self).__init__(*pargs)
		self.table_data = []
		self.header_data = []
	
	def setFile(self, file):
		self.emit(QtCore.SIGNAL("layoutAboutToBeChanged()"))
		self.table_data = file.rows()
		self.header_data = file.structure.column_names
		self.structure = file.structure
		self.emit(QtCore.SIGNAL("layoutChanged()"))
	
	def rowCount(self, parent):
		return len(self.table_data)

	def columnCount(self, parent):
		return len(self.header_data)
	
	def data(self, index, role):
		if not index.isValid():
			return QtCore.QVariant()
		elif role != QtCore.Qt.DisplayRole:
			return QtCore.QVariant()
		
		cell = self.table_data[index.row()][index.column()]
		field = self.structure[index.column()]
		if isinstance(field, wdbc.structures.HashField) or isinstance(field, wdbc.structures.DataField):
			cell = hexlify(cell)
		if isinstance(cell, str) and len(cell) > 200:
			cell = cell[:200] + "..."
		return QtCore.QVariant(cell)
	
	def headerData(self, col, orientation, role):
		if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
			return QtCore.QVariant(self.header_data[col])
		return QtCore.QAbstractTableModel.headerData(self, col, orientation, role)
	
	def sizeHintForRow(self, row):
		return 20

	def sort(self, Ncol, order):
		self.emit(QtCore.SIGNAL("layoutAboutToBeChanged()"))
		self.table_data = sorted(self.table_data, key=operator.itemgetter(Ncol))
		if order == QtCore.Qt.AscendingOrder:
			self.table_data.reverse()
		self.emit(QtCore.SIGNAL("layoutChanged()"))


if __name__ == "__main__":
	main()
