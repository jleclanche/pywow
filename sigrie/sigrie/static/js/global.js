var onloads = []
var tabQueue = []

function toggle(a, b) {
	if(a) document.getElementById(a).style.display = document.getElementById(a).style.display == "none" ? "block" : "none"
	if(b) document.getElementById(b).style.display = document.getElementById(b).style.display == "none" ? "block" : "none"
}

function trim(str) {
	var str = str.replace(/^\s\s*/, '')
	var i = str.length
	while (/\s/.test(str.charAt(--i)));
	return str.slice(0, i + 1)
}

function addLoadEvent(func) {
	onloads.push(func)
}

function triggerLoadEvents() {
	for (var i = 0; i < onloads.length; i++) {
		onloads[i]()
	}
	
	var search = document.getElementById('searchbar')
	if ((typeof(search) != 'undefined') && (search != null)) {
		search.onfocus = search.onblur = function() {
			if (this.value.length == 0) {
				addClass(this, 'emptytext')
			}
			else {
				removeClass(this, 'emptytext')
			}
		}
		search.onblur()
	}
}

function hasClass(object, cls) {
	var classes = object.className.split(" ")
	for (var i = 0; i < classes.length; i++) {
		if (cls == classes[i]) return true;
	}
	return false
}

function addClass(object, cls) {
	var classes = object.className.split(" ")
	for (var i = 0; i < classes.length; i++) {
		if (cls == classes[i]) return;
	}
	classes.push(cls)
	var className = ""
	for (i = 0; i < classes.length; i++) {
		className = className + " " + classes[i]
	}
	object.className = className.replace(/^\s\s*/, '').replace(/\s\s*$/, '')
}

function removeClass(object, cls) {
	var classes = object.className.split(" ")
	var className = ""
	for (i = 0; i < classes.length; i++) {
		if (cls == classes[i]) continue;
		className = className + " " + classes[i]
	}
	object.className = className.replace(/^\s\s*/, '').replace(/\s\s*$/, '')
}

function addTab(id, name) {
	tabQueue.push({'id': id, 'name': name})
}

function initTabs() {
	var tabTarget = document.getElementById("dview-content")
	var tabBar = document.createElement("div")
	var tabView = document.createElement("div")
	
	tabView.appendChild(tabBar)
	tabTarget.appendChild(tabView)
	
	addClass(tabView, "tabview")
	tabView.style.clear = "right"
	
	while(tabQueue.length > 0) {
		var cur = tabQueue.pop()
		var tab = document.createElement("div")
		var content = document.createElement("div")
		var table = document.createElement("table")
		var pageTop = document.createElement("div")
		var pageBottom = document.createElement("div")
		
		addClass(tab, "tabbutton")
		tab.id = "tab_" + cur.id
		tab.textContent = tab.innerText = cur.name
		
		addClass(content, "tabcontent")
		addClass(content, "tableview-container")
		content.id = "tab_" + cur.id + "_content"
		content.style.display = "none"
		
		addClass(table, "sorttable")
		table.setAttribute("name", cur.id)
		table.setAttribute("template", "template_"+cur.id) // XXX shouldn't need prefix
		
		addClass(pageTop, "tableview-pagewidget")
		addClass(pageBottom, "tableview-pagewidget")
		
		if (tabBar.childNodes.length > 0) {
			tabBar.insertBefore(tab, tabBar.firstChild)
		}
		else {
			tabBar.appendChild(tab)
		}
		tabView.appendChild(content)
		content.appendChild(table)
	}
}

function showLinkString(color, linkString, content) {
	var s = "/script print('Shift click to link:', '\\124c" + color + "\\124H" + linkString + "\\124h[" + content + "]\\124h\\124r')"
	prompt("Copy the following in game.", s) // \nOr try the addon! http://sigrie.com/about/findit
}

function showLinkRaw(text) {
	var s = "/script _=" + text + ";print('Shift click to link:', _)"
	prompt("Copy the following in game.", s) // \nOr try the addon! http://sigrie.com/about/findit
}

function getOffsetTop(element, stopElement) {
	var top = element.offsetTop
	
	while ((typeof(element.offsetParent) == "object") && (element.offsetParent != null) && (element.offsetParent != stopElement)) {
		element = element.offsetParent
		if (typeof(element.offsetTop) == "number") top += element.offsetTop
	}
	
	return top
}

function getOffsetLeft(element, stopElement) {
	var left = element.offsetLeft
	
	while ((typeof(element.offsetParent) == "object") && (element.offsetParent != null) && (element.offsetParent != stopElement)) {
		element = element.offsetParent
		if (typeof(element.offsetTop) == "number") left += element.offsetLeft
	}
	
	return left
}

function setImageSrc(img, url) {
	if (img.src == url) return false;
	img.src = url
}

function URL(inputURL) {
	var DEFAULT_HTTP_PORT = 80
	
	this.query = {}
	this.hash = {}
	this.url = {}
	
	this.validateType = function(type, name) {
		if ((type != "query") && (type != "hash") && (type != "url")) throw new Error("Unknown type '" + type + "' in call to URL." + name + "()");
	}
	
	this.setKey = function(type, key, value) {
		this.validateType(type, "setKey")
		this[type][key] = value
	}
	
	this.getKey = function(type, key, def) {
		this.validateType(type, "getKey")
		if (typeof(this[type][key]) != "undefined") return this[type][key];
		if (typeof(def) != "undefined") return def;
		return false
	}
	
	this.merge = function(type, values) {
		this.validateType(type, "merge")
		for (var key in values) {
			this.setKey(type, key, values[key])
		}
	}
	
	this.remove = function(type, key) {
		this.validateType(type, "remove")
		delete this[type][key]
	}
	
	this.clear = function(type) {
		this.validateType(type, "clear")
		this[type] = {}
	}
	
	this.set = function(type, values) {
		this.validateType(type, "set")
		this.clear(type)
		this.merge(type, values)
	}
	
	this.serialize = function(query) {
		var result = ""
		for (var key in query) {
			if (result.length > 0) result += "&";
			result += encodeURIComponent(key)
			var value = encodeURIComponent(query[key])
			if (value.length > 0) result += "=" + value;
		}
		return result
	}
	
	this.unserialize = function(input) {
		var result = {}
		var match
		while (match = input.match(/(?:^|&|;)([^&=;]+)(?:=([^&=;]*))?/)) {
			input = input.substr(match[0].length)
			var value = match[2]
			if (typeof(value) == "undefined") value = "";
			result[decodeURIComponent(match[1])] = decodeURIComponent(value).replace(/\+/g, ' ')
		}
		return result
	}
	
	this.parseURL = function(url) {
		//                        1-SCHEME     2-HOST       3-PORT                       4-PATH    5-QUERY     6-HASH
		//                         -----    -------------    -----                        -----     -----       ----
		var match = url.match(/^(?:(\w+):\/*([\w\.\-\d]+)(?::(\d+)|)(?=(?:\/|$))|)(?:$|\/?(.*?)(?:\?(.*?)?|)(?:#(.*)|)$)/)
		if (!match) return;
		
		if ((typeof(match[1]) == "string") && (match[1].length > 0)) {
			this.setKey("url", "scheme", match[1])
			this.setKey("url", "host", match[2])
			
			if (isNaN(parseInt(match[3]))) {
				this.setKey("url", "port", DEFAULT_HTTP_PORT)
			}
			else {
				this.setKey("url", "port", parseInt(match[3]))
			}
		}
		else {
			this.setKey("url", "scheme", currentURL.url.scheme)
			this.setKey("url", "host", currentURL.url.host)
			this.setKey("url", "port", currentURL.url.port)
		}
		
		this.setKey("url", "path", match[4])
		
		if (typeof(match[5]) == "string") this.set("query", this.unserialize(match[5]));
		if (typeof(match[6]) == "string") this.set("hash", this.unserialize(match[6]));
	}
	
	this.toString = function() {
		if ((typeof(this.url.scheme) != "string") || (this.url.scheme.length < 1)) this.url.scheme = "http";
		if ((typeof(this.url.host) != "string") || (this.url.host.length < 1)) return "";
		if (typeof(this.url.path) != "string") this.url.path = "";
		
		var port = (this.url.port == DEFAULT_HTTP_PORT) ? ("") : (":" + this.url.port)
		var query = this.serialize(this.query)
		var hash = this.serialize(this.hash)
		var result = this.url.scheme + "://" + this.url.host + port + "/" + this.url.path
		
		if (query.length > 0) result += "?" + query;
		if (hash.length > 0) result += "#" + hash;
		
		return result;
	}
	
	if (inputURL.length > 0) this.parseURL(inputURL);
}

currentURL = new URL(document.location.href)
