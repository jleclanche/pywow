/**
 * Sigrie map engine
 * Belhorma Bendebiche <amro256@gmail.com>
 */

var maplib = {
	renderMaps: function(maps,defaultfile) {
		if (typeof (defaultfile) == "undefined") defaultfile = "";
		var jstooltip = document.createElement("div")
		var defaultid = 0
		var container = document.getElementById("map-container")
		jstooltip.id = "sigrie-maptooltip"
		jstooltip.className = "sigrie-tooltip tt-hover tt-hover-external"
		jstooltip.style.visibility = "hidden"
		jstooltip.style.padding = "4px"
		maplib.jstooltip = jstooltip
		maplib.hide()
		maplib.maps = maps
		maplib.mapDivs = []
		if (maps.length > 1) {
			var mapWidget = document.createElement("div")
			mapWidget.id = "sigrie-map-floorswitch"
			mapWidget.className = "sigrie-map-floorswitch"
			mapWidget.innerHTML = "Current map: "
			container.appendChild(mapWidget)
			var selectBox = document.createElement("select")
			for (var m in maps) {
				var option = document.createElement("option")
				option.innerHTML = maps[m].name
				option.mapIndex = m
				selectBox.appendChild(option)
				if (maps[m].name == defaultfile)
				{
					defaultid = m
					option.selected = "true"
				}
			}
			mapWidget.appendChild(selectBox)
			selectBox.onchange = function(f) {
				for (var m in maplib.maps) {
					if (m == maplib.selectBox.selectedIndex) maplib.mapDivs[m].style.visibility = "visible"
					else maplib.mapDivs[m].style.visibility = "hidden"
				}
			}
			maplib.selectBox = selectBox
		}
		var innerMapContainer = document.createElement("div")
		innerMapContainer.style.height = "325px"
		innerMapContainer.style.width = "488px"
		innerMapContainer.style.position = "relative"
		innerMapContainer.appendChild(jstooltip)
		container.appendChild(innerMapContainer)
		for (var m in maps) {
			var map = maps[m]
			var mapDiv = document.createElement("div")
			mapDiv.id = "map-" + map.name
			mapDiv.className = "map"
			mapDiv.style.width = "488px"
			mapDiv.style.height = "325px"
			mapDiv.style.marginBottom = "-325px"
			mapDiv.style.position = "relative"
			mapDiv.style.backgroundImage = "url('/static/img/maps/" + map.file + ".thumbnail.jpg')"
			innerMapContainer.appendChild(mapDiv)
			maplib.mapDivs[maplib.mapDivs.length] = mapDiv
			mapDiv.style.visibility = "hidden"
			for (var i in map.nodes) {
				var n = map.nodes[i]
				var node = document.createElement("div")
				var nodeClass = "node"
				if (typeof(n[2]) == "string") nodeClass = n[2];
				node.className = nodeClass
				node.label = n[0] + ", " + n[1]
				if (n.length == 3) node.label = n[2] + " (" + n[0] + ", " + n[1] + ")"
				node.style.position = "absolute"
				node.style.left = "" + n[0] + "%"
				node.style.top = "" + n[1] + "%"
				node.onmouseover = function(e) { maplib.startTooltip(this) }
				node.onmouseout = function(e) { maplib.hide() }
				mapDiv.appendChild(node)
			}
		}
		maplib.mapDivs[defaultid].style.visibility = "visible"
	},
	
	startTooltip: function(node) {
		maplib.jstooltip.innerHTML = node.label
		maplib.jstooltip.style.left = "" + (node.offsetLeft+16) + "px"
		maplib.jstooltip.style.top = "" + (node.offsetTop-20) + "px"
		maplib.jstooltip.style.visibility = "visible"
	},
	
	hide: function() {
		maplib.jstooltip.style.visibility = "hidden"
	}
}
