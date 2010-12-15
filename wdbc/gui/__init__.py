#!/usr/bin/python
# -*- coding: utf-8 -*-

import operator
import os
from binascii import hexlify
from optparse import OptionParser
from PySide.QtCore import *
from PySide.QtGui import *
from pywow import wdbc


class WDBCClient(QApplication):
	def __init__(self, argv):
		QApplication.__init__(self, argv)
		self.mainWindow = MainWindow()
		
		arguments = OptionParser()
		arguments.add_option("-b", "--build", type="int", dest="build", default=0)
		arguments.add_option("--get", action="store_true", dest="get", help="get from the environment")
		
		args, files = arguments.parse_args(argv[1:])
		
		for name in files:
			if args.get:
				file = wdbc.get(name, args.build)
			else:
				file = wdbc.fopen(name, args.build)
			
			self.mainWindow.setFile(file)

class MainWindow(QMainWindow):
	def __init__(self, *args):
		QMainWindow.__init__(self, *args)
		self.resize(1332, 886)
		self.setMinimumSize(640, 480)
		
		def openFile():
			filename, filters = QFileDialog.getOpenFileName(self, "Open file", "/var/www/sigrie/caches", "DBC/Cache files (*.dbc *.wdb *.db2 *.dba *.wcf)")
			file = wdbc.fopen(filename)
			self.setFile(file)
		
		def reopen():
			current = self.file.build
			build, ok = QInputDialog.getInt(self, "Reopen as build...", "Build number", value=current, minValue=-1)
			if ok and build != current:
				file = wdbc.fopen(self.file.file.name, build)
				self.setFile(file)
		
		fileMenu = self.menuBar().addMenu("&File")
		fileMenu.addAction("Open", openFile, "Ctrl+O")
		fileMenu.addAction("Reopen as build...", reopen, "Ctrl+B")
		fileMenu.addAction("Exit", self, SLOT("close()"), "Ctrl+Q")
		
		centralWidget = QWidget(self)
		self.setCentralWidget(centralWidget)
		
		verticalLayout = QVBoxLayout(centralWidget)
		self.maintable = MainTable(centralWidget)
		verticalLayout.addWidget(self.maintable)
	
	def setFile(self, file):
		self.file = file
		self.setWindowTitle("%s - Sigrie Reader" % (file.file.name))
		self.maintable.setFile(file)
		msg = "%i rows - Using %s build %i" % (len(file), file.structure, file.build)
		self.statusBar().showMessage(msg)


class MainTable(QWidget):
	def __init__(self, *args):
		QWidget.__init__(self, *args)
		
		# create table
		self.table = table = QTableView()
		table.setModel(TableModel(self))
		table.verticalHeader().setVisible(True)
		table.setSortingEnabled(True)
		
		# layout
		layout = QVBoxLayout()
		layout.addWidget(table)
		self.setLayout(layout)
	
	def setFile(self, file):
		return self.table.model().setFile(file)


class TableModel(QAbstractTableModel):
	def __init__(self, *args):
		QAbstractTableModel.__init__(self, *args)
		self.table_data = []
		self.header_data = []

	def columnCount(self, parent):
		return len(self.header_data)
	
	def rowCount(self, parent):
		return len(self.table_data)
	
	def data(self, index, role):
		if not index.isValid() or role != Qt.DisplayRole:
			return
		
		cell = self.table_data[index.row()][index.column()]
		field = self.structure[index.column()]
		if isinstance(field, wdbc.structures.HashField) or isinstance(field, wdbc.structures.DataField):
			cell = hexlify(cell)
		if isinstance(cell, str) and len(cell) > 200:
			cell = cell[:200] + "..."
		return cell
	
	def headerData(self, col, orientation, role):
		if orientation == Qt.Horizontal and role == Qt.DisplayRole:
			return self.header_data[col]
		return QAbstractTableModel.headerData(self, col, orientation, role)
	
	def setFile(self, file):
		self.emit(SIGNAL("layoutAboutToBeChanged()"))
		self.table_data = file.rows()
		self.header_data = file.structure.column_names
		self.structure = file.structure
		self.emit(SIGNAL("layoutChanged()"))

	def sort(self, column, order):
		self.emit(SIGNAL("layoutAboutToBeChanged()"))
		self.table_data = sorted(self.table_data, key=operator.itemgetter(column))
		if order == Qt.AscendingOrder:
			self.table_data.reverse()
		self.emit(SIGNAL("layoutChanged()"))


def main():
	import signal
	import sys
	signal.signal(signal.SIGINT, signal.SIG_DFL)
	app = WDBCClient(sys.argv)
	
	app.mainWindow.show()
	sys.exit(app.exec_())

if __name__ == "__main__":
	main()
