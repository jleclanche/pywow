PAGE_SIZE = 50
var tablelib = {
	init: function() {
		secondDraw = false
		tablelib.tableData = {}
		tablelib.parseDocument()
	},
	parseDocument: function() {
		var tables = document.getElementsByTagName("table")
		for(var i = 0; i < tables.length; i++) {
			if(hasClass(tables[i], "sorttable")) {
				var data = null
				eval("if (typeof(" + tables[i].getAttribute("name") + ") == 'object') data = " + tables[i].getAttribute("name"))
				if ((data === null) || (data.length < 1)) continue; // No shoes? No shirt? No data? No service.
				
				var template = null
				eval("if (typeof(" + tables[i].getAttribute("template") + ") == 'object') template = " + tables[i].getAttribute("template"))
				if (template === null) {
					template = {'columns_shown': {}, 'column_names': {}, 'column_order': [], 'hooks': {}}
					
					for (var key in data[0]) {
						template.columns_shown[key] = true
						template.column_names[key] = key
						template.column_order.push(key)
						template.hooks[key] = false
					}
				}
				else if (typeof(template['extends']) == 'object') {
					for (var key in template['extends']) {
						if (typeof(template[key]) == 'undefined') template[key] = template['extends'][key];
					}
					template['extends'] = false
				}
				
				tablelib.tableData[tables[i].getAttribute("name")] = {elem: tables[i], data: data, filteredData: data, template: template}
				tablelib.buildTable(tables[i].getAttribute("name"))
			}
		}
	},
	addButton: function(text, name) {
		var btn = document.createElement("a")
		btn.className = "button inactive"
		btn.innerHTML = text
		btn.href = "javascript:;"
		btn.setAttribute("tblname", name)
		return btn
	},
	buildTable: function(name) {
		var table = tablelib.tableData[name]
		var options = tablelib.expandTableOptions(currentURL.getKey("hash", "table__" + name, ""))
		var element = tablelib.tableData[name].elem
		var data = tablelib.tableData[name].data
		var template = tablelib.tableData[name].template
		var columns = template["column_order"]
		var names = template["column_names"] || {}
		var shown = template["columns_shown"] || tablelib.buildColumnsShown(name)
		var hooks = template["hooks"] || {}
		var i
		var thead = document.createElement("thead")
		var headrow = document.createElement("tr")
		table.name = name
		table.sort = [{"name": columns[0], "descending": true}]
		tablelib.tableData[name].pageCount = Math.ceil(data.length / PAGE_SIZE)
		tablelib.tableData[name].currentPage = options.page
		for (i = 0; i < columns.length; i++) {
			if (shown[columns[i]] == false) continue;
			var th = document.createElement("th")
			var thlink = document.createElement("a")
			thlink.href = "javascript:;"
			thlink.setAttribute("tblname", name)
			thlink.setAttribute("colname", columns[i])
			thlink.onclick = function() {
				if (hasClass(this, "descending")) {
					removeClass(this, "descending")
					addClass(this, "ascending")
				} else if (hasClass(this, "ascending")) {
					removeClass(this, "ascending")
					addClass(this, "descending")
				} else {
					addClass(this, "descending")
				}
				var ths = headrow.getElementsByTagName("a")
				for (i = 0; i < ths.length; i++) {
					if (ths[i] == this) continue
					removeClass(ths[i], "descending")
					removeClass(ths[i], "ascending")
				}
				tablelib.sortData(tablelib.tableData[this.getAttribute("tblname")], this.getAttribute("colname"), hasClass(this, "descending"))
			}
			var headername = document.createTextNode(names[columns[i]] || columns[i])
			thlink.appendChild(headername)
			th.appendChild(thlink)
			headrow.appendChild(th)
		}
		thead.appendChild(headrow)
		tbody = document.createElement("tbody")
		element.appendChild(thead)
		element.appendChild(tbody)
		//create pagewidget
		var pageWidget = document.createElement("div")
		pageWidget.className = "sorttable-pagewidget"
		var pageCount = document.createElement("span")
		var firstButton = tablelib.addButton("« First", name)
		var prevButton = tablelib.addButton("‹ Prev", name)
		var nextButton = tablelib.addButton("Next ›", name)
		var lastButton = tablelib.addButton("Last »", name)
		table.firstButton = firstButton
		table.prevButton = prevButton
		table.nextButton = nextButton
		table.lastButton = lastButton
		table.pageCountWidget = pageCount
		firstButton.onclick = function() {
			if (hasClass(this, "inactive")) return;
			var table = tablelib.tableData[this.getAttribute("tblname")]
			table.currentPage = 1
			tablelib.drawTable(table)
			addClass(table.firstButton, "inactive")
			addClass(table.prevButton, "inactive")
			removeClass(table.nextButton, "inactive")
			removeClass(table.lastButton, "inactive")
			currentURL.setKey("hash", "table__" + this.getAttribute("tblname"), tablelib.compressTableOptions({"page": table.currentPage, "columns": table.sort}))
			document.location.href = currentURL
		}
		prevButton.onclick = function() {
			if (hasClass(this, "inactive")) return;
			var table = tablelib.tableData[this.getAttribute("tblname")]
			table.currentPage = table.currentPage - 1
			if (table.currentPage <= 1) {
				table.currentPage = 1
				addClass(table.firstButton, "inactive")
				addClass(table.prevButton, "inactive")
				removeClass(table.nextButton, "inactive")
				removeClass(table.lastButton, "inactive")
			} else if (table.currentPage < table.pageCount) {
				removeClass(table.nextButton, "inactive")
				removeClass(table.lastButton, "inactive")
			}
			tablelib.drawTable(table)
			currentURL.setKey("hash", "table__" + this.getAttribute("tblname"), tablelib.compressTableOptions({"page": table.currentPage, "columns": table.sort}))
			document.location.href = currentURL
		}
		lastButton.onclick = function() {
			if (hasClass(this, "inactive")) return;
			var table = tablelib.tableData[this.getAttribute("tblname")]
			table.currentPage = table.pageCount
			tablelib.drawTable(table)
			addClass(table.nextButton, "inactive")
			addClass(table.lastButton, "inactive")
			removeClass(table.prevButton, "inactive")
			removeClass(table.firstButton, "inactive")
			currentURL.setKey("hash", "table__" + this.getAttribute("tblname"), tablelib.compressTableOptions({"page": table.currentPage, "columns": table.sort}))
			document.location.href = currentURL
		}
		nextButton.onclick = function() {
			if (hasClass(this, "inactive")) return;
			var table = tablelib.tableData[this.getAttribute("tblname")]
			table.currentPage = table.currentPage + 1
			if (table.currentPage >= table.pageCount) {
				table.currentPage = table.pageCount
				addClass(table.nextButton, "inactive")
				addClass(table.lastButton, "inactive")
				removeClass(table.firstButton, "inactive")
				removeClass(table.prevButton, "inactive")
			} else if (table.currentPage > 1) {
				removeClass(table.firstButton, "inactive")
				removeClass(table.prevButton, "inactive")
			}
			tablelib.drawTable(table)
			currentURL.setKey("hash", "table__" + this.getAttribute("tblname"), tablelib.compressTableOptions({"page": table.currentPage, "columns": table.sort}))
			document.location.href = currentURL
		}
		pageWidget.appendChild(firstButton)
		pageWidget.appendChild(prevButton)
		pageWidget.appendChild(pageCount)
		pageWidget.appendChild(nextButton)
		pageWidget.appendChild(lastButton)
		if ((table.currentPage < table.pageCount) && (table.pageCount > 1)) {
			removeClass(nextButton, "inactive")
			removeClass(lastButton, "inactive")
		}
		if (table.currentPage > 1) {
			removeClass(prevButton, "inactive")
			removeClass(firstButton, "inactive")
		}
		element.parentNode.insertBefore(pageWidget, element)
		var searchbox = document.getElementById(name + "-searchbox")
		if (searchbox) {
			searchbox.onkeyup = function() {
				tablelib.filterTable(table, this.value)
			}
		}
		tablelib.drawTable(table)
		for (var i in options.columns) {
			var column = options.columns[i]
			tablelib.sortData(table, column.name, column.descending)
		}
	},
	sortData: function(table, col, descending, silent) {
		if (typeof(silent) == "undefined") silent = false;
		sortcol = col
		table.filteredData.sort(tablelib.sortFunc)
		table.sort = [{"name": col, "descending": descending}] // TODO: Multiple sorts
		if (!descending) {
			table.filteredData.reverse()
		}
		tablelib.drawTable(table)
		if (!silent) {
			currentURL.setKey("hash", "table__" + table.name, tablelib.compressTableOptions({"page": table.currentPage, "columns": table.sort}))
			document.location.href = currentURL.toString()
		}
	},
	filterTable: function(table, filter) {
		table.filteredData = []
		table.currentPage = 1
		for (var i = 0; i < table.data.length; i++) {
			if (table.data[i].name.toLowerCase().match(filter.toLowerCase())!=null) {
				table.filteredData.push(table.data[i])
			}
		}
		table.pageCount = Math.ceil(table.filteredData.length / PAGE_SIZE)
		tablelib.drawTable(table)
	},
	getPageRange: function(table) {
		if (table.currentPage == table.pageCount) return (((table.currentPage-1)*PAGE_SIZE)+1) + "-" + table.filteredData.length  + " (" + table.filteredData.length + " total)"
		else if (table.filteredData.length == 0) return "0 - 0 (0 total)"
		else return (((table.currentPage-1)*PAGE_SIZE)+1) + "-" + (table.currentPage*PAGE_SIZE) + " (" + table.filteredData.length + " total)"
	},
	drawTable: function(table) {
		var element = table.elem
		var columns = table.template["column_order"]
		var shown = table.template["columns_shown"]
		var hooks = table.template["hooks"] || {}
		var tbody = element.getElementsByTagName("tbody")[0]
		var trs = tbody.childNodes
		table.pageCountWidget.innerHTML = tablelib.getPageRange(table)
		while (trs.length > 0) tbody.removeChild(trs[0])
		for (var d = ((table.currentPage-1)*PAGE_SIZE)+1; d <= table.filteredData.length && d < table.currentPage*PAGE_SIZE; d++) {
			var obj = table.filteredData[d-1]
			if (!obj) continue;
			if (!obj["elem"]) {
				var tr = document.createElement("tr")
				for (var c in columns) {
					if (shown[columns[c]] == false) continue;
					var td = document.createElement("td")
					if (hooks[columns[c]]) td = hooks[columns[c]](obj[columns[c]], td, obj, obj["id"])
					else td.innerHTML = obj[columns[c]]
					tr.appendChild(td)
				}
				obj["elem"] = tr
				tbody.appendChild(tr)
			} else tbody.appendChild(obj["elem"])
		}
	},
	sortFunc: function(ai, bi) {
		var a = ai[sortcol]
		var b = bi[sortcol]
		if (typeof(a) == "string") {
			if (a.toLowerCase() > b.toLowerCase()) return 1
			else if (a.toLowerCase() == b.toLowerCase()) return 0
			else return -1
		} else if (typeof(a) == "number") {
			return a-b
		}
	},
	expandTableOptions: function(serial) {
		var result = {'page': 1, 'columns': []}
		var match = 0
		
		if (match = serial.match(/(\d+):([\+\-,\w]*)/)) {
			result.page = parseInt(match[1])
			var columns = match[2]
			
			while (match = columns.match(/^([\+\-])(\w+),?/)) {
				var column = {'descending': (match[1] == '-'), 'name': match[2]}
				result.columns.push(column)
				columns = columns.substr(match[0].length)
			}
		}
		
		return result
	},
	compressTableOptions: function(options) {
		var columns = ""
		
		for (var i in options.columns) {
			var column = options.columns[i]
			if (columns.length > 0) columns += ",";
			if (column.descending) {
				columns += "-"
			} else {
				columns += "+"
			}
			columns += column.name
		}
		
		return options.page + ":" + columns
	},
	buildColumnsShown: function(name) {
		var template = tablelib.tableData[name].template
		var columns = template["column_order"]
		var data = tablelib.tableData[name].data
		var shown = {}
		
		for (var i = 0; i < columns.length; i++) {
			var column = columns[i]
			shown[column] = false
			for (var j = 0; j < data.length && !shown[column]; j++) {
				shown[column] = ((typeof(data[j][column]) != "undefined") && (data[j][column] != ""))
			}
		}
		
		tablelib.tableData[name].template.columns_shown = shown
		return shown
	}
}
addLoadEvent(tablelib.init)
