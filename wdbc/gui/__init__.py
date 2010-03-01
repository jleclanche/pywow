#!/usr/bin/python
# -*- coding: utf-8 -*-

import operator
import os
import signal
import sys

from binascii import hexlify
from PyQt4 import QtCore, QtGui

from pywow import wdbc, structures

fname = sys.argv[1]
build = len(sys.argv) > 2 and int(sys.argv[2]) or 0
try:
	f = wdbc.fopen(fname, build=build)
except Exception, e:
	print "%s could not be read: %s" % (fname, e)
	exit(1)
ARRAY = f.rows()

HEADER_DATA = f.structure.column_names

def main():
	signal.signal(signal.SIGINT, signal.SIG_DFL)
	app = QtGui.QApplication(sys.argv)
	w = MainWindow()
	w.show()
	w.setWindowTitle("%s - Sigrie Reader" % fname)
	sys.exit(app.exec_())


class MainWindow(QtGui.QMainWindow):
	def __init__(self, *args):
		QtGui.QMainWindow.__init__(self, *args)
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


class MainTable(QtGui.QWidget):
	def __init__(self, *args):
		QtGui.QWidget.__init__(self, *args)
		
		# create table
		#self.get_table_data()
		self.tabledata = ARRAY
		table = self.createTable()
		
		# layout
		layout = QtGui.QVBoxLayout()
		layout.addWidget(table)
		self.setLayout(layout)
	
	def createTable(self):
		# create the view
		tv = QtGui.QTableView()
		
		# set the table model
		header = HEADER_DATA
		tm = MainTableModel(self.tabledata, header, self) 
		tv.setModel(tm)
		
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
	def __init__(self, datain, header_data, parent=None, *args):
		QtCore.QAbstractTableModel.__init__(self, parent, *args)
		self.arraydata = datain
		self.header_data = header_data
	
	def rowCount(self, parent):
		return len(self.arraydata)

	def columnCount(self, parent):
		return len(self.header_data)
	
	def data(self, index, role):
		if not index.isValid():
			return QtCore.QVariant()
		elif role != QtCore.Qt.DisplayRole:
			return QtCore.QVariant()
		
		cell = self.arraydata[index.row()][index.column()]
		field = f.structure[index.column()]
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
		self.arraydata = sorted(self.arraydata, key=operator.itemgetter(Ncol))
		if order == QtCore.Qt.AscendingOrder:
			self.arraydata.reverse()
		self.emit(QtCore.SIGNAL("layoutChanged()"))


if __name__ == "__main__":
	main()

