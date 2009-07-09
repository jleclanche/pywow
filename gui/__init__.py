#!/usr/bin/python
# -*- coding: utf-8 -*-

import operator
import os
import sys

from PyQt4 import QtCore, QtGui

import wdbc

#fname = "/home/adys/bin/reader/DBFilesClientOriginal/MailTemplate.dbc"
#fname = "/home/adys/wow/Cache/WDB/enGB/itemcache.wdb"
#fname = "/home/adys/bin/reader/DBFilesClientOriginal/Spell.dbc"
fname = sys.argv[1]
build = len(sys.argv) > 2 and int(sys.argv[2]) or 0
f = wdbc.fopen(fname, build=build)
_array = f.rows()
headerdata = f.structure.column_names


def main():
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
		self.tabledata = _array
		table = self.createTable()
		
		# layout
		layout = QtGui.QVBoxLayout()
		layout.addWidget(table)
		self.setLayout(layout)
	
	def createTable(self):
		# create the view
		tv = QtGui.QTableView()
		
		# set the table model
		header = headerdata
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
	def __init__(self, datain, headerdata, parent=None, *args):
		QtCore.QAbstractTableModel.__init__(self, parent, *args)
		self.arraydata = datain
		self.headerdata = headerdata
	
	def rowCount(self, parent):
		return len(self.arraydata)

	def columnCount(self, parent):
		return len(self.arraydata[0])
	
	def data(self, index, role):
		if not index.isValid():
			return QtCore.QVariant()
		elif role != QtCore.Qt.DisplayRole:
			return QtCore.QVariant()
		return QtCore.QVariant(self.arraydata[index.row()][index.column()])
	
	def headerData(self, col, orientation, role):
		if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
			return QtCore.QVariant(self.headerdata[col])
		return QtCore.QAbstractTableModel.headerData(self, col, orientation, role)
	
	def sizeHintForRow(self, row):
		return 20

	def sort(self, Ncol, order):
		self.emit(QtCore.SIGNAL("layoutAboutToBeChanged()"))
		self.arraydata = sorted(self.arraydata, key=operator.itemgetter(Ncol))
		if order == QtCore.Qt.AscendingOrder:
			self.arraydata.reverse()
		self.emit(QtCore.SIGNAL("layoutChanged()"))


class TableView(QtGui.QTableView):
	def verticalHeader(self, col):
		return "Foo"
	
	def sizeHintForRow(self, row):
		return 20


if __name__ == "__main__":
	main()

