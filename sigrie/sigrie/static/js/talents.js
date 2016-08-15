/**
 * WoWTal - WoWTal.com
 * © 2010 Jerome Leclanche <jerome@leclan.ch>
 *        Nathan Adams <dinnerbone@dinnerbone.com>
 *        Christopher Chedeau <vjeuxx@gmail.com>
 * For Curse
 * Available under MIT License. See LICENSE.
 */

var BASE_URL = "http://wowtal.com/"
var TALENT_ICON_SIZE = 39 // Size in pixels for each talent icon
var TALENT_ICON_MARGIN = 17 // Size in pixels for the margin between talents
var TALENT_ARROW_OFFSET = 10 // Amount of pixels to offset the left and top of the arrows by
var TALENT_ARROW_SIZE = 8 // Size in pixels of the branch arrows
var TALENT_POINTS_PER_ROW = 5 // How many points are required for each row to unlock the next
var TALENT_BASE64 = "f-qR3eOHQ9dSIMwk8pabYt6yrJUFNXLTh4n2KWEoz0uC5j7xmAgDlZiPcs_BGV1v"
var TALENT_RANGE_BITS = 24
var TALENT_RANGE_HIGH = ((1 << TALENT_RANGE_BITS) - 1)
var TALENT_RANGE_HIGH_MASK = (63 << (TALENT_RANGE_BITS - 6))
var TALENT_RANGE_LOW_MASK = ((1 << (TALENT_RANGE_BITS - 6)) - 1)
var TALENT_UPDATE_INTERVAL = 500 // Time in MS to wait after the user stops updating talents to update the URL
var TALENT_MAX_COLS = 4 // Maximum columns per row
var TALENT_LEVEL_OFFSET = 10 // The level you start receiving points at
var TALENT_GLYPHS_PER_TYPE = 3 // Maximum amount of glyphs per type
var TALENT_SPEND_MIN = 31 // Minimum amount of points in a tree before you can spend in another
var TALENT_NUM_ROLES = 4 // Number of different roles of a tree
var TALENT_MAX_LEVEL = 85 // Maximum Level
var TALENT_ROLE_NAMES = ["Unknown", "Tanking", "Healing", "Damage"]
var TALENT_ROLE_TOOLTIPS = ["",
	"Can draw the attention of enemies, protecting allies from harm.",
	"Capable of healing injured allies.",
	"Expert at dealing damage to enemies."
]

var IMAGE_PATH = "http://static.mmo-champion.com/db/img/wowtal/"
var ICONS_PATH = "http://static.mmo-champion.com/db/img/icons/"
var JS_PATH = "http://static.mmo-champion.com/db/js/talents/"
var ICONS_PATH_GREYSCALE = ICONS_PATH + "greyscale/"

function getElementsByClass(searchClass, node, tag) {
	var classElements = new Array()
	if ( node == null )
		node = document
	if ( tag == null )
		tag = "*"
	var els = node.getElementsByTagName(tag)
	var elsLen = els.length
	var pattern = new RegExp("(^|\\s)" + searchClass + "(\\s|$)")
	for (i = 0, j = 0; i < elsLen; i++) {
		if ( pattern.test(els[i].className) ) {
			classElements[j] = els[i]
			j++
		}
	}
	return classElements;
}

function swapClass(element, a, b, cond) {
	if (cond) {
		addClass(element, a)
		removeClass(element, b)
	}
	else {
		addClass(element, b)
		removeClass(element, a)
	}
}

function addBoxShadow(element, size, color) {
	element.style.WebkitBoxShadow = size ? "0 0 " + size + "px " + color : ""
	element.style.MozBoxShadow = size ? "0 0 " + size + "px " + color : ""
	element.style.BoxShadow = size ? "0 0 " + size + "px " + color : ""
}

function flatten(array) {
    var flat = []
    for (var i = 0, l = array.length; i < l; i++){
        var type = Object.prototype.toString.call(array[i]).split(" ").pop().split("]").shift().toLowerCase();
        if (type) { flat = flat.concat(/^(array|collection|arguments|object)$/.test(type) ? flatten(array[i]) : array[i]); }
    }
    return flat
}

if (!Array.indexOf) {
  Array.indexOf = [].indexOf ?
      function (arr, obj, from) { return arr.indexOf(obj, from); }:
      function (arr, obj, from) { // (for IE6)
        var l = arr.length,
            i = from ? parseInt( (1*from) + (from<0 ? l:0), 10) : 0;
        i = i<0 ? 0 : i;
        for (; i<l; i++) {
          if (i in arr && arr[i] === obj) { return i; }
        }
        return -1;
      };
}

var TALENT_CLASS_LIST = ["Death Knight", "Druid", "Hunter", "Mage", "Paladin", "Priest", "Rogue", "Shaman", "Warlock", "Warrior"]
var TALENT_MASTERY_COLORS = [
	[[255, 0, 0], [77, 128, 255], [204, 0, 255]],
	[[255, 184, 26], [255, 0, 0], [77, 128, 255]],
	[[77, 0, 255], [204, 51, 204], [0, 255, 153]],
	[[255, 184, 26], [255, 0, 0], [77, 128, 255]],
	[[255, 184, 26], [255, 0, 0], [77, 128, 255]],
	[[255, 184, 26], [255, 0, 0], [77, 128, 255]],
	[[255, 184, 26], [255, 0, 0], [77, 128, 255]],
	[[255, 184, 26], [255, 0, 0], [77, 128, 255]],
	[[255, 184, 26], [255, 0, 0], [77, 128, 255]],
	[[255, 184, 26], [255, 0, 0], [77, 128, 255]]
]

var TALENT_SPELLS_FIRST = {
	33917: "Mangle",
	11366: "Pyroblast",
	15407: "Mind Flay",
	88625: "Holy Word: Chastise",
	23881: "Bloodthirst"
}


talentlib = {
	init: function() {
		talentlib.currentClass = false
		talentlib.container = document.getElementById("sigrie-talent-calculator")

		if ((typeof(talentlib.container) == "undefined") || (!talentlib.container)) return;

		talentlib.maxLevel = TALENT_MAX_LEVEL // Set default level here, ignore maxPoints line
		talentlib.maxPoints = 0
		talentlib.points = 0
		talentlib.updateTimer = -1

		addClass(talentlib.container, "tal-calculator")

		httplib.request(JS_PATH + "base.js", {
			"success": function() {
				if (!talentlib.drawClassStrip()) return false;

				talentlib.updateGlyphsArray()
				talentlib.updateSpellsArray()

				talentlib.currentBuild = talent_definitions["latest"]
				talentlib.restoreTalents()
			},
			"failure": talentlib.destroyCalculator,
			"content": "js"
		})
	},

	selectClass: function(class_id, build, talentString, glyphString) {
		if (isNaN(build)) build = talentlib.currentBuild;
		if ((class_id == talentlib.currentClass) && (build == talentlib.currentBuild)) return false;

		var success = function() {
			if ((typeof(talent_definitions[class_id]) != "object") || (typeof(talent_definitions[class_id][build]) != "object")) {
				return talentlib.destroyCalculator("Invalid javascript returned loading class '" + class_id + "' for build '" + build + "'")
			}
			if ((typeof(talentlib.currentClass) == "string") && (talentlib.currentClass.length > 0)) talentlib.unloadClass();

			talentlib.currentClassName = class_id
			for (var i = 0; i < TALENT_CLASS_LIST.length; i++) {
				var cur = TALENT_CLASS_LIST[i]
				if (cur.replace(/[^\w]/, "").toLowerCase() == class_id) {
					talentlib.currentClassName = cur
					break
				}
			}

			for (var id in talentlib.classes) {
				swapClass(talentlib.classes[id], "tal-active", "tal-inactive", id == class_id)
			}

			getElementsByClass("tal-tal")[0].style.display = "block";

			var pane = getElementsByClass("tal-pane", talentlib.container)[0]

			talentlib.currentBuild = build
			talentlib.currentClass = class_id
			talentlib.parseTabs()
			talentlib.drawMenu(true)
			talentlib.drawClassStrip()

			pane.style.display = "block"
			talentlib.drawMastery()
			talentlib.drawTalentPane()
			talentlib.drawGlyphs()

			talentlib.selectTree(-1)

			if (typeof(talentString) == "string") {
				talentlib.loadTalentString(talentString)
				talentlib.loadGlyphString(glyphString)
				talentlib.drawTalentPane()
			} else {
				currentURL.setKey("hash", "k", "." + (talentlib.currentBuild).toString(36) + "." + talentlib.currentClass)
				document.location.hash = "#" + currentURL.serialize(currentURL.hash)
				getElementsByClass("tal-link")[0].setAttribute("value", BASE_URL + document.location.hash)
			}

			talentlib.toggleSummary(talentlib.points > 0)
		}

		if (typeof class_id != "undefined") {
			if ((typeof(talent_definitions[class_id]) != "object") || (typeof(talent_definitions[class_id][build]) != "object")) {
				httplib.request(JS_PATH + build + "-" + class_id + ".js", {
					"success": success,
					"failure": talentlib.destroyCalculator,
					"content": "js",
					"method": "script"
				})
			} else {
				success()
			}
		}
	},

	unloadClass: function() {
		if (typeof(talentlib.trees) == "object") {
			for (var tree = 0; tree < talentlib.trees.length; tree++) {
				for (var row in talentlib.trees[tree].rows) {
					for (var col in talentlib.trees[tree].rows[row]) {
						if (!isNaN(col)) {
							var talent = talentlib.trees[tree].rows[row][col]

							talent.image.parentNode.removeChild(talent.image)
							talent.rankDiv.parentNode.removeChild(talent.rankDiv)
							talent.container.parentNode.removeChild(talent.container)

							if (typeof(talent.branches) != "undefined") {
								for (var i = 0; i < talent.branches.length; i++) {
									talent.branches[i].parentNode.removeChild(talent.branches[i])
								}
							}

							delete talentlib.trees[tree].rows[row][col]
						}
					}
				}
			}
		}

		talentlib.points = 0
		currentURL.remove("hash", "k")
		document.location.hash = "#" + currentURL.serialize(currentURL.hash)
		getElementsByClass("tal-link")[0].setAttribute("value", BASE_URL + document.location.hash)
		talentlib.currentClass = false
	},

	resetAll: function() {
		for (var i = 0; i < 3; ++i) {
			talentlib.resetTree(i)
			talentlib.resetGlyph(i)
		}
		talentlib.selectTree(-1)
		talentlib.toggleSummary(false)
		talentlib.saveTalents()
	},

	resetTree: function(treeindex) {
		var tree = talentlib.trees[treeindex]
		var wasCapped = (talentlib.points == talentlib.maxPoints)

		for (var y = 0; y < tree.rowcount; y++) {
			var row = tree.rows[y]

			for (var x = 0; x < TALENT_MAX_COLS; x++) {
				if (typeof(row[x]) == "object") {
					var talent = row[x]
					talent.rank = 0
				}
			}

			row.points = 0
		}

		talentlib.points -= tree.points
		tree.points = 0

		if (wasCapped) {
			talentlib.drawTalentPane()
		}
		else {
			talentlib.drawTree(treeindex)
		}

		talentlib.drawInfoBox()
		talentlib.startUpdateTimer()
	},

	drawClassStrip: function() {
		var strip = talentlib.classStrip

		if ((typeof(talent_definitions["talentsAtLevel"]) == "undefined") || (isNaN(talent_definitions["talentsAtLevel"][talentlib.maxLevel]))) {
			var points = "undefined"
			if (typeof(talent_definitions["talentsAtLevel"][talentlib.maxLevel]) != "undefined") points = talent_definitions["talentsAtLevel"][talentlib.maxLevel];
			talentlib.destroyCalculator("Invalid default level specified (" + talentlib.maxLevel + " => " + points + "). " +
			                            'Please <a href="http://www.wikihow.com/Clear-Your-Browser\'s-Cache" target="_blank">clear your cache</a> and try again.')
			return false
		}

		// Create a reverse table for looking up points->level
		talent_definitions["levelForTalents"] = {}
		for (var level in talent_definitions["talentsAtLevel"]) {
			if (!isNaN(level)) {
				var points = talent_definitions["talentsAtLevel"][level]
				if (typeof(talent_definitions["levelForTalents"][points]) == "undefined") {
					talent_definitions["levelForTalents"][points] = level
				}
			}
		}

		talentlib.maxPoints = talent_definitions["talentsAtLevel"][talentlib.maxLevel]

		if (typeof(strip) == "undefined") {
			strip = talentlib.classStrip = getElementsByClass("tal-classstrip", talentlib.container, 'div')[0]
			talentlib.classes = []

			for (var i in TALENT_CLASS_LIST) {
				var name = TALENT_CLASS_LIST[i]
				var id = name.replace(/[^\w]/, "").toLowerCase()
				var element = talentlib.classes[id] = document.createElement("div")
				var icon = document.createElement("img")

				element.draggable = false
				element.icon = icon
				element.class_id = id

				setImageSrc(icon, ICONS_PATH + "class-" + id + ".png")
				icon.alt = name
				icon.width = 50
				icon.height = 50
				icon.onclick = function() { talentlib.selectClass(this.parentNode.class_id) }
				addClass(element, "tal-class")
				addClass(element, "tal-class-" + id)

				element.appendChild(icon)
				strip.appendChild(element)
			}
		}

		if (typeof(strip.noneselected) != "object") {
			var element = document.createElement("div")
			addClass(element, "tal-class-noneselected")
			talentlib.container.appendChild(element)
			strip.noneselected = element
			element.innerHTML = "Please select a class from the above menu."
		} else {
			if (strip.noneselected.parentNode == talentlib.container) talentlib.container.removeChild(strip.noneselected);
			strip.nonseelected = false
		}

		return true
	},

	addIcon: function(element, name, link, icon) {
		element.innerHTML = ""
		var a = document.createElement("a")
		a.href = link ? link : "javascript: void(0);"
		element.appendChild(a)

		var img = document.createElement("img")
		img.src = icon ? icon : link + "/icon"
		a.appendChild(img)

		var text = document.createTextNode(name)
		a.appendChild(text)

		return element
	},

	getCurrentClass: function () {
		var i = 0;
		for (var i = 0; i < TALENT_CLASS_LIST.length; ++i) {
			if (TALENT_CLASS_LIST[i] == talentlib.currentClassName) return i;
		}
		return -1;
	},

	findClass: function (name) {
		name = name.toLowerCase().replace(" ", "")
		for (var i = 0; i < TALENT_CLASS_LIST.length; ++i) {
			if (TALENT_CLASS_LIST[i].toLowerCase().replace(" ", "") == name) return i;
		}
		return -1
	},

	getTreeColor: function (i) {
		return 'rgb(' + TALENT_MASTERY_COLORS[talentlib.getCurrentClass()][i] + ')'
	},

	drawRoles: function(element, roles) {
		element.innerHTML = ''
		for (var i = TALENT_NUM_ROLES - 1; i >= 0; --i) {
			if (roles >= Math.pow(2, i)) {
				roles -= Math.pow(2, i);
				var img = document.createElement("img")
				img.src = IMAGE_PATH + "role" + i + ".png"
				talentlib.addTooltip(img,
					'<div class="tt-spell sigrie-tooltip">' +
						'<div class="tt-name tts-name">' + TALENT_ROLE_NAMES[i] + "</div>" +
						'<div class="tts-description">' + TALENT_ROLE_TOOLTIPS[i] + "</div>" +
					"</div>")
				element.appendChild(img)
			}
		}
	},

	getRolesText: function (roles) {
		var res = []
		for (var i = TALENT_NUM_ROLES - 1; i >= 0; --i) {
			if (roles >= Math.pow(2, i)) {
				roles -= Math.pow(2, i);
				res.push(TALENT_ROLE_NAMES[i])
			}
		}
		return res.join(", ")
	},

	drawMastery: function() {
		var trees = talentlib.trees
		var summaries = getElementsByClass("tal-summary")
		var toggle = getElementsByClass("tal-togglesummary", talentlib.container)[0]
		toggle.onclick = talentlib.toggleSummary

		var reset = getElementsByClass("tal-infobox-reset", talentlib.container)[0]
		reset.onclick = talentlib.resetAll

		var prefill = getElementsByClass("tal-infobox-prefill")[0]
		prefill.onclick = talentlib.createPreviewTalentScript

		for (var i = 0; i < trees.length; i++) {
			var color = talentlib.getTreeColor(i)
			var summary = talent_definitions.tabs[trees[i].id];
			summaries[i].style.borderColor = color

			var name = getElementsByClass("tal-summary-name", summaries[i])[0]
			name.innerHTML = summary.name

			!function (id) {
				name.onclick = function () {
					talentlib.selectTree(id)
					for (var i = 0; i < talentlib.trees.length; ++i) {
						talentlib.resetTree(i)
					}
					talentlib.drawTree(id)
					talentlib.toggleSummary()
				}
			}(i)

			var icon = getElementsByClass("tal-summary-icon", summaries[i])[0]
			icon.style.backgroundImage = "url(" + ICONS_PATH + summary.icon + ".png)"
			icon.onclick = name.onclick
			addBoxShadow(icon, 100, color)

			var roles = getElementsByClass("tal-summary-roles", summaries[i])[0]
			talentlib.drawRoles(roles, summary.roles)

			var text = getElementsByClass("tal-summary-text", summaries[i])[0]
			text.innerHTML = summary.description.replace(/\$G([^:]+):([^;]+);/g, "&lt;$1/$2&gt;")

			var spells = getElementsByClass("tal-summary-spell", summaries[i])
			for (var id in spells) {
				spells[id].innerHTML = ""
				spells[id].style.display = "none"
			}
			var k = 0
			for (var id = 0; id < talent_definitions.primarySpells.length; ++id) {
				var spell = talent_definitions.primarySpells[id]
				if (spell.tab == trees[i].id) {
					talentlib.addIcon(spells[k], spell.name, "http://db.mmo-champion.com/s/" + spell.spell + "/", ICONS_PATH + spell.icon + ".png")

					var tooltip = talent_definitions[talentlib.currentClass][talentlib.currentBuild].primaries[spell.spell];
					talentlib.addTooltip(spells[k].firstChild, tooltip)
					spells[k].style.display = "block"
					k += 1;
				}
			}

			var mastery_slot = getElementsByClass("tal-summary-mastery", summaries[i])[0]

            var mastery = {name: 'Mastery: ', tooltip: '<div class="tt-spell sigrie-tooltip">', id: 0}

            var masteries = summary.masteries
            for (var id = 0; id < summary.masteries.length; ++id) {
                mastery.name += summary.masteries[id].name
                if (id != summary.masteries.length - 1) {
                    mastery.name += " / "
                }

                mastery.id = summary.masteries[id].id

                mastery.tooltip +=
					'<div class="tt-name tts-name">' + summary.masteries[id].name+ "</div>" +
					'<div class="tts-description">' + summary.masteries[id].description + "</div>"
            }
            mastery.tooltip += '</div>'

			talentlib.addIcon(mastery_slot, mastery.name, "http://db.mmo-champion.com/s/" + mastery.id, ICONS_PATH + "spell_holy_championsbond.png")
			talentlib.addTooltip(mastery_slot.firstChild, mastery.tooltip)
			mastery_slot.style.display = "block"
		}
	},

	toggleSummary: function(show) {
		var toggle = getElementsByClass("tal-togglesummary", talentlib.container)[0]
		var summary = getElementsByClass("tal-summaries", talentlib.container)[0]
		var pane = getElementsByClass("tal-pane", talentlib.container)[0]

		var display = false
		if (typeof show == "boolean") {
			display = show
		}
		else if (summary.style.display == "block") {
			display = true
		}

		if (display) {
			summary.style.display = "none"
			pane.style.display = "block"
			toggle.innerHTML = "Show Summary"
		}
		else {
			summary.style.display = "block"
			pane.style.display = "none"
			toggle.innerHTML = "Show Talents"
		}
	},

	drawTalentPane: function() {
		if (typeof(talentlib.currentClass) != "string") return false;
		var pane = talentlib.talentPane
		var tabs = talentlib.tabs
		var trees = talentlib.trees

		if (typeof(pane) == "undefined") {
			talentlib.talentPane = pane = getElementsByClass("tal-pane", talentlib.container)[0]

			tabs = talentlib.tabs = []

			for (var i = 0; i < trees.length; i++) {
				var tab = document.createElement("div")
				var tree = document.createElement("div")
				var background = document.createElement("img")
				background.draggable = false

				addClass(tab, "tal-tab")
				addClass(tree, "tal-tree")
				addClass(background, "tal-tree-background")

				tab.appendChild(background)
				tab.appendChild(tree)
				pane.appendChild(tab)

				tabs.push({
					"tab": tab,
					"background": background,
					"tree": tree,
					"talents": [],
					"left": tree.offsetLeft,
					"top": tree.offsetTop
				})
			}
		}

		for (var tree = 0; tree < talentlib.trees.length; tree++) {
			talentlib.drawTree(tree, 0, talentlib.trees[tree].rowcount, true)
		}
	},

	drawMenu: function(complete) {
		if (typeof(complete) != "boolean") complete = false;
		talentlib.drawInfoBox(complete)
	},

	findSelectedTree: function () {
		if (talentlib.points == 0) return -1;

		var tree = 0
		for (var i = 1; i < talentlib.trees.length; ++i) {
			var points = talentlib.trees[i].points
			if (points > talentlib.trees[tree].points) {
				tree = i
			}
		}
		return tree
	},

	selectTree: function (selected) {
		talentlib.selectedTree = selected

		var summaries = getElementsByClass("tal-summary-tree")

		for (var i = 0; i < talentlib.trees.length; ++i) {
			if (i == selected) {
				addBoxShadow(summaries[i], 10, talentlib.getTreeColor(i))
				addBoxShadow(talentlib.tabs[i].tab, 10, talentlib.getTreeColor(i))
				removeClass(talentlib.tabs[i].tab, "tal-disabled")
			} else {
				addBoxShadow(summaries[i], null)
				addBoxShadow(talentlib.tabs[i].tab, null)
				addClass(talentlib.tabs[i].tab, "tal-disabled")
			}
		}

		talentlib.drawInfoBox()
	},

	drawInfoBox: function(complete) {
		if (typeof(complete) != "boolean") complete = false;
		var container = talentlib.infoboxContainer
		var buildstr = ""
		var maximumLevelParent = null

		if (typeof(container) == "undefined") container = talentlib.infoboxContainer = getElementsByClass("tal-infobox", talentlib.container)[0]

		if (typeof(container.currentClass) == "undefined") container.currentClass = getElementsByClass("tal-infobox-class", talentlib.container)[0]
		if (typeof(container.spentPoints) == "undefined") container.spentPoints = getElementsByClass("tal-infobox-spentpoints", talentlib.container)[0]
		if (typeof(container.remaining) == "undefined") container.remaining = getElementsByClass("tal-infobox-remainingpoints", talentlib.container)[0]
		if (typeof(container.requiredLevel) == "undefined") container.requiredLevel = getElementsByClass("tal-infobox-requiredlevel", talentlib.container)[0]

		if (typeof(container.maximumLevel) == "undefined") {
			span = container.maximumLevel = getElementsByClass("tal-infobox-maxlevel", talentlib.container)[0]
			maximumLevelParent = span.parentNode

			span.onclick = function() {
				var input = document.createElement("input")
				var currentLevel = talentlib.maxLevel
				var currentPoints = talentlib.maxPoints
				input.value = currentLevel
				maximumLevelParent.replaceChild(input, span)
				input.focus()
				input.select()

				input.onblur = function() {
					var level = parseInt(input.value)
					var points = talent_definitions["talentsAtLevel"][level]

					if ((level < TALENT_LEVEL_OFFSET) || (isNaN(level)) || (isNaN(points)) || points < talentlib.points || level > TALENT_MAX_LEVEL) {
						level = currentLevel
						points = currentPoints
					}

					span.innerHTML = level
					talentlib.maxLevel = level
					talentlib.maxPoints = points
					span.onmouseup = function() {}
					input.onblur = function() {}

					maximumLevelParent.replaceChild(span, input)
					talentlib.drawTalentPane()
					talentlib.drawInfoBox()

					return false
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
						if (input.parentNode != null) container.summary.replaceChild(span, input);
					}
					else if (key == 38) { // Up arrow
						input.value = parseInt(input.value) + 1
					}
					else if (key == 40) { // Down arrow
						input.value = parseInt(input.value) - 1
					}
				}
			}
		}

		if (typeof(container.trees) == "undefined") {
			container.trees = {"length": 0}

			var containers = getElementsByClass("tal-summary-tree", talentlib.container)
			var icons = getElementsByClass("tal-tree-icon", talentlib.container)
			var resets = getElementsByClass("tal-tree-reset", talentlib.container)
			var names = getElementsByClass("tal-tree-name", talentlib.container)
			var points = getElementsByClass("tal-tree-point", talentlib.container)
			var link = getElementsByClass("tal-link", talentlib.container)[0]

			link.onclick = link.select

			for (var i = 0; i < talentlib.trees.length; i++) {
				var tree = {}

				tree.container = containers[i]
				tree.pointsLabel = names[i]
				tree.icon = icons[i]
				tree.reset = resets[i]
				tree.points = points[i]

				tree.reset.treeid = i
				tree.reset.onclick = function() {
					talentlib.resetTree(this.treeid)
					if (talentlib.points == 0) {
						talentlib.selectTree(-1)
						talentlib.drawTree(this.treeid)
						talentlib.toggleSummary(false)
					} else {
						talentlib.selectTree(talentlib.findSelectedTree())
					}
					return false
				}

				container.trees[i] = tree
				container.trees.length++
			}
		}

		for (var i = 0; i < talentlib.trees.length; i++) {
			var tree = container.trees[i]
			setImageSrc(tree.icon, ICONS_PATH + talentlib.trees[i].icon + ".png")
			tree.points.innerHTML = talentlib.trees[i].points
			tree.pointsLabel.innerHTML = talentlib.trees[i].name + ": "

			if (buildstr.length > 0) buildstr += "/";
			buildstr += talentlib.trees[i].points
		}

		var roles = getElementsByClass("tal-tree-roles")
		for (var i = 0; i < talentlib.trees.length; i++) {
			var tree = container.trees[i]
			var summary = talent_definitions.tabs[talentlib.trees[i].id]
			talentlib.addTooltip(tree.icon,
				'<div class="tt-spell sigrie-tooltip">' +
					'<div class="tts-rank">' + talentlib.getRolesText(summary.roles) + "</div>" +
					'<div class="tt-name tts-name">' + talentlib.trees[i].name + "</div>" +
					'<div class="tts-description">' + summary.description + "</div>" +
					'<div class="tal-tooltip-learn" style="display: block;">Click to toggle summary</div>' +
				"</div>")
			tree.icon.onclick = talentlib.toggleSummary

			talentlib.drawRoles(roles[i], summary.roles)
		}

		container.currentClass.innerHTML = talentlib.currentClassName + " (" + buildstr + ")"
		if (typeof talentlib.selectedTree != "undefined" && talentlib.selectedTree != -1) {
			container.currentClass.innerHTML = talentlib.trees[talentlib.selectedTree].name + " " + container.currentClass.innerHTML
		}
		container.spentPoints.innerHTML = talentlib.points
		container.remaining.innerHTML = talentlib.maxPoints
		container.requiredLevel.innerHTML = Math.max(1, talent_definitions["levelForTalents"][talentlib.points])
		container.maximumLevel.innerHTML = talentlib.maxLevel
	},

	drawInfoboxPair: function(text) {
		var value = document.createElement("span")
		var label = document.createElement("span")
		var container = talentlib.infoboxContainer

		label.innerHTML = text + ": "
		value.labelElement = label

		addClass(value, "tal-infobox-value")
		addClass(label, "tal-infobox-label")

		container.summary.appendChild(label)
		container.summary.appendChild(value)
		container.summary.appendChild(document.createElement("br"))

		return value
	},

	drawGlyphs: function() {
		var glyphs = getElementsByClass("tal-glyph", talentlib.container)
		talentlib.glyphs_slots = [[], [], []]
		talentlib.chosen_glyphs = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

		for (var k in glyphs) {
			!function (k) {
				var slot = glyphs[k].getAttribute("data-glyphslot")
				var type = glyphs[k].getAttribute("data-glyphtype")

				talentlib.glyphs_slots[type][slot] = glyphs[k]

				talentlib.setGlyph(type, slot, -1)
				glyphs[k].onmousedown = function(event) {
					if (typeof(event) == "undefined") event = window.event;

					var rightClick = false
					if (typeof(event.which) == "number") rightClick = (event.which == 3)
					if (typeof(event.button) == "number") rightClick = (event.button == 2)

					if (rightClick) {
						talentlib.closeGlyphsList(type, slot, -1)
					} else {
						talentlib.drawGlyphsList(glyphs[k], type, slot)
					}
				}

				glyphs[k].oncontextmenu = function () { return false; }
			}(k)
		}

		var back = getElementsByClass("tal-glyph-overlay-back")[0]
		back.onclick = function () { talentlib.closeGlyphsList() }

		var resets = getElementsByClass("tal-glyph-reset")
		for (var id in resets) {
			!function (id) {
				var type = resets[id].getAttribute("data-glyphtype")

				resets[id].onclick = function () {
					talentlib.resetGlyph(type)
					talentlib.saveTalents()
				}
			}(id)
		}
	},

	resetGlyph: function (type) {
		for (var slot = 0; slot < TALENT_GLYPHS_PER_TYPE; ++slot) {
			talentlib.setGlyph(type, slot, -1)
		}
	},

	updateSpellsArray: function () {
	    var newSpells = []

		for (var i = 0; i < talent_definitions["primarySpells"].length; ++i) {
			var spell = talent_definitions["primarySpells"][i]
			if (spell.spell in TALENT_SPELLS_FIRST) {
				newSpells.unshift(spell)
			} else {
				newSpells.push(spell)
			}
		}

		talent_definitions["primarySpells"] = newSpells
	},

	updateGlyphsArray: function () {
		// Drain Soul: Mage -> Warlock
		talent_definitions.glyphs.WARLOCK[58271] = talent_definitions.glyphs.MAGE[58271]
		delete talent_definitions.glyphs.MAGE[58271]

		// Penguin: Druid -> Mage
		talent_definitions.glyphs.MAGE[58239] = talent_definitions.glyphs.DRUID[58239]
		delete talent_definitions.glyphs.DRUID[58239]

		var glyphs = {}
		var k = 0

		for (var cls in talent_definitions.glyphs) {
			var class_glyphs = talent_definitions.glyphs[cls]
			var class_id = talentlib.findClass(cls)

			glyphs[class_id] = [[], [], []]
			for (var i in class_glyphs) {
				var glyph = class_glyphs[i]
				glyph.id = +i
				glyphs[class_id][glyph.type].push(glyph)
			}
			for (var i in glyphs[class_id]) {
				glyphs[class_id][i].sort(function (a, b) { return a.name > b.name ? 1 : -1; })
			}
		}
		talent_definitions.glyphs = glyphs
	},

	drawGlyphsList: function (element, type, slot) {
		var overlay = getElementsByClass("tal-glyph-overlay")[0]
		var back = getElementsByClass("tal-glyph-overlay-back")[0]

		back.style.display = "block"
		back.onclick = function () { talentlib.closeGlyphsList() }
		overlay.style.display = "block"

		var table = getElementsByClass("tal-glyph-table", overlay)[0]

		while (table.firstChild) {
			table.removeChild(table.firstChild)
		}

		var tbody = document.createElement("tbody")
		table.appendChild(tbody)

		var glyphs = talent_definitions.glyphs[talentlib.getCurrentClass()][type]
		for (var i in glyphs) {
			var glyph = glyphs[i]
			var tr = document.createElement("tr")

			var icon = document.createElement("td")
			addClass(icon, "tal-glyph-icon")
			icon.innerHTML = '<img src="' + ICONS_PATH + glyph.icon + '.png" />'
			tr.appendChild(icon)

			var name = document.createElement("td")
			addClass(name, "tal-glyph-name")
			name.innerHTML = glyph.spell_name
			tr.appendChild(name)

			var desc = document.createElement("td")
			addClass(desc, "tal-glyph-desc")
			desc.setAttribute("title", glyph.description)
			desc.innerHTML = '<div class="crop">' + glyph.description + "</div>"
			tr.appendChild(desc)

			tbody.appendChild(tr)
			if (Array.indexOf(talentlib.chosen_glyphs[type], +i + 1) != -1) {
				addClass(tr, "tal-glyph-used")
			}
			else {
				+function (glyph_id) {
					tr.onclick = function() { talentlib.closeGlyphsList(type, slot, glyph_id) }
				}(i)
			}
		}
		tr = document.createElement("tr")
		td = document.createElement("td")
		addClass(td, "tal-glyph-empty")
		td.innerHTML = "&lt;Empty Glyph&gt;"
		td.colSpan = 10
		tr.appendChild(td)
		tbody.appendChild(tr)
		tr.onclick = function() { talentlib.closeGlyphsList(type, slot, -1) }

		var quit = getElementsByClass("tal-glyph-quit")[0]
		quit.onclick = function () { talentlib.closeGlyphsList() }
	},

	closeGlyphsList: function(type, slot, glyph_id) {
		var overlay = getElementsByClass("tal-glyph-overlay")[0]
		var back = getElementsByClass("tal-glyph-overlay-back")[0]

		overlay.style.display = "none"
		back.style.display = "none"

		if (typeof type != "undefined") {
			talentlib.setGlyph(type, slot, glyph_id)
			talentlib.startUpdateTimer()
		}
	},

	setGlyph: function(type, slot, glyph_id) {
		var glyph_slot = talentlib.glyphs_slots[type][slot]
		var glyph = talent_definitions.glyphs[talentlib.getCurrentClass()][type][glyph_id]

		if (glyph_id != -1) {
			talentlib.addIcon(glyph_slot, glyph.spell_name, null, ICONS_PATH + glyph.icon + ".png")
			talentlib.addTooltip(glyph_slot,
					'<div class="tt-spell sigrie-tooltip">' +
						'<div class="tt-name tts-name">' + glyph.spell_name + "</div>" +
						'<div class="tts-description">' + glyph.description + "</div>" +
						'<div class="tal-tooltip-unlearn">Right click to remove</div>' +
					"</div>")
			removeClass(glyph_slot, "tal-glyph-emptyglyph")
		} else {
			talentlib.addIcon(glyph_slot, "<Empty Glyph>", null, IMAGE_PATH + "empty.png")
			addClass(glyph_slot, "tal-glyph-emptyglyph")
			talentlib.addTooltip(glyph_slot,
					'<div class="tt-spell sigrie-tooltip">' +
						'<div class="tt-name tts-name">&lt;Empty Glyph&gt;</div>' +
						'<div class="tal-tooltip-learn" style="display: block;">Click to learn a glyph</div>' +
					"</div>")
		}
		glyph_slot.firstChild.onclick = function () { return false; }

		talentlib.chosen_glyphs[type][slot] = +glyph_id + 1
	},

	drawTree: function(treeindex, rowstart, rowend, isDrawing) {
		var tree = talentlib.trees[treeindex]
		var tab = talentlib.tabs[treeindex]
		var deps = []

		if (typeof(rowstart) == "undefined") rowstart = 0;
		if (typeof(rowend) == "undefined") rowend = tree.rowcount;
		if (typeof(isDrawing) == "undefined") isDrawing = false;

		for (var row = rowstart; row < rowend; row++) {
			for (var col in tree.rows[row]) {
				if (!isNaN(col)) {
					var talent = tree.rows[row][col]
					talentlib.drawTalent(treeindex, col, row)

					if ((isDrawing) && (talent.dependants.length > 0)) {
						deps.push(talent.dependants)
					}
				}
			}
		}

		for (var i = 0; (i < deps.length) && (isDrawing); i++) {
			for (var j = 0; j < deps[i].length; j++) {
				var talent = deps[i][j]
				talentlib.drawTalentBranches(treeindex, talent.column, talent.row)
			}
		}

		if (isDrawing) {
			setImageSrc(tab.background, IMAGE_PATH + "/backgrounds/" + tree.background + ".png")
			tab.background.style.width = tab.tree.clientWidth + "px"
			tab.background.style.height = tab.tree.clientHeight + "px"
		}
	},

	drawTalent: function(treeindex, col, row) {
		var tree = talentlib.trees[treeindex]
		var tab = talentlib.tabs[treeindex]
		var talent = tree.rows[row][col]
		var container = talent.container
		var image = talent.image
		var overlay = talent.image
		var rank = talent.rankDiv

		if (typeof(container) == "undefined") {
			tab.tree.appendChild(container = talent.container = document.createElement("div"))
			container.appendChild(image = talent.image = document.createElement("img"))
			container.appendChild(rank = talent.rankDiv = document.createElement("div"))

			addClass(container, "tal-talent")
			container.style.top = (tab.top + (row * (TALENT_ICON_SIZE + TALENT_ICON_MARGIN) + TALENT_ICON_MARGIN)) + "px"
			container.style.left = (tab.left + (col * (TALENT_ICON_SIZE + TALENT_ICON_MARGIN) + TALENT_ICON_MARGIN)) + "px"
			container.onmousedown = function(event) {
				if (typeof(event) == "undefined") event = window.event;

				var rightClick = false;
				if (typeof(event.which) == "number") rightClick = (event.which == 3);
				if (typeof(event.button) == "number") rightClick = (event.button == 2);
				if (typeof(event.shiftKey) == "boolean") rightClick = rightClick || event.shiftKey;

				if (rightClick) {
					talentlib.decreaseRank(treeindex, col, row)
					return false
				}
				else {
					talentlib.increaseRank(treeindex, col, row)
					return false
				}
			}
			container.onmouseover = function() {
				talentlib.showTalentTooltip(treeindex, col, row)
			}
			container.onmouseout = talentlib.hideTooltips
			container.oncontextmenu = function() { return false; }

			addClass(image, "tal-talent-icon")
			addClass(rank, "tal-rank")
		}
		else {
			// We don't want to draw branches when we're still drawing talents
			talentlib.drawTalentBranches(treeindex, col, row)
		}

		rank.innerHTML = talent.rank

		if (talent.rank == talent.ranks) {
			addClass(rank, "tal-rank-max")
			addClass(container, "tal-rank-max")
		}
		else {
			removeClass(rank, "tal-rank-max")
			removeClass(container, "tal-rank-max")
		}

		var canSpend = (talentlib.points < talentlib.maxPoints) && (tree.points >= (row * TALENT_POINTS_PER_ROW))
		canSpend = canSpend && ((talentlib.points >= TALENT_SPEND_MIN) || (talentlib.points == 0) || (tree.points > 0))

// 		if (talentlib.selectedTree != -1 && talentlib.selectedTree != treeindex) {
// 			canSpend = false
// 		}

		if ((canSpend) && (talent.depends_points > 0)) {
			var dep = tree.rows[talent.depends_row][talent.depends_column]
			canSpend = (dep.rank >= talent.depends_points)
		}

		if ((canSpend) || (talent.rank > 0)) {
			addClass(rank, "tal-rank-spendable")
			addClass(container, "tal-rank-spendable")
			setImageSrc(image, ICONS_PATH + talent.icon + ".png")
		}
		else {
			removeClass(rank, "tal-rank-spendable")
			removeClass(container, "tal-rank-spendable")
			setImageSrc(image, ICONS_PATH_GREYSCALE + talent.icon + ".png")
		}
	},

	drawTalentBranches: function(treeindex, col, row) {
		var tree = talentlib.trees[treeindex]
		var tab = talentlib.tabs[treeindex]
		var talent = tree.rows[row][col]
		var branches = talent.branches

		if ((talent.depends_points <= 0) || (talent.depends_column < 0) || (talent.depends_row < 0)) return false;

		var depends = tree.rows[talent.depends_row][talent.depends_column]
		var canSpend = (depends.rank >= talent.depends_points) && (tree.points >= TALENT_POINTS_PER_ROW * row)
		if ((canSpend) && (talent.rank < talent.ranks)) canSpend = (talentlib.points < talentlib.maxPoints);
// 		if (talentlib.selectedTree != -1 && talentlib.selectedTree != treeindex) {
// 			canSpend = false
// 		}

		if (typeof(branches) == "undefined") {
			branches = talent.branches = []
			var depTop = getOffsetTop(depends.container)
			var depLeft = getOffsetLeft(depends.container)
			var talTop = getOffsetTop(talent.container)
			var talLeft = getOffsetLeft(talent.container)
			depTop = depends.container.offsetTop
			depLeft = depends.container.offsetLeft
			talTop = talent.container.offsetTop
			talLeft = talent.container.offsetLeft
			var arrow = document.createElement("div")
			var doneArrow = false

			addClass(arrow, "tal-arrow");
			if (!canSpend) addClass(arrow, "tal-branch-disabled");
			branches.push(arrow)

			if (row > talent.depends_row) {
				var branch = document.createElement("div")
				var size = row - talent.depends_row
				var height = (TALENT_ICON_SIZE + TALENT_ICON_MARGIN) * size - TALENT_ICON_MARGIN

				addClass(branch, "tal-branch-ver")
				if (!canSpend) addClass(branch, "tal-branch-disabled");
				branch.style.height = height + "px"
				branch.style.top = (depTop + TALENT_ICON_MARGIN) + "px"
				branch.style.left = (talLeft + TALENT_ARROW_OFFSET) + "px"
				branches.push(branch)
				tab.tree.appendChild(branch)

				addClass(arrow, "tal-branch-ver")
				arrow.style.top = talTop + "px"
				arrow.style.left = (talLeft + TALENT_ARROW_OFFSET) + "px"
				doneArrow = true
			}
			if (col > talent.depends_column) {
				var branch = document.createElement("div")
				var size = col - talent.depends_column
				var width = (TALENT_ICON_SIZE + TALENT_ICON_MARGIN) * size

				addClass(branch, "tal-branch-hor")
				if (!canSpend) addClass(branch, "tal-branch-disabled");
				branch.style.width = width + "px"
				branch.style.top = (depTop + TALENT_ARROW_OFFSET) + "px"
				branch.style.left = (depLeft + TALENT_ICON_MARGIN) + "px"
				branches.push(branch)
				tab.tree.appendChild(branch)

				if (!doneArrow) {
					addClass(arrow, "tal-branch-hor")
					addClass(arrow, "tal-arrow-right")
					arrow.style.top = (talTop + TALENT_ARROW_OFFSET) + "px"
					arrow.style.left = talLeft + "px"
					doneArrow = true
				}
			}
			else {
				var branch = document.createElement("div")
				var size = talent.depends_column - col
				var width = (TALENT_ICON_SIZE + TALENT_ICON_MARGIN) * size

				addClass(branch, "tal-branch-hor")
				if (!canSpend) addClass(branch, "tal-branch-disabled");
				branch.style.width = width + "px"
				branch.style.top = (depTop + TALENT_ARROW_OFFSET) + "px"
				branch.style.left = (talLeft + TALENT_ICON_MARGIN) + "px"
				branches.push(branch)
				tab.tree.appendChild(branch)

				if (!doneArrow) {
					addClass(arrow, "tal-branch-hor")
					addClass(arrow, "tal-arrow-left")
					arrow.style.top = (talTop + TALENT_ARROW_OFFSET) + "px"
					arrow.style.left = (talLeft + TALENT_ICON_SIZE - TALENT_ARROW_SIZE) + "px"
					doneArrow = true
				}
			}

			tab.tree.appendChild(arrow)
		}
		else {
			for (var i = 0; i < branches.length; i++) {
				var branch = branches[i]

				if (canSpend) {
					removeClass(branch, "tal-branch-disabled")
				}
				else {
					addClass(branch, "tal-branch-disabled")
				}
			}
		}
	},

	parseTabs: function() {
		var trees = talentlib.trees = {}
		var talents = talent_definitions[talentlib.currentClass][talentlib.currentBuild].talents
		var deps = []
		trees.length = 0

		for (var id in talent_definitions.tabs) {
			var tab = talent_definitions.tabs[id]

			if (tab["class"].toUpperCase() == talentlib.currentClass.toUpperCase()) {
				if (typeof(trees[tab.page]) == "undefined") trees.length++;

				if ((typeof(trees[tab.page]) == "undefined") || (trees[tab.page].id > id)) {
					trees[tab.page] = {
						"name": tab.name,
						"id": id,
						"icon": tab.icon,
						"points": 0,
						"rows": {},
						"rowcount": 0,
						"background": tab.internal_name.toLowerCase()
					}
				}
			}
		}

		for (var id in talents) {
			var talent = talents[id]
			var page = talent_definitions.tabs[talent.tab].page
			var tree = talentlib.trees[page]
			var dep_points = -1
			var dep_col = -1
			var dep_row = -1

			if (talent.depends > 0) {
				var dep = talents[talent.depends]
				if (dep) {
					dep_points = talent.depends_count + 1
					dep_col = dep.column
					dep_row = dep.row
				}
			}

			if (typeof(trees[page].rows[talent.row]) != "object") {
				trees[page].rows[talent.row] = {"points": 0}
				trees[page].rowcount++
			}

			var newtal = trees[page].rows[talent.row][talent.column] = {
				"ranks": talent.max_ranks,
				"id": id,
				"rank": 0,
				"icon": talent.icon,
				"depends_points": dep_points,
				"depends_column": dep_col,
				"depends_row": dep_row,
				"dependants": [],
				"row": talent.row,
				"column": talent.column,
				"name": talent.name,
				"treeindex": page,
				"active": talent.active
			}

			if (dep_points > -1) {
				deps.push({
					"row": talent.row,
					"col": talent.column,
					"page": page,
					"dep_row": dep_row,
					"dep_col": dep_col
				})
			}
		}

		for (var i = 0; i < deps.length; i++) {
			var dep = deps[i]
			var talent = trees[dep.page].rows[dep.row][dep.col]
			var dependancy = trees[dep.page].rows[dep.dep_row][dep.dep_col]
			dependancy.dependants.push(talent)
		}
	},

	increaseRank: function(treeindex, col, row) {
		var tree = talentlib.trees[treeindex]
		var talent = tree.rows[row][col]

		if (talent.rank == talent.ranks) return false;
		if (tree.points < (row * TALENT_POINTS_PER_ROW)) return false;
		if (talentlib.points >= talentlib.maxPoints) return false;
		if ((talentlib.points > 0) && (talentlib.points < TALENT_SPEND_MIN) && (tree.points <= 0)) return false;
// 		if (talentlib.selectedTree != -1 && talentlib.selectedTree != treeindex) return false

		if (talent.depends_points > 0) {
			var dep = tree.rows[talent.depends_row][talent.depends_column]
			if (dep.rank < talent.depends_points) return false;
		}

		if (talentlib.selectedTree == -1) {
			talentlib.selectTree(treeindex)
		    talentlib.drawTree(treeindex)
		}

		talent.rank++
		tree.points++
		tree.rows[row].points++
		talentlib.points++

		if (talentlib.points == talentlib.maxPoints) {
			talentlib.drawTalentPane()
		}
		else if ((tree.points == TALENT_SPEND_MIN) || (talentlib.points == 1)) {
			talentlib.drawTalentPane()
		}
		else if (tree.points % TALENT_POINTS_PER_ROW == 0) {
			talentlib.drawTree(treeindex, row + 1)
		}

		for (var i = 0; i < talent.dependants.length; i++) {
			var dependant = talent.dependants[i]
			talentlib.drawTalent(treeindex, dependant.column, dependant.row)
		}

		talentlib.drawTalent(treeindex, col, row)
		talentlib.updateTalentTooltip(treeindex, col, row)
		talentlib.startUpdateTimer()
		talentlib.drawInfoBox()
	},

	decreaseRank: function(treeindex, col, row) {
		var tree = talentlib.trees[treeindex]
		var talent = tree.rows[row][col]
		var lastrow = Math.min(Math.floor(tree.points / TALENT_POINTS_PER_ROW), tree.rowcount - 1)

		if (talent.rank == 0) return false;
		if (tree.points == (row * TALENT_POINTS_PER_ROW)) return false;
		if ((talentlib.points > TALENT_SPEND_MIN) && (tree.points == TALENT_SPEND_MIN)) return false;

		var invalid = false
		var points = 0

		tree.rows[row].points--
		for (var i = 0; (i <= lastrow) && (!invalid); i++) {
			points += tree.rows[i].points
			if ((typeof(tree.rows[i + 1]) == "object") && (tree.rows[i + 1].points > 0)) {
				if (points < (i + 1) * TALENT_POINTS_PER_ROW) invalid = true;
			}
		}
		tree.rows[row].points++
		if (invalid) {
			return false;
		}

		if (talent.dependants.length > 0) {
			for (var i = 0; i < talent.dependants.length; i++) {
				var dep = talent.dependants[i]
				if (dep.rank > 0) {
					if (dep.depends_points >= talent.rank) return false;
				}
			}
		}

		talent.rank--
		var oldpoints = tree.points--
		tree.rows[row].points--
		talentlib.points--

		if (talentlib.points == talentlib.maxPoints - 1) {
			talentlib.drawTalentPane()
		}
		else if ((tree.points == TALENT_SPEND_MIN - 1) || (talentlib.points == 0)) {
			talentlib.drawTalentPane()
		}
		else if (oldpoints % TALENT_POINTS_PER_ROW == 0) {
			talentlib.drawTree(treeindex, row + 1)
		}

		for (var i = 0; i < talent.dependants.length; i++) {
			var dependant = talent.dependants[i]
			talentlib.drawTalent(treeindex, dependant.column, dependant.row)
		}


		if (talentlib.points == 0) {
			talentlib.selectTree(-1)
    		for (var i = 0; i < talentlib.trees.length; i++) {
			    talentlib.drawTree(i)
		    }
		}

		talentlib.drawTalent(treeindex, col, row)
		talentlib.updateTalentTooltip(treeindex, col, row)
		talentlib.startUpdateTimer()
		talentlib.drawInfoBox()
	},

	addTooltip: function(element, text) {
		element.onmouseover = function() {
			talentlib.showTooltip(element, text)
		}
		element.onmouseout = talentlib.hideTooltip
	},

	showTooltip: function(element, text) {
		var tooltip = getElementsByClass("tal-tooltip-spell")[0]

		tooltip.style.visibility = "visible"
		tooltip.innerHTML = text

		var left = getOffsetLeft(element) + element.offsetWidth
		if ((left + tooltip.offsetWidth) > document.body.clientWidth) {
			left -= element.offsetWidth + tooltip.offsetWidth
		}

		tooltip.style.left = left + "px"
		tooltip.style.top = (getOffsetTop(element) - tooltip.offsetHeight) + "px"
	},

	hideTooltip: function() {
		var tooltip = getElementsByClass("tal-tooltip-spell")[0]

		tooltip.style.visibility = 'hidden'
	},

	showTalentTooltip: function(treeindex, col, row) {
		var tree = talentlib.trees[treeindex]
		var talent = tree.rows[row][col]
		var tooltip = talentlib.tooltip

		talentlib.hideTooltips()

		if (typeof(tooltip) == "undefined") {
			document.body.appendChild(tooltip = talentlib.tooltip = document.createElement("div"))
			tooltip.appendChild(tooltip.nameDiv = document.createElement("div"))
			tooltip.appendChild(tooltip.rankDiv = document.createElement("div"))
			tooltip.appendChild(tooltip.reqDiv = document.createElement("div"))
			tooltip.appendChild(tooltip.rowDiv = document.createElement("div"))
			tooltip.appendChild(tooltip.curDiv = document.createElement("div"))
			tooltip.appendChild(tooltip.nextDiv = document.createElement("div"))
			tooltip.appendChild(tooltip.learnDiv = document.createElement("div"))
			tooltip.appendChild(tooltip.unlearnDiv = document.createElement("div"))

			addClass(tooltip, "tal-tooltip")
			addClass(tooltip, "sigrie-tooltip")

			addClass(tooltip.nameDiv, "tt-name")
			addClass(tooltip.nameDiv, "tts-name")
			addClass(tooltip.reqDiv, "ttt-depends")
			addClass(tooltip.rowDiv, "ttt-row")
			addClass(tooltip.rankDiv, "ttt-rank")
			addClass(tooltip.curDiv, "ttt-cur_rank")
			addClass(tooltip.nextDiv, "ttt-next_rank")
			addClass(tooltip.learnDiv, "tal-tooltip-learn")
			addClass(tooltip.unlearnDiv, "tal-tooltip-unlearn")

			tooltip.learnDiv.innerHTML = "Left click to add a point"
			tooltip.unlearnDiv.innerHTML = "Right click to remove a point"
		}

		talentlib.updateTalentTooltip(treeindex, col, row)

		tooltip.style.visibility = "visible"
	},

	updateTalentTooltip: function(treeindex, col, row) {
		var tree = talentlib.trees[treeindex]
		var talent = tree.rows[row][col]
		var tooltip = talentlib.tooltip
		var tooltips = talent_definitions[talentlib.currentClass][talentlib.currentBuild].tooltips[talent.id]
		var spendable = talentlib.points < talentlib.maxPoints
		var prefix = ""
		var suffix = ""

		if (!talent.active) {
			prefix = "<div class='tts-description'>"
			suffix = "</div>"
		}

		tooltip.nameDiv.innerHTML = talent.name
		tooltip.rankDiv.innerHTML = "Rank " + talent.rank + "/" + talent.ranks

		if (talent.rank > 0) {
			tooltip.curDiv.innerHTML = prefix + tooltips[talent.rank] + suffix
			removeClass(tooltip, "tal-tooltip-unlearnt")
		}
		else {
			tooltip.curDiv.innerHTML = ""
			addClass(tooltip, "tal-tooltip-unlearnt")
		}

		if (talent.rank < talent.ranks) {
			tooltip.nextDiv.innerHTML = prefix + tooltips[talent.rank + 1] + suffix
			removeClass(tooltip, "tal-tooltip-maxed")
		}
		else {
			tooltip.nextDiv.innerHTML = ""
			addClass(tooltip, "tal-tooltip-maxed")
			spendable = false
		}

		if (talent.depends_points > 0) {
			var dep = tree.rows[talent.depends_row][talent.depends_column]

			if (talent.depends_points == 1) {
				tooltip.reqDiv.innerHTML = "Requires " + talent.depends_points + " point in " + dep.name
			}
			else {
				tooltip.reqDiv.innerHTML = "Requires " + talent.depends_points + " points in " + dep.name
			}

			if (dep.rank < talent.depends_points) {
				addClass(tooltip, "tal-tooltip-missingdep")
				spendable = false
			}
			else {
				removeClass(tooltip, "tal-tooltip-missingdep")
			}
		}
		else {
			tooltip.reqDiv.innerHTML = ""
			removeClass(tooltip, "tal-tooltip-missingdep")
		}

		if (tree.points < (row * TALENT_POINTS_PER_ROW)) {
			addClass(tooltip, "tal-tooltip-missingpoints")
			spendable = false
		}
		else {
			removeClass(tooltip, "tal-tooltip-missingpoints")
		}

		if (row > 0) {
			tooltip.rowDiv.innerHTML = "Requires " + (row * TALENT_POINTS_PER_ROW) + " points in " + tree.name + " talents"
		}
		else {
			tooltip.rowDiv.innerHTML = ""
		}

		if (spendable) {
			addClass(tooltip, "tal-tooltip-spendable")
		}
		else {
			removeClass(tooltip, "tal-tooltip-spendable")
		}

		var left = getOffsetLeft(talent.container) + talent.container.offsetWidth
		if ((left + tooltip.offsetWidth) > (getOffsetLeft(talentlib.container) + talentlib.container.clientWidth)) {
			left -= talent.container.offsetWidth + tooltip.offsetWidth
		}

		var top = getOffsetTop(talent.container) - tooltip.offsetHeight
		if (top < 0) {
			top += talent.container.offsetHeight + tooltip.offsetHeight
		}

		tooltip.style.left = left + "px"
		tooltip.style.top = top + "px"
	},

	hideTooltips: function() {
		if (typeof(talentlib.tooltip) != "undefined") talentlib.tooltip.style.visibility = "hidden";
	},

	saveTalents: function() {
		var talents = talentlib.buildTalentString()
		var glyphs = talentlib.buildGlyphString()
		currentURL.setKey("hash", "k", talents + "." + (talentlib.currentBuild).toString(36) + "." + talentlib.currentClass  + "." + glyphs)

		document.location.hash = "#" + currentURL.serialize(currentURL.hash)
		getElementsByClass("tal-link")[0].setAttribute("value", BASE_URL + document.location.hash)
	},

	restoreTalents: function() {
		var key = currentURL.getKey("hash", "k", "")
		talentlib.unloadClass()

		var parts = key.split('.')
		talentlib.selectClass(parts[2], parseInt(parts[1], 36), parts[0] || "", parts[3] || "")

		currentURL.setKey("hash", "k", key)
		document.location.hash = "#" + currentURL.serialize(currentURL.hash)
		getElementsByClass("tal-link")[0].setAttribute("value", BASE_URL + document.location.hash)
	},

	getGlyphsSchema: function() {
		var schema = []
		var class_glyphs = talent_definitions.glyphs[talentlib.getCurrentClass()]
		var k = 0
		for (var type in class_glyphs) {
			for (var slot = 0; slot < TALENT_GLYPHS_PER_TYPE; ++slot) {
				schema[k++] = class_glyphs[type].length + 1
			}
		}
		return schema
	},

	buildGlyphString: function() {
		return SmallHash.encode(
			flatten(talentlib.chosen_glyphs),
			talentlib.getGlyphsSchema(),
			TALENT_BASE64)
	},

	loadGlyphString: function(input) {
		var glyphs = SmallHash.decode(
			input,
			talentlib.getGlyphsSchema(),
			TALENT_BASE64
		)

		for (var i in glyphs) {
			talentlib.setGlyph(
				Math.floor(i / TALENT_GLYPHS_PER_TYPE),
				Math.floor(i % TALENT_GLYPHS_PER_TYPE),
				glyphs[i] - 1
			)
		}
	},

	buildTalentString: function() {
		var rangelow = 0
		var rangehigh = TALENT_RANGE_HIGH
		var pos = 0
		var cont = true
		var talents = []
		var visible = [] // 0 = visible, 1 = working on the talent this pass, 2 = done
		var treepoints = {}
		var result = ""
		var pointsleft = talentlib.maxPoints

		for (var t = 0; t < talentlib.trees.length; t++) {
			var tree = talentlib.trees[t]
			treepoints[t] = 0

			for (var y = 0; y < tree.rowcount; y++) {
				for (var x = 0; x < TALENT_MAX_COLS; x++) {
					var talent = tree.rows[y][x]
					if (typeof(talent) == "object") {
						talent._buildpos = talents.push(talent) - 1
						visible.push(0)
					}
				}
			}
		}

		while (cont) {
			cont = false

			for (var i = 0; i < visible.length; i++) {
				var vis = visible[i]
				var talent = talents[i]
				var tree = talentlib.trees[talent.treeindex]

				if (vis == 0) {
					if (treepoints[talent.treeindex] >= talent.row * TALENT_POINTS_PER_ROW) {
						vis = 1

						if (talent.depends_points > 0) {
							var dep = tree.rows[talent.depends_row][talent.depends_column]
							if ((visible[dep._buildpos] != 2) || (dep.rank < talent.depends_points)) vis = 0;
						}
					}
					visible[i] = vis
				}
			}

			for (var i = 0; i < talents.length; i++) {
				var talent = talents[i]
				var tree = talentlib.trees[talent.treeindex]

				if (pointsleft <= 0) break;

				if (visible[i] == 1) {
					cont = true
					visible[i] = 2

					var ranks = Math.min(talent.ranks, pointsleft) + 1
					var rank = Math.min(talent.rank, ranks - 1)
					var len = rangehigh - rangelow

					treepoints[talent.treeindex] += rank
					pointsleft -= rank

					rangehigh = rangelow + Math.floor(len * (rank + 1) / ranks)
					rangelow += Math.floor(len * rank / ranks)

					while ((rangelow & TALENT_RANGE_HIGH_MASK) == (rangehigh & TALENT_RANGE_HIGH_MASK)) {
						pos = (rangelow >> TALENT_RANGE_BITS - 6) & 63
						var len = rangehigh - rangelow
						rangelow = ((rangelow & TALENT_RANGE_LOW_MASK) << 6)
						rangehigh = rangelow + len * 64 - 1
						result += TALENT_BASE64.substr(pos, 1)
					}
				}
			}
		}

		pos = (rangehigh >> (TALENT_RANGE_BITS - 6)) & 63
		result += TALENT_BASE64.substr(pos, 1)

		return result
	},

	loadTalentString: function(input) {
		var rangelow = 0
		var rangehigh = TALENT_RANGE_HIGH
		var rangeval = 0
		var cont = true
		var talents = []
		var visible = [] // 0 = visible, 1 = working on the talent this pass, 2 = done
		var pointsleft = talentlib.maxPoints

		for (var t = 0; t < talentlib.trees.length; t++) {
			var tree = talentlib.trees[t]

			for (var y = 0; y < tree.rowcount; y++) {
				for (var x = 0; x < TALENT_MAX_COLS; x++) {
					var talent = tree.rows[y][x]
					if (typeof(talent) == "object") {
						talent._buildpos = talents.push(talent) - 1
						visible.push(0)
					}
				}
			}
		}

		for (var i = 0; i < TALENT_RANGE_BITS / 6; i++) {
			rangeval = (rangeval & (TALENT_RANGE_HIGH >> 6)) << 6
			if ((input.length > 0) && (TALENT_BASE64.indexOf(input.substr(0, 1) >= 0))) {
				rangeval = rangeval | TALENT_BASE64.indexOf(input.substr(0, 1))
				input = input.substr(1);
			}
		}

		while (cont) {
			cont = false

			for (var i = 0; i < visible.length; i++) {
				var vis = visible[i]
				var talent = talents[i]
				var tree = talentlib.trees[talent.treeindex]

				if (vis == 0) {
					if (tree.points >= talent.row * TALENT_POINTS_PER_ROW) {
						vis = 1

						if (talent.depends_points > 0) {
							var dep = tree.rows[talent.depends_row][talent.depends_column]
							if ((visible[dep._buildpos] != 2) || (dep.rank < talent.depends_points)) vis = 0;
						}
					}
					visible[i] = vis
				}
			}

			for (var i = 0; i < talents.length; i++) {
				var talent = talents[i]
				var tree = talentlib.trees[talent.treeindex]

				if (pointsleft <= 0) break;

				if (visible[i] == 1) {
					cont = true
					visible[i] = 2

					var ranks = Math.min(talent.ranks, pointsleft) + 1
					var rank = 0
					var len = rangehigh - rangelow

					for (rank = 0; rank < ranks; rank++) {
						if ((rangeval >= rangelow + Math.floor(len * rank / ranks)) && (rangeval < rangelow + Math.floor(len * (rank + 1) / ranks))) break;
					}

					talent.rank = rank
					tree.points += rank
					tree.rows[talent.row].points += rank
					talentlib.points += rank
					pointsleft -= rank

					rangehigh = rangelow + Math.floor(len * (rank + 1) / ranks)
					rangelow += Math.floor(len * rank / ranks)

					while ((rangelow & TALENT_RANGE_HIGH_MASK) == (rangehigh & TALENT_RANGE_HIGH_MASK)) {
						len = rangehigh - rangelow
						rangelow = ((rangelow & TALENT_RANGE_LOW_MASK) << 6)
						rangehigh = rangelow + len * 64 - 1
						rangeval = (rangeval & (TALENT_RANGE_HIGH >> 6)) << 6

						if ((input.length > 0) && (TALENT_BASE64.indexOf(input.substr(0, 1) >= 0))) {
							rangeval = rangeval | TALENT_BASE64.indexOf(input.substr(0, 1))
							input = input.substr(1)
						}
					}
				}
			}
		}

		talentlib.selectTree(talentlib.findSelectedTree())
		talentlib.drawInfoBox()
	},

	talentExists: function(tree, row, col) {
		if (tree >= 3) return false;
		if (row >= 7) return false;
		if (col >= 4) return false;
		return !!talentlib.trees[tree].rows[row][col];
	},

	getHorizontalDependency: function(tree, row, col) {
		var talent = talentlib.trees[tree].rows[row][col]
		if (!talent) return 0;
		if (talent.depends_points == 0 || talent.depends_row != row) return 0;
		return talent.depends_column;
	},

	createPreviewTalentScript: function() {
		var ret = ""
		var selectedTree = talentlib.selectedTree
		if (selectedTree == -1) return false;
		for (var i = 0; i < 3; i++) {
			var tree = (selectedTree + i) % 3
			ret += (tree + 1) + ","
			var index = 0
			for (row = 0; row < 7; row++) { // maxRows = 7
				var waiting = ""
				for (col = 0; col < 4; col++) { // maxCols = 4
					if (talentlib.talentExists(tree, row, col)) index++;
					else continue;

					var points = talentlib.trees[tree].rows[row][col].rank
					if (points > 0) {
						if (talentlib.getHorizontalDependency(tree, row, col) > col) {
							waiting = (index * 10 + points) + "," + waiting
						} else {
							ret += (index * 10 + points) + ","
						}
					}
				}
				ret += waiting
			}
		}

		return prompt("Copy the following in-game. Only previews the talents, does not actually learn them. Buggy for Arcane Mages!",
		              "/run t,p,a={" + ret + "}SetPreviewPrimaryTalentTree(t[1],GetActiveTalentGroup())for i=1,#t do a=t[i]if a<9 then p=a else AddPreviewTalentPoints(p,floor(a/10),a%10)end end"
		)
	},

	startUpdateTimer: function() {
		if (talentlib.updateTimer > -1) {
			window.clearTimeout(talentlib.updateTimer)
		}
		talentlib.updateTimer = window.setTimeout(talentlib.saveTalents, TALENT_UPDATE_INTERVAL)
	},

	destroyCalculator: function(error) {
		if (typeof(error) == "object") error = error.status + " (" + error.statusText + ") in request to: " + error.url;

		talentlib.container.innerHTML = "Uhoh! An error has occured. Please reload the page and try again. " +
		                                "If this error persists, please contact someone on <a href='http://webchat.quakenet.org/?channels=mmo-champion'>IRC</a>.<br />\n" +
		                                "Error details: " + error
	}
}

addLoadEvent(talentlib.init)
