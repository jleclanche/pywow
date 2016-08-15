/**
 * Generic
 */

function doGenericName(txt, cell, row, id) {
	cell.innerHTML = ""
	if (txt == "") txt = "** No Name #"+id+" **";
	var n = document.createTextNode(txt)
	var a = document.createElement("a")
	var link = row["link"]
	cell.style.textAlign = "left" // dont center name column
	cell.style.width = "100%" // Give it maximum width possible
	a.style.verticalAlign = "bottom"
	
	if (link) {
		a.href = link
		
		// add tooltips
		a.onmouseover = function(evt) { ttlib.startTooltip(this) }
		a.onmouseout = function(evt) { ttlib.hide() }
	}
	
	a.appendChild(n)
	cell.appendChild(a)
	
	return cell
}

function doGenericNameWithIcon(txt, cell, row, id) {
	span = doGenericName(txt, cell, row, id)
	span.style.paddingLeft = "2px"
	
	img = document.createElement("img")
	img.width = 20
	img.height = 20
	img.src = "http://static.mmo-champion.com/db/img/icons/" + row["icon"] + ".png"
	img.style.margin = "2px 4px 0px 0" // TODO move to css
	img.style["float"] = "left"
	a = document.createElement("a")
	a.href = row["link"]
	a.appendChild(img)
	cell.insertBefore(a, cell.firstChild)
	cell.style.verticalAlign = "sub"
	return cell
}

function doGenericLookupReplace(txt, cell, row, array) {
	cell.innerHTML = array[txt]
	return cell
}

function doGenericLinkReplace(txt, cell, link) {
	cell.innerHTML = ""
	var a = document.createElement("a")
	a.href = link
	a.innerHTML = txt
	a.className = "link"
	cell.appendChild(a)
	return cell
}

function doSkillWithLevel(txt, cell, row) {
	if (row["required_skill_id"]) {
		var skill = document.createElement("a")
		skill.href = "/skill/" + row["required_skill_id"]
		skill.appendChild(document.createTextNode(txt))
		skill.className = "link"
	} else {
		var skill = document.createTextNode(txt)
	}
	cell.appendChild(skill)
	if (row["required_skill_level"] > 1) {
		var rank = document.createTextNode(" (" + row["required_skill_level"] + ")")
		cell.appendChild(rank)
	}
	return cell
}

function doGenericBoolean(txt, cell, row) {
	if (txt == 1) {
		cell.innerHTML = "Yes"
	} else {
		cell.innerHTML = "No"
	}
	return cell
}


/**
 * Achievements
 */

function doAchievementFaction(txt, cell, row) {
	txt += 1 // FIXME should be serverside
	return doGenericLookupReplace(txt, cell, row, FACTIONS)
}

function doAchievementInstance(txt, cell, row) {
	link = "/instance/" + row["instance_id"]
	return doGenericLinkReplace(txt, cell, link)
}

sorttable_template_achievement = {
	"column_order": ["name", "instance", "points", "faction"],
	
	"hooks": {
		"name": doGenericNameWithIcon,
		"faction": doAchievementFaction,
		"instance": doAchievementInstance
	}
}
template_required_for_achievement = sorttable_template_achievement


/**
 * Creatures
 */

function doCreatureCategory(txt, cell, row) {
	link = "/creatures/?category=" + txt
	return doGenericLinkReplace(CREATURE_CATEGORIES[txt], cell, link)
}

function doCreatureType(txt, cell, row) {
	link = "/creatures/?type=" + txt
	return doGenericLinkReplace(CREATURE_TYPES[txt], cell, link)
}

function doCreatureFamily(txt, cell, row) {
	link = "/creatures/?family=" + txt
	return doGenericLinkReplace(CREATURE_FAMILIES[txt], cell, link)
}

function doCreatureName(txt, cell, row) {
	cell = doGenericName(txt, cell, row)
	if (row["title"]) {
		cell.style.lineHeight = "1.1em"
		cell.appendChild(document.createElement("br"))
		var title = document.createTextNode("<" + row["title"] + ">")
		var span = document.createElement("span")
		span.appendChild(title)
		span.style.fontSize = "80%"
		cell.appendChild(span)
	}
	return cell
}

function doLootPercent(txt, cell, row) {
	if (Math.floor(txt) != txt) {
		cell.innerHTML = txt.toFixed(1)
	} else {
		cell.innerHTML = txt
	}
	cell.innerHTML += "%"
	return cell
}

sorttable_template_creature = {
	"column_order": ["name", "category", "type", "family"],
	
	"column_names": {
		"required_skill": "Req. Skill",
		"required_level": "Req. Lvl"
	},
	
	"hooks": {
		"name": doCreatureName,
		"category": doCreatureCategory,
		"family": doCreatureFamily,
		"type": doCreatureType,
		"required_skill": doSkillWithLevel,
		"percent": doLootPercent // TODO move this to template_creature__loot_item
	}
}
template_creaturespell_spell = sorttable_template_creature
template_item__creature_quest_drops = sorttable_template_creature
template_creature__node_zone = sorttable_template_creature
template_creature_starts_quests = sorttable_template_creature
template_creature_faction = sorttable_template_creature


template_solditem_vendor = {
	"column_order": ["name", "price", "category"],
	
	"hooks": {
		"name": doCreatureName,
		"category": doCreatureCategory,
		"family": doCreatureFamily,
		"type": doCreatureType
	}
}

template_trainedspell_spell = {
	"extends": sorttable_template_creature,
	"column_order": ["name", "required_level", "required_skill", "price"]
}

template_creature__loot_item = {
	"extends": sorttable_template_creature,
	"column_order": ["name", "category", "type", "family", "percent"],
	"columns_shown": {"percent": true},
	"column_names": {
		"percent": "%"
	}
}


/**
 * Enchants
 */

sorttable_template_enchant = {
	"column_names": {
		"required_skill": "Req. Skill",
		"required_skill_level": "Req. Skill level"
	},
	
	"column_order": ["name", "required_skill", "charges"],
	
	"hooks": {
		"name": doGenericName,
		"required_skill": doSkillWithLevel
	}
}
template_enchant_required_skill = sorttable_template_enchant
template_enchant_effects = sorttable_template_enchant


/**
 * Encounters
 */

function doEncounterInstance(txt, cell, row) {
	link = "/instance/" + row["instance_id"]
	return doGenericLinkReplace(txt, cell, link)
}

sorttable_template_encounter = {
	"column_order": ["name", "instance"],
	
	"hooks": {
		"name": doGenericName,
		"instance": doEncounterInstance
	}
}
template_encounter_instance = sorttable_template_encounter
template_encounter_instance__heroic = sorttable_template_encounter


/**
 * Glyphs
 */

function doGlyphType(txt, cell, row) {
	link = "/glyphs/?minor=" + txt
	txt = txt == 1 ? "+ Major Glyph" : "- Minor Glyph"
	return doGenericLinkReplace(txt, cell, link)
}

sorttable_template_glyph = {
	"column_names": {
		"minor": "Type"
	},
	
	"column_order": ["name", "minor"],
	
	"columns_shown": {
		"minor": true
	},
	
	"hooks": {
		"name": doGenericName,
		"minor": doGlyphType
	}
}

template_glyph_spell = sorttable_template_glyph


/**
 * Holidays
 */

sorttable_template_holiday = {
	"column_order": ["name"],
	
	"hooks": {
		"name": doGenericName
	}
}


/**
 * Factions
 */

function doFactionParent(txt, cell, row) {
	link = "/faction/" + row["parent_id"]
	return doGenericLinkReplace(txt, cell, link)
}

sorttable_template_faction = {
	"column_order": ["name", "parent"],
	
	"hooks": {
		"name": doGenericName,
		"parent": doFactionParent
	}
}
template_faction_parent = sorttable_template_faction


/**
 * Instances
 */

function doInstanceZone(txt, cell, row) {
	link = "/z/" + row["zone_id"]
	return doGenericLinkReplace(txt, cell, link)
 	return cell
}

sorttable_template_instance = {
	"column_names": {
		"max_players": "Max. players"
	},
	
	"column_order": ["name", "zone", "max_players"],
	
	"hooks": {
		"name": doGenericName,
 		"zone": doInstanceZone
	}
}
template_instance_continent = sorttable_template_instance
template_instance_zone = sorttable_template_instance


/**
 * Items
 */

function doItemLevel(txt, cell, row) {
	cell.innerHTML = txt
	if (row["required_level"] > 1) {
		cell.innerHTML += " (Req. " + row["required_level"] + ")"
	}
	
	return cell
}

function doItemCategory(txt, cell, row) {
	link = "/items/" + txt + "/" + row["subcategory"]
	return doGenericLinkReplace(ITEM_SUBCLASSES[row["category"]][row["subcategory"]], cell, link)
}

function doItemSlot(txt, cell, row) {
	link = "/items/?slot=" + txt
	txt = SLOTS[txt]
	if (row["bag_slots"]) {
		txt = row["bag_slots"] + " slot " + txt
	}
	return doGenericLinkReplace(txt, cell, link)
}

function doItemName(txt, cell, row) {
	cell = doGenericNameWithIcon(txt, cell, row)
	cell.getElementsByTagName("a")[1].className = "q"+row["quality"]
	if (row["stock"]) {
		var limit = document.createTextNode(" (" + row["stock"] + ")")
		var span = document.createElement("span")
		span.appendChild(limit)
		cell.appendChild(span)
	}
	return cell
}

sorttable_template_item = {
	"column_names": {
		"required_level": "Req. Level"
	},
	
	"column_order": ["name", "price", "level", "category", "slot", "count", "percent"],
	
	"hooks": {
		"name": doItemName,
		"level": doItemLevel,
		"category": doItemCategory,
		"slot": doItemSlot,
		"percent": doLootPercent // TODO move this to template_creature__loot_item
	}
}

template_item__loot_item = {
	"extends": sorttable_template_item,
	"column_order": ["name", "level", "category", "count", "percent"],
	"columns_shown": {"percent": true},
	"column_names": {
		"percent": "%"
	}
}

template_creature_quest_drops = sorttable_template_item
template_item__contains = sorttable_template_item

template_item_related = sorttable_template_item
template_item_zone_bind = sorttable_template_item
template_item_required_holiday = sorttable_template_item
template_item_required_skill = sorttable_template_item
template_item_socket_bonus = sorttable_template_item
template_item_required_faction = sorttable_template_item
template_item_required_spell = sorttable_template_item
template_item_spells = sorttable_template_item // XXX name
template_spell_item_teaches = sorttable_template_item
template_item_starts_quest = sorttable_template_item
template_enchant_property = sorttable_template_item
template_quest_drops = sorttable_template_item
template_itemextendedcost_item = sorttable_template_item
template_item_page = sorttable_template_item

template_solditem_item = sorttable_template_item

function doItemDisenchantAmount(txt, cell, row) {
	var min = txt
	var max = row["amount_max"]
	cell.innerHTML = min
	if (max > min) cell.innerHTML += "-" + max;
	return cell
}

template_item_disenchant = {
	"column_names": {
		"amount_min": "Amount",
		"percent": "%"
	},
	
	"column_order": ["name", "amount_min", "percent"],
	
	"hooks": {
		"name": doItemName,
		"amount_min": doItemDisenchantAmount
	}
}

template_drops = {
	"extends": sorttable_template_item,
	"column_names": {
		"percent": "%"
	}
}


/**
 * Item sets
 */

sorttable_template_itemset = {
	"column_names": {
		"required_skill": "Req. Skill",
		"required_skill_level": "Req. Skill level"
	},
	
	"column_order": ["name", "required_skill"],
	
	"hooks": {
		"name": doGenericName,
		"required_skill": doSkillWithLevel
	}
}
template_itemset_required_skill = sorttable_template_itemset
template_spell_itemset_bonus = sorttable_template_itemset


/**
 * Objects
 */

function doObjectType(txt, cell, row) {
	link = "/objects/" + txt
	return doGenericLinkReplace(row["get_type_display"], cell, link)
}

sorttable_template_object = {
	"column_order": ["name", "type"],
	
	"hooks": {
		"name": doGenericName,
		"type": doObjectType
	}
}
template_object_starts_quests = sorttable_template_object
template__gameobject_page = sorttable_template_object


/**
 * Mails
 */

sorttable_template_mail = {
	"column_order": ["name"],
	"hooks": {
		"name": doGenericName
	}
}
template_mail_attachment = sorttable_template_mail


/**
 * Pages
 */

function doPageNext(txt, cell, row) {
	link = "/page/" + txt
	return doGenericLinkReplace(txt, cell, link)
}

sorttable_template_page = {
	"column_order": ["name", "next_page_id"],
	
	"column_names": {
		"next_page_id": "Next Page"
	},
	
	"hooks": {
		"name": doGenericName,
		"next_page_id": doPageNext
	}
}
template_page_next_page = sorttable_template_page


/**
 * Quests
 */

function doQuestZone(txt, cell, row) {
	link = "/zone/" + row["zone_id"]
	return doGenericLinkReplace(txt, cell, link)
}

function doQuestLevel(txt, cell, row) {
	var lvl = txt
	if (lvl == -1) lvl = "Any"
	cell.innerHTML = lvl
	var t = row["get_type"]
	if (t) {
		var span = document.createElement("span")
		span.style.fontSize = "75%"
		span.innerHTML += " (" + t + ")"
		cell.appendChild(span)
	}
	return cell
}

sorttable_template_quest = {
	"column_names": {
		"get_type": "Type",
		"required_level": "Req.",
		"zone_id": "Zone Id"
	},
	
	"column_order": ["name", "level", "required_level", "zone"],
	
	"hooks": {
		"level": doQuestLevel,
		"name": doGenericName,
		"zone": doQuestZone
	}
}
template_item_reward_from = sorttable_template_quest
template_questrewardfaction_quest = sorttable_template_quest
template_quest_zone = sorttable_template_quest
template_required_for_quest = sorttable_template_quest
template_quest_provided_item = sorttable_template_quest
template_quest_spell_trigger = sorttable_template_quest
template_quest_spell_reward = sorttable_template_quest
template_quest_ends_at_npc = sorttable_template_quest
template_creature__starts_quests = sorttable_template_quest
template_quest_skill_reward = sorttable_template_quest


/**
 * Skills
 */

function doSkillCategory(txt, cell, row) {
	link = "/skills/" + txt
	return doGenericLinkReplace(SKILL_CATEGORIES[txt], cell, link)
}

sorttable_template_skill = {
	"column_names": {
		"is_tradeskill": "Tradeskill"
	},
	
	"column_order": ["name", "category", "is_tradeskill"],
	
	"hooks": {
		"name": doGenericNameWithIcon,
		"is_tradeskill": doGenericBoolean,
		"category": doSkillCategory
	}
}

template_skill_spells = sorttable_template_skill


/**
 * Spells
 */

function doSpellDispel(txt, cell, row) {
	link = "/spells/?dispel_type=" + txt
	return doGenericLinkReplace(DISPEL_TYPES[txt], cell, link)
}

function doSpellPrimarySkill(txt, cell, row) {
	link = "/skill/" + row["primary_skill_id"]
	return doGenericLinkReplace(txt, cell, link)
}

function doSpellName(txt, cell, row) {
	cell = doGenericNameWithIcon(txt, cell, row)
	if (row["rank"]) {
		var rank = document.createTextNode(" (" + row["rank"] + ")")
		var span = document.createElement("span")
		span.appendChild(rank)
		span.style.fontSize = "80%"
		cell.appendChild(span)
	}
	return cell
}

sorttable_template_spell = {
	"column_names": {
		"dispel_type": "Dispel Type",
		"get_mechanic_display": "Mechanic",
		"primary_skill": "Skill",
		"required_level": "Lvl",
		"skill_levels": "Skill levels",
		"created_item": "Creates",
		"required_skill": "Req. Skill"
	},
	
	"column_order": ["name", "created_item", "reagents", "skill_levels", "primary_skill", "get_mechanic_display"],
	
	"hooks": {
		"name": doSpellName,
		"dispel_type": doSpellDispel,
		"primary_skill": doSpellPrimarySkill,
		"required_skill": doSkillWithLevel
	}
}

template_trainedspell_trainer = {
	"extends": sorttable_template_spell,
	"column_order": ["name", "required_level", "required_skill", "price"]
}

template_skillspell_skill = sorttable_template_spell
template_spell_reagents = sorttable_template_spell
template_spell_createditem = sorttable_template_spell
template_item_tool_for_spell = sorttable_template_spell
template_spelleffectproperty_trigger_spell = sorttable_template_spell
template_creaturespell_creature = sorttable_template_spell


/**
 * Talents
 */

function doTalentTab(txt, cell, row) {
	link = "/talents/?tab=" + row["tab_id"]
	return doGenericLinkReplace(txt, cell, link)
}

sorttable_template_talent = {
	"column_names": {
		"max_ranks": "Ranks"
	},
	
	"column_order": ["name", "tab", "max_ranks"],
	
	"hooks": {
		"name": doGenericName,
		"tab": doTalentTab
	}
}
template_talentrank_spell = sorttable_template_talent


/**
 * Zones
 */

function doZoneParentArea(txt, cell, row) {
	link = "/z/" + row["parent_area_id"]
	return doGenericLinkReplace(txt, cell, link)
}

function doZoneTerritory(txt, cell, row) {
	link = "/zones/?territory=" + txt
	return doGenericLinkReplace(ZONE_PVP_TYPES[txt], cell, link)
}

sorttable_template_zone = {
	"column_names": {
		"parent_area": "Parent area"
	},
	
	"column_order": ["name", "level", "territory", "parent_area"],
	
	"hooks": {
		"name": doGenericName,
		"parent_area": doZoneParentArea,
		"territory": doZoneTerritory
	}
}
template_zone_parent_area = sorttable_template_zone


function doCreatureLevelDataHealth(txt, cell, row) {
	var hp = txt
	var power = row["power"]
	var power_type = row["power_type"]
	
	cell.innerHTML = txt + " HP"
	
	if (power == 0 && power_type == 1) return cell;
	
	cell.innerHTML += " / " + power + " " + POWER_TYPES[power_type]
	
	return cell
}

function doCreatureLevelDataLevel(txt, cell, row) {
	var heroic_level = row["heroic_level"]
	var group_size = row["group_size"]
	
	cell.innerHTML = txt
	if (heroic_level) {
		cell.innerHTML += " (Heroic " + (group_size || 5) + "-man)"
	} else if (group_size) {
		cell.innerHTML += " (" + group_size + "-man)"
	}
	
	return cell
}

template_creatureleveldata_creature = {
	"column_names": {
		"heroic_level": "Heroic level",
		"group_size": "Group size",
		"health": "Health / Power"
	},
	
	"column_order": ["level", "health"],
// 	"columns_shown": {"power": true},
	"hooks": {
		"level": doCreatureLevelDataLevel,
		"health": doCreatureLevelDataHealth
	}
}
