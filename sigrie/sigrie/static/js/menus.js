var SigrieMenus = function() {
	var that = this
	
	// Config
	this.offsetTop = 5
	this.offsetLeft = -8
	this.hideDelay = 300
	// End config
	
	this.init = function() {
		this.menus = [] // Currently shown menus, in order from parent to child
		this.hideTimeout = -1
		
		this.findMenus()
	}
	
	this.findMenus = function() {
		var elements = document.getElementsByTagName("a")
		var buffer = [] // Ugh, live arrays
		
		for (var i in elements) {
			if (typeof(elements[i]) == "object") buffer.push(elements[i]);
		}
		
		for (var i in buffer) {
			var element = buffer[i]
			var menu = element.getAttribute("rel")
			
			if ((typeof(menu) == "string") && (typeof(sgMenus[menu]) == "object")) {
				element.menu = menu
				element.onmouseover = function() { that.showMenu(this.menu, 0, this) }
			}
		}
	}
	
	this.showMenu = function(type, depth, button, parent) {
		this.clearMenus(depth)
		
		var menu = {
			"type": type,
			"button": button,
			"list": document.createElement("ul"),
			"depth": depth
		}
		var menuid = this.menus.push(menu) - 1
		var de = document.documentElement
		var body = document.body
		
		addClass(button, "selected")
		addClass(menu.list, "menuitem")
		
		body.appendChild(menu.list)
		
		this.populateMenu(menuid, parent)
		
		menu.list.style.position = "absolute"
		
		var top = getOffsetTop(button)
		var left = getOffsetLeft(button)
		
		if (depth == 0) {
			top += button.offsetHeight
		}
		else {
			left += button.offsetWidth
		}
		
		var diff = (top + menu.list.offsetHeight) - (de.clientHeight + body.scrollTop + de.scrollTop)
		if (diff > 0) top -= diff;
		
		menu.list.style.top = top + "px"
		menu.list.style.left = left + "px"
		
		button.onmouseout = menu.list.onmouseout = function() { that.resetHideTimer() }
		menu.list.onmouseover = function() { that.stopHideTimer() }
		
		this.stopHideTimer()
	}
	
	this.clearMenus = function(depth) {
		while (this.menus.length > depth) {
			var menu = this.menus.pop()
			removeClass(menu.button, "selected")
			
			menu.list.parentNode.removeChild(menu.list)
		}
	}
	
	this.populateMenu = function(menuid, parent) {
		var menu = this.menus[menuid]
		var type = sgMenus[menu.type]
		
		if (typeof(type) != "object") return;
		
		for (var i in type) {
			var li = document.createElement("li")
			var a = document.createElement("a")
			
			if ((typeof(type[i].header) == "boolean") && (type[i].header === true)) {
				addClass(li, "menuheader")
			}
			
			if (typeof(type[i].icon) == "string") {
				var icon = document.createElement("img")
				icon.src = "http://db.mmo-champion.com/static/img/icons/" + type[i].icon + ".png"
				icon.className = "menuicon"
				li.appendChild(icon)
			}
			
			if ((typeof(type[i].submenu) == "string") && (typeof(sgMenus[type[i].submenu]) == "object")) {
				addClass(li, "submenu")
				
				li.subtype = type[i].submenu
				li.submenu = type[i]
				li.onmouseover = function() { that.showMenu(this.subtype, this.menu.depth + 1, this, this.submenu) }
			}
			else {
				li.onmouseover = function() { that.clearMenus(this.menu.depth + 1) }
			}
			
			a.textContent = a.innerText = type[i].name
			li.menu = menu
			
			var href = type[i].href
			if (typeof(href) == "string") {
				if (href[0] == "$") {
					href = parent.href + href.substring(1)
				}
				a.href = href
			}
			else {
				a.href = "javascript:;"
				a.onclick = function() { return false }
			}
			
			li.appendChild(a)
			menu.list.appendChild(li)
		}
	}
	
	this.resetHideTimer = function() {
		if (this.hideTimeout >= 0) window.clearTimeout(this.hideTimeout)
		this.hideTimeout = window.setTimeout(function() { that.hideTimer() }, this.hideDelay)
	}
	
	this.stopHideTimer = function() {
		window.clearTimeout(this.hideTimeout)
		this.hideTimeout = -1
	}
	
	this.hideTimer = function() {
		this.stopHideTimer()
		this.clearMenus(0)
	}
}

sigrieMenus = new SigrieMenus()
addLoadEvent(function(){sigrieMenus.init()})
