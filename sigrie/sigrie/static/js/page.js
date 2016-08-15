/**
 * Page widget lib
 * Example: http://db.mmo-champion.com/i/39317/news-from-the-north/
 */

pagelib = {
	init: function() {
		pagelib.container = document.getElementById("pagewidget")
		if ((typeof(pagelib.container) == "undefined") || (!pagelib.container)) return;
		var initid = parseInt(pagelib.container.getAttribute("rel"))
		if (initid < 0) return;
		
		pagelib.cache = {}
		pagelib.id = -1
		pagelib.loading = -1
		pagelib.nextId = -1
		pagelib.pos = 0
		
		pagelib.loadPage(initid)
	},
	
	loadPage: function(id) {
		id = parseInt(id)
		if (id < 0) return false;
		if (pagelib.loading >= 0) return false;
		
		pagelib.loading = id
			
		if (typeof(pagelib.cache[id]) == "object") {
			pagelib.parsePage(pagelib.cache[id])
		}
		else {
			httplib.request("/p/" + id + "/tooltip/js", {
				"content": "json",
				"success": function(result) {pagelib.parsePage(result.response)}
			})
		}
		return true
	},
	
	parsePage: function(page) {
		page.id = parseInt(page.id)
		if (page.id != parseInt(pagelib.loading)) return false;
		
		if (pagelib.pos == 0) {
			pagelib.pos = 1
		}
		else if (page.id == pagelib.nextId) {
			pagelib.pos++
		}
		else {
			pagelib.pos--
		}
		
		pagelib.cache[page.id] = page
		if (typeof(pagelib.cache[page.id].prevId) != "number") pagelib.cache[page.id].prevId = pagelib.id;
		pagelib.id = page.id
		pagelib.loading = -1
		
		if ((typeof(page.nextpage) == "undefined") || (parseInt(page.nextpage) < 0)) {
			pagelib.nextId = -1
		}
		else {
			pagelib.nextId = parseInt(page.nextpage)
		}
		
		pagelib.configureNavigation()
		pagelib.setText(page.tooltip)
	},
	
	configureNavigation: function(page) {
		if (typeof(pagelib.header) != "object") {
			pagelib.container.appendChild(pagelib.header = document.createElement("div"))
			pagelib.header.id = "pagewidget-header"
		}
		if (typeof(pagelib.nextLink) != "object") {
			pagelib.header.appendChild(pagelib.nextLink = document.createElement("a"))
			pagelib.nextLink.href = "javascript:;"
			pagelib.nextLink.innerHTML = "Next &rsaquo;"
			pagelib.nextLink.onclick = pagelib.nextPage
			addClass(pagelib.nextLink, "page-next")
			addClass(pagelib.nextLink, "button")
		}
		if (typeof(pagelib.posLink) != "object") {
			pagelib.header.appendChild(pagelib.posLink = document.createElement("a"))
			pagelib.posLink.href = "/p/" + pagelib.id
			pagelib.posLink.innerHTML = "Page 0"
			addClass(pagelib.posLink, "page-pos")
		}
		if (typeof(pagelib.prevLink) != "object") {
			pagelib.header.appendChild(pagelib.prevLink = document.createElement("a"))
			pagelib.prevLink.href = "javascript:;"
			pagelib.prevLink.innerHTML = "&lsaquo; Prev"
			pagelib.prevLink.onclick = pagelib.prevPage
			addClass(pagelib.prevLink, "page-prev")
			addClass(pagelib.prevLink, "button")
		}
		if (parseInt(pagelib.nextId) < 0) {
			addClass(pagelib.nextLink, "inactive")
		}
		else {
			removeClass(pagelib.nextLink, "inactive")
		}
		if ((pagelib.cache.count == 0) || (parseInt(pagelib.cache[pagelib.id].prevId) < 0)) {
			addClass(pagelib.prevLink, "inactive")
		}
		else {
			removeClass(pagelib.prevLink, "inactive")
		}
		pagelib.posLink.href = "/p/" + pagelib.id
		pagelib.posLink.innerHTML = "Page " + pagelib.pos
	},
	
	setText: function(text) {
		if (typeof(pagelib.text) != "object") {
			pagelib.text = document.createElement("div")
			pagelib.text.id = "pagewidget-text"
			pagelib.container.appendChild(pagelib.text)
		}
		pagelib.text.innerHTML = text
	},
	
	nextPage: function() {
		if (!pagelib.loadPage(pagelib.nextId)) {
			pagelib.configureNavigation()
		}
	},
	
	prevPage: function() {
		if ((pagelib.cache.count == 0) || (!pagelib.loadPage(pagelib.cache[pagelib.id].prevId))) {
			pagelib.configureNavigation()
		}
	}
}

addLoadEvent(pagelib.init)