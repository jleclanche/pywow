//Sigrie Tooltips (External)
var URL_BASE = "^http://db\\.mmo-champion\\.com"
var URL_REGEX = URL_BASE + "/(a|c|e|g|i|o|q|s|t|z|is|ach|npc|achievement|creature|enchant|glyph|itemset|item|object|skill|spell|talent|zone)/([^#\?]+?)(\\/?\\?[^#]*|)(#.*|)$"
// wowhead
var WH_URL_BASE = "^http://(www\\.|bc\\.|beta\\.|cata\\.|dev\\.|ptr\\.|wotlk\\.)?wowhead\\.com"
var WH_URL_REGEX = WH_URL_BASE + "/\\??(achievement|item|itemset|npc|object|quest|spell|itemset|item)=(\\d+).*$"

// omniwow
var OW_URL_BASE = "^http://(www\\.)?wowdb\\.com"
var OW_URL_REGEX = OW_URL_BASE + "/(spell|npc|achievement|quest|itemset|item)\\.aspx\\?id=(\\d+)$"

var TOOLTIP_RETRIEVING_HTML = "<span class='sigrie-tooltip tt-retrieving'>Retrieving tooltip...</span>"
var TOOLTIP_MAX_WIDTH = 310
var TOOLTIP_TIMEOUT_HTML = "<span class='sigrie-tooltip tt-retrieving'>Timeout retrieving tooltip</span>"
var TOOLTIP_TIMEOUT_MS = 3000

var ttlib = {
	init: function() {
		var jstooltip = document.createElement("div")
		jstooltip.id = "sigrie-tooltip"
		jstooltip.className = "tt-hover tt-hover-external"
		document.getElementsByTagName("body")[0].appendChild(jstooltip)
		ttlib.jstooltip = jstooltip
		ttlib.hide()
		ttlib.queue = new Array()
		ttlib.currentRequest = null
		ttlib.currentMouseover = ""
		ttlib.cache = new Object()
		ttlib.failureTimer = -1
		ttlib.URLValidators = []
		document.onmousemove = ttlib.mouseMove
		
		ttlib.registerURL(
			function(url) {
				if (url.match(URL_REGEX)) {
					var match = url.match(URL_REGEX)
					return "http://db.mmo-champion.com/" + match[1] + "/" + match[2] + "/tooltip/js" + match[3]
				}
			},
			false
		)
		/*
		// Disabled WH + WDB support
		ttlib.registerURL(
			function(url) {
				if (url.match(WH_URL_REGEX)) {
					var match = url.match(WH_URL_REGEX)
					return "http://db.mmo-champion.com/" + match[2][0] + match[3] + "/tooltip/js"
				}
			},
			false
		)
		ttlib.registerURL(
			function(url) {
				if (url.match(OW_URL_REGEX)) {
					var match = url.match(OW_URL_REGEX)
					return "http://db.mmo-champion.com/" + match[2][0] + match[3] + "/tooltip/js"
				}
			},
			false
		)
		*/
		
		ttlib.parseDocument()
		if (typeof(document.addEventListener) == "function") document.addEventListener('DOMNodeInserted', ttlib.DOMNodeInserted, true);
	},
	
	mouseMove: function(e) {
		if (ttlib.jstooltip.style.visibility == "hidden") return
		var cursor = ttlib.cursorPosition(e)
		var de = document.documentElement
		var body = document.body
		var y = cursor.y - 15
		var x = cursor.x + 20
		if (cursor.y + ttlib.jstooltip.offsetHeight > de.clientHeight + body.scrollTop + de.scrollTop) { // Bottom clamp
			var diff = (de.clientHeight+body.scrollTop+de.scrollTop)-(cursor.y+ttlib.jstooltip.offsetHeight)
			y += diff
		}
		if (y < 0) { // Top clamp
			y = 0
		}
		ttlib.jstooltip.style.left = "" + (x) + "px"
		ttlib.jstooltip.style.top = "" + (y) + "px"
	},
	
	request: function(url) {
		var script = document.createElement("script")
		script.type = "text/javascript"
		script.src = url
		ttlib.currentRequest["tag"] = script
		document.getElementsByTagName("head")[0].appendChild(script)
	},
	
	queueRequest: function(url) {
		var req = new Object()
		req["url"] = url
		req["cache"] = url
		ttlib.queue.push(req)
		ttlib.processQueue()
	},
	
	processQueue: function() {
		if (ttlib.queue.length > 0 && ttlib.currentRequest == null) {
			ttlib.currentRequest = ttlib.queue.pop()
			ttlib.request(ttlib.currentRequest["url"])
			ttlib.failureTimer = window.setTimeout(ttlib.timeoutTooltip, TOOLTIP_TIMEOUT_MS)
		}
	},
	
	getValid: function(url) {
		var result = ""
		for (var i = 0; (result.length < 1) && (i < ttlib.URLValidators.length); i++) {
			var validator = ttlib.URLValidators[i]
			result = validator(url)
			if (typeof(result) != "string") result = "";
		}
		return result
	},
	
	startTooltip: function(atag) {
		ttlib.currentMouseover = atag["rel"]
		if (ttlib.cache[atag["rel"]]) {
			ttlib.jstooltip.innerHTML = ttlib.cache[atag["rel"]]
		} else {
			ttlib.jstooltip.innerHTML = TOOLTIP_RETRIEVING_HTML
			ttlib.queueRequest(atag["rel"])
		}
		ttlib.show();
	},
	
	parseDocument: function() {
		ttlib.parseElement(document)
	},
	
	parseElement: function(element) {
		if (typeof(element.getElementsByTagName) == "undefined") return false;
		var links = element.getElementsByTagName("a")
		var upval
		for(var i = 0; i<links.length; i++) {
			var valid = ttlib.getValid(links[i].href)
			if(valid != "") {
				links[i]["rel"] = valid
				links[i].onmouseover = function(evt) { ttlib.startTooltip(this) }
				links[i].onmouseout = function(evt) { ttlib.hide() }
			}
		}
	},
	
	cursorPosition: function(e) {
		e = e || window.event
		var cursor = {x:0, y:0}
		if (e.pageX || e.pageY) {
			cursor.x = e.pageX
			cursor.y = e.pageY
		} else {
			var de = document.documentElement
			var b = document.body
			cursor.x = e.clientX + (de.scrollLeft || b.scrollLeft) - (de.clientLeft || 0)
			cursor.y = e.clientY + (de.scrollTop || b.scrollTop) - (de.clientTop || 0)
		}
		return cursor
	},
	
	show: function() {
		if (ttlib.jstooltip.style.width > TOOLTIP_MAX_WIDTH || ttlib.jstooltip.style.width > TOOLTIP_MAX_WIDTH
			|| ttlib.jstooltip.offsetWidth > TOOLTIP_MAX_WIDTH || ttlib.jstooltip.offsetWidth > TOOLTIP_MAX_WIDTH) {
			ttlib.jstooltip.style.width = TOOLTIP_MAX_WIDTH
		} else {
			ttlib["jstooltip"]["style"]["width"] = ttlib["jstooltip"]["style"]["width"]
		}
		ttlib.jstooltip.style.visibility = "visible"
	},
	
	hide: function() {
		ttlib.jstooltip.style.visibility = "hidden"
		ttlib.currentMouseover = null
	},
	
	removeChildren: function() {
		var scripts = document.getElementsByTagName("script")
		var head = document.getElementsByTagName("head").item(0)
		for (var i=0; i<scripts.length; i++) {
			var script = scripts[i]
			var src = script.getAttribute("src")
			if(src!=null && src.indexOf("tooltip/js") > 0 && src.indexOf("db.mmo-champion.com") > 0) {
				head.removeChild(script)
				return
			}
		}	
	},
	
	timeoutTooltip: function() {
		registertooltip({tooltip: TOOLTIP_TIMEOUT_HTML});
		ttlib.failureTimer = -1
	},
	
	registerURL: function(callback, recheckDocument) {
		if (typeof(recheckDocument) != "boolean") recheckDocument = true;
		ttlib.URLValidators.push(callback)
		if (recheckDocument) ttlib.parseDocument();
	},
	
	DOMNodeInserted: function(event) {
		if (typeof(event.target) == "object") ttlib.parseElement(event.target);
	}
}

function registertooltip(str) {
	window.clearTimeout(ttlib.failureTimer)
	ttlib.failureTimer = -1
	ttlib.cache[ttlib.currentRequest["cache"]] = str.tooltip;
	try {
		setTimeout("ttlib.removeChildren()", 0)
	} catch (e) {}
	if (ttlib.currentMouseover == ttlib.currentRequest["cache"]) {
		ttlib.jstooltip.innerHTML = str.tooltip
		ttlib.show()
	}
	ttlib.currentRequest = null
	ttlib.processQueue()
}

addLoadEvent(ttlib.init)
