// Sigrie Tooltips (Internal)
var URL_BASE = "(^|http://db\.mmo-champion\.com|http://.*\.sigrie\.com/|http://sigrie\.dinnerbone\.com)/"
var URL_REGEX = URL_BASE + "(a|c|e|g|i|o|q|s|t|z|is|ach|npc|achievement|creature|enchant|glyph|itemset|item|object|skill|spell|talent|zone)/([^#]+?)(?:\\/\\?([^#]+)|$|#.*$)"
var TOOLTIP_RETRIEVING_HTML = '<span class="sigrie-tooltip tt-retrieving">Retrieving tooltip...</span>'
var TOOLTIP_ERROR_HTML = '<span class="sigrie-tooltip tt-error">Error retrieving tooltip</span>'
var TOOLTIP_MAX_WIDTH = 310
TOOLTIP_CLASS_BLACKLIST = "tt-name"

var ttlib = {
	init: function() {
		var jstooltip = document.createElement("div")
		var pagetooltip = document.getElementById('dview-tooltip')
		jstooltip.id = "sigrie-tooltip"
		jstooltip.className = "tt-hover"
		document.getElementsByTagName("body")[0].appendChild(jstooltip)
		ttlib.jstooltip = jstooltip
		ttlib.hide()
		ttlib.parseDocument()
		ttlib.requestcount = 0
		ttlib.requests = new Array()
		ttlib.queue = new Array()
		ttlib.currentRequest = null
		ttlib.cursorX = 0
		ttlib.cursorY = 0
		ttlib.cursorAdjustedX = 0
		ttlib.cursorAdjustedY = 0
		ttlib.currentMouseover = ""
		ttlib.cache = new Object()
		document.onmousemove = ttlib.mouseMove
		if ((typeof(pagetooltip) != "undefined") && (pagetooltip != null)) ttlib.hookHeirloomLevel(pagetooltip);
		if (typeof(document.addEventListener) == "function") document.addEventListener('DOMNodeInserted', ttlib.DOMNodeInserted, true);
	},
	mouseMove: function(e) {
		var cursor = ttlib.cursorPosition(e)
		ttlib.cursorY = cursor.y
		ttlib.cursorX = cursor.x
		ttlib.cursorAdjustedX = cursor.x + 15
		ttlib.cursorAdjustedY = cursor.y - 20
		if (ttlib.jstooltip.style.visibility != "hidden") ttlib.clampTooltip();
	},
	clampTooltip: function() {
		var x = ttlib.cursorX
		var y = ttlib.cursorY
		var ax = ttlib.cursorAdjustedX
		var ay = ttlib.cursorAdjustedY
		var de = document.documentElement
		var body = document.body
		if (y + ttlib.jstooltip.offsetHeight > de.clientHeight + body.scrollTop + de.scrollTop) {
			var ydiff = (de.clientHeight + body.scrollTop + de.scrollTop) - (y + ttlib.jstooltip.offsetHeight)
			ay += ydiff
		}
		if (x + ttlib.jstooltip.offsetWidth + 20 > de.clientWidth + body.scrollLeft + de.scrollLeft) {
			ax -= ttlib.jstooltip.offsetWidth + 20
		}
		ttlib.jstooltip.style.left = "" + (ax) + "px"
		ttlib.jstooltip.style.top = "" + (ay) + "px"
	},
	requestSuccess: function(result) {
		var tooltip = ttlib.currentRequest["tooltip"]
		ttlib.cache[ttlib.currentRequest["cache"]] = result.responseText
		if ((tooltip != ttlib.jstooltip) || (ttlib.currentRequest["cache"] == ttlib.currentMouseover))
		{
			tooltip.style.left = "0px"
			tooltip.style.top = "0px"
			tooltip.innerHTML = result.responseText
			ttlib.hookHeirloomLevel(tooltip)
			if (tooltip == ttlib.jstooltip) {
				ttlib.show()
				ttlib.clampTooltip()
			}
		}
		ttlib.currentRequest = null
		ttlib.processQueue()
	},
	requestFailure: function(result) {
		tooltip.innerHTML = TOOLTIP_ERROR_HTML
		ttlib.currentRequest = null
		ttlib.processQueue()
	},
	queueRequest: function(url, tooltip) {
		var req = new Object()
		var requrl = url
		if (typeof(tooltip) == "undefined") tooltip = ttlib.jstooltip;
		
		if (typeof(requrl) == "object") {
			requrl = requrl.href
			if (requrl.indexOf("?") != -1) requrl = requrl.replace('?', "/tooltip?")
			else if (requrl.indexOf('#') != -1) requrl = requrl.replace('#', "/tooltip#")
			else requrl = url.href + "/tooltip"
		}
		
		req["url"] = requrl
		req["cache"] = url
		req["tooltip"] = tooltip
		ttlib.queue.push(req)
		ttlib.processQueue()
	},
	processQueue: function() {
		if (ttlib.queue.length > 0 && ttlib.currentRequest == null) {
			ttlib.currentRequest = ttlib.queue.pop()
			ttlib.requestcount++
			httplib.request(ttlib.currentRequest["url"], {
				'success': ttlib.requestSuccess,
				'failure': ttlib.requestFailure
			})
		}
	},
	isValid: function(url) {
		if (url.parentNode.className.match(TOOLTIP_CLASS_BLACKLIST)) return false;
		url = url.getAttribute("href") || "#" // check for <a>
		return url.match(URL_REGEX) // we use getAttribute because href always returns an absolute url
	},
	startTooltip: function(atag) {
		ttlib.currentMouseover = atag
		if (ttlib.cache[atag]) {
			ttlib.jstooltip.style.left = "0px"
			ttlib.jstooltip.style.top = "0px"
			ttlib.jstooltip.innerHTML = ttlib.cache[atag]
			ttlib.show()
			ttlib.clampTooltip()
		} else {
			ttlib.jstooltip.innerHTML = TOOLTIP_RETRIEVING_HTML
			ttlib.show()
			ttlib.queueRequest(atag)
		}
	},
	parseDocument: function() {
		ttlib.parseElement(document)
	},
	parseElement: function(element) {
		if (typeof(element.getElementsByTagName) == "undefined") return false;
		var links = element.getElementsByTagName("a")
		for(var i = 0; i < links.length; i++) {
			if(ttlib.isValid(links[i])) {
				links[i].onmouseover = function(evt) { ttlib.startTooltip(this) }
				links[i].onmouseout = function(evt) { ttlib.hide() }
			}
		}
	},
	cursorPosition: function(e) {
		e = e || window.event
		var cursor = {x: 0, y: 0}
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
		if(ttlib.jstooltip.style.width > TOOLTIP_MAX_WIDTH || ttlib.jstooltip.style.width > TOOLTIP_MAX_WIDTH
			|| ttlib.jstooltip.offsetWidth > TOOLTIP_MAX_WIDTH || ttlib.jstooltip.offsetWidth > TOOLTIP_MAX_WIDTH) {
			ttlib.jstooltip.style.width = TOOLTIP_MAX_WIDTH;
		} else {
			ttlib["jstooltip"]["style"]["width"] = ttlib["jstooltip"]["style"]["width"]
		}
		ttlib.jstooltip.style.visibility = "visible"
	},
	hide: function() {
		ttlib.jstooltip.style.visibility = "hidden"
		ttlib.currentMouseover = null
	},
	hookHeirloomLevel: function(tooltip) {
		var reqel = null
		var elements = tooltip.getElementsByTagName("SPAN")
		for (var i = 0; i < elements.length; i++) {
			var element = elements[i]
			if (hasClass(element, "tti-current_level")) {
				reqel = element
				break
			}
		}
		if ((reqel == null) || (typeof(reqel.onclick) == "function")) return;
		reqel.onmouseover = function() {
			this.style.cursor = "pointer"
		}
		reqel.onmouseout = function() {
			this.style.cursor = "default"
		}
		reqel.onmouseup = function() {
			var input = document.createElement("input")
			var cached = true
			input.value = reqel.innerText || reqel.textContent
			reqel.parentNode.replaceChild(input, reqel)
			input.focus()
			input.select()
			input.onblur = function() {
				var level = parseInt(input.value)
				var old = parseInt(reqel.innerText || reqel.textContent)
				if ((level <= 0) || (isNaN(level))) level = old;
				if (level == old) {
					reqel.innerText = reqel.textContent = level
				}
				else if (ttlib.scaleHeirloom(level, tooltip)) {
					reqel.innerText = reqel.textContent = level + "..."
					reqel.onmouseup = function() {}
				}
				input.onblur = function() {}
				if (input.parentNode != null) input.parentNode.replaceChild(reqel, input);
			}
			input.onkeydown = function(e) {
				if (typeof(e) == "undefined") e = window.event;
				var key = 0
				var value = parseInt(input.value)
				if (typeof(e.key) != "undefined") key = e.which;
				if (typeof(e.keyCode) != "undefined") key = e.keyCode;
				
				if ((isNaN(value)) && (input.value.length > 0)) value = input.value = 0;
				
				if (key == 13) { // Enter
					input.onblur()
				}
				else if (key == 27) { // Escape
					input.onblur = function() {}
					if (input.parentNode != null) input.parentNode.replaceChild(reqel, input);
				}
				else if (key == 38) { // Up arrow
					input.value = parseInt(input.value) + 1
				}
				else if (key == 40) { // Down arrow
					input.value = parseInt(input.value) - 1
				}
			}
		}
	},
	scaleHeirloom: function(level, tooltip) {
		if (typeof(tooltip) == "undefined") tooltip = ttlib.jstooltip;
		var url = document.location.href
		var match = url.match(URL_REGEX)
		if (!match) return false;
		url = match[1] + "/" + match[2] + "/" + match[3] + "/tooltip/?level=" + encodeURIComponent(level)
		if ((typeof(match[4]) == "string") && (match[4].length > 0)) url += "&" + match[4];
		
		if (typeof(ttlib.cache[url]) == "string") {
			tooltip.innerHTML = ttlib.cache[url]
			ttlib.hookHeirloomLevel(tooltip)
			return false
		}
		else {
			ttlib.queueRequest(url, tooltip)
			return true
		}
	},
	DOMNodeInserted: function(event) {
		if (typeof(event.target) == "object") ttlib.parseElement(event.target);
	},
	predefineTooltip: function(url, tooltip) {
		ttlib.cache[url] = tooltip
	}
}

addLoadEvent(ttlib.init)

function SigrieTooltip(initargs) {
	// NYI
}