var SigrieFilters = function() {
	var that = this // Don't ask.
	
	this.maximumFilters = 12
	
	this.init = function() {
		// Find or create the required DOM elements
		this.filterbox = document.getElementById("filterbox")
		this.filterContainer = document.getElementById("filters")
		this.apply = document.createElement("button")
		this.add = document.createElement("button")
		
		if (this.filterbox == null) return false;
		
		if (typeof(currentURL) == "undefined") new URL(document.location.href);
		
		this.filters = []
		
		this.apply.textContent = this.apply.innerText = "Apply filters"
		this.apply.onclick = function() {
			that.submitFilters()
			return false
		}
		this.apply.style.display = "none"
		this.filterbox.appendChild(this.apply)

		this.add.textContent = this.add.innerText = "Add filter"
		this.add.onclick = function() {
			that.addFilter()
			return false
		}
		this.filterbox.appendChild(this.add)
		
		if (this.filterbox.getAttribute("searchtype") == "all") {
			// "Nerf /search/"
			this.hookTabs()
			this.masterTypes = sigrieDefinitions["quest"]
		}
		else {
			// Repopulate the filters
			this.masterTypes = sigrieDefinitions[this.filterbox.getAttribute("searchtype")]
			this.repopulateFilters()
		}
	}
	
	this.repopulateFilters = function() {
		if (this.searching) return; // Searching + repopulation = bad idea!
		for (var key in currentURL.query) {
			var match = null
			var filterid = -1
			var value = currentURL.query[key]
			var types = this.masterTypes
			var fields = []
			var fKey = false
			var negate = false
			
			if (match = key.match(/^(.+)__not$/i)) {
				negate = true
				key = match[1]
			}
			
			while (match = key.match(/([\w_]+?)(?:__|$)/)) { // Buffer the fields first
				fields.push(match[1])
				key = key.substr(match[0].length)
			}
			
			for (var fieldid = 0; fieldid < fields.length; fieldid++) {
				var field = fields[fieldid]
				var last = (fieldid == fields.length - 1)
				var found = false
				if (!types) break;
				
				if (field == "pk") {
					for (var j in types) {
						if ((typeof(types[j].primaryKey) == "boolean") && (types[j].primaryKey === true)) {
							field = j
							break
						}
					}
				}
				if ((!found) && (typeof(types[field]) != "object")) { // Is this an undefined field?
					for (var j in types) {
						if ((typeof(types[j].dbColumn) == "string") && (types[j].dbColumn == field) && (types[j].type == "foreignKey")) {
							field = j
							found = true
							break
						}
					}
					if ((!found) && (match = field.match(/^(.+)_id$/i))) { // Couldn't find any defined keys to use, let's see if it looks like any we know
						if ((typeof(types[match[1]]) == "object") && (types[match[1]].type == "foreignKey")) {
							found = true
							field = match[1]
						}
					}
				}
				
				if (typeof(types[field]) == "object") {
					if (filterid < 0) {
						filterid = this.addFilter(false)
					}
					this.addField(filterid, types, field, false)
					
					types = types[field]
					if (types.type == "foreignKey") {
						types = sigrieDefinitions[types.key]
						fKey = true
					}
					
					this.filters[filterid].value.value = value
					this.filters[filterid].negater.checkbox.checked = negate
				}
				else if (fKey) { // We've just been looking at foreign field, and we can't find this field... Default!
					for (var j in types) { // Find a primary key
						if ((typeof(types[j].primaryKey) == "boolean") && (types[j].primaryKey === true)) {
							fields.splice(fieldid, 1, j, field)
							fieldid--
							break
						}
					}
					fKey = false
				}
				else if ((last) && (filterid >= 0)) { // It's likely a modifier, "gt" "lte" "imatches" etc
					this.setModifierValue(filterid, field)
					found = true
					fKey = false
				}
				else { // No idea what it is, let's get the hell out of here
// 					alert("Unknown field '" + field + "', filterid #" + filterid);
					fKey = false
					break
				}
			}
			
			if (fKey) { // Finish up default/primary keys
				for (var j in types) {
					if ((typeof(types[j].primaryKey) == "boolean") && (types[j].primaryKey === true)) {
						this.addField(filterid, types, j, false)
						this.filters[filterid].value.value = value
						break
					}
				}
			}
		}
	}

	this.addFilter = function(populate) {
		if (typeof(populate) != "boolean") populate = true;

		var filter = {
			"div": document.createElement("div"),
			"fields": [],
			"value": document.createElement("input"),
			"remove": document.createElement("button"),
			"modifier": false,
			"negater": {
				"checkbox": document.createElement("input"),
				"label": document.createElement("label")
			}
		}
		var id = this.filters.push(filter) - 1
		
		filter.div.className = "filter"
		filter.remove.textContent = filter.remove.innerText = "Delete"
		filter.remove.onclick = function() { that.removeFilter(id) }
		
		filter.negater.checkbox.id = "filter" + id + "neg"
		filter.negater.checkbox.type = "checkbox"
		filter.negater.label.htmlFor = "filter" + id + "neg"
		filter.negater.label.textContent = filter.negater.label.innerText = "Negate"

		filter.div.appendChild(filter.value)
		filter.div.appendChild(filter.negater.checkbox)
		filter.div.appendChild(filter.negater.label)
		filter.div.appendChild(filter.remove)
		this.filterContainer.appendChild(filter.div)
		
		if (populate) {
			this.addField(id, this.masterTypes)
		}
		
		this.countFilters()
		
		return id
	}
	
	this.removeFilter = function(filterid) {
		var filter = this.filters[filterid]
		if (filter.fields.length > 0) this.removeField(filterid, 0); // Dispose properly
		this.filterContainer.removeChild(filter.div)
		this.filters[filterid] = false

		
		this.countFilters()
	}
	
	this.addField = function(filterid, types, value, addFields) {
		if (typeof(addFields) != "boolean") addFields = true;
		var filter = this.filters[filterid]
		var field = document.createElement("select")
		var fieldid = filter.fields.push({"element": field, "types": types}) - 1
		
		this.setModifier(filterid, "")
		field.onchange = function() {
			that.onFieldChange(filterid, fieldid)
		}
		
		for (var key in types) {
			var option = document.createElement("option")
			
			option.value = key
			option.textContent = option.innerText = types[key].name
			if ((typeof(value) != "undefined") && (value == key)) option.selected = true
			
			field.appendChild(option)
		}
		
		filter.div.insertBefore(field, filter.value)
		this.onFieldChange(filterid, fieldid, addFields)

		return fieldid
	}
	
	this.removeField = function(filterid, fieldid) {
		var filter = this.filters[filterid]
		
		while (fieldid < filter.fields.length) {
			var field = filter.fields.pop()
			filter.div.removeChild(field.element)
		}
	}
	
	this.onFieldChange = function(filterid, fieldid, addFields) {
		if (typeof(addFields) != "boolean") addFields = true;
		var filter = this.filters[filterid]
		var field = filter.fields[fieldid]
		var oldType = "string"
		var type = field.types[field.element.value]
		
		if (fieldid < filter.fields.length) this.removeField(filterid, fieldid + 1);
		
		if (typeof(filter.value.type) == "string") oldType = filter.value.type;
		
		if (type.type == "foreignKey") {
			if (addFields) this.addField(filterid, sigrieDefinitions[type.key])
		}
		else if (typeof(type.choices) != "object") {
			this.setValueType(filterid, "input")
			this.setModifier(filterid, type.type)
			
			if (typeof(type.size) == "number") filter.size = type.size
			if (typeof(type.maxLength) == "number") filter.maxLength = type.maxLength
			
			if ((type.type != oldType) || (!type.validator(type, filter.value.value))) {
				filter.value.value = type["default"]
			}
		}
		else {
			var choices = type.choices
			this.setValueType(filterid, "select")
			this.setModifier(filterid, "")
			
			for (var key in choices) {
				var option = document.createElement("option")
				
				option.value = choices[key].value
				option.textContent = option.innerText = choices[key].name
				
				if ((typeof(type["default"]) != "undefined") && (type["default"] == choices[key].value)) {
					option.selected = true
				}
				
				filter.value.appendChild(option)
			}
		}
	}
	
	this.setValueType = function(filterid, type) { // Supported types: "input", "select"
		var filter = this.filters[filterid]
		var oldType = filter.value.nodeName
		
		if (oldType != type) {
			var value = document.createElement(type)
			filter.div.replaceChild(value, filter.value)
			filter.value = value
		}
		
		if (type == "select") { // Empty out select elements
			while (filter.value.firstChild) {
				filter.value.removeChild(filter.value.firstChild)
			}
		}
		
		if (typeof(value.onkeyup) != "function") {
			value.onkeyup = this.valueKeyPress
		}
		if (typeof(value.onblur) != "function") {
			value.onblur = function() { that.revalidateFilter(filterid) }
		}
	}
	
	this.setModifierValue = function(filterid, value) {
		var filter = this.filters[filterid]
		if (!filter.modifier) return;
		var options = filter.modifier.getElementsByTagName("option")
		
		for (var i in options) {
			var option = options[i]
			option.selected = (option.value == value)
		}
	}
	
	this.setModifier = function(filterid, type) {
		var filter = this.filters[filterid]
		var visible = (type == "integer") || (type == "string")
		
		if ((visible) && (!filter.modifier)) { // It's not currently visible, but we want it to be
			filter.modifier = document.createElement("select")
			filter.div.insertBefore(filter.modifier, filter.value)
		}
		else if ((!visible) && (filter.modifier)) { // It's visible, but we don't want it to be
			filter.div.removeChild(filter.modifier)
			filter.modifier = false
		}
		else if ((visible) && (filter.modifier)) { // We want it, and it's there, but clear it first
			while (filter.modifier.firstChild) {
				filter.modifier.removeChild(filter.modifier.firstChild)
			}
		}
		
		if (!visible) return;
		
		if (type == "integer") {
			var options = [
				{"value": "", "name": "Equal to"},
				{"value": "gt", "name": "Greater than"},
				{"value": "lt", "name": "Lesser than"},
				{"value": "gte", "name": "Greater than or equals"},
				{"value": "lte", "name": "Lesser than or equals"},
				{"value": "band", "name": "Binary AND"},
				{"value": "in", "name": "In"}
			] // Done differently than expected because "what the hell there's a blank name?!"
			for (var i in options) {
				var option = document.createElement("option")
				option.value = options[i].value
				option.textContent = option.innerText = options[i].name
				filter.modifier.appendChild(option)
			}
		}
		else if (type == "string") {
			var options = {
				"Case insensitive": {
					"imatches": "Contains words",
					"icontains": "Contains string",
					"istartswith": "Starts with",
					"iendswith": "Ends with",
					"iexact": "Exactly matches",
					"iregex": "Matches regex"
				},
				"Case sensitive": {
					"matches": "Contains words",
					"contains": "Contains string",
					"startswith": "Starts with",
					"endswith": "Ends with",
					"exact": "Exactly matches",
					"regex": "Matches regex"
				},
				"Miscellaneous": {
					"in": "In"
				}
			}
			for (var group in options) {
				var optgroup = document.createElement("optgroup")
				optgroup.label = group
				for (var key in options[group]) {
					var option = document.createElement("option")
					option.value = key
					option.textContent = option.innerText = options[group][key]
					optgroup.appendChild(option)
				}
				filter.modifier.appendChild(optgroup)
			}
		}
	}

	this.submitFilters = function() {
		var cancel = false
		var url = new URL(document.location.href)
		url.clear("query")
		
		for (var filterid in this.filters) {
			var filter = this.filters[filterid]
			if (filter) {
				var name = ""
				var value = filter.value.value
				
				if (value.length > 0) {
					for (var fieldid in filter.fields) {
						var field = filter.fields[fieldid]
						if (name.length > 0) name += "__"
						name += field.element.value
					}
					
					if (!this.revalidateFilter(filterid)) {
						cancel = true
					}
					
					if ((filter.modifier) && (filter.modifier.value.length > 0)) {
						name += "__" +filter.modifier.value
					}
					
					if (filter.negater.checkbox.checked) name += "__not";
					
					url.setKey("query", name, value)
				}
			}
		}
		
		if (!cancel) {
			document.location.href = url.toString()
		}
	}
	
	this.valueKeyPress = function(event) { // I. Hate. Browser wars.
		if (typeof(event) != "object") event = window.event; // Hello, Microsoft!
		var key = 0
		
		if (typeof(event.keyCode) != "undefined") key = event.keyCode;
		if (typeof(event.which) != "undefined") key = event.which;
		
		if (key == 13) { // Enter
			that.submitFilters() // That not this... Yeah.
		}
	}
	
	this.revalidateFilter = function(filterid) {
		var filter = this.filters[filterid]
		var field = filter.fields[filter.fields.length - 1]
		var type = field.types[field.element.value]
		var valid = type.validator(type, filter.value.value, filter.modifier.value)
		
		if (valid) {
			filter.value.className = ""
		} else {
			filter.value.className = "invalid"
		}
		
		return valid
	}
	
	this.clearFilters = function() {
		for (var filterid in this.filters) {
			var filter = this.filters[filterid]
			if (typeof(filter) == "object") {
				this.removeFilter(filterid)
			}
		}
		this.filters = []
	}
	
	this.hookTabs = function() {
		if (typeof(tvlib) != "object") return;
		if (typeof(tvlib.onTabClick) != "function") return; // Just to be safe.
		var old = tvlib.onTabClick;
		tvlib.onTabClick = function(self, silent) {
			old(self, silent)
			that.clearFilters()
			var match = self.id.match(/tab_(\w+)/i)
			if (typeof(sigrieDefinitions[match[1]]) == "object") {
				that.masterTypes = sigrieDefinitions[match[1]]
				that.filterbox.style.display = ""
			}
			else {
				that.filterbox.style.display = "none"
			}
		}
	}
	
	this.countFilters = function(silent) {
		var count = 0
		
		for (i in this.filters) {
			var filter = this.filters[i]
			if (typeof(filter) == "object") count++
		}
		
		if ((typeof(silent) != "boolean") || (silent === false)) {
			if (count > 0) {
				this.apply.style.display = ""
			}
			else {
				this.apply.style.display = "none"
			}
			
			if (count < this.maximumFilters) {
				this.add.style.display = ""
			}
			else {
				this.add.style.display = "none"
			}
		}
		
		return count
	}
}

sigrieFilters = new SigrieFilters()
addLoadEvent(function(){sigrieFilters.init()}); // Because otherwise we have a fight over 'this'