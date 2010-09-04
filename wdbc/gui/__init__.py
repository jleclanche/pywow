#!/usr/bin/python
# -*- coding: utf-8 -*-

import operator
import os
import signal
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from binascii import hexlify
from optparse import OptionParser
from pywow import wdbc

arguments = OptionParser()
arguments.add_option("-b", "--build", type="int", dest="build", default=0)
arguments.add_option("--get", action="store_true", dest="get", help="get from the environment")


def main():
	signal.signal(signal.SIGINT, signal.SIG_DFL)
	app = QApplication(sys.argv)
	args, name = arguments.parse_args(sys.argv[1:])
	name = name[0]
	if args.get:
		file = wdbc.get(name, build=args.build)
	else:
		file = wdbc.fopen(name, build=args.build)
	
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
		
		self.statusbar = QStatusBar()
		self.setStatusBar(self.statusbar)
	
	def setFile(self, file, name):
		self.setWindowTitle("%s - Sigrie Reader" % (name))
		self.maintable.model.setFile(file)
		msg = "%i rows - Using %s build %i" % (len(file), file.structure, file.build)
		self.statusbar.showMessage(msg)


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
