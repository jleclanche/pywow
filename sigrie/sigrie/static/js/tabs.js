// Sigrie TabViews
var tvlib = {
	init: function() {
		tvlib.tabNames = {}
		tvlib.tabs = []
		tvlib.parseDocument()
		tvlib.loadCurrentTab()
	},
	loadCurrentTab: function() {
		if (typeof(document.location.hash) != "string") return false;
		var current = currentURL.getKey("hash", "tab")
		if (current === false) return false;
		
		if (typeof(tvlib.tabNames[current]) == "object") {
			var tab = tvlib.tabNames[current]
			tvlib.onTabClick(tab)
		}
	},
	parseDocument: function() {
		var divs = document.getElementsByTagName("div")
		var tabviews = Array()
		var tabbuttons = Array()
		var tabcontents = Array()
		for (var i = 0; i < divs.length; i++) {
			if (hasClass(divs[i], "tabview")) {
				tabviews.push(divs[i])
				var children = divs[i].getElementsByTagName("div")
				for (var j = 0; j < children.length; j++) {
					var tab = children[j]
					if (hasClass(tab, "tabbutton")) {
						var content = document.getElementById(tab.id + "_content")
						tab["parent"] = divs[i]
						tab["onclick"] = function(evt) {tvlib.onTabClick(this)}
						content["parent"] = divs[i]
						tab["content"] = content
						content.style.display = "none"
						if (hasClass(tab, "selected")) {
							tvlib.selected = tab
						}
						if (typeof(tab.id) == "string") {
							var id = tab.id
							id = id.match(/(?:tab_)?([\w\d_]+)/)[1]
							tvlib.tabNames[id] = tab
							tab.name = id
						}
						
						tab.index = tvlib.tabs.push(tab) - 1
						
						if (typeof(tab.addEventListener) == "function") {
							tab.addEventListener('DOMMouseScroll', tvlib.onTabScroll, false)
							tab.addEventListener('mousewheel', tvlib.onTabScroll, false)
						}
						else if (typeof(tab.attachEvent) == "function") {
							tab.attachEvent('onmousewheel', tvlib.onTabScroll)
						}
					}
				}
			}
		}
		
		if ((typeof(tvlib.selected) != "object") && (tvlib.tabs.length > 0)) tvlib.selected = tvlib.tabs[0];
		if (typeof(tvlib.selected) == "object") tvlib.onTabClick(tvlib.selected, true);
	},
	onTabScroll: function(event) {
		if (typeof(event) != "object") event = window.event;
		if (typeof(tvlib.selected) != "object") tvlib.selected = tvlib.tabs[0];
		var tab = tvlib.selected
		var newTab = tab
		var amount = 0
		
		if (typeof(event.detail) == "number") amount = event.detail
		if (typeof(event.wheelDelta) == "number") amount = event.wheelDelta
		
		// Tehehe! Browser wars claims another victim! :D
		if (typeof(event.stopPropagation) == "function") event.stopPropagation();
		if (typeof(event.preventDefault) == "function") event.preventDefault();
		event["return"] = false
		event.cancel = true
		event.cancelBubble = true
		
		if (amount < 0) { // Scroll up
			if (tab.index + 1 < tvlib.tabs.length) {
				newTab = tvlib.tabs[tab.index + 1]
			}
			else {
				return false
			}
		}
		else { // Scroll down
			if (tab.index > 0) {
				newTab = tvlib.tabs[tab.index - 1]
			}
			else {
				return false
			}
		}
		tvlib.onTabClick(newTab)
		return false
	},
	onTabClick: function(self, silent) {
		if (typeof(silent) != "boolean") silent = false;
		tvlib.hideAll(self["parent"])
		self["content"].style.display = "block"
		addClass(self, "selected")
		tvlib.selected = self
		
		if (!silent) {
			if (typeof(self.name) == "string") {
				currentURL.setKey("hash", "tab", self.name)
				document.location.href = currentURL.toString()
			}
		}
	},
	hideAll: function(div) {
		var children = div.getElementsByTagName("div");
		for (var i = 0; i < children.length; i++) {
			if (hasClass(children[i], "tabcontent")) {
				children[i].style.display = "none"
			} else if (hasClass(children[i], "tabbutton")) {
				removeClass(children[i], "selected")
			}
		}
	}
}
addLoadEvent(tvlib.init)
