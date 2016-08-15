// See ./manifest for non-minified files
var onloads=[]
var tabQueue=[]
function toggle(a,b){if(a)document.getElementById(a).style.display=document.getElementById(a).style.display=="none"?"block":"none"
if(b)document.getElementById(b).style.display=document.getElementById(b).style.display=="none"?"block":"none"}
function trim(str){var str=str.replace(/^\s\s*/,'')
var i=str.length
while(/\s/.test(str.charAt(--i)));return str.slice(0,i+1)}
function addLoadEvent(func){onloads.push(func)}
function triggerLoadEvents(){for(var i=0;i<onloads.length;i++){onloads[i]()}
var search=document.getElementById('searchbar')
if((typeof(search)!='undefined')&&(search!=null)){search.onfocus=search.onblur=function(){if(this.value.length==0){addClass(this,'emptytext')}
else{removeClass(this,'emptytext')}}
search.onblur()}}
function hasClass(object,cls){var classes=object.className.split(" ")
for(var i=0;i<classes.length;i++){if(cls==classes[i])return true;}
return false}
function addClass(object,cls){var classes=object.className.split(" ")
for(var i=0;i<classes.length;i++){if(cls==classes[i])return;}
classes.push(cls)
var className=""
for(i=0;i<classes.length;i++){className=className+" "+classes[i]}
object.className=className.replace(/^\s\s*/,'').replace(/\s\s*$/,'')}
function removeClass(object,cls){var classes=object.className.split(" ")
var className=""
for(i=0;i<classes.length;i++){if(cls==classes[i])continue;className=className+" "+classes[i]}
object.className=className.replace(/^\s\s*/,'').replace(/\s\s*$/,'')}
function addTab(id,name){tabQueue.push({'id':id,'name':name})}
function initTabs(){var tabTarget=document.getElementById("dview-content")
var tabBar=document.createElement("div")
var tabView=document.createElement("div")
tabView.appendChild(tabBar)
tabTarget.appendChild(tabView)
addClass(tabView,"tabview")
tabView.style.clear="right"
while(tabQueue.length>0){var cur=tabQueue.pop()
var tab=document.createElement("div")
var content=document.createElement("div")
var table=document.createElement("table")
var pageTop=document.createElement("div")
var pageBottom=document.createElement("div")
addClass(tab,"tabbutton")
tab.id="tab_"+cur.id
tab.textContent=tab.innerText=cur.name
addClass(content,"tabcontent")
addClass(content,"tableview-container")
content.id="tab_"+cur.id+"_content"
content.style.display="none"
addClass(table,"sorttable")
table.setAttribute("name",cur.id)
table.setAttribute("template","template_"+cur.id)
addClass(pageTop,"tableview-pagewidget")
addClass(pageBottom,"tableview-pagewidget")
if(tabBar.childNodes.length>0){tabBar.insertBefore(tab,tabBar.firstChild)}
else{tabBar.appendChild(tab)}
tabView.appendChild(content)
content.appendChild(table)}}
function showLinkString(color,linkString,content){var s="/script print('Shift click to link:', '\\124c"+color+"\\124H"+linkString+"\\124h["+content+"]\\124h\\124r')"
prompt("Copy the following in game.",s)}
function showLinkRaw(text){var s="/script _="+text+";print('Shift click to link:', _)"
prompt("Copy the following in game.",s)}
function getOffsetTop(element,stopElement){var top=element.offsetTop
while((typeof(element.offsetParent)=="object")&&(element.offsetParent!=null)&&(element.offsetParent!=stopElement)){element=element.offsetParent
if(typeof(element.offsetTop)=="number")top+=element.offsetTop}
return top}
function getOffsetLeft(element,stopElement){var left=element.offsetLeft
while((typeof(element.offsetParent)=="object")&&(element.offsetParent!=null)&&(element.offsetParent!=stopElement)){element=element.offsetParent
if(typeof(element.offsetTop)=="number")left+=element.offsetLeft}
return left}
function setImageSrc(img,url){if(img.src==url)return false;img.src=url}
function URL(inputURL){var DEFAULT_HTTP_PORT=80
this.query={}
this.hash={}
this.url={}
this.validateType=function(type,name){if((type!="query")&&(type!="hash")&&(type!="url"))throw new Error("Unknown type '"+type+"' in call to URL."+name+"()");}
this.setKey=function(type,key,value){this.validateType(type,"setKey")
this[type][key]=value}
this.getKey=function(type,key,def){this.validateType(type,"getKey")
if(typeof(this[type][key])!="undefined")return this[type][key];if(typeof(def)!="undefined")return def;return false}
this.merge=function(type,values){this.validateType(type,"merge")
for(var key in values){this.setKey(type,key,values[key])}}
this.remove=function(type,key){this.validateType(type,"remove")
delete this[type][key]}
this.clear=function(type){this.validateType(type,"clear")
this[type]={}}
this.set=function(type,values){this.validateType(type,"set")
this.clear(type)
this.merge(type,values)}
this.serialize=function(query){var result=""
for(var key in query){if(result.length>0)result+="&";result+=encodeURIComponent(key)
var value=encodeURIComponent(query[key])
if(value.length>0)result+="="+value;}
return result}
this.unserialize=function(input){var result={}
var match
while(match=input.match(/(?:^|&|;)([^&=;]+)(?:=([^&=;]*))?/)){input=input.substr(match[0].length)
var value=match[2]
if(typeof(value)=="undefined")value="";result[decodeURIComponent(match[1])]=decodeURIComponent(value).replace(/\+/g,' ')}
return result}
this.parseURL=function(url){var match=url.match(/^(?:(\w+):\/*([\w\.\-\d]+)(?::(\d+)|)(?=(?:\/|$))|)(?:$|\/?(.*?)(?:\?(.*?)?|)(?:#(.*)|)$)/)
if(!match)return;if((typeof(match[1])=="string")&&(match[1].length>0)){this.setKey("url","scheme",match[1])
this.setKey("url","host",match[2])
if(isNaN(parseInt(match[3]))){this.setKey("url","port",DEFAULT_HTTP_PORT)}
else{this.setKey("url","port",parseInt(match[3]))}}
else{this.setKey("url","scheme",currentURL.url.scheme)
this.setKey("url","host",currentURL.url.host)
this.setKey("url","port",currentURL.url.port)}
this.setKey("url","path",match[4])
if(typeof(match[5])=="string")this.set("query",this.unserialize(match[5]));if(typeof(match[6])=="string")this.set("hash",this.unserialize(match[6]));}
this.toString=function(){if((typeof(this.url.scheme)!="string")||(this.url.scheme.length<1))this.url.scheme="http";if((typeof(this.url.host)!="string")||(this.url.host.length<1))return"";if(typeof(this.url.path)!="string")this.url.path="";var port=(this.url.port==DEFAULT_HTTP_PORT)?(""):(":"+this.url.port)
var query=this.serialize(this.query)
var hash=this.serialize(this.hash)
var result=this.url.scheme+"://"+this.url.host+port+"/"+this.url.path
if(query.length>0)result+="?"+query;if(hash.length>0)result+="#"+hash;return result;}
if(inputURL.length>0)this.parseURL(inputURL);}
currentURL=new URL(document.location.href)
if(typeof(JSON)=="undefined"){JSON={parse:function(text){var ret=!(/[^,:{}\[\]0-9.\-+Eaeflnr-u \n\r\t]/.test(text.replace(/"(\\.|[^"\\])*"/g,'')))&&eval('('+text+')')
if(!ret)throw new Error("Invalid JSON");return ret}}}
httplib={request:function(url,options){if(typeof(url)=="string")url=new URL(url);var defaults={"method":"get","query":{},"success":function(){},"failure":function(){},"content":"auto"}
for(var key in defaults){if(typeof(options[key])=="undefined")options[key]=defaults[key];}
if((options.method=="get")||(options.method=="script"))url.merge("query",options.query);options["url"]=url
if((options.method=="get")&&(options.content=="js")&&(url.url.host!=currentURL.url.host))options.method="script";if(options.method=="script"){var script=document.createElement("script")
script.onload=function(event){if(typeof(event)!="object")event=window.event;httplib.scriptLoaded(event,options)}
script.onreadystatechange=function(event){if(typeof(event)!="object")event=window.event;if((script.readyState=="loaded")||(script.readyState=="complete"))httplib.scriptLoaded(event,options);}
script.src=options.url.toString()
document.documentElement.appendChild(script)}
else{var xhr=httplib.XMLHttpRequest()
xhr.options=options
xhr.onreadystatechange=httplib.readyStateChange
if((options.content=="xml")&&(typeof(xhr.overrideMimeType)=="function"))xhr.overrideMimeType("text/xml");xhr.open(options.method.toUpperCase(),url.toString(),true)
if(options.method=="post"){xhr.send(url.serialize(url.query))}
else{xhr.send("")}}},scriptLoaded:function(event,options){var result={}
result.status=200
result.statusText="LOADED"
result.responseText=true
result.response=true
result.xhr=false
result.url=options.url
if(typeof(options.success)=="function")options.success(result);httplib.log("Successful request to "+options.url+" via <script> tag")},readyStateChange:function(){if(this.readyState==4){var result={}
result.status=this.status
result.statusText=this.statusText
result.responseText=this.responseText
result.xhr=this
result.url=this.options.url
result.headers=httplib.parseHeaders(this.getAllResponseHeaders())
if(this.status==200){if((typeof(this.options.content)!="string")||(this.options.content=="auto")){if(typeof(result.headers["Content-Type"])!="string")result.headers["Content-Type"]="text/plain";switch(result.headers["Content-Type"]){case"application/json":this.options.content="json"
break
case"application/xml":case"text/xml":this.options.content="xml"
break
default:this.options.content="text"}}
if(this.options.content=="json"){var json=httplib.stripJSONP(this.responseText)
try{result.response=JSON.parse(json)}
catch(ex){try{result.response=eval("("+json+")")}
catch(evalex){if(typeof(this.options.failure)=="function")this.options.failure(result);httplib.log("Invalid JSON returned in request from "+this.options["url"]+" (Exceptions are '"+ex+"' and '"+evalex+"'):\n"+json)
return}}}
else if(this.options.content=="js"){try{result.response=eval(this.responseText)}
catch(ex){if(typeof(this.options.failure)=="function")this.options.failure(result);httplib.log("Invalid javascript returned in request from "+this.options["url"]+" ("+ex+")\n"+this.responseText)}}
else if(this.options.content=="xml"){result.response=this.responseXml}
else{result.response=this.responseText}
if(typeof(this.options.success)=="function")this.options.success(result);httplib.log("Successful request to "+this.options["url"])}
else{if(typeof(this.options.failure)=="function")this.options.failure(result);httplib.log("Failed request to "+this.options["url"])}}},stripJSONP:function(json){var match
if(match=json.match(/^\s*([\w\d_\$]+)\(({[\s\S]*})\)[;\s]*$/i)){json=match[2]}
return json},parseHeaders:function(input){var result={}
var match
while(match=input.match(/^([\w\d\-\_]+): (.+)$/m)){input=input.substr(match[0].length)
result[match[1]]=match[2]}
return result},XMLHttpRequest:function(){if(typeof(XMLHttpRequest)!="undefined")return new XMLHttpRequest();try{return new ActiveXObject("Msxml2.XMLHTTP.6.0")}
catch(e){}
try{return new ActiveXObject("Msxml2.XMLHTTP.3.0")}
catch(e){}
try{return new ActiveXObject("Msxml2.XMLHTTP")}
catch(e){}
throw new Error("Unsupported browser, XmlHttpRequest cannot be created")},log:function(text){if((typeof(console)!="undefined")&&(typeof(console.log)=="function"))console.log(text);}}
var URL_BASE="(^|http://db\.mmo-champion\.com|http://.*\.sigrie\.com/|http://sigrie\.dinnerbone\.com)/"
var URL_REGEX=URL_BASE+"(a|c|e|g|i|o|q|s|t|z|is|ach|npc|achievement|creature|enchant|glyph|itemset|item|object|skill|spell|talent|zone)/([^#]+?)(?:\\/\\?([^#]+)|$|#.*$)"
var TOOLTIP_RETRIEVING_HTML='<span class="sigrie-tooltip tt-retrieving">Retrieving tooltip...</span>'
var TOOLTIP_ERROR_HTML='<span class="sigrie-tooltip tt-error">Error retrieving tooltip</span>'
var TOOLTIP_MAX_WIDTH=310
TOOLTIP_CLASS_BLACKLIST="tt-name"
var ttlib={init:function(){var jstooltip=document.createElement("div")
var pagetooltip=document.getElementById('dview-tooltip')
jstooltip.id="sigrie-tooltip"
jstooltip.className="tt-hover"
document.getElementsByTagName("body")[0].appendChild(jstooltip)
ttlib.jstooltip=jstooltip
ttlib.hide()
ttlib.parseDocument()
ttlib.requestcount=0
ttlib.requests=new Array()
ttlib.queue=new Array()
ttlib.currentRequest=null
ttlib.cursorX=0
ttlib.cursorY=0
ttlib.cursorAdjustedX=0
ttlib.cursorAdjustedY=0
ttlib.currentMouseover=""
ttlib.cache=new Object()
document.onmousemove=ttlib.mouseMove
if((typeof(pagetooltip)!="undefined")&&(pagetooltip!=null))ttlib.hookHeirloomLevel(pagetooltip);if(typeof(document.addEventListener)=="function")document.addEventListener('DOMNodeInserted',ttlib.DOMNodeInserted,true);},mouseMove:function(e){var cursor=ttlib.cursorPosition(e)
ttlib.cursorY=cursor.y
ttlib.cursorX=cursor.x
ttlib.cursorAdjustedX=cursor.x+15
ttlib.cursorAdjustedY=cursor.y-20
if(ttlib.jstooltip.style.visibility!="hidden")ttlib.clampTooltip();},clampTooltip:function(){var x=ttlib.cursorX
var y=ttlib.cursorY
var ax=ttlib.cursorAdjustedX
var ay=ttlib.cursorAdjustedY
var de=document.documentElement
var body=document.body
if(y+ttlib.jstooltip.offsetHeight>de.clientHeight+body.scrollTop+de.scrollTop){var ydiff=(de.clientHeight+body.scrollTop+de.scrollTop)-(y+ttlib.jstooltip.offsetHeight)
ay+=ydiff}
if(x+ttlib.jstooltip.offsetWidth+20>de.clientWidth+body.scrollLeft+de.scrollLeft){ax-=ttlib.jstooltip.offsetWidth+20}
ttlib.jstooltip.style.left=""+(ax)+"px"
ttlib.jstooltip.style.top=""+(ay)+"px"},requestSuccess:function(result){var tooltip=ttlib.currentRequest["tooltip"]
ttlib.cache[ttlib.currentRequest["cache"]]=result.responseText
if((tooltip!=ttlib.jstooltip)||(ttlib.currentRequest["cache"]==ttlib.currentMouseover))
{tooltip.style.left="0px"
tooltip.style.top="0px"
tooltip.innerHTML=result.responseText
ttlib.hookHeirloomLevel(tooltip)
if(tooltip==ttlib.jstooltip){ttlib.show()
ttlib.clampTooltip()}}
ttlib.currentRequest=null
ttlib.processQueue()},requestFailure:function(result){tooltip.innerHTML=TOOLTIP_ERROR_HTML
ttlib.currentRequest=null
ttlib.processQueue()},queueRequest:function(url,tooltip){var req=new Object()
var requrl=url
if(typeof(tooltip)=="undefined")tooltip=ttlib.jstooltip;if(typeof(requrl)=="object"){requrl=requrl.href
if(requrl.indexOf("?")!=-1)requrl=requrl.replace('?',"/tooltip?")
else if(requrl.indexOf('#')!=-1)requrl=requrl.replace('#',"/tooltip#")
else requrl=url.href+"/tooltip"}
req["url"]=requrl
req["cache"]=url
req["tooltip"]=tooltip
ttlib.queue.push(req)
ttlib.processQueue()},processQueue:function(){if(ttlib.queue.length>0&&ttlib.currentRequest==null){ttlib.currentRequest=ttlib.queue.pop()
ttlib.requestcount++
httplib.request(ttlib.currentRequest["url"],{'success':ttlib.requestSuccess,'failure':ttlib.requestFailure})}},isValid:function(url){if(url.parentNode.className.match(TOOLTIP_CLASS_BLACKLIST))return false;url=url.getAttribute("href")||"#"
return url.match(URL_REGEX)},startTooltip:function(atag){ttlib.currentMouseover=atag
if(ttlib.cache[atag]){ttlib.jstooltip.style.left="0px"
ttlib.jstooltip.style.top="0px"
ttlib.jstooltip.innerHTML=ttlib.cache[atag]
ttlib.show()
ttlib.clampTooltip()}else{ttlib.jstooltip.innerHTML=TOOLTIP_RETRIEVING_HTML
ttlib.show()
ttlib.queueRequest(atag)}},parseDocument:function(){ttlib.parseElement(document)},parseElement:function(element){if(typeof(element.getElementsByTagName)=="undefined")return false;var links=element.getElementsByTagName("a")
for(var i=0;i<links.length;i++){if(ttlib.isValid(links[i])){links[i].onmouseover=function(evt){ttlib.startTooltip(this)}
links[i].onmouseout=function(evt){ttlib.hide()}}}},cursorPosition:function(e){e=e||window.event
var cursor={x:0,y:0}
if(e.pageX||e.pageY){cursor.x=e.pageX
cursor.y=e.pageY}else{var de=document.documentElement
var b=document.body
cursor.x=e.clientX+(de.scrollLeft||b.scrollLeft)-(de.clientLeft||0)
cursor.y=e.clientY+(de.scrollTop||b.scrollTop)-(de.clientTop||0)}
return cursor},show:function(){if(ttlib.jstooltip.style.width>TOOLTIP_MAX_WIDTH||ttlib.jstooltip.style.width>TOOLTIP_MAX_WIDTH||ttlib.jstooltip.offsetWidth>TOOLTIP_MAX_WIDTH||ttlib.jstooltip.offsetWidth>TOOLTIP_MAX_WIDTH){ttlib.jstooltip.style.width=TOOLTIP_MAX_WIDTH;}else{ttlib["jstooltip"]["style"]["width"]=ttlib["jstooltip"]["style"]["width"]}
ttlib.jstooltip.style.visibility="visible"},hide:function(){ttlib.jstooltip.style.visibility="hidden"
ttlib.currentMouseover=null},hookHeirloomLevel:function(tooltip){var reqel=null
var elements=tooltip.getElementsByTagName("SPAN")
for(var i=0;i<elements.length;i++){var element=elements[i]
if(hasClass(element,"tti-current_level")){reqel=element
break}}
if((reqel==null)||(typeof(reqel.onclick)=="function"))return;reqel.onmouseover=function(){this.style.cursor="pointer"}
reqel.onmouseout=function(){this.style.cursor="default"}
reqel.onmouseup=function(){var input=document.createElement("input")
var cached=true
input.value=reqel.innerText||reqel.textContent
reqel.parentNode.replaceChild(input,reqel)
input.focus()
input.select()
input.onblur=function(){var level=parseInt(input.value)
var old=parseInt(reqel.innerText||reqel.textContent)
if((level<=0)||(isNaN(level)))level=old;if(level==old){reqel.innerText=reqel.textContent=level}
else if(ttlib.scaleHeirloom(level,tooltip)){reqel.innerText=reqel.textContent=level+"..."
reqel.onmouseup=function(){}}
input.onblur=function(){}
if(input.parentNode!=null)input.parentNode.replaceChild(reqel,input);}
input.onkeydown=function(e){if(typeof(e)=="undefined")e=window.event;var key=0
var value=parseInt(input.value)
if(typeof(e.key)!="undefined")key=e.which;if(typeof(e.keyCode)!="undefined")key=e.keyCode;if((isNaN(value))&&(input.value.length>0))value=input.value=0;if(key==13){input.onblur()}
else if(key==27){input.onblur=function(){}
if(input.parentNode!=null)input.parentNode.replaceChild(reqel,input);}
else if(key==38){input.value=parseInt(input.value)+1}
else if(key==40){input.value=parseInt(input.value)-1}}}},scaleHeirloom:function(level,tooltip){if(typeof(tooltip)=="undefined")tooltip=ttlib.jstooltip;var url=document.location.href
var match=url.match(URL_REGEX)
if(!match)return false;url=match[1]+"/"+match[2]+"/"+match[3]+"/tooltip/?level="+encodeURIComponent(level)
if((typeof(match[4])=="string")&&(match[4].length>0))url+="&"+match[4];if(typeof(ttlib.cache[url])=="string"){tooltip.innerHTML=ttlib.cache[url]
ttlib.hookHeirloomLevel(tooltip)
return false}
else{ttlib.queueRequest(url,tooltip)
return true}},DOMNodeInserted:function(event){if(typeof(event.target)=="object")ttlib.parseElement(event.target);},predefineTooltip:function(url,tooltip){ttlib.cache[url]=tooltip}}
addLoadEvent(ttlib.init)
function SigrieTooltip(initargs){}
CREATURE_TYPES={0:"",1:"Elite",2:"Rare-Elite",3:"Boss",4:"Rare",5:""}
CREATURE_CATEGORIES={0:"Not Specified",1:"Beast",2:"Dragonkin",3:"Demon",4:"Elemental",5:"Giant",6:"Undead",7:"Humanoid",8:"Critter",9:"Mechanical",10:"",11:"Totem",12:"Non-combat Pet",13:"Gas Cloud"}
CREATURE_FAMILIES={0:"",1:"Wolf",2:"Cat",3:"Spider",4:"Bear",5:"Boar",6:"Crocolisk",7:"Carrion Bird",8:"Crab",9:"Gorilla",10:"Stag",11:"Raptor",12:"Tallstrider",20:"Scorpid",21:"Turtle",24:"Bat",25:"Hyena",26:"Bird of Prey",27:"Wind Serpent",30:"Dragonhawk",31:"Ravager",32:"Warp Stalker",33:"Sporebat",34:"Nether Ray",35:"Serpent",37:"Moth",38:"Chimaera",39:"Devilsaur",41:"Silithid",42:"Worm",43:"Rhino",44:"Wasp",45:"Core Hound",46:"Spirit Beast"}
DISPEL_TYPES={0:"",1:"Magic",2:"Curse",3:"Disease",4:"Poison",5:"Stealth",6:"Invisibility",9:"Enrage"}
FACTIONS={0:"Both",1:"Horde",2:"Alliance"}
POWER_TYPES={0:"Mana",1:"Rage",2:"Focus",3:"Energy",4:"Consumable",5:"Runes",6:"Runic Power"}
ZONE_PVP_TYPES={0:"Contested",2:"Alliance",4:"Horde",6:"Sanctuary"}
SLOTS={0:"",1:"Head",2:"Neck",3:"Shoulder",4:"Shirt",5:"Chest",6:"Waist",7:"Legs",8:"Feet",9:"Wrist",10:"Hands",11:"Finger",12:"Trinket",13:"One-Hand",14:"Shield",15:"Ranged",16:"Back",17:"Two-Hand",18:"Bag",19:"Tabard",20:"Chest",21:"Main Hand",22:"Off-Hand",23:"Held In Off-hand",24:"Projectile",25:"Thrown",26:"Ranged",28:"Relic"}
SKILL_CATEGORIES={0:"",5:"Attributes",6:"Weapon Skills",7:"Class Skills",8:"Armor Proficiencies",9:"Secondary Skills",10:"Languages",11:"Professions",12:"Not Displayed"}
ITEM_SUBCLASSES={0:{0:'Consumable',1:'Potion',2:'Elixir',3:'Flask',4:'Scroll',5:'Food & Drink',6:'Item Enhancement',7:'Bandage',8:'Other'},1:{0:'Bag',1:'Soul Bag',2:'Herb Bag',3:'Enchanting Bag',4:'Engineering Bag',5:'Gem Bag',6:'Mining Bag',7:'Leatherworking Bag',8:'Inscription Bag'},2:{0:'Axe',1:'Axe',2:'Bow',3:'Gun',4:'Mace',5:'Mace',6:'Polearm',7:'Sword',8:'Sword',9:'Obsolete',10:'Staff',11:'Exotic',12:'Exotic',13:'Fist Weapon',14:'Miscellaneous',15:'Dagger',16:'Thrown',17:'Spear',18:'Crossbow',19:'Wand',20:'Fishing Pole'},3:{0:'Red',1:'Blue',2:'Yellow',3:'Purple',4:'Green',5:'Orange',6:'Meta',7:'Simple',8:'Prismatic'},4:{0:'Miscellaneous',1:'Cloth',2:'Leather',3:'Mail',4:'Plate',5:'Buckler(OBSOLETE)',6:'Shield',7:'Libram',8:'Idol',9:'Totem',10:'Sigil'},5:{0:'Reagent'},6:{0:'Wand(OBSOLETE)',1:'Bolt(OBSOLETE)',2:'Arrow',3:'Bullet',4:'Thrown(OBSOLETE)'},7:{0:'Trade Goods',1:'Parts',2:'Explosives',3:'Devices',4:'Jewelcrafting',5:'Cloth',6:'Leather',7:'Metal & Stone',8:'Meat',9:'Herb',10:'Elemental',11:'Other',12:'Enchanting',13:'Materials',14:'Armor Enchantment',15:'Weapon Enchantment'},8:{0:'Generic(OBSOLETE)'},9:{0:'Book',1:'Leatherworking',2:'Tailoring',3:'Engineering',4:'Blacksmithing',5:'Cooking',6:'Alchemy',7:'First Aid',8:'Enchanting',9:'Fishing',10:'Jewelcrafting',11:'Inscription'},10:{0:'Currency',7:'Unknown'},11:{0:'Quiver(OBSOLETE)',1:'Quiver(OBSOLETE)',2:'Quiver',3:'Ammo Pouch'},12:{0:'Quest',8:'Unknown',3:'Unknown'},13:{0:'Key',1:'Lockpick'},14:{0:'Permanent'},15:{0:'Junk',1:'Reagent',2:'Pet',3:'Holiday',4:'Other',5:'Mount',12:'Unknown'},16:{1:'Warrior',2:'Paladin',3:'Hunter',4:'Rogue',5:'Priest',6:'Death Knight',7:'Shaman',8:'Mage',9:'Warlock',11:'Druid'}}
sgMenus={}
sgMenus.achievements_81=[{"name":"Realm First Feats","href":"/achievements/81/?serverfirst=1"}]
sgMenus.achievements_96=[{"name":"Eastern Kingdoms","href":"/achievements/14861"},{"name":"Kalimdor","href":"/achievements/15081"},{"name":"Outland","href":"/achievements/14862"},{"name":"Northrend","href":"/achievements/14863"},{"name":"Cataclysm","href":"/achievements/15070"}]
sgMenus.achievements_97=[{"name":"Eastern Kingdoms","href":"/achievements/14777"},{"name":"Kalimdor","href":"/achievements/14778"},{"name":"Outland","href":"/achievements/14779"},{"name":"Northrend","href":"/achievements/14780"},{"name":"Cataclysm","href":"/achievements/15069"}]
sgMenus.achievements_95=[{"name":"Arena","href":"/achievements/165"},{"name":"Alterac Valley","href":"/achievements/14801"},{"name":"Arathi Basin","href":"/achievements/14802"},{"name":"Eye of the Storm","href":"/achievements/14803"},{"name":"Warsong Gulch","href":"/achievements/14804"},{"name":"Strand of the Ancients","href":"/achievements/14881"},{"name":"Wintergrasp","href":"/achievements/14901"},{"name":"Isle of Conquest","href":"/achievements/15003"},{"name":"Battle for Gilneas","href":"/achievements/15073"},{"name":"Twin Peaks","href":"/achievements/15074"},{"name":"Tol Barad","href":"/achievements/15075"},{"name":"Rated Battleground","href":"/achievements/15092"}]
sgMenus.achievements_168=[{"name":"Classic","href":"/achievements/14808"},{"name":"The Burning Crusade","href":"/achievements/14805"},{"name":"Lich King Dungeon","href":"/achievements/14806"},{"name":"Lich King Raid","href":"/achievements/14922"},{"name":"Cataclysm Dungeon","href":"/achievements/15067"},{"name":"Cataclysm Raid","href":"/achievements/15068"}]
sgMenus.achievements_169=[{"name":"Cooking","href":"/achievements/170"},{"name":"Fishing","href":"/achievements/171"},{"name":"First Aid","href":"/achievements/172"},{"name":"Archaeology","href":"/achievements/15071"}]
sgMenus.achievements_201=[{"name":"Classic","href":"/achievements/14864"},{"name":"The Burning Crusade","href":"/achievements/14865"},{"name":"Wrath of the Lich King","href":"/achievements/14866"},{"name":"Cataclysm","href":"/achievements/15072"}]
sgMenus.achievements_155=[{"name":"Lunar Festival","href":"/achievements/160"},{"name":"Love is in the Air","href":"/achievements/187"},{"name":"Children's Week","href":"/achievements/163"},{"name":"Noblegarden","href":"/achievements/159"},{"name":"Midsummer","href":"/achievements/161"},{"name":"Brewfest","href":"/achievements/162"},{"name":"Hallow's End","href":"/achievements/158"},{"name":"Pilgrim's Bounty","href":"/achievements/14981"},{"name":"Winter Veil","href":"/achievements/156"},{"name":"Darkmoon Faire","href":"/achievements/157"},{"name":"Argent Tournament","href":"/achievements/14941"}]
sgMenus.achievements_15088=[{"name":"General","href":"/achievements/15088"},{"name":"Quests","href":"/achievements/15077"},{"name":"Player vs. Player","href":"/achievements/15078"},{"name":"Dungeons & Raids","href":"/achievements/15079"},{"name":"Professions","href":"/achievements/15080"},{"name":"Reputation","href":"/achievements/15089"}]
sgMenus.achievements=[{"name":"General","href":"/achievements/92"},{"name":"Quests","href":"/achievements/96","submenu":"achievements_96"},{"name":"Exploration","href":"/achievements/97","submenu":"achievements_97"},{"name":"Player vs. Player","href":"/achievements/95","submenu":"achievements_95"},{"name":"Dungeons & Raids","href":"/achievements/168","submenu":"achievements_168"},{"name":"Professions","href":"/achievements/169","submenu":"achievements_169"},{"name":"Reputation","href":"/achievements/201","submenu":"achievements_201"},{"name":"World Events","href":"/achievements/155","submenu":"achievements_155"},{"name":"Feats of Strength","href":"/achievements/81","submenu":"achievements_81"},{"name":"","header":true},{"name":"Guild","href":"/achievements/15088","submenu":"achievements_15088"},{"name":"Statistics","href":"/achievements/?statistic=1"}]
sgMenus.creatures_1_cunning=[{"name":"Bats","href":"/creatures/1/24"},{"name":"Birds of Prey","href":"/creatures/1/26"},{"name":"Chimaeras","href":"/creatures/1/38"},{"name":"Dragonhawks","href":"/creatures/1/30"},{"name":"Nether Rays","href":"/creatures/1/34"},{"name":"Ravagers","href":"/creatures/1/31"},{"name":"Serpents","href":"/creatures/1/35"},{"name":"Silithids","href":"/creatures/1/41"},{"name":"Spiders","href":"/creatures/1/3"},{"name":"Sporebats","href":"/creatures/1/33"},{"name":"Wind Serpents","href":"/creatures/1/27"}]
sgMenus.creatures_1_ferocity=[{"name":"Carrion Birds","href":"/creatures/1/7"},{"name":"Cats","href":"/creatures/1/2"},{"name":"Core Hounds","href":"/creatures/1/45"},{"name":"Devilsaurs","href":"/creatures/1/39"},{"name":"Hyenas","href":"/creatures/1/25"},{"name":"Raptors","href":"/creatures/1/11"},{"name":"Moths","href":"/creatures/1/37"},{"name":"Spirit Beasts","href":"/creatures/1/46"},{"name":"Tallstriders","href":"/creatures/1/12"},{"name":"Wasps","href":"/creatures/1/44"},{"name":"Wolves","href":"/creatures/1/1"}]
sgMenus.creatures_1_tenacity=[{"name":"Bears","href":"/creatures/1/4"},{"name":"Boars","href":"/creatures/1/5"},{"name":"Crabs","href":"/creatures/1/8"},{"name":"Crocolisks","href":"/creatures/1/6"},{"name":"Gorillas","href":"/creatures/1/9"},{"name":"Rhinos","href":"/creatures/1/43"},{"name":"Scorpids","href":"/creatures/1/20"},{"name":"Turtles","href":"/creatures/1/21"},{"name":"Warp Stalkers","href":"/creatures/1/32"},{"name":"Worms","href":"/creatures/1/42"}]
sgMenus.creatures_1=[{"name":"Cunning","href":"javascript:;","submenu":"creatures_1_cunning"},{"name":"Ferocity","href":"javascript:;","submenu":"creatures_1_ferocity"},{"name":"Tenacity","href":"javascript:;","submenu":"creatures_1_tenacity"},{"name":"","header":true},{"name":"No Family","href":"/creatures/1/0"},]
sgMenus.creatures=[{"name":"Beasts","href":"/creatures/1","submenu":"creatures_1"},{"name":"Companions","href":"/creatures/12"},{"name":"Critters","href":"/creatures/8"},{"name":"Dragonkins","href":"/creatures/2"},{"name":"Demons","href":"/creatures/3"},{"name":"Elementals","href":"/creatures/4"},{"name":"Gas Clouds","href":"/creatures/13"},{"name":"Giants","href":"/creatures/5"},{"name":"Humanoids","href":"/creatures/7"},{"name":"Mechanicals","href":"/creatures/9"},{"name":"Totems","href":"/creatures/11"},{"name":"Undead","href":"/creatures/6"},{"name":"Uncategorized","href":"/creatures/10"},{"name":"Hunter pets","header":true},{"name":"Cunning","href":"javascript:;","submenu":"creatures_1_cunning"},{"name":"Ferocity","href":"javascript:;","submenu":"creatures_1_ferocity"},{"name":"Tenacity","href":"javascript:;","submenu":"creatures_1_tenacity"},{"name":"Quick filters","header":true},{"name":"By type","href":"javascript:;","submenu":"creatures_filter_type"}]
sgMenus.creatures_filter_type=[{"name":"Arena organizers","href":"/creatures/?arena_organizer=1"},{"name":"Auctioneers","href":"/creatures/?auctioneer=1"},{"name":"Bankers","href":"/creatures/?banker=1"},{"name":"Battlemasters","href":"/creatures/?battlemaster=1"},{"name":"Flightmasters","href":"/creatures/?flightmaster=1"},{"name":"Innkeepers","href":"/creatures/?innkeeper=1"},{"name":"Stable Masters","href":"/creatures/?stable_master=1"},{"name":"Trainers","href":"/creatures/?trainer=1"},{"name":"Vendors","href":"/creatures/?vendor=1"}]
sgMenus.items_0=[{"name":"Consumables","href":"/items/0/0","icon":"inv_drink_03"},{"name":"Potions","href":"/items/0/1","icon":"inv_potion_52"},{"name":"Elixirs","href":"/items/0/2","icon":"inv_potion_43"},{"name":"Flasks","href":"/items/0/3","icon":"inv_potion_41"},{"name":"Scrolls","href":"/items/0/4","icon":"inv_scroll_07"},{"name":"Food & Drink","href":"/items/0/5","icon":"inv_misc_food_08"},{"name":"Item Enhancements","href":"/items/0/6"},{"name":"Bandages","href":"/items/0/7","icon":"inv_misc_bandage_05"},{"name":"Other","href":"/items/0/8","icon":"inv_stone_04"}]
sgMenus.items_1=[{"name":"Bags","href":"/items/1/0","icon":"inv_misc_bag_07"},{"name":"Soul Bags","href":"/items/1/1","icon":"inv_misc_bag_soulbag"},{"name":"Herb Bags","href":"/items/1/2","icon":"inv_misc_bag_18"},{"name":"Enchanting Bags","href":"/items/1/3","icon":"inv_misc_bag_enchantedrunecloth"},{"name":"Engineering Bags","href":"/items/1/4","icon":"inv_misc_enggizmos_17"},{"name":"Gem Bags","href":"/items/1/5","icon":"inv_misc_bag_15"},{"name":"Mining Bags","href":"/items/1/6","icon":"inv_misc_bag_10_blue"},{"name":"Leatherworking Bags","href":"/items/1/7","icon":"inv_misc_bag_20"},{"name":"Inscription Bags","href":"/items/1/8","icon":"inv_misc_bag_13"}]
sgMenus.items_2=[{"name":"One-Handed","header":true},{"name":"1H Axes","href":"/items/2/0","icon":"inv_axe_01"},{"name":"1H Maces","href":"/items/2/4","icon":"inv_mace_10"},{"name":"1H Swords","href":"/items/2/7","icon":"inv_sword_04"},{"name":"Daggers","href":"/items/2/15","icon":"inv_weapon_shortblade_05"},{"name":"Fist Weapons","href":"/items/2/13","icon":"inv_weapon_hand_01"},{"name":"Miscellaneous","href":"/items/2/14","icon":"inv_misc_flower_04"},{"name":"Two-Handed","header":true},{"name":"2H Axes","href":"/items/2/1","icon":"inv_axe_09"},{"name":"2H Maces","href":"/items/2/5","icon":"inv_hammer_10"},{"name":"2H Swords","href":"/items/2/8","icon":"inv_sword_26"},{"name":"Polearms","href":"/items/2/6","icon":"inv_spear_08"},{"name":"Staves","href":"/items/2/10","icon":"inv_staff_08"},{"name":"Fishing Poles","href":"/items/2/20","icon":"inv_fishingpole_02"},{"name":"Ranged","header":true},{"name":"Bows","href":"/items/2/2","icon":"inv_weapon_bow_07"},{"name":"Crossbows","href":"/items/2/18","icon":"inv_weapon_crossbow_07"},{"name":"Guns","href":"/items/2/3","icon":"inv_weapon_rifle_01"},{"name":"Thrown","href":"/items/2/16","icon":"inv_throwingknife_02"},{"name":"Wands","href":"/items/2/19","icon":"inv_wand_07"}]
sgMenus.items_3=[{"name":"Blue","href":"/items/3/1","icon":"inv_jewelcrafting_empyreansapphire_02"},{"name":"Green","href":"/items/3/4","icon":"inv_jewelcrafting_seasprayemerald_02"},{"name":"Purple","href":"/items/3/3","icon":"inv_jewelcrafting_shadowsongamethyst_02"},{"name":"Orange","href":"/items/3/5","icon":"inv_jewelcrafting_pyrestone_02"},{"name":"Red","href":"/items/3/0","icon":"inv_jewelcrafting_crimsonspinel_02"},{"name":"Yellow","href":"/items/3/2","icon":"inv_jewelcrafting_lionseye_02"},{"name":"","header":true},{"name":"Meta","href":"/items/3/6","icon":"inv_misc_gem_diamond_06"},{"name":"Simple","href":"/items/3/7","icon":"inv_misc_gem_pearl_02"},{"name":"Prismatic","href":"/items/3/8","icon":"inv_enchant_voidsphere"},{"name":"Hydraulic","href":"/items/3/9","icon":"inv_gizmo_gnomishflameturret"},{"name":"Cogwheel","href":"/items/3/10","icon":"inv_misc_enggizmos_30"}]
sgMenus.items_4_slotfilter=[{"name":"Head","href":"$?slot=1"},{"name":"Shoulder","href":"$?slot=3"},{"name":"Chest","href":"$?slot__in=5,20"},{"name":"Waist","href":"$?slot=6"},{"name":"Legs","href":"$?slot=7"},{"name":"Feet","href":"$?slot=8"},{"name":"Wrist","href":"$?slot=9"},{"name":"Hands","href":"$?slot=10"}]
sgMenus.items_4_0=[{"name":"Back","href":"/items/4/?slot=16"},{"name":"Neck","href":"/items/4/0/?slot=2"},{"name":"Finger","href":"/items/4/0/?slot=11"},{"name":"Trinket","href":"/items/4/0/?slot=12"},{"name":"Held In Off-hand","href":"/items/4/0/?slot=23"}]
sgMenus.items_4_relics=[{"name":"Librams","href":"/items/4/7"},{"name":"Idols","href":"/items/4/8"},{"name":"Totems","href":"/items/4/9"},{"name":"Sigils","href":"/items/4/10"}]
sgMenus.items_4=[{"name":"Cloth","href":"/items/4/1","submenu":"items_4_slotfilter","icon":"inv_chest_cloth_21"},{"name":"Leather","href":"/items/4/2","submenu":"items_4_slotfilter","icon":"inv_chest_leather_09"},{"name":"Mail","href":"/items/4/3","submenu":"items_4_slotfilter","icon":"inv_chest_chain_05"},{"name":"Plate","href":"/items/4/4","submenu":"items_4_slotfilter","icon":"inv_chest_plate01"},{"name":"Shields","href":"/items/4/6","icon":"inv_shield_04"},{"name":"","header":true},{"name":"Miscellaneous","href":"/items/4/0","submenu":"items_4_0"},{"name":"Relics","href":"/items/?slot=28","submenu":"items_4_relics"}]
sgMenus.items_5=[{"name":"Reagents","href":"/items/5/0"}]
sgMenus.items_6=[{"name":"Arrows","href":"/items/6/2","icon":"inv_misc_ammo_arrow_01"},{"name":"Bullets","href":"/items/6/3","icon":"inv_misc_ammo_bullet_06"}]
sgMenus.items_7=[{"name":"Trade Goods","href":"/items/7/0"},{"name":"Parts","href":"/items/7/1","icon":"inv_gizmo_pipe_01"},{"name":"Explosives","href":"/items/7/2","icon":"inv_misc_bomb_05"},{"name":"Devices","href":"/items/7/3","icon":"inv_misc_spyglass_02"},{"name":"Jewelcrafting","href":"/items/7/4","icon":"inv_misc_gem_crystalcut_01"},{"name":"Cloth","href":"/items/7/5","icon":"inv_fabric_linen_01"},{"name":"Leather","href":"/items/7/6","icon":"inv_misc_leatherscrap_03"},{"name":"Metal & Stone","href":"/items/7/7","icon":"inv_ingot_02"},{"name":"Meat","href":"/items/7/8","icon":"inv_misc_food_14"},{"name":"Herb","href":"/items/7/9","icon":"inv_misc_flower_02"},{"name":"Elemental","href":"/items/7/10","icon":"spell_nature_tranquility"},{"name":"Other","href":"/items/7/11","icon":"inv_misc_ticket_tarot_furies"},{"name":"Enchanting","href":"/items/7/12","icon":"trade_engraving"},{"name":"Armor Enchantments","href":"/items/7/14","icon":"inv_inscription_armorscroll01"},{"name":"Weapon Enchantments","href":"/items/7/15"}]
sgMenus.items_8=[{"name":"Generic(OBSOLETE)","href":"/items/8/0"}]
sgMenus.items_9=[{"name":"Alchemy","href":"/items/9/6","icon":"trade_alchemy"},{"name":"Blacksmithing","href":"/items/9/4","icon":"trade_blacksmithing"},{"name":"Cooking","href":"/items/9/5","icon":"inv_misc_food_15"},{"name":"Enchanting","href":"/items/9/8","icon":"trade_engraving"},{"name":"Engineering","href":"/items/9/3","icon":"trade_engineering"},{"name":"First Aid","href":"/items/9/7","icon":"spell_holy_sealofsacrifice"},{"name":"Fishing","href":"/items/9/9","icon":"trade_fishing"},{"name":"Jewelcrafting","href":"/items/9/10","icon":"inv_jewelcrafting_delicatecopperwire"},{"name":"Leatherworking","href":"/items/9/1","icon":"trade_leatherworking"},{"name":"Tailoring","href":"/items/9/2","icon":"trade_tailoring"},{"name":"Book","href":"/items/9/0","icon":"inv_misc_book_07"}]
sgMenus.items_10=[{"name":"Currency","href":"/items/10/0"}]
sgMenus.items_11=[{"name":"Quivers","href":"/items/11/2","icon":"inv_misc_quiver_09"},{"name":"Ammo Pouches","href":"/items/11/3","icon":"inv_misc_ammo_bullet_01"}]
sgMenus.items_12=[{"name":"Quest","href":"/items/12/0"}]
sgMenus.items_13=[{"name":"Keys","href":"/items/13/0"}]
sgMenus.items_14=[{"name":"Permanent","href":"/items/14/0"}]
sgMenus.items_15=[{"name":"Pets","href":"/items/15/2","icon":"inv_box_petcarrier_01"},{"name":"Mounts","href":"/items/15/5","icon":"ability_mount_ridinghorse"},{"name":"Reagents","href":"/items/15/1","icon":"inv_misc_dust_01"},{"name":"Holiday","href":"/items/15/3","icon":"inv_misc_plant_03"},{"name":"Junk","href":"/items/15/0","icon":"inv_box_01"},{"name":"Other","href":"/items/15/4","icon":"inv_misc_ticket_tarot_stack_01"}]
sgMenus.items_glyph_type=[{"name":"Prime Glyph","href":"$?itemspell_item__spell__glyph__flags=2"},{"name":"Major Glyph","href":"$?itemspell_item__spell__glyph__flags=0"},{"name":"Minor Glyph","href":"$?itemspell_item__spell__glyph__flags=1"}]
sgMenus.items_16=[{"name":"Death Knight","href":"/items/16/6","submenu":"items_glyph_type","icon":"class-deathknight"},{"name":"Druid","href":"/items/16/11","submenu":"items_glyph_type","icon":"class-druid"},{"name":"Hunter","href":"/items/16/3","submenu":"items_glyph_type","icon":"class-hunter"},{"name":"Mage","href":"/items/16/8","submenu":"items_glyph_type","icon":"class-mage"},{"name":"Paladin","href":"/items/16/2","submenu":"items_glyph_type","icon":"class-paladin"},{"name":"Priest","href":"/items/16/5","submenu":"items_glyph_type","icon":"class-priest"},{"name":"Rogue","href":"/items/16/4","submenu":"items_glyph_type","icon":"class-rogue"},{"name":"Shaman","href":"/items/16/7","submenu":"items_glyph_type","icon":"class-shaman"},{"name":"Warlock","href":"/items/16/9","submenu":"items_glyph_type","icon":"class-warlock"},{"name":"Warrior","href":"/items/16/1","submenu":"items_glyph_type","icon":"class-warrior"}]
sgMenus.items=[{"name":"By subclass","header":true},{"name":"Weapons","href":"/items/2","submenu":"items_2"},{"name":"Armor","href":"/items/4","submenu":"items_4"},{"name":"Bags","href":"/items/1","submenu":"items_1"},{"name":"Consumables","href":"/items/0","submenu":"items_0"},{"name":"Gems","href":"/items/3","submenu":"items_3"},{"name":"Glyphs","href":"/items/16","submenu":"items_16"},{"name":"Miscellaneous","href":"/items/15","submenu":"items_15"},{"name":"Projectiles","href":"/items/6","submenu":"items_6"},{"name":"Quivers","href":"/items/11","submenu":"items_11"},{"name":"Recipes","href":"/items/9","submenu":"items_9"},{"name":"Trade Goods","href":"/items/7","submenu":"items_7"},{"name":"Currency","href":"/items/10","icon":"spell_holy_championsbond"},{"name":"Keys","href":"/items/13","icon":"inv_misc_key_12"},{"name":"Quest Items","href":"/items/12","icon":"inv_misc_head_dragon_01"},{"name":"Quick filters","header":true},{"name":"Arena","href":"javascript:;","submenu":"items_arena"},{"name":"Starts a Quest","href":"/items/?starts_quest__gt=1"}]
sgMenus.items_arena=[{"name":"Level 80","header":true},{"name":"Season 8 (Current)","href":"/items/?name__startswith=Wrathful%20Gladiator's"},{"name":"Season 7","href":"/items/?name__startswith=Relentless%20Gladiator's"},{"name":"Season 6","href":"/items/?name__startswith=Furious%20Gladiator's"},{"name":"Season 5","href":"/items/?name__startswith=Deadly%20Gladiator's"},{"name":"Level 70","header":true},{"name":"Season 4","href":"/items/?name__startswith=Brutal%20Gladiator's"},{"name":"Season 3","href":"/items/?name__startswith=Vengeful%20Gladiator's"},{"name":"Season 2","href":"/items/?name__startswith=Merciless%20Gladiator's"},{"name":"Season 1","href":"/items/?name__startswith=Gladiator's&itemset_id__lt=770"}]
sgMenus.itemsets=[{"name":"Usable by...","header":true},{"name":"Death Knight","href":"/itemsets/?items__class_mask__band=32","icon":"class-deathknight"},{"name":"Druid","href":"/itemsets/?items__class_mask__band=1024","icon":"class-druid"},{"name":"Hunter","href":"/itemsets/?items__class_mask__band=4","icon":"class-hunter"},{"name":"Mage","href":"/itemsets/?items__class_mask__band=128","icon":"class-mage"},{"name":"Paladin","href":"/itemsets/?items__class_mask__band=2","icon":"class-paladin"},{"name":"Priest","href":"/itemsets/?items__class_mask__band=16","icon":"class-priest"},{"name":"Rogue","href":"/itemsets/?items__class_mask__band=8","icon":"class-rogue"},{"name":"Shaman","href":"/itemsets/?items__class_mask__band=64","icon":"class-shaman"},{"name":"Warlock","href":"/itemsets/?items__class_mask__band=256","icon":"class-warlock"},{"name":"Warrior","href":"/itemsets/?items__class_mask__band=1","icon":"class-warrior"}]
sgMenus.objects=[{"name":"Containers","href":"/objects/3"},{"name":"Destructible Buildings","href":"/objects/33"},{"name":"Elevators","href":"/objects/11"},{"name":"Fishing Schools","href":"/objects/25"},{"name":"Guild Banks","href":"/objects/34"},{"name":"Generic","href":"/objects/5"},{"name":"Mailboxes","href":"/objects/19"},{"name":"Meeting Stones","href":"/objects/23"},{"name":"PvP Capture Points","href":"/objects/29"},{"name":"Questgivers","href":"/objects/2"},{"name":"Texts","href":"/objects/9"},{"name":"Transports","href":"/objects/15"},{"name":"Miscellaneous","href":"javascript:;","submenu":"objects_misc"}]
sgMenus.objects_misc=[{"name":"Area Damage","href":"/objects/12"},{"name":"Aura Generators","href":"/objects/30"},{"name":"Barbershop Chairs","href":"/objects/32"},{"name":"Binders","href":"/objects/4"},{"name":"Buttons","href":"/objects/1"},{"name":"Cameras","href":"/objects/13"},{"name":"Chairs","href":"/objects/7"},{"name":"Doors","href":"/objects/0"},{"name":"Duel Flags","href":"/objects/16"},{"name":"Dungeon Portals","href":"/objects/31"},{"name":"Fishing Nodes","href":"/objects/17"},{"name":"Flag Drops","href":"/objects/26"},{"name":"Flag Stands","href":"/objects/24"},{"name":"Goobers","href":"/objects/10"},{"name":"Guard Posts","href":"/objects/21"},{"name":"Map Objects","href":"/objects/14"},{"name":"Mini-games","href":"/objects/27"},{"name":"Spellcasters","href":"/objects/22"},{"name":"Spell targets","href":"/objects/8"},{"name":"Summoning Rituals","href":"/objects/18"},{"name":"Trap Doors","href":"/objects/35"},{"name":"Traps","href":"/objects/6"},{"name":"Unused","href":"/objects/20"}]
sgMenus.quests=[{"name":"Dungeon","href":"/quests/?type=81"},{"name":"Group","href":"/quests/?type=1"},{"name":"Heroic","href":"/quests/?type=85"},{"name":"PvP","href":"/quests/?type=41"},{"name":"Raid","href":"/quests/?type=62"},{"name":"Raid (10)","href":"/quests/?type=88"},{"name":"Raid (25)","href":"/quests/?type=89"},{"name":"Quick filters","header":true},{"name":"Random dungeons","href":"/quests/?name__contains=Random"}]
sgMenus.spells_classes_dk=[{"name":"Blood","href":"/spells/770"},{"name":"Frost","href":"/spells/771"},{"name":"Unholy","href":"/spells/772"},{"name":"Runeforging","href":"/spells/776"}]
sgMenus.spells_classes_dr=[{"name":"Balance","href":"/spells/574"},{"name":"Feral Combat","href":"/spells/134"},{"name":"Restoration","href":"/spells/573"}]
sgMenus.spells_classes_hu=[{"name":"Beast Mastery","href":"/spells/50"},{"name":"Marksmanship","href":"/spells/163"},{"name":"Survival","href":"/spells/51"}]
sgMenus.spells_classes_ma=[{"name":"Arcane","href":"/spells/237"},{"name":"Fire","href":"/spells/8"},{"name":"Frost","href":"/spells/6"}]
sgMenus.spells_classes_pa=[{"name":"Retribution","href":"/spells/594"},{"name":"Protection","href":"/spells/267"},{"name":"Holy","href":"/spells/184"}]
sgMenus.spells_classes_pr=[{"name":"Discipline","href":"/spells/613"},{"name":"Holy","href":"/spells/56"},{"name":"Shadow Magic","href":"/spells/78"}]
sgMenus.spells_classes_ro=[{"name":"Assassination","href":"/spells/253"},{"name":"Combat","href":"/spells/38"},{"name":"Subtlety","href":"/spells/39"},{"name":"Lockpicking","href":"/spells/633"}]
sgMenus.spells_classes_sh=[{"name":"Elemental Combat","href":"/spells/375"},{"name":"Enhancement","href":"/spells/373"},{"name":"Restoration","href":"/spells/374"}]
sgMenus.spells_classes_wl=[{"name":"Affliction","href":"/spells/355"},{"name":"Demonology","href":"/spells/354"},{"name":"Destruction","href":"/spells/593"}]
sgMenus.spells_classes_wa=[{"name":"Arms","href":"/spells/26"},{"name":"Fury","href":"/spells/256"},{"name":"Protection","href":"/spells/257"}]
sgMenus.spells_classes=[{"name":"Death Knight","href":"/spells/?primary_skill__in=770,771,772,776","icon":"class-deathknight","submenu":"spells_classes_dk"},{"name":"Druid","href":"/spells/?primary_skill__in=134,573,574","icon":"class-druid","submenu":"spells_classes_dr"},{"name":"Hunter","href":"/spells/?primary_skill__in=50,51,163","icon":"class-hunter","submenu":"spells_classes_hu"},{"name":"Mage","href":"/spells/?primary_skill__in=6,8,237","icon":"class-mage","submenu":"spells_classes_ma"},{"name":"Paladin","href":"/spells/?primary_skill__in=184,267,594","icon":"class-paladin","submenu":"spells_classes_pa"},{"name":"Priest","href":"/spells/?primary_skill__in=56,78,613","icon":"class-priest","submenu":"spells_classes_pr"},{"name":"Rogue","href":"/spells/?primary_skill__in=38,39,253,633","icon":"class-rogue","submenu":"spells_classes_ro"},{"name":"Shaman","href":"/spells/?primary_skill__in=373,374,375","icon":"class-shaman","submenu":"spells_classes_sh"},{"name":"Warlock","href":"/spells/?primary_skill__in=354,355,593","icon":"class-warlock","submenu":"spells_classes_wl"},{"name":"Warrior","href":"/spells/?primary_skill__in=26,256,257","icon":"class-warrior","submenu":"spells_classes_wa"}]
sgMenus.spells_tradeskills=[{"name":"Primary Skills","header":true},{"name":"Alchemy","href":"/spells/171","icon":"trade_alchemy"},{"name":"Blacksmithing","href":"/spells/164","icon":"trade_blacksmithing"},{"name":"Enchanting","href":"/spells/333","icon":"trade_engraving"},{"name":"Engineering","href":"/spells/202","icon":"trade_engineering"},{"name":"Herbalism","href":"/spells/182","icon":"trade_herbalism"},{"name":"Inscription","href":"/spells/773","icon":"inv_inscription_tradeskill01"},{"name":"Jewelcrafting","href":"/spells/755","icon":"inv_misc_gem_02"},{"name":"Leatherworking","href":"/spells/165","icon":"trade_leatherworking"},{"name":"Mining","href":"/spells/186","icon":"trade_mining"},{"name":"Skinning","href":"/spells/393","icon":"inv_misc_pelt_wolf_01"},{"name":"Tailoring","href":"/spells/197","icon":"trade_tailoring"},{"name":"Secondary Skills","header":true},{"name":"Archeology","href":"/spells/794","icon":"trade_archaeology"},{"name":"Cooking","href":"/spells/185","icon":"inv_misc_food_15"},{"name":"First Aid","href":"/spells/129","icon":"spell_holy_sealofsacrifice"},{"name":"Fishing","href":"/spells/356","icon":"trade_fishing"},{"name":"Riding","href":"/spells/762","icon":"spell_nature_swiftness"}]
sgMenus.spells=[{"name":"Tradeskills","href":"/spells/?primary_skill__is_tradeskill=1","submenu":"spells_tradeskills"},{"name":"Class Skills","href":"javascript:;","submenu":"spells_classes"},{"name":"Companions","href":"/spells/778"},{"name":"Mounts","href":"/spells/777"},{"name":"Glyphs","href":"/spells/810"},{"name":"Guild Perks","href":"/spells/816"},{"name":"Uncategorized","href":"/spells/?primary_skill__isnull=1"}]
sgMenus.skills=[{"name":"Class Skills","href":"/skills/7"},{"name":"Professions","href":"/skills/11"},{"name":"Secondary Skills","href":"/skills/9"},{"name":"Armor Proficiencies","href":"/skills/8"},{"name":"Weapon Skills","href":"/skills/6"},{"name":"Languages","href":"/skills/10"},{"name":"","header":true},{"name":"Tradeskills","href":"/skills/?is_tradeskill=1"}]
sgMenus.sigrie=[{"name":"Items","href":"/items","submenu":"items"},{"name":"Achievements","href":"/achievements","submenu":"achievements"},{"name":"Creatures","href":"/creatures","submenu":"creatures"},{"name":"Spells","href":"/spells","submenu":"spells"},{"name":"Quests","href":"/quests","submenu":"quests"},{"name":"Skills","href":"/skills","submenu":"skills"},{"name":"Objects","href":"/objects","submenu":"objects"},{"name":"Item Sets","href":"/itemsets","submenu":"itemsets"},{"name":"Zones","href":"/zones"},{"name":"Factions","href":"/factions"},{"name":"Tools","header":true},{"name":"Talent Calculator","href":"/utils/talent","icon":"ability_marksmanship"},{"name":"Miscellaneous","header":true},{"name":"About Sigrie","href":"/about"},{"name":"Latest Additions","href":"/latest"},{"name":"Changelog","href":"/changelog"}]
sgMenus.index_more=[{"name":"Database","header":true},{"name":"Item Sets","href":"/itemsets"},{"name":"Factions","href":"/factions"},{"name":"Tools","header":true},{"name":"Talent Calculator","href":"/utils/talent"},{"name":"Miscellaneous","header":true},{"name":"About Sigrie","href":"/about"},{"name":"Latest Additions","href":"/latest"},{"name":"Changelog","href":"/changelog"}]
function doGenericName(txt,cell,row,id){cell.innerHTML=""
if(txt=="")txt="** No Name #"+id+" **";var n=document.createTextNode(txt)
var a=document.createElement("a")
var link=row["link"]
cell.style.textAlign="left"
cell.style.width="100%"
a.style.verticalAlign="bottom"
if(link){a.href=link
a.onmouseover=function(evt){ttlib.startTooltip(this)}
a.onmouseout=function(evt){ttlib.hide()}}
a.appendChild(n)
cell.appendChild(a)
return cell}
function doGenericNameWithIcon(txt,cell,row,id){span=doGenericName(txt,cell,row,id)
span.style.paddingLeft="2px"
img=document.createElement("img")
img.width=20
img.height=20
img.src="/static/img/icons/"+row["icon"]+".png"
img.style.margin="2px 4px 0px 0"
img.style["float"]="left"
a=document.createElement("a")
a.href=row["link"]
a.appendChild(img)
cell.insertBefore(a,cell.firstChild)
cell.style.verticalAlign="sub"
return cell}
function doGenericLookupReplace(txt,cell,row,array){cell.innerHTML=array[txt]
return cell}
function doGenericLinkReplace(txt,cell,link){cell.innerHTML=""
var a=document.createElement("a")
a.href=link
a.innerHTML=txt
a.className="link"
cell.appendChild(a)
return cell}
function doSkillWithLevel(txt,cell,row){if(row["required_skill_id"]){var skill=document.createElement("a")
skill.href="/skill/"+row["required_skill_id"]
skill.appendChild(document.createTextNode(txt))
skill.className="link"}else{var skill=document.createTextNode(txt)}
cell.appendChild(skill)
if(row["required_skill_level"]>1){var rank=document.createTextNode(" ("+row["required_skill_level"]+")")
cell.appendChild(rank)}
return cell}
function doGenericBoolean(txt,cell,row){if(txt==1){cell.innerHTML="Yes"}else{cell.innerHTML="No"}
return cell}
function doAchievementFaction(txt,cell,row){txt+=1
return doGenericLookupReplace(txt,cell,row,FACTIONS)}
function doAchievementInstance(txt,cell,row){link="/instance/"+row["instance_id"]
return doGenericLinkReplace(txt,cell,link)}
sorttable_template_achievement={"column_order":["name","instance","points","faction"],"hooks":{"name":doGenericNameWithIcon,"faction":doAchievementFaction,"instance":doAchievementInstance}}
template_required_for_achievement=sorttable_template_achievement
function doCreatureCategory(txt,cell,row){link="/creatures/?category="+txt
return doGenericLinkReplace(CREATURE_CATEGORIES[txt],cell,link)}
function doCreatureType(txt,cell,row){link="/creatures/?type="+txt
return doGenericLinkReplace(CREATURE_TYPES[txt],cell,link)}
function doCreatureFamily(txt,cell,row){link="/creatures/?family="+txt
return doGenericLinkReplace(CREATURE_FAMILIES[txt],cell,link)}
function doCreatureName(txt,cell,row){cell=doGenericName(txt,cell,row)
if(row["title"]){cell.style.lineHeight="1.1em"
cell.appendChild(document.createElement("br"))
var title=document.createTextNode("<"+row["title"]+">")
var span=document.createElement("span")
span.appendChild(title)
span.style.fontSize="80%"
cell.appendChild(span)}
return cell}
function doLootPercent(txt,cell,row){if(Math.floor(txt)!=txt){cell.innerHTML=txt.toFixed(1)}else{cell.innerHTML=txt}
cell.innerHTML+="%"
return cell}
sorttable_template_creature={"column_order":["name","category","type","family"],"column_names":{"required_skill":"Req. Skill","required_level":"Req. Lvl"},"hooks":{"name":doCreatureName,"category":doCreatureCategory,"family":doCreatureFamily,"type":doCreatureType,"required_skill":doSkillWithLevel,"percent":doLootPercent}}
template_creaturespell_spell=sorttable_template_creature
template_item__creature_quest_drops=sorttable_template_creature
template_creature__node_zone=sorttable_template_creature
template_creature_starts_quests=sorttable_template_creature
template_creature_faction=sorttable_template_creature
template_solditem_vendor={"column_order":["name","price","category"],"hooks":{"name":doCreatureName,"category":doCreatureCategory,"family":doCreatureFamily,"type":doCreatureType}}
template_trainedspell_spell={"extends":sorttable_template_creature,"column_order":["name","required_level","required_skill","price"]}
template_creature__loot_item={"extends":sorttable_template_creature,"column_order":["name","category","type","family","percent"],"columns_shown":{"percent":true},"column_names":{"percent":"%"}}
sorttable_template_enchant={"column_names":{"required_skill":"Req. Skill","required_skill_level":"Req. Skill level"},"column_order":["name","required_skill","charges"],"hooks":{"name":doGenericName,"required_skill":doSkillWithLevel}}
template_enchant_required_skill=sorttable_template_enchant
template_enchant_effects=sorttable_template_enchant
function doEncounterInstance(txt,cell,row){link="/instance/"+row["instance_id"]
return doGenericLinkReplace(txt,cell,link)}
sorttable_template_encounter={"column_order":["name","instance"],"hooks":{"name":doGenericName,"instance":doEncounterInstance}}
template_encounter_instance=sorttable_template_encounter
template_encounter_instance__heroic=sorttable_template_encounter
function doGlyphType(txt,cell,row){link="/glyphs/?minor="+txt
txt=txt==1?"+ Major Glyph":"- Minor Glyph"
return doGenericLinkReplace(txt,cell,link)}
sorttable_template_glyph={"column_names":{"minor":"Type"},"column_order":["name","minor"],"columns_shown":{"minor":true},"hooks":{"name":doGenericName,"minor":doGlyphType}}
template_glyph_spell=sorttable_template_glyph
sorttable_template_holiday={"column_order":["name"],"hooks":{"name":doGenericName}}
function doFactionParent(txt,cell,row){link="/faction/"+row["parent_id"]
return doGenericLinkReplace(txt,cell,link)}
sorttable_template_faction={"column_order":["name","parent"],"hooks":{"name":doGenericName,"parent":doFactionParent}}
template_faction_parent=sorttable_template_faction
function doInstanceZone(txt,cell,row){link="/z/"+row["zone_id"]
return doGenericLinkReplace(txt,cell,link)
return cell}
sorttable_template_instance={"column_names":{"max_players":"Max. players"},"column_order":["name","zone","max_players"],"hooks":{"name":doGenericName,"zone":doInstanceZone}}
template_instance_continent=sorttable_template_instance
template_instance_zone=sorttable_template_instance
function doItemLevel(txt,cell,row){cell.innerHTML=txt
if(row["required_level"]>1){cell.innerHTML+=" (Req. "+row["required_level"]+")"}
return cell}
function doItemCategory(txt,cell,row){link="/items/"+txt+"/"+row["subcategory"]
return doGenericLinkReplace(ITEM_SUBCLASSES[row["category"]][row["subcategory"]],cell,link)}
function doItemSlot(txt,cell,row){link="/items/?slot="+txt
txt=SLOTS[txt]
if(row["bag_slots"]){txt=row["bag_slots"]+" slot "+txt}
return doGenericLinkReplace(txt,cell,link)}
function doItemName(txt,cell,row){cell=doGenericNameWithIcon(txt,cell,row)
cell.getElementsByTagName("a")[1].className="q"+row["quality"]
if(row["stock"]){var limit=document.createTextNode(" ("+row["stock"]+")")
var span=document.createElement("span")
span.appendChild(limit)
cell.appendChild(span)}
return cell}
sorttable_template_item={"column_names":{"required_level":"Req. Level"},"column_order":["name","price","level","category","slot","count","percent"],"hooks":{"name":doItemName,"level":doItemLevel,"category":doItemCategory,"slot":doItemSlot,"percent":doLootPercent}}
template_item__loot_item={"extends":sorttable_template_item,"column_order":["name","level","category","count","percent"],"columns_shown":{"percent":true},"column_names":{"percent":"%"}}
template_creature_quest_drops=sorttable_template_item
template_item__contains=sorttable_template_item
template_item_related=sorttable_template_item
template_item_zone_bind=sorttable_template_item
template_item_required_holiday=sorttable_template_item
template_item_required_skill=sorttable_template_item
template_item_socket_bonus=sorttable_template_item
template_item_required_faction=sorttable_template_item
template_item_required_spell=sorttable_template_item
template_item_spells=sorttable_template_item
template_spell_item_teaches=sorttable_template_item
template_item_starts_quest=sorttable_template_item
template_enchant_property=sorttable_template_item
template_quest_drops=sorttable_template_item
template_itemextendedcost_item=sorttable_template_item
template_item_page=sorttable_template_item
template_solditem_item=sorttable_template_item
function doItemDisenchantAmount(txt,cell,row){var min=txt
var max=row["amount_max"]
cell.innerHTML=min
if(max>min)cell.innerHTML+="-"+max;return cell}
template_item_disenchant={"column_names":{"amount_min":"Amount","percent":"%"},"column_order":["name","amount_min","percent"],"hooks":{"name":doItemName,"amount_min":doItemDisenchantAmount}}
template_drops={"extends":sorttable_template_item,"column_names":{"percent":"%"}}
sorttable_template_itemset={"column_names":{"required_skill":"Req. Skill","required_skill_level":"Req. Skill level"},"column_order":["name","required_skill"],"hooks":{"name":doGenericName,"required_skill":doSkillWithLevel}}
template_itemset_required_skill=sorttable_template_itemset
template_spell_itemset_bonus=sorttable_template_itemset
function doObjectType(txt,cell,row){link="/objects/"+txt
return doGenericLinkReplace(row["get_type_display"],cell,link)}
sorttable_template_object={"column_order":["name","type"],"hooks":{"name":doGenericName,"type":doObjectType}}
template_object_starts_quests=sorttable_template_object
template__gameobject_page=sorttable_template_object
sorttable_template_mail={"column_order":["name"],"hooks":{"name":doGenericName}}
template_mail_attachment=sorttable_template_mail
function doPageNext(txt,cell,row){link="/page/"+txt
return doGenericLinkReplace(txt,cell,link)}
sorttable_template_page={"column_order":["name","next_page_id"],"column_names":{"next_page_id":"Next Page"},"hooks":{"name":doGenericName,"next_page_id":doPageNext}}
template_page_next_page=sorttable_template_page
function doQuestZone(txt,cell,row){link="/zone/"+row["zone_id"]
return doGenericLinkReplace(txt,cell,link)}
function doQuestLevel(txt,cell,row){var lvl=txt
if(lvl==-1)lvl="Any"
cell.innerHTML=lvl
var t=row["get_type"]
if(t){var span=document.createElement("span")
span.style.fontSize="75%"
span.innerHTML+=" ("+t+")"
cell.appendChild(span)}
return cell}
sorttable_template_quest={"column_names":{"get_type":"Type","required_level":"Req.","zone_id":"Zone Id"},"column_order":["name","level","required_level","zone"],"hooks":{"level":doQuestLevel,"name":doGenericName,"zone":doQuestZone}}
template_item_reward_from=sorttable_template_quest
template_questrewardfaction_quest=sorttable_template_quest
template_quest_zone=sorttable_template_quest
template_required_for_quest=sorttable_template_quest
template_quest_provided_item=sorttable_template_quest
template_quest_spell_trigger=sorttable_template_quest
template_quest_spell_reward=sorttable_template_quest
template_quest_ends_at_npc=sorttable_template_quest
template_creature__starts_quests=sorttable_template_quest
template_quest_skill_reward=sorttable_template_quest
function doSkillCategory(txt,cell,row){link="/skills/"+txt
return doGenericLinkReplace(SKILL_CATEGORIES[txt],cell,link)}
sorttable_template_skill={"column_names":{"is_tradeskill":"Tradeskill"},"column_order":["name","category","is_tradeskill"],"hooks":{"name":doGenericNameWithIcon,"is_tradeskill":doGenericBoolean,"category":doSkillCategory}}
template_skill_spells=sorttable_template_skill
function doSpellDispel(txt,cell,row){link="/spells/?dispel_type="+txt
return doGenericLinkReplace(DISPEL_TYPES[txt],cell,link)}
function doSpellPrimarySkill(txt,cell,row){link="/skill/"+row["primary_skill_id"]
return doGenericLinkReplace(txt,cell,link)}
function doSpellName(txt,cell,row){cell=doGenericNameWithIcon(txt,cell,row)
if(row["rank"]){var rank=document.createTextNode(" ("+row["rank"]+")")
var span=document.createElement("span")
span.appendChild(rank)
span.style.fontSize="80%"
cell.appendChild(span)}
return cell}
sorttable_template_spell={"column_names":{"dispel_type":"Dispel Type","get_mechanic_display":"Mechanic","primary_skill":"Skill","required_level":"Lvl","skill_levels":"Skill levels","created_item":"Creates","required_skill":"Req. Skill"},"column_order":["name","created_item","reagents","skill_levels","primary_skill","get_mechanic_display"],"hooks":{"name":doSpellName,"dispel_type":doSpellDispel,"primary_skill":doSpellPrimarySkill,"required_skill":doSkillWithLevel}}
template_trainedspell_trainer={"extends":sorttable_template_spell,"column_order":["name","required_level","required_skill","price"]}
template_skillspell_skill=sorttable_template_spell
template_spell_reagents=sorttable_template_spell
template_spell_createditem=sorttable_template_spell
template_item_tool_for_spell=sorttable_template_spell
template_spelleffectproperty_trigger_spell=sorttable_template_spell
template_creaturespell_creature=sorttable_template_spell
function doTalentTab(txt,cell,row){link="/talents/?tab="+row["tab_id"]
return doGenericLinkReplace(txt,cell,link)}
sorttable_template_talent={"column_names":{"max_ranks":"Ranks"},"column_order":["name","tab","max_ranks"],"hooks":{"name":doGenericName,"tab":doTalentTab}}
template_talentrank_spell=sorttable_template_talent
function doZoneParentArea(txt,cell,row){link="/z/"+row["parent_area_id"]
return doGenericLinkReplace(txt,cell,link)}
function doZoneTerritory(txt,cell,row){link="/zones/?territory="+txt
return doGenericLinkReplace(ZONE_PVP_TYPES[txt],cell,link)}
sorttable_template_zone={"column_names":{"parent_area":"Parent area"},"column_order":["name","level","territory","parent_area"],"hooks":{"name":doGenericName,"parent_area":doZoneParentArea,"territory":doZoneTerritory}}
template_zone_parent_area=sorttable_template_zone
function doCreatureLevelDataHealth(txt,cell,row){var hp=txt
var power=row["power"]
var power_type=row["power_type"]
cell.innerHTML=txt+" HP"
if(power==0&&power_type==1)return cell;cell.innerHTML+=" / "+power+" "+POWER_TYPES[power_type]
return cell}
function doCreatureLevelDataLevel(txt,cell,row){var heroic_level=row["heroic_level"]
var group_size=row["group_size"]
cell.innerHTML=txt
if(heroic_level){cell.innerHTML+=" (Heroic "+(group_size||5)+"-man)"}else if(group_size){cell.innerHTML+=" ("+group_size+"-man)"}
return cell}
template_creatureleveldata_creature={"column_names":{"heroic_level":"Heroic level","group_size":"Group size","health":"Health / Power"},"column_order":["level","health"],"hooks":{"level":doCreatureLevelDataLevel,"health":doCreatureLevelDataHealth}}
sigrieDefinitions={};var fields={"integer":function(custom){if(typeof(custom)!="object")custom={};var result={"type":"integer","size":7,"default":"","validator":function(type,value,modifier){if((modifier!="in")&&(isNaN(value)))return false;if(typeof(type.min)=="number"){if(value<type.min)return false;}
if(typeof(type.max)=="number"){if(value>type.max)return false;}
return true}}
for(var key in custom){result[key]=custom[key]}
return result},"string":function(custom){if(typeof(custom)!="object")custom={};var result={"type":"string","default":"","size":30,"validator":function(type,value,modifier){if(typeof(type.maxLength)=="number"){if(value.length>type.maxLength)return false;}
return true;}}
for(var key in custom){result[key]=custom[key]}
return result},"foreignKey":function(name,custom){if(typeof(custom)!="object")custom={};var result={"type":"foreignKey","key":name}
for(var key in custom){result[key]=custom[key]}
return result}}
var choices={"binds":[{"value":0,"name":"None"},{"value":1,"name":"Binds when picked up"},{"value":2,"name":"Binds when equipped"},{"value":3,"name":"Binds when used"},{"value":4,"name":"Quest Item"},{"value":5,"name":"Binds to account"}],"classes":[{"value":1,"name":"Warrior"},{"value":2,"name":"Paladin"},{"value":3,"name":"Hunter"},{"value":4,"name":"Rogue"},{"value":5,"name":"Priest"},{"value":6,"name":"Death Knight"},{"value":7,"name":"Shaman"},{"value":8,"name":"Mage"},{"value":9,"name":"Warlock"},{"value":11,"name":"Druid"}],"creatureCategories":[{"value":0,"name":"Not Specified"},{"value":1,"name":"Beast"},{"value":2,"name":"Dragonkin"},{"value":3,"name":"Demon"},{"value":4,"name":"Elemental"},{"value":5,"name":"Giant"},{"value":6,"name":"Undead"},{"value":7,"name":"Humanoid"},{"value":8,"name":"Critter"},{"value":9,"name":"Mechanical"},{"value":10,"name":"Uncategorized"},{"value":11,"name":"Totem"},{"value":12,"name":"Non-combat Pet"},{"value":13,"name":"Gas Cloud"}],"creatureTypes":[{"value":0,"name":"Normal"},{"value":1,"name":"Elite"},{"value":2,"name":"Rare-Elite"},{"value":3,"name":"Boss"},{"value":4,"name":"Rare"}],"dispelTypes":[{"value":1,"name":"Magic"},{"value":2,"name":"Curse"},{"value":3,"name":"Disease"},{"value":4,"name":"Poison"},{"value":9,"name":"Enrage"}],"gemColors":[{"value":1,"name":"Meta"},{"value":2,"name":"Red"},{"value":4,"name":"Yellow"},{"value":8,"name":"Blue"}],"itemCategories":[{"value":0,"name":"Consumable"},{"value":1,"name":"Bags"},{"value":2,"name":"Weapons"},{"value":3,"name":"Gems"},{"value":4,"name":"Armor"},{"value":6,"name":"Projectiles"},{"value":7,"name":"Trade Goods"},{"value":9,"name":"Recipes"},{"value":10,"name":"Currency"},{"value":11,"name":"Quivers"},{"value":12,"name":"Quest Items"},{"value":13,"name":"Keys"},{"value":15,"name":"Miscellaneous"},{"value":16,"name":"Glyphs"}],"itemQualities":[{"value":0,"name":"Poor"},{"value":1,"name":"Common"},{"value":2,"name":"Uncommon"},{"value":3,"name":"Rare"},{"value":4,"name":"Epic"},{"value":5,"name":"Legendary"},{"value":6,"name":"Artifact"},{"value":7,"name":"Heirloom"}],"races":[{"value":1,"name":"Human"},{"value":2,"name":"Orc"},{"value":3,"name":"Dwarf"},{"value":4,"name":"Night Elf"},{"value":5,"name":"Undead"},{"value":6,"name":"Tauren"},{"value":7,"name":"Gnome"},{"value":8,"name":"Troll"},{"value":10,"name":"Blood Elf"},{"value":11,"name":"Draenei"}],"schools":[{"value":0,"name":"Physical"},{"value":1,"name":"Holy"},{"value":2,"name":"Fire"},{"value":3,"name":"Nature"},{"value":4,"name":"Frost"},{"value":5,"name":"Shadow"},{"value":6,"name":"Arcane"}],"slots":[{"value":0,"name":"None"},{"value":1,"name":"Head"},{"value":2,"name":"Neck"},{"value":3,"name":"Shoulder"},{"value":4,"name":"Shirt"},{"value":5,"name":"Chest"},{"value":6,"name":"Waist"},{"value":7,"name":"Legs"},{"value":8,"name":"Feet"},{"value":9,"name":"Wrist"},{"value":10,"name":"Hands"},{"value":11,"name":"Finger"},{"value":12,"name":"Trinket"},{"value":13,"name":"One-Hand"},{"value":14,"name":"Shield"},{"value":15,"name":"Ranged"},{"value":16,"name":"Back"},{"value":17,"name":"Two-Hand"},{"value":18,"name":"Bag"},{"value":19,"name":"Tabard"},{"value":20,"name":"Chest"},{"value":21,"name":"Main Hand"},{"value":22,"name":"Off-Hand"},{"value":23,"name":"Held In Off-hand"},{"value":24,"name":"Projectile"},{"value":25,"name":"Thrown"},{"value":26,"name":"Ranged"},{"value":28,"name":"Relic"}],"boolean":[{"value":0,"name":"No"},{"value":1,"name":"Yes"}],"faction":[{"value":-1,"name":"Both"},{"value":0,"name":"Horde"},{"value":1,"name":"Alliance"}],"pvpZoneType":[{"value":0,"name":"Contested"},{"value":2,"name":"Alliance"},{"value":4,"name":"Horde"},{"value":6,"name":"Sanctuary"}],"questTypes":[{"value":1,"name":"Group"},{"value":41,"name":"PvP"},{"value":62,"name":"Raid"},{"value":81,"name":"Dungeon"},{"value":82,"name":"World Event"},{"value":85,"name":"Heroic"},{"value":88,"name":"Raid (10)"},{"value":89,"name":"Raid (25)"}]}
sigrieDefinitions.achievement={"id":fields.integer({"name":"Id","primaryKey":true}),"faction":fields.integer({"name":"Faction","choices":choices.faction,"default":-1}),"Instance":fields.foreignKey("instance",{"name":"Instance"}),"parent":fields.foreignKey("achievement",{"name":"Parent Achievement"}),"name":fields.string({"name":"Name","maxLength":256}),"points":fields.integer({"name":"Awards points"}),"statistic":fields.integer({"name":"Statistic","choices":choices.boolean,"default":1}),"serverfirst":fields.integer({"name":"Realm first","choices":choices.boolean,"default":1}),"icon":fields.string({"name":"Icon","maxLength":32}),"objective":fields.string({"name":"Objective"}),"reward":fields.string({"name":"Reward"}),"category":fields.foreignKey("achievementCategory",{"name":"Category"})};sigrieDefinitions.achievementCategory={"id":fields.integer({"name":"Id","primaryKey":true}),"parent":fields.foreignKey("achievementCategory",{"name":"Parent"}),"name":fields.string({"name":"Name","maxLength":64})}
sigrieDefinitions.creature={"id":fields.integer({"name":"Id","primaryKey":true}),"name":fields.string({"name":"Name","maxLength":256}),"title":fields.string({"name":"Title","maxLength":128}),"category":fields.integer({"name":"Category","choices":choices.creatureCategories}),"family":fields.integer({"name":"Family"}),"type":fields.integer({"name":"Type","choices":choices.creatureTypes}),"can_repair":fields.integer({"name":"Can repair","choices":choices.boolean})}
sigrieDefinitions.enchant={"id":fields.integer({"name":"Id","primaryKey":true}),"charges":fields.integer({"name":"Charges"}),"name":fields.string({"name":"Name","maxLength":64}),"gem":fields.foreignKey("item",{"name":"Gem"}),"required_level":fields.integer({"name":"Required level"}),"required_skill":fields.foreignKey("skill",{"name":"Required skill"}),"required_skill_level":fields.integer({"name":"Required skill level"})}
sigrieDefinitions.faction={"id":fields.integer({"name":"Id","primaryKey":true}),"name":fields.string({"name":"Name","maxLength":256}),"description":fields.string({"name":"Description"})}
sigrieDefinitions.glyph={"id":fields.integer({"name":"Id","primaryKey":true}),"name":fields.string({"name":"Name","maxLength":64}),"icon":fields.string({"name":"Icon","maxLength":64})}
sigrieDefinitions.holiday={"name":fields.string({"name":"Name","maxLength":256}),"description":fields.string({"name":"Description"}),"icon":fields.string({"name":"Icon","maxLength":64})}
sigrieDefinitions.instance={"id":fields.integer({"name":"Id","primaryKey":true}),"name":fields.string({"name":"Name","maxLength":256})}
sigrieDefinitions.item={"id":fields.integer({"name":"Id","primaryKey":true}),"category":fields.integer({"name":"Category","choices":choices.itemCategories}),"subcategory":fields.integer({"name":"Subcategory"}),"name":fields.string({"name":"Name","maxLength":256}),"icon":fields.string({"name":"Icon","maxLength":64}),"quality":fields.integer({"name":"Quality","choices":choices.itemQualities}),"conjured":fields.integer({"name":"Conjured","choices":choices.boolean,"default":1}),"openable":fields.integer({"name":"Openable","choices":choices.boolean,"default":1}),"heroic":fields.integer({"name":"Heroic","choices":choices.boolean,"default":1}),"unique_equipped":fields.integer({"name":"Unique-Equipped","choices":choices.boolean,"default":1}),"group_loot":fields.integer({"name":"Group loot","choices":choices.boolean,"default":1}),"refundable":fields.integer({"name":"Refundable","choices":choices.boolean,"default":1}),"chart":fields.integer({"name":"Chart","choices":choices.boolean,"default":1}),"prospecting":fields.integer({"name":"Prospectable at level"}),"usable_in_arena":fields.integer({"name":"Usable in arenas","choices":choices.boolean,"default":1}),"milling":fields.integer({"name":"Millable at level"}),"buy_price":fields.integer({"name":"Sold for (copper)"}),"sell_price":fields.integer({"name":"Bought for (copper)"}),"slot":fields.integer({"name":"Slot","choices":choices.slots}),"level":fields.integer({"name":"Level"}),"required_level":fields.integer({"name":"Required level"}),"required_skill":fields.foreignKey("skill",{"name":"Required skill"}),"required_skill_level":fields.integer({"name":"Required skill level"}),"required_spell":fields.foreignKey("spell",{"name":"Required spell"}),"required_faction":fields.foreignKey("faction",{"name":"Required faction"}),"unique":fields.integer({"name":"Unique count"}),"stack":fields.integer({"name":"Stack count"}),"bag_slots":fields.integer({"name":"Bag slots"}),"damage_type":fields.integer({"name":"Damage type","choices":choices.schools}),"armor":fields.integer({"name":"Armor"}),"fire_resist":fields.integer({"name":"Fire resistance"}),"nature_resist":fields.integer({"name":"Nature resistance"}),"frost_resist":fields.integer({"name":"Frost resistance"}),"shadow_resist":fields.integer({"name":"Shadow resistance"}),"arcane_resist":fields.integer({"name":"Arcane resistance"}),"speed":fields.integer({"name":"Attack speed"}),"teaches_spell":fields.foreignKey("spell",{"name":"Teaches spell"}),"bind":fields.integer({"name":"Binding","choices":choices.binds}),"note":fields.string({"name":"Note","maxLength":1024}),"starts_quest":fields.foreignKey("quest",{"name":"Starts quest"}),"lockpicking":fields.integer({"name":"Requires Lockpicking"}),"random_enchantment":fields.integer({"name":"Random properties","choices":choices.boolean,"default":1}),"block":fields.integer({"name":"Block"}),"itemset":fields.foreignKey("itemset",{"name":"Part of item set"}),"durability":fields.integer({"name":"Durability"}),"zone_bind":fields.foreignKey("zone",{"name":"Bound to zone"}),"instance_bind":fields.foreignKey("instance",{"name":"Bound to instance"}),"socket_bonus":fields.foreignKey("enchant",{"name":"Socket bonus"}),"gem_properties":fields.foreignKey("enchant",{"name":"Gem properties"}),"gem_color":fields.integer({"name":"Matches socket","choices":choices.gemColors}),"disenchanting":fields.integer({"name":"Disenchantable at level"}),"bonus_armor":fields.integer({"name":"Bonus armor"}),"unique_category":fields.foreignKey("itemUniqueCategory",{"name":"Unique category"}),"required_holiday":fields.foreignKey("holiday",{"name":"Required holiday"})}
sigrieDefinitions.itemUniqueCategory={"id":fields.integer({"name":"Id","primaryKey":true}),"name":fields.string({"name":"Name","maxLength":256}),"amount":fields.integer({"name":"Amount"}),"equipped":fields.integer({"name":"Unique-Equipped","choices":choices.boolean,"default":1})}
sigrieDefinitions.itemset={"id":fields.integer({"name":"Id","primaryKey":true}),"name":fields.string({"name":"Name","maxLength":256}),"required_skill":fields.foreignKey("skill",{"name":"Required skill"}),"required_skill_level":fields.integer({"name":"Required skill level"})}
sigrieDefinitions.object={"id":fields.integer({"name":"Id","primaryKey":true}),"name":fields.string({"name":"Name","maxLength":64}),"type":fields.integer({"name":"Type"})}
sigrieDefinitions.page={"id":fields.integer({"name":"Id","primaryKey":true}),"name":fields.string({"name":"Name","maxLength":64}),"text":fields.string({"name":"Text"}),"next_page":fields.foreignKey("page",{"name":"Next page"})}
sigrieDefinitions.quest={"id":fields.integer({"name":"Id","primaryKey":true}),"level":fields.integer({"name":"Level"}),"category":fields.integer({"name":"Category Id"}),"zone":fields.foreignKey("zone",{"name":"Zone"}),"type":fields.integer({"name":"Type","choices":choices.questTypes}),"suggested_players":fields.integer({"name":"Suggested players"}),"followup":fields.foreignKey("quest",{"name":"Follow up"}),"required_money":fields.integer({"name":"Required money"}),"money_reward":fields.integer({"name":"Money reward"}),"money_reward_cap":fields.integer({"name":"Money reward at level 80"}),"spell_reward":fields.foreignKey("spell",{"name":"Rewards spell"}),"spell_trigger":fields.foreignKey("spell",{"name":"Triggers spell"}),"raid":fields.integer({"name":"Completable in raid","choices":choices.boolean,"default":1}),"daily":fields.integer({"name":"Daily","choices":choices.boolean,"default":1}),"flags_pvp":fields.integer({"name":"Flags PvP","choices":choices.boolean,"default":1}),"talents_reward":fields.integer({"name":"Talents rewarded"}),"name":fields.string({"name":"Name","maxLength":512}),"objective":fields.string({"name":"Objective"}),"description":fields.string({"name":"Description"}),"summary":fields.string({"name":"Summary"}),"quick_summary":fields.string({"name":"Quick summary"})}
sigrieDefinitions.skill={"id":fields.integer({"name":"Id","primaryKey":true}),"name":fields.string({"name":"Name","maxLength":256}),"description":fields.string({"name":"Description"}),"is_tradeskill":fields.integer({"name":"Is a tradeskill","choices":choices.boolean,"default":1})}
sigrieDefinitions.spell={"id":fields.integer({"name":"Id","primaryKey":true}),"dispel_type":fields.integer({"name":"Dispel Type","choices":choices.dispelTypes}),"cast_time":fields.integer({"name":"Cast Time (seconds)"}),"power_cost_type":fields.integer({"name":"Power cost type"}),"power_cost_amount":fields.integer({"name":"Power cost amount"}),"min_range":fields.integer({"name":"Minimum range"}),"max_range":fields.integer({"name":"Maximum range"}),"max_stack":fields.integer({"name":"Maximum stack"}),"created_item":fields.foreignKey("item",{"name":"Creates Item"}),"icon":fields.string({"name":"Icon","maxLength":64}),"buff_icon":fields.string({"name":"Buff icon","maxLength":64}),"name":fields.string({"name":"Name","maxLength":512}),"rank":fields.string({"name":"Rank","maxLength":32}),"description":fields.string({"name":"Description"}),"buff_description":fields.string({"name":"Buff description"}),"power_percent":fields.integer({"name":"Power cost (%)"}),"max_target_level":fields.integer({"name":"Maximum target level"}),"runic_power_gain":fields.integer({"name":"Runic power gain"}),"primary_skill":fields.foreignKey("skill",{"name":"Skill Category"}),"passive":fields.integer({"name":"Passive","choices":choices.boolean,"default":1}),"not_usable_in_combat":fields.integer({"name":"Not usable in combat","choices":choices.boolean,"default":1}),"channeled":fields.integer({"name":"Channeled","choices":choices.boolean,"default":1})}
sigrieDefinitions.zone={"id":fields.integer({"name":"Id","primaryKey":true}),"level":fields.integer({"name":"Level"}),"parent_area":fields.foreignKey("zone",{"name":"Parent area"}),"name":fields.string({"name":"Name","maxLength":128}),"pvp":fields.integer({"name":"Territory","choices":choices.pvpZoneType})}
sigrieDefinitions.talent={"id":fields.integer({"name":"Id","primaryKey":true}),"depends":fields.foreignKey("talent",{"name":"Depends on"})}
PAGE_SIZE=50
var tablelib={init:function(){secondDraw=false
tablelib.tableData={}
tablelib.parseDocument()},parseDocument:function(){var tables=document.getElementsByTagName("table")
for(var i=0;i<tables.length;i++){if(hasClass(tables[i],"sorttable")){var data=null
eval("if (typeof("+tables[i].getAttribute("name")+") == 'object') data = "+tables[i].getAttribute("name"))
if((data===null)||(data.length<1))continue;var template=null
eval("if (typeof("+tables[i].getAttribute("template")+") == 'object') template = "+tables[i].getAttribute("template"))
if(template===null){template={'columns_shown':{},'column_names':{},'column_order':[],'hooks':{}}
for(var key in data[0]){template.columns_shown[key]=true
template.column_names[key]=key
template.column_order.push(key)
template.hooks[key]=false}}
else if(typeof(template['extends'])=='object'){for(var key in template['extends']){if(typeof(template[key])=='undefined')template[key]=template['extends'][key];}
template['extends']=false}
tablelib.tableData[tables[i].getAttribute("name")]={elem:tables[i],data:data,filteredData:data,template:template}
tablelib.buildTable(tables[i].getAttribute("name"))}}},addButton:function(text,name){var btn=document.createElement("a")
btn.className="button inactive"
btn.innerHTML=text
btn.href="javascript:;"
btn.setAttribute("tblname",name)
return btn},buildTable:function(name){var table=tablelib.tableData[name]
var options=tablelib.expandTableOptions(currentURL.getKey("hash","table__"+name,""))
var element=tablelib.tableData[name].elem
var data=tablelib.tableData[name].data
var template=tablelib.tableData[name].template
var columns=template["column_order"]
var names=template["column_names"]||{}
var shown=template["columns_shown"]||tablelib.buildColumnsShown(name)
var hooks=template["hooks"]||{}
var i
var thead=document.createElement("thead")
var headrow=document.createElement("tr")
table.name=name
table.sort=[{"name":columns[0],"descending":true}]
tablelib.tableData[name].pageCount=Math.ceil(data.length/PAGE_SIZE)
tablelib.tableData[name].currentPage=options.page
for(i=0;i<columns.length;i++){if(shown[columns[i]]==false)continue;var th=document.createElement("th")
var thlink=document.createElement("a")
thlink.href="javascript:;"
thlink.setAttribute("tblname",name)
thlink.setAttribute("colname",columns[i])
thlink.onclick=function(){if(hasClass(this,"descending")){removeClass(this,"descending")
addClass(this,"ascending")}else if(hasClass(this,"ascending")){removeClass(this,"ascending")
addClass(this,"descending")}else{addClass(this,"descending")}
var ths=headrow.getElementsByTagName("a")
for(i=0;i<ths.length;i++){if(ths[i]==this)continue
removeClass(ths[i],"descending")
removeClass(ths[i],"ascending")}
tablelib.sortData(tablelib.tableData[this.getAttribute("tblname")],this.getAttribute("colname"),hasClass(this,"descending"))}
var headername=document.createTextNode(names[columns[i]]||columns[i])
thlink.appendChild(headername)
th.appendChild(thlink)
headrow.appendChild(th)}
thead.appendChild(headrow)
tbody=document.createElement("tbody")
element.appendChild(thead)
element.appendChild(tbody)
var pageWidget=document.createElement("div")
pageWidget.className="sorttable-pagewidget"
var pageCount=document.createElement("span")
var firstButton=tablelib.addButton("« First",name)
var prevButton=tablelib.addButton("‹ Prev",name)
var nextButton=tablelib.addButton("Next ›",name)
var lastButton=tablelib.addButton("Last »",name)
table.firstButton=firstButton
table.prevButton=prevButton
table.nextButton=nextButton
table.lastButton=lastButton
table.pageCountWidget=pageCount
firstButton.onclick=function(){if(hasClass(this,"inactive"))return;var table=tablelib.tableData[this.getAttribute("tblname")]
table.currentPage=1
tablelib.drawTable(table)
addClass(table.firstButton,"inactive")
addClass(table.prevButton,"inactive")
removeClass(table.nextButton,"inactive")
removeClass(table.lastButton,"inactive")
currentURL.setKey("hash","table__"+this.getAttribute("tblname"),tablelib.compressTableOptions({"page":table.currentPage,"columns":table.sort}))
document.location.href=currentURL}
prevButton.onclick=function(){if(hasClass(this,"inactive"))return;var table=tablelib.tableData[this.getAttribute("tblname")]
table.currentPage=table.currentPage-1
if(table.currentPage<=1){table.currentPage=1
addClass(table.firstButton,"inactive")
addClass(table.prevButton,"inactive")
removeClass(table.nextButton,"inactive")
removeClass(table.lastButton,"inactive")}else if(table.currentPage<table.pageCount){removeClass(table.nextButton,"inactive")
removeClass(table.lastButton,"inactive")}
tablelib.drawTable(table)
currentURL.setKey("hash","table__"+this.getAttribute("tblname"),tablelib.compressTableOptions({"page":table.currentPage,"columns":table.sort}))
document.location.href=currentURL}
lastButton.onclick=function(){if(hasClass(this,"inactive"))return;var table=tablelib.tableData[this.getAttribute("tblname")]
table.currentPage=table.pageCount
tablelib.drawTable(table)
addClass(table.nextButton,"inactive")
addClass(table.lastButton,"inactive")
removeClass(table.prevButton,"inactive")
removeClass(table.firstButton,"inactive")
currentURL.setKey("hash","table__"+this.getAttribute("tblname"),tablelib.compressTableOptions({"page":table.currentPage,"columns":table.sort}))
document.location.href=currentURL}
nextButton.onclick=function(){if(hasClass(this,"inactive"))return;var table=tablelib.tableData[this.getAttribute("tblname")]
table.currentPage=table.currentPage+1
if(table.currentPage>=table.pageCount){table.currentPage=table.pageCount
addClass(table.nextButton,"inactive")
addClass(table.lastButton,"inactive")
removeClass(table.firstButton,"inactive")
removeClass(table.prevButton,"inactive")}else if(table.currentPage>1){removeClass(table.firstButton,"inactive")
removeClass(table.prevButton,"inactive")}
tablelib.drawTable(table)
currentURL.setKey("hash","table__"+this.getAttribute("tblname"),tablelib.compressTableOptions({"page":table.currentPage,"columns":table.sort}))
document.location.href=currentURL}
pageWidget.appendChild(firstButton)
pageWidget.appendChild(prevButton)
pageWidget.appendChild(pageCount)
pageWidget.appendChild(nextButton)
pageWidget.appendChild(lastButton)
if((table.currentPage<table.pageCount)&&(table.pageCount>1)){removeClass(nextButton,"inactive")
removeClass(lastButton,"inactive")}
if(table.currentPage>1){removeClass(prevButton,"inactive")
removeClass(firstButton,"inactive")}
element.parentNode.insertBefore(pageWidget,element)
var searchbox=document.getElementById(name+"-searchbox")
if(searchbox){searchbox.onkeyup=function(){tablelib.filterTable(table,this.value)}}
tablelib.drawTable(table)
for(var i in options.columns){var column=options.columns[i]
tablelib.sortData(table,column.name,column.descending)}},sortData:function(table,col,descending,silent){if(typeof(silent)=="undefined")silent=false;sortcol=col
table.filteredData.sort(tablelib.sortFunc)
table.sort=[{"name":col,"descending":descending}]
if(!descending){table.filteredData.reverse()}
tablelib.drawTable(table)
if(!silent){currentURL.setKey("hash","table__"+table.name,tablelib.compressTableOptions({"page":table.currentPage,"columns":table.sort}))
document.location.href=currentURL.toString()}},filterTable:function(table,filter){table.filteredData=[]
table.currentPage=1
for(var i=0;i<table.data.length;i++){if(table.data[i].name.toLowerCase().match(filter.toLowerCase())!=null){table.filteredData.push(table.data[i])}}
table.pageCount=Math.ceil(table.filteredData.length/PAGE_SIZE)
tablelib.drawTable(table)},getPageRange:function(table){if(table.currentPage==table.pageCount)return(((table.currentPage-1)*PAGE_SIZE)+1)+"-"+table.filteredData.length+" ("+table.filteredData.length+" total)"
else if(table.filteredData.length==0)return"0 - 0 (0 total)"
else return(((table.currentPage-1)*PAGE_SIZE)+1)+"-"+(table.currentPage*PAGE_SIZE)+" ("+table.filteredData.length+" total)"},drawTable:function(table){var element=table.elem
var columns=table.template["column_order"]
var shown=table.template["columns_shown"]
var hooks=table.template["hooks"]||{}
var tbody=element.getElementsByTagName("tbody")[0]
var trs=tbody.childNodes
table.pageCountWidget.innerHTML=tablelib.getPageRange(table)
while(trs.length>0)tbody.removeChild(trs[0])
for(var d=((table.currentPage-1)*PAGE_SIZE)+1;d<=table.filteredData.length&&d<table.currentPage*PAGE_SIZE;d++){var obj=table.filteredData[d-1]
if(!obj)continue;if(!obj["elem"]){var tr=document.createElement("tr")
for(var c in columns){if(shown[columns[c]]==false)continue;var td=document.createElement("td")
if(hooks[columns[c]])td=hooks[columns[c]](obj[columns[c]],td,obj,obj["id"])
else td.innerHTML=obj[columns[c]]
tr.appendChild(td)}
obj["elem"]=tr
tbody.appendChild(tr)}else tbody.appendChild(obj["elem"])}},sortFunc:function(ai,bi){var a=ai[sortcol]
var b=bi[sortcol]
if(typeof(a)=="string"){if(a.toLowerCase()>b.toLowerCase())return 1
else if(a.toLowerCase()==b.toLowerCase())return 0
else return-1}else if(typeof(a)=="number"){return a-b}},expandTableOptions:function(serial){var result={'page':1,'columns':[]}
var match=0
if(match=serial.match(/(\d+):([\+\-,\w]*)/)){result.page=parseInt(match[1])
var columns=match[2]
while(match=columns.match(/^([\+\-])(\w+),?/)){var column={'descending':(match[1]=='-'),'name':match[2]}
result.columns.push(column)
columns=columns.substr(match[0].length)}}
return result},compressTableOptions:function(options){var columns=""
for(var i in options.columns){var column=options.columns[i]
if(columns.length>0)columns+=",";if(column.descending){columns+="-"}else{columns+="+"}
columns+=column.name}
return options.page+":"+columns},buildColumnsShown:function(name){var template=tablelib.tableData[name].template
var columns=template["column_order"]
var data=tablelib.tableData[name].data
var shown={}
for(var i=0;i<columns.length;i++){var column=columns[i]
shown[column]=false
for(var j=0;j<data.length&&!shown[column];j++){shown[column]=((typeof(data[j][column])!="undefined")&&(data[j][column]!=""))}}
tablelib.tableData[name].template.columns_shown=shown
return shown}}
addLoadEvent(tablelib.init)
var SigrieMenus=function(){var that=this
this.offsetTop=5
this.offsetLeft=-8
this.hideDelay=300
this.init=function(){this.menus=[]
this.hideTimeout=-1
this.findMenus()}
this.findMenus=function(){var elements=document.getElementsByTagName("a")
var buffer=[]
for(var i in elements){if(typeof(elements[i])=="object")buffer.push(elements[i]);}
for(var i in buffer){var element=buffer[i]
var menu=element.getAttribute("rel")
if((typeof(menu)=="string")&&(typeof(sgMenus[menu])=="object")){element.menu=menu
element.onmouseover=function(){that.showMenu(this.menu,0,this)}}}}
this.showMenu=function(type,depth,button,parent){this.clearMenus(depth)
var menu={"type":type,"button":button,"list":document.createElement("ul"),"depth":depth}
var menuid=this.menus.push(menu)-1
var de=document.documentElement
var body=document.body
addClass(button,"selected")
addClass(menu.list,"menuitem")
body.appendChild(menu.list)
this.populateMenu(menuid,parent)
menu.list.style.position="absolute"
var top=getOffsetTop(button)
var left=getOffsetLeft(button)
if(depth==0){top+=button.offsetHeight}
else{left+=button.offsetWidth}
var diff=(top+menu.list.offsetHeight)-(de.clientHeight+body.scrollTop+de.scrollTop)
if(diff>0)top-=diff;menu.list.style.top=top+"px"
menu.list.style.left=left+"px"
button.onmouseout=menu.list.onmouseout=function(){that.resetHideTimer()}
menu.list.onmouseover=function(){that.stopHideTimer()}
this.stopHideTimer()}
this.clearMenus=function(depth){while(this.menus.length>depth){var menu=this.menus.pop()
removeClass(menu.button,"selected")
menu.list.parentNode.removeChild(menu.list)}}
this.populateMenu=function(menuid,parent){var menu=this.menus[menuid]
var type=sgMenus[menu.type]
if(typeof(type)!="object")return;for(var i in type){var li=document.createElement("li")
var a=document.createElement("a")
if((typeof(type[i].header)=="boolean")&&(type[i].header===true)){addClass(li,"menuheader")}
if(typeof(type[i].icon)=="string"){var icon=document.createElement("img")
icon.src="/static/img/icons/"+type[i].icon+".png"
icon.className="menuicon"
li.appendChild(icon)}
if((typeof(type[i].submenu)=="string")&&(typeof(sgMenus[type[i].submenu])=="object")){addClass(li,"submenu")
li.subtype=type[i].submenu
li.submenu=type[i]
li.onmouseover=function(){that.showMenu(this.subtype,this.menu.depth+1,this,this.submenu)}}
else{li.onmouseover=function(){that.clearMenus(this.menu.depth+1)}}
a.textContent=a.innerText=type[i].name
li.menu=menu
var href=type[i].href
if(typeof(href)=="string"){if(href[0]=="$"){href=parent.href+href.substring(1)}
a.href=href}
else{a.href="javascript:;"
a.onclick=function(){return false}}
li.appendChild(a)
menu.list.appendChild(li)}}
this.resetHideTimer=function(){if(this.hideTimeout>=0)window.clearTimeout(this.hideTimeout)
this.hideTimeout=window.setTimeout(function(){that.hideTimer()},this.hideDelay)}
this.stopHideTimer=function(){window.clearTimeout(this.hideTimeout)
this.hideTimeout=-1}
this.hideTimer=function(){this.stopHideTimer()
this.clearMenus(0)}}
sigrieMenus=new SigrieMenus()
addLoadEvent(function(){sigrieMenus.init()})
var SigrieFilters=function(){var that=this
this.maximumFilters=12
this.init=function(){this.filterbox=document.getElementById("filterbox")
this.filterContainer=document.getElementById("filters")
this.apply=document.createElement("button")
this.add=document.createElement("button")
if(this.filterbox==null)return false;if(typeof(currentURL)=="undefined")new URL(document.location.href);this.filters=[]
this.apply.textContent=this.apply.innerText="Apply filters"
this.apply.onclick=function(){that.submitFilters()
return false}
this.apply.style.display="none"
this.filterbox.appendChild(this.apply)
this.add.textContent=this.add.innerText="Add filter"
this.add.onclick=function(){that.addFilter()
return false}
this.filterbox.appendChild(this.add)
if(this.filterbox.getAttribute("searchtype")=="all"){this.hookTabs()
this.masterTypes=sigrieDefinitions["quest"]}
else{this.masterTypes=sigrieDefinitions[this.filterbox.getAttribute("searchtype")]
this.repopulateFilters()}}
this.repopulateFilters=function(){if(this.searching)return;for(var key in currentURL.query){var match=null
var filterid=-1
var value=currentURL.query[key]
var types=this.masterTypes
var fields=[]
var fKey=false
var negate=false
if(match=key.match(/^(.+)__not$/i)){negate=true
key=match[1]}
while(match=key.match(/([\w_]+?)(?:__|$)/)){fields.push(match[1])
key=key.substr(match[0].length)}
for(var fieldid=0;fieldid<fields.length;fieldid++){var field=fields[fieldid]
var last=(fieldid==fields.length-1)
var found=false
if(!types)break;if(field=="pk"){for(var j in types){if((typeof(types[j].primaryKey)=="boolean")&&(types[j].primaryKey===true)){field=j
break}}}
if((!found)&&(typeof(types[field])!="object")){for(var j in types){if((typeof(types[j].dbColumn)=="string")&&(types[j].dbColumn==field)&&(types[j].type=="foreignKey")){field=j
found=true
break}}
if((!found)&&(match=field.match(/^(.+)_id$/i))){if((typeof(types[match[1]])=="object")&&(types[match[1]].type=="foreignKey")){found=true
field=match[1]}}}
if(typeof(types[field])=="object"){if(filterid<0){filterid=this.addFilter(false)}
this.addField(filterid,types,field,false)
types=types[field]
if(types.type=="foreignKey"){types=sigrieDefinitions[types.key]
fKey=true}
this.filters[filterid].value.value=value
this.filters[filterid].negater.checkbox.checked=negate}
else if(fKey){for(var j in types){if((typeof(types[j].primaryKey)=="boolean")&&(types[j].primaryKey===true)){fields.splice(fieldid,1,j,field)
fieldid--
break}}
fKey=false}
else if((last)&&(filterid>=0)){this.setModifierValue(filterid,field)
found=true
fKey=false}
else{fKey=false
break}}
if(fKey){for(var j in types){if((typeof(types[j].primaryKey)=="boolean")&&(types[j].primaryKey===true)){this.addField(filterid,types,j,false)
this.filters[filterid].value.value=value
break}}}}}
this.addFilter=function(populate){if(typeof(populate)!="boolean")populate=true;var filter={"div":document.createElement("div"),"fields":[],"value":document.createElement("input"),"remove":document.createElement("button"),"modifier":false,"negater":{"checkbox":document.createElement("input"),"label":document.createElement("label")}}
var id=this.filters.push(filter)-1
filter.div.className="filter"
filter.remove.textContent=filter.remove.innerText="Delete"
filter.remove.onclick=function(){that.removeFilter(id)}
filter.negater.checkbox.id="filter"+id+"neg"
filter.negater.checkbox.type="checkbox"
filter.negater.label.htmlFor="filter"+id+"neg"
filter.negater.label.textContent=filter.negater.label.innerText="Negate"
filter.div.appendChild(filter.value)
filter.div.appendChild(filter.negater.checkbox)
filter.div.appendChild(filter.negater.label)
filter.div.appendChild(filter.remove)
this.filterContainer.appendChild(filter.div)
if(populate){this.addField(id,this.masterTypes)}
this.countFilters()
return id}
this.removeFilter=function(filterid){var filter=this.filters[filterid]
if(filter.fields.length>0)this.removeField(filterid,0);this.filterContainer.removeChild(filter.div)
this.filters[filterid]=false
this.countFilters()}
this.addField=function(filterid,types,value,addFields){if(typeof(addFields)!="boolean")addFields=true;var filter=this.filters[filterid]
var field=document.createElement("select")
var fieldid=filter.fields.push({"element":field,"types":types})-1
this.setModifier(filterid,"")
field.onchange=function(){that.onFieldChange(filterid,fieldid)}
for(var key in types){var option=document.createElement("option")
option.value=key
option.textContent=option.innerText=types[key].name
if((typeof(value)!="undefined")&&(value==key))option.selected=true
field.appendChild(option)}
filter.div.insertBefore(field,filter.value)
this.onFieldChange(filterid,fieldid,addFields)
return fieldid}
this.removeField=function(filterid,fieldid){var filter=this.filters[filterid]
while(fieldid<filter.fields.length){var field=filter.fields.pop()
filter.div.removeChild(field.element)}}
this.onFieldChange=function(filterid,fieldid,addFields){if(typeof(addFields)!="boolean")addFields=true;var filter=this.filters[filterid]
var field=filter.fields[fieldid]
var oldType="string"
var type=field.types[field.element.value]
if(fieldid<filter.fields.length)this.removeField(filterid,fieldid+1);if(typeof(filter.value.type)=="string")oldType=filter.value.type;if(type.type=="foreignKey"){if(addFields)this.addField(filterid,sigrieDefinitions[type.key])}
else if(typeof(type.choices)!="object"){this.setValueType(filterid,"input")
this.setModifier(filterid,type.type)
if(typeof(type.size)=="number")filter.size=type.size
if(typeof(type.maxLength)=="number")filter.maxLength=type.maxLength
if((type.type!=oldType)||(!type.validator(type,filter.value.value))){filter.value.value=type["default"]}}
else{var choices=type.choices
this.setValueType(filterid,"select")
this.setModifier(filterid,"")
for(var key in choices){var option=document.createElement("option")
option.value=choices[key].value
option.textContent=option.innerText=choices[key].name
if((typeof(type["default"])!="undefined")&&(type["default"]==choices[key].value)){option.selected=true}
filter.value.appendChild(option)}}}
this.setValueType=function(filterid,type){var filter=this.filters[filterid]
var oldType=filter.value.nodeName
if(oldType!=type){var value=document.createElement(type)
filter.div.replaceChild(value,filter.value)
filter.value=value}
if(type=="select"){while(filter.value.firstChild){filter.value.removeChild(filter.value.firstChild)}}
if(typeof(value.onkeyup)!="function"){value.onkeyup=this.valueKeyPress}
if(typeof(value.onblur)!="function"){value.onblur=function(){that.revalidateFilter(filterid)}}}
this.setModifierValue=function(filterid,value){var filter=this.filters[filterid]
if(!filter.modifier)return;var options=filter.modifier.getElementsByTagName("option")
for(var i in options){var option=options[i]
option.selected=(option.value==value)}}
this.setModifier=function(filterid,type){var filter=this.filters[filterid]
var visible=(type=="integer")||(type=="string")
if((visible)&&(!filter.modifier)){filter.modifier=document.createElement("select")
filter.div.insertBefore(filter.modifier,filter.value)}
else if((!visible)&&(filter.modifier)){filter.div.removeChild(filter.modifier)
filter.modifier=false}
else if((visible)&&(filter.modifier)){while(filter.modifier.firstChild){filter.modifier.removeChild(filter.modifier.firstChild)}}
if(!visible)return;if(type=="integer"){var options=[{"value":"","name":"Equal to"},{"value":"gt","name":"Greater than"},{"value":"lt","name":"Lesser than"},{"value":"gte","name":"Greater than or equals"},{"value":"lte","name":"Lesser than or equals"},{"value":"band","name":"Binary AND"},{"value":"in","name":"In"}]
for(var i in options){var option=document.createElement("option")
option.value=options[i].value
option.textContent=option.innerText=options[i].name
filter.modifier.appendChild(option)}}
else if(type=="string"){var options={"Case insensitive":{"imatches":"Contains words","icontains":"Contains string","istartswith":"Starts with","iendswith":"Ends with","iexact":"Exactly matches","iregex":"Matches regex"},"Case sensitive":{"matches":"Contains words","contains":"Contains string","startswith":"Starts with","endswith":"Ends with","exact":"Exactly matches","regex":"Matches regex"},"Miscellaneous":{"in":"In"}}
for(var group in options){var optgroup=document.createElement("optgroup")
optgroup.label=group
for(var key in options[group]){var option=document.createElement("option")
option.value=key
option.textContent=option.innerText=options[group][key]
optgroup.appendChild(option)}
filter.modifier.appendChild(optgroup)}}}
this.submitFilters=function(){var cancel=false
var url=new URL(document.location.href)
url.clear("query")
for(var filterid in this.filters){var filter=this.filters[filterid]
if(filter){var name=""
var value=filter.value.value
if(value.length>0){for(var fieldid in filter.fields){var field=filter.fields[fieldid]
if(name.length>0)name+="__"
name+=field.element.value}
if(!this.revalidateFilter(filterid)){cancel=true}
if((filter.modifier)&&(filter.modifier.value.length>0)){name+="__"+filter.modifier.value}
if(filter.negater.checkbox.checked)name+="__not";url.setKey("query",name,value)}}}
if(!cancel){document.location.href=url.toString()}}
this.valueKeyPress=function(event){if(typeof(event)!="object")event=window.event;var key=0
if(typeof(event.keyCode)!="undefined")key=event.keyCode;if(typeof(event.which)!="undefined")key=event.which;if(key==13){that.submitFilters()}}
this.revalidateFilter=function(filterid){var filter=this.filters[filterid]
var field=filter.fields[filter.fields.length-1]
var type=field.types[field.element.value]
var valid=type.validator(type,filter.value.value,filter.modifier.value)
if(valid){filter.value.className=""}else{filter.value.className="invalid"}
return valid}
this.clearFilters=function(){for(var filterid in this.filters){var filter=this.filters[filterid]
if(typeof(filter)=="object"){this.removeFilter(filterid)}}
this.filters=[]}
this.hookTabs=function(){if(typeof(tvlib)!="object")return;if(typeof(tvlib.onTabClick)!="function")return;var old=tvlib.onTabClick;tvlib.onTabClick=function(self,silent){old(self,silent)
that.clearFilters()
var match=self.id.match(/tab_(\w+)/i)
if(typeof(sigrieDefinitions[match[1]])=="object"){that.masterTypes=sigrieDefinitions[match[1]]
that.filterbox.style.display=""}
else{that.filterbox.style.display="none"}}}
this.countFilters=function(silent){var count=0
for(i in this.filters){var filter=this.filters[i]
if(typeof(filter)=="object")count++}
if((typeof(silent)!="boolean")||(silent===false)){if(count>0){this.apply.style.display=""}
else{this.apply.style.display="none"}
if(count<this.maximumFilters){this.add.style.display=""}
else{this.add.style.display="none"}}
return count}}
sigrieFilters=new SigrieFilters()
addLoadEvent(function(){sigrieFilters.init()});var tvlib={init:function(){tvlib.tabNames={}
tvlib.tabs=[]
tvlib.parseDocument()
tvlib.loadCurrentTab()},loadCurrentTab:function(){if(typeof(document.location.hash)!="string")return false;var current=currentURL.getKey("hash","tab")
if(current===false)return false;if(typeof(tvlib.tabNames[current])=="object"){var tab=tvlib.tabNames[current]
tvlib.onTabClick(tab)}},parseDocument:function(){var divs=document.getElementsByTagName("div")
var tabviews=Array()
var tabbuttons=Array()
var tabcontents=Array()
for(var i=0;i<divs.length;i++){if(hasClass(divs[i],"tabview")){tabviews.push(divs[i])
var children=divs[i].getElementsByTagName("div")
for(var j=0;j<children.length;j++){var tab=children[j]
if(hasClass(tab,"tabbutton")){var content=document.getElementById(tab.id+"_content")
tab["parent"]=divs[i]
tab["onclick"]=function(evt){tvlib.onTabClick(this)}
content["parent"]=divs[i]
tab["content"]=content
content.style.display="none"
if(hasClass(tab,"selected")){tvlib.selected=tab}
if(typeof(tab.id)=="string"){var id=tab.id
id=id.match(/(?:tab_)?([\w\d_]+)/)[1]
tvlib.tabNames[id]=tab
tab.name=id}
tab.index=tvlib.tabs.push(tab)-1
if(typeof(tab.addEventListener)=="function"){tab.addEventListener('DOMMouseScroll',tvlib.onTabScroll,false)
tab.addEventListener('mousewheel',tvlib.onTabScroll,false)}
else if(typeof(tab.attachEvent)=="function"){tab.attachEvent('onmousewheel',tvlib.onTabScroll)}}}}}
if((typeof(tvlib.selected)!="object")&&(tvlib.tabs.length>0))tvlib.selected=tvlib.tabs[0];if(typeof(tvlib.selected)=="object")tvlib.onTabClick(tvlib.selected,true);},onTabScroll:function(event){if(typeof(event)!="object")event=window.event;if(typeof(tvlib.selected)!="object")tvlib.selected=tvlib.tabs[0];var tab=tvlib.selected
var newTab=tab
var amount=0
if(typeof(event.detail)=="number")amount=event.detail
if(typeof(event.wheelDelta)=="number")amount=event.wheelDelta
if(typeof(event.stopPropagation)=="function")event.stopPropagation();if(typeof(event.preventDefault)=="function")event.preventDefault();event["return"]=false
event.cancel=true
event.cancelBubble=true
if(amount<0){if(tab.index+1<tvlib.tabs.length){newTab=tvlib.tabs[tab.index+1]}
else{return false}}
else{if(tab.index>0){newTab=tvlib.tabs[tab.index-1]}
else{return false}}
tvlib.onTabClick(newTab)
return false},onTabClick:function(self,silent){if(typeof(silent)!="boolean")silent=false;tvlib.hideAll(self["parent"])
self["content"].style.display="block"
addClass(self,"selected")
tvlib.selected=self
if(!silent){if(typeof(self.name)=="string"){currentURL.setKey("hash","tab",self.name)
document.location.href=currentURL.toString()}}},hideAll:function(div){var children=div.getElementsByTagName("div");for(var i=0;i<children.length;i++){if(hasClass(children[i],"tabcontent")){children[i].style.display="none"}else if(hasClass(children[i],"tabbutton")){removeClass(children[i],"selected")}}}}
addLoadEvent(tvlib.init)
var maplib={renderMaps:function(maps,defaultfile){if(typeof(defaultfile)=="undefined")defaultfile="";var jstooltip=document.createElement("div")
var defaultid=0
var container=document.getElementById("map-container")
jstooltip.id="sigrie-maptooltip"
jstooltip.className="sigrie-tooltip tt-hover tt-hover-external"
jstooltip.style.visibility="hidden"
jstooltip.style.padding="4px"
maplib.jstooltip=jstooltip
maplib.hide()
maplib.maps=maps
maplib.mapDivs=[]
if(maps.length>1){var mapWidget=document.createElement("div")
mapWidget.id="sigrie-map-floorswitch"
mapWidget.className="sigrie-map-floorswitch"
mapWidget.innerHTML="Current map: "
container.appendChild(mapWidget)
var selectBox=document.createElement("select")
for(var m in maps){var option=document.createElement("option")
option.innerHTML=maps[m].name
option.mapIndex=m
selectBox.appendChild(option)
if(maps[m].name==defaultfile)
{defaultid=m
option.selected="true"}}
mapWidget.appendChild(selectBox)
selectBox.onchange=function(f){for(var m in maplib.maps){if(m==maplib.selectBox.selectedIndex)maplib.mapDivs[m].style.visibility="visible"
else maplib.mapDivs[m].style.visibility="hidden"}}
maplib.selectBox=selectBox}
var innerMapContainer=document.createElement("div")
innerMapContainer.style.height="325px"
innerMapContainer.style.width="488px"
innerMapContainer.style.position="relative"
innerMapContainer.appendChild(jstooltip)
container.appendChild(innerMapContainer)
for(var m in maps){var map=maps[m]
var mapDiv=document.createElement("div")
mapDiv.id="map-"+map.name
mapDiv.className="map"
mapDiv.style.width="488px"
mapDiv.style.height="325px"
mapDiv.style.marginBottom="-325px"
mapDiv.style.position="relative"
mapDiv.style.backgroundImage="url('/static/img/maps/"+map.file+".thumbnail.jpg')"
innerMapContainer.appendChild(mapDiv)
maplib.mapDivs[maplib.mapDivs.length]=mapDiv
mapDiv.style.visibility="hidden"
for(var i in map.nodes){var n=map.nodes[i]
var node=document.createElement("div")
var nodeClass="node"
if(typeof(n[2])=="string")nodeClass=n[2];node.className=nodeClass
node.label=n[0]+", "+n[1]
if(n.length==3)node.label=n[2]+" ("+n[0]+", "+n[1]+")"
node.style.position="absolute"
node.style.left=""+n[0]+"%"
node.style.top=""+n[1]+"%"
node.onmouseover=function(e){maplib.startTooltip(this)}
node.onmouseout=function(e){maplib.hide()}
mapDiv.appendChild(node)}}
maplib.mapDivs[defaultid].style.visibility="visible"},startTooltip:function(node){maplib.jstooltip.innerHTML=node.label
maplib.jstooltip.style.left=""+(node.offsetLeft+16)+"px"
maplib.jstooltip.style.top=""+(node.offsetTop-20)+"px"
maplib.jstooltip.style.visibility="visible"},hide:function(){maplib.jstooltip.style.visibility="hidden"}}
pagelib={init:function(){pagelib.container=document.getElementById("pagewidget")
if((typeof(pagelib.container)=="undefined")||(!pagelib.container))return;var initid=parseInt(pagelib.container.getAttribute("rel"))
if(initid<0)return;pagelib.cache={}
pagelib.id=-1
pagelib.loading=-1
pagelib.nextId=-1
pagelib.pos=0
pagelib.loadPage(initid)},loadPage:function(id){id=parseInt(id)
if(id<0)return false;if(pagelib.loading>=0)return false;pagelib.loading=id
if(typeof(pagelib.cache[id])=="object"){pagelib.parsePage(pagelib.cache[id])}
else{httplib.request("/p/"+id+"/tooltip/js",{"content":"json","success":function(result){pagelib.parsePage(result.response)}})}
return true},parsePage:function(page){page.id=parseInt(page.id)
if(page.id!=parseInt(pagelib.loading))return false;if(pagelib.pos==0){pagelib.pos=1}
else if(page.id==pagelib.nextId){pagelib.pos++}
else{pagelib.pos--}
pagelib.cache[page.id]=page
if(typeof(pagelib.cache[page.id].prevId)!="number")pagelib.cache[page.id].prevId=pagelib.id;pagelib.id=page.id
pagelib.loading=-1
if((typeof(page.nextpage)=="undefined")||(parseInt(page.nextpage)<0)){pagelib.nextId=-1}
else{pagelib.nextId=parseInt(page.nextpage)}
pagelib.configureNavigation()
pagelib.setText(page.tooltip)},configureNavigation:function(page){if(typeof(pagelib.header)!="object"){pagelib.container.appendChild(pagelib.header=document.createElement("div"))
pagelib.header.id="pagewidget-header"}
if(typeof(pagelib.nextLink)!="object"){pagelib.header.appendChild(pagelib.nextLink=document.createElement("a"))
pagelib.nextLink.href="javascript:;"
pagelib.nextLink.innerHTML="Next &rsaquo;"
pagelib.nextLink.onclick=pagelib.nextPage
addClass(pagelib.nextLink,"page-next")
addClass(pagelib.nextLink,"button")}
if(typeof(pagelib.posLink)!="object"){pagelib.header.appendChild(pagelib.posLink=document.createElement("a"))
pagelib.posLink.href="/p/"+pagelib.id
pagelib.posLink.innerHTML="Page 0"
addClass(pagelib.posLink,"page-pos")}
if(typeof(pagelib.prevLink)!="object"){pagelib.header.appendChild(pagelib.prevLink=document.createElement("a"))
pagelib.prevLink.href="javascript:;"
pagelib.prevLink.innerHTML="&lsaquo; Prev"
pagelib.prevLink.onclick=pagelib.prevPage
addClass(pagelib.prevLink,"page-prev")
addClass(pagelib.prevLink,"button")}
if(parseInt(pagelib.nextId)<0){addClass(pagelib.nextLink,"inactive")}
else{removeClass(pagelib.nextLink,"inactive")}
if((pagelib.cache.count==0)||(parseInt(pagelib.cache[pagelib.id].prevId)<0)){addClass(pagelib.prevLink,"inactive")}
else{removeClass(pagelib.prevLink,"inactive")}
pagelib.posLink.href="/p/"+pagelib.id
pagelib.posLink.innerHTML="Page "+pagelib.pos},setText:function(text){if(typeof(pagelib.text)!="object"){pagelib.text=document.createElement("div")
pagelib.text.id="pagewidget-text"
pagelib.container.appendChild(pagelib.text)}
pagelib.text.innerHTML=text},nextPage:function(){if(!pagelib.loadPage(pagelib.nextId)){pagelib.configureNavigation()}},prevPage:function(){if((pagelib.cache.count==0)||(!pagelib.loadPage(pagelib.cache[pagelib.id].prevId))){pagelib.configureNavigation()}}}
addLoadEvent(pagelib.init)