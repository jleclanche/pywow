// from global.js
var onloads = new Array();
function addLoadEvent(func) {
	onloads[onloads.length] = func;
}
if (typeof(window.onload) == "function") addLoadEvent(window.onload);
window.onload = function() {
	for (var i = 0; i < onloads.length; i++) {
		onloads[i]();
	}
}
// Pull other files
var tooltipcss = document.createElement("link");
tooltipcss.type = "text/css";
tooltipcss.rel = "stylesheet";
tooltipcss.href = "http://db.mmo-champion.com/static/css/tooltip.css";
head = document.getElementsByTagName("head")[0];
head.appendChild(tooltipcss);
var tooltipjs = document.createElement("script");
tooltipjs.type = "text/javascript";
tooltipjs.src = "http://db.mmo-champion.com/static/js/tooltip.js";
head.appendChild(tooltipjs);
if (/msie/i.test(navigator.userAgent) && !/opera/i.test(navigator.userAgent)) {
	var iecss = document.createElement("link");
	iecss.type = "text/css";
	iecss.rel = "stylesheet";
	iecss.href = "http://db.mmo-champion.com/static/css/tooltip-ie.css";
	head.appendChild(iecss);
}
